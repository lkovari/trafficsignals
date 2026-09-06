#!/usr/bin/env python3
from __future__ import annotations

import csv
import io
import os
import subprocess
import sys
import time
from pathlib import Path

from PIL import Image

sys.path.insert(0, str(Path(__file__).resolve().parent))

from kresz_map import ID_TO_CODE
from palette import (
    CSV_PATH,
    DRAWABLE,
    PNG_DIR,
    RASTER_WIDTH,
    ROOT,
    SNAPPED_SVG_DIR,
    SVG_DIR,
    rasterize_svg,
    snap_raster,
    snap_svg_text,
    write_drawable_png,
)
from remove_watermark import remove_lk_watermark, snap_raster_photo

import fetch_wikimedia as wiki


def load_inventory() -> list[dict[str, str]]:
    with CSV_PATH.open(encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def svg_path_for(row: dict[str, str]) -> Path | None:
    wiki_file = row.get("wiki_file", "").strip()
    if wiki_file:
        candidate = SVG_DIR / wiki_file.replace(" ", "_")
        if candidate.exists():
            return candidate
    code = row.get("kresz_code") or ID_TO_CODE.get(row["id"], "")
    if code:
        candidate = SVG_DIR / f"Hungary_road_sign_{code}.svg"
        if candidate.exists():
            return candidate
    return None


def ensure_svgs(inventory: list[dict[str, str]]) -> None:
    wanted: list[str] = []
    for row in inventory:
        if svg_path_for(row) is not None:
            continue
        code = row.get("kresz_code") or ID_TO_CODE.get(row["id"], "")
        wiki_file = row.get("wiki_file", "").strip()
        filename = wiki_file or (f"Hungary road sign {code}.svg" if code else "")
        if filename:
            wanted.append(filename)
    unique = list(dict.fromkeys(wanted))
    if not unique:
        return
    print(f"downloading {len(unique)} svgs")
    urls = wiki.imageinfo(unique)
    for filename in unique:
        url = urls.get(filename)
        if not url:
            continue
        dest = SVG_DIR / filename.replace(" ", "_")
        if dest.exists():
            continue
        try:
            wiki.download(url, dest)
            time.sleep(0.4)
        except Exception as exc:
            print(f"download failed {filename}: {exc}")


def render_from_svg(sign_id: str, source: Path) -> bool:
    snapped = SNAPPED_SVG_DIR / source.name
    SNAPPED_SVG_DIR.mkdir(parents=True, exist_ok=True)
    snapped.write_text(snap_svg_text(source.read_text(encoding="utf-8", errors="replace")), encoding="utf-8")
    png_path = PNG_DIR / f"{sign_id}.png"
    if not rasterize_svg(snapped, png_path, width=RASTER_WIDTH):
        return False
    image = snap_raster(Image.open(png_path))
    write_drawable_png(sign_id, image)
    return True


def git_original(sign_id: str) -> Image.Image | None:
    for ext in (".jpg", ".jpeg", ".png"):
        rel = f"app/src/main/res/drawable-xxhdpi/{sign_id}{ext}"
        try:
            data = subprocess.check_output(
                ["git", "show", f"HEAD:{rel}"],
                cwd=ROOT,
                stderr=subprocess.DEVNULL,
            )
        except subprocess.CalledProcessError:
            continue
        if data:
            return Image.open(io.BytesIO(data))
    return None


def render_from_raster(path: Path) -> None:
    image = git_original(path.stem) or Image.open(path)
    image = remove_lk_watermark(image)
    image = snap_raster_photo(image)
    write_drawable_png(path.stem, image)


def main() -> None:
    inventory = load_inventory()
    if os.environ.get("UNIFY_DOWNLOAD") == "1":
        ensure_svgs(inventory)
    svg_ok = 0
    raster_ok = 0
    done: set[str] = set()
    for row in inventory:
        sign_id = row["id"]
        source = svg_path_for(row)
        if source is not None and render_from_svg(sign_id, source):
            svg_ok += 1
            done.add(sign_id)
            if svg_ok % 25 == 0:
                print(f"svg {svg_ok}", flush=True)
            continue
        existing = next(iter(DRAWABLE.glob(f"{sign_id}.*")), None)
        if existing is None:
            print(f"missing {sign_id}")
            continue
        render_from_raster(existing)
        raster_ok += 1
        done.add(sign_id)
        if raster_ok % 50 == 0:
            print(f"raster {raster_ok}", flush=True)
    extras = [
        path
        for path in DRAWABLE.iterdir()
        if path.is_file()
        and path.suffix.lower() in {".png", ".jpg", ".jpeg"}
        and path.stem not in done
        and not path.stem.startswith("kategoria_")
    ]
    for path in extras:
        render_from_raster(path)
        raster_ok += 1
        done.add(path.stem)
    leftover_jpg = [
        path
        for path in list(DRAWABLE.glob("*.jpg")) + list(DRAWABLE.glob("*.jpeg"))
        if not path.stem.startswith("kategoria_")
    ]
    for path in leftover_jpg:
        render_from_raster(path)
        raster_ok += 1
    print(f"svg={svg_ok} raster={raster_ok}", flush=True)
    jpg_left = list(DRAWABLE.glob("*.jpg")) + list(DRAWABLE.glob("*.jpeg"))
    print(f"jpg_left={len(jpg_left)}", flush=True)


if __name__ == "__main__":
    main()
