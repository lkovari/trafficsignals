#!/usr/bin/env python3
import csv
import json
import subprocess
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

from kresz_map import ID_TO_CODE

ROOT = Path("/Users/kovarilaszlo/src/mobile/trafficsignals")
CSV_PATH = ROOT / "tools/sign-art/inventory.csv"
CACHE = ROOT / "tools/sign-art/cache"
SVG_DIR = CACHE / "svg"
PNG_DIR = CACHE / "png"
DRAWABLE = ROOT / "app/src/main/res/drawable-xxhdpi"
USER_AGENT = "TrafficSignalsPort/2.0 (https://github.com/lkovari/trafficsignals; educational KRESZ catalog)"
API = "https://commons.wikimedia.org/w/api.php"


def api(params: dict) -> dict:
    params = dict(params)
    params["format"] = "json"
    req = urllib.request.Request(
        API + "?" + urllib.parse.urlencode(params),
        headers={"User-Agent": USER_AGENT},
    )
    with urllib.request.urlopen(req, timeout=60) as response:
        return json.loads(response.read().decode("utf-8"))


def imageinfo(filenames: list[str]) -> dict[str, str]:
    urls = {}
    for i in range(0, len(filenames), 40):
        chunk = filenames[i : i + 40]
        titles = "|".join(f"File:{name}" for name in chunk)
        for attempt in range(6):
            try:
                data = api(
                    {
                        "action": "query",
                        "titles": titles,
                        "prop": "imageinfo",
                        "iiprop": "url",
                    }
                )
                break
            except urllib.error.HTTPError as exc:
                if exc.code != 429:
                    raise
                wait = 15 * (attempt + 1)
                print(f"rate limited metadata, sleep {wait}s")
                time.sleep(wait)
        else:
            continue
        for page in data.get("query", {}).get("pages", {}).values():
            if page.get("missing") is not None:
                continue
            infos = page.get("imageinfo")
            title = page.get("title", "").removeprefix("File:")
            if infos and title:
                urls[title] = infos[0]["url"]
        time.sleep(1.0)
    return urls


def download(url: str, dest: Path) -> None:
    dest.parent.mkdir(parents=True, exist_ok=True)
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    for attempt in range(6):
        try:
            with urllib.request.urlopen(req, timeout=60) as response:
                dest.write_bytes(response.read())
            return
        except urllib.error.HTTPError as exc:
            if exc.code != 429:
                raise
            wait = 20 * (attempt + 1)
            print(f"rate limited download, sleep {wait}s")
            time.sleep(wait)
    raise RuntimeError(f"could not download {url}")


def rasterize(svg_path: Path, png_path: Path) -> bool:
    png_path.parent.mkdir(parents=True, exist_ok=True)
    try:
        subprocess.run(
            ["rsvg-convert", "-w", "1024", "--keep-aspect-ratio", "-o", str(png_path), str(svg_path)],
            check=True,
            capture_output=True,
        )
        return png_path.exists() and png_path.stat().st_size > 0
    except subprocess.CalledProcessError:
        return False


def replace_drawable(sign_id: str, png_path: Path) -> None:
    for existing in DRAWABLE.glob(f"{sign_id}.*"):
        existing.unlink()
    dest = DRAWABLE / f"{sign_id}.png"
    dest.write_bytes(png_path.read_bytes())


def main() -> None:
    only_ids = set(sys.argv[1:]) if len(sys.argv) > 1 else None
    CACHE.mkdir(parents=True, exist_ok=True)
    inventory = []
    with CSV_PATH.open(encoding="utf-8") as handle:
        inventory.extend(csv.DictReader(handle))

    wanted = []
    for row in inventory:
        if only_ids is not None and row["id"] not in only_ids:
            continue
        code = ID_TO_CODE.get(row["id"])
        if code:
            row["kresz_code"] = code
            wanted.append((row["id"], f"Hungary road sign {code}.svg"))

    unique_files = list(dict.fromkeys(name for _, name in wanted))
    print(f"requesting metadata for {len(unique_files)} files")
    urls = imageinfo(unique_files)
    print(f"found {len(urls)} commons files")

    replaced = 0
    for sign_id, filename in wanted:
        url = urls.get(filename)
        if not url:
            continue
        svg_path = SVG_DIR / filename.replace(" ", "_")
        if not svg_path.exists():
            try:
                download(url, svg_path)
            except Exception as exc:
                print(f"download failed {filename}: {exc}")
                continue
            time.sleep(0.4)
        png_path = PNG_DIR / f"{sign_id}.png"
        if rasterize(svg_path, png_path):
            replace_drawable(sign_id, png_path)
            for row in inventory:
                if row["id"] == sign_id:
                    row["wiki_file"] = filename
                    row["status"] = "wikimedia"
                    break
            replaced += 1

    with CSV_PATH.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=["id", "category", "old_file", "hu_title", "en_title", "kresz_code", "wiki_file", "status"],
        )
        writer.writeheader()
        writer.writerows(inventory)
    wiki = sum(1 for row in inventory if row.get("status") == "wikimedia")
    print(f"replaced={replaced} wikimedia_rows={wiki}")


if __name__ == "__main__":
    main()
