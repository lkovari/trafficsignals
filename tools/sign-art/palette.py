#!/usr/bin/env python3
from __future__ import annotations

import colorsys
import re
import subprocess
from pathlib import Path

import numpy as np
from PIL import Image, ImageFilter

ROOT = Path("/Users/kovarilaszlo/src/mobile/trafficsignals")
CSV_PATH = ROOT / "tools/sign-art/inventory.csv"
CACHE = ROOT / "tools/sign-art/cache"
SVG_DIR = CACHE / "svg"
SNAPPED_SVG_DIR = CACHE / "svg_snapped"
PNG_DIR = CACHE / "png"
DRAWABLE = ROOT / "app/src/main/res/drawable-xxhdpi"

SIGN_RED = (0xC8, 0x10, 0x2E)
SIGN_BLUE = (0x00, 0x50, 0xA0)
SIGN_YELLOW = (0xF5, 0xC4, 0x00)
WHITE = (255, 255, 255)
BLACK = (0x1B, 0x1F, 0x24)
ASPHALT = (0x1B, 0x1F, 0x24)
SIGN_RED_HEX = "#C8102E"
SIGN_BLUE_HEX = "#0050A0"
WHITE_HEX = "#FFFFFF"
RASTER_WIDTH = 1024

NAMED_RGB = {
    "red": (255, 0, 0),
    "crimson": (220, 20, 60),
    "firebrick": (178, 34, 34),
    "darkred": (139, 0, 0),
    "indianred": (205, 92, 92),
    "orangered": (255, 69, 0),
    "blue": (0, 0, 255),
    "navy": (0, 0, 128),
    "mediumblue": (0, 0, 205),
    "darkblue": (0, 0, 139),
    "royalblue": (65, 105, 225),
    "steelblue": (70, 130, 180),
    "dodgerblue": (30, 144, 255),
    "cornflowerblue": (100, 149, 237),
    "deepskyblue": (0, 191, 255),
    "lightskyblue": (135, 206, 250),
    "skyblue": (135, 206, 235),
    "lightblue": (173, 216, 230),
    "midnightblue": (25, 25, 112),
}


def rgb_to_hsv_deg(r: float, g: float, b: float) -> tuple[float, float, float]:
    h, s, v = colorsys.rgb_to_hsv(r / 255.0, g / 255.0, b / 255.0)
    return h * 360.0, s, v


def classify_rgb(r: int, g: int, b: int) -> str | None:
    mx = max(r, g, b)
    mn = min(r, g, b)
    if mx < 18:
        return None
    if mn > 250:
        return None
    if mx - mn < 18:
        return None
    h, s, v = rgb_to_hsv_deg(r, g, b)
    if s < 0.18 or v < 0.12:
        return None
    if 38 <= h <= 72:
        return None
    if 72 < h <= 168:
        return None
    if h <= 22 or h >= 338 or (r > g + 28 and r > b + 20 and r >= 80 and not (175 <= h <= 280)):
        return "red"
    if 175 <= h <= 280 or (b > r + 18 and b > g + 8 and b >= 60):
        if v >= 0.70 and s <= 0.90:
            return "lightblue"
        return "blue"
    return None


def parse_hex(token: str) -> tuple[int, int, int] | None:
    raw = token.lstrip("#")
    if len(raw) == 3:
        raw = "".join(ch * 2 for ch in raw)
    if len(raw) in (6, 8) and re.fullmatch(r"[0-9a-fA-F]+", raw):
        return int(raw[0:2], 16), int(raw[2:4], 16), int(raw[4:6], 16)
    return None


def target_for_kind(kind: str) -> tuple[int, int, int]:
    if kind == "red":
        return SIGN_RED
    if kind == "blue":
        return SIGN_BLUE
    return WHITE


def snap_hex_token(token: str) -> str:
    rgb = parse_hex(token)
    if rgb is None:
        return token
    kind = classify_rgb(*rgb)
    if kind is None:
        return token
    r, g, b = target_for_kind(kind)
    return f"#{r:02X}{g:02X}{b:02X}"


def snap_svg_text(text: str) -> str:
    def hex_sub(match: re.Match[str]) -> str:
        return snap_hex_token(match.group(0))

    text = re.sub(r"#(?:[0-9a-fA-F]{3}|[0-9a-fA-F]{6}|[0-9a-fA-F]{8})\b", hex_sub, text)

    def rgb_sub(match: re.Match[str]) -> str:
        vals = []
        for part in match.group(1).split(","):
            part = part.strip()
            if part.endswith("%"):
                vals.append(int(round(float(part[:-1]) * 2.55)))
            else:
                vals.append(int(round(float(part))))
        if len(vals) < 3:
            return match.group(0)
        kind = classify_rgb(vals[0], vals[1], vals[2])
        if kind is None:
            return match.group(0)
        r, g, b = target_for_kind(kind)
        return f"rgb({r},{g},{b})"

    text = re.sub(
        r"rgb\(\s*([0-9.]+%?\s*,\s*[0-9.]+%?\s*,\s*[0-9.]+%?)\s*\)",
        rgb_sub,
        text,
        flags=re.IGNORECASE,
    )

    names = sorted(NAMED_RGB.keys(), key=len, reverse=True)
    name_re = re.compile(
        r"(?P<pre>[\s:\"'=;])(?P<name>" + "|".join(names) + r")(?P<post>[\s;\"']|$)",
        re.IGNORECASE,
    )

    def name_sub(match: re.Match[str]) -> str:
        rgb = NAMED_RGB[match.group("name").lower()]
        kind = classify_rgb(*rgb)
        if kind is None:
            return match.group(0)
        r, g, b = target_for_kind(kind)
        return f"{match.group('pre')}#{r:02X}{g:02X}{b:02X}{match.group('post')}"

    return name_re.sub(name_sub, text)


def rasterize_svg(svg_path: Path, png_path: Path, width: int = RASTER_WIDTH) -> bool:
    png_path.parent.mkdir(parents=True, exist_ok=True)
    try:
        subprocess.run(
            ["rsvg-convert", "-w", str(width), "--keep-aspect-ratio", "-o", str(png_path), str(svg_path)],
            check=True,
            capture_output=True,
        )
        return png_path.exists() and png_path.stat().st_size > 0
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False


def local_range(rgb: np.ndarray) -> np.ndarray:
    pad = np.pad(rgb.astype(np.int16), ((1, 1), (1, 1), (0, 0)), mode="edge")
    windows = [pad[dy : dy + rgb.shape[0], dx : dx + rgb.shape[1]] for dy in range(3) for dx in range(3)]
    stacked = np.stack(windows, axis=0)
    return (stacked.max(axis=0) - stacked.min(axis=0)).max(axis=2)


def rgb_to_hsv_arrays(rgb: np.ndarray) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    r = rgb[:, :, 0].astype(np.float32) / 255.0
    g = rgb[:, :, 1].astype(np.float32) / 255.0
    b = rgb[:, :, 2].astype(np.float32) / 255.0
    mx = np.maximum(np.maximum(r, g), b)
    mn = np.minimum(np.minimum(r, g), b)
    chroma = mx - mn
    s = np.divide(chroma, mx, out=np.zeros_like(mx), where=mx > 1e-6)
    v = mx
    h = np.zeros_like(mx)
    rc = np.divide(mx - r, chroma, out=np.zeros_like(mx), where=chroma > 1e-6)
    gc = np.divide(mx - g, chroma, out=np.zeros_like(mx), where=chroma > 1e-6)
    bc = np.divide(mx - b, chroma, out=np.zeros_like(mx), where=chroma > 1e-6)
    h = np.where((chroma > 1e-6) & (mx == r), bc - gc, h)
    h = np.where((chroma > 1e-6) & (mx == g) & (mx != r), 2.0 + rc - bc, h)
    h = np.where((chroma > 1e-6) & (mx == b) & (mx != r) & (mx != g), 4.0 + gc - rc, h)
    h = np.mod(h / 6.0, 1.0) * 360.0
    return h, s, v


def snap_raster(image: Image.Image) -> Image.Image:
    arr = np.array(image.convert("RGBA"))
    rgb = arr[:, :, :3]
    r = rgb[:, :, 0].astype(np.int16)
    g = rgb[:, :, 1].astype(np.int16)
    b = rgb[:, :, 2].astype(np.int16)
    mx = np.maximum(np.maximum(r, g), b)
    mn = np.minimum(np.minimum(r, g), b)
    chroma = mx - mn
    h, s, v = rgb_to_hsv_arrays(rgb)
    base = (mx >= 18) & (mn <= 250) & (chroma >= 18) & (s >= 0.18) & (v >= 0.12)
    yellow = (h >= 38) & (h <= 72)
    green = (h > 72) & (h <= 168)
    red_hue = (h <= 22) | (h >= 338)
    red_dom = (r > g + 28) & (r > b + 20) & (r >= 80)
    blue_hue = (h >= 175) & (h <= 280)
    blue_dom = (b > r + 18) & (b > g + 8) & (b >= 60)
    red = base & ~yellow & ~green & (red_hue | red_dom) & ~blue_hue
    blueish = base & ~yellow & ~green & ~red & (blue_hue | blue_dom)
    lightblue = blueish & (v >= 0.70) & (s <= 0.90)
    blue = blueish & ~lightblue
    face = np.array(
        Image.fromarray((blue.astype(np.uint8) * 255), mode="L").filter(ImageFilter.MaxFilter(11))
    ) > 0
    light_on_face = lightblue & face
    other_blue = blue | (lightblue & ~face)
    arr[red, 0:3] = SIGN_RED
    arr[other_blue, 0:3] = SIGN_BLUE
    arr[light_on_face, 0:3] = WHITE
    return Image.fromarray(arr, mode="RGBA")


def ensure_min_size(image: Image.Image, min_side: int = 512) -> Image.Image:
    width, height = image.size
    longest = max(width, height)
    if longest >= min_side:
        return image
    scale = min_side / longest
    return image.resize(
        (max(1, int(round(width * scale))), max(1, int(round(height * scale)))),
        Image.Resampling.LANCZOS,
    )


def write_drawable_png(sign_id: str, image: Image.Image) -> Path:
    DRAWABLE.mkdir(parents=True, exist_ok=True)
    for existing in DRAWABLE.glob(f"{sign_id}.*"):
        existing.unlink()
    dest = DRAWABLE / f"{sign_id}.png"
    out = image.convert("RGBA")
    alpha = np.array(out.split()[-1])
    if int(alpha.min()) == 255:
        out.convert("RGB").save(dest, format="PNG", optimize=True)
    else:
        out.save(dest, format="PNG", optimize=True)
    return dest


def fit_on_canvas(image: Image.Image, size: int, margin: int, background: tuple[int, int, int]) -> Image.Image:
    canvas = Image.new("RGBA", (size, size), background + (255,))
    inner = max(1, size - 2 * margin)
    work = image.convert("RGBA")
    work.thumbnail((inner, inner), Image.Resampling.LANCZOS)
    x = (size - work.width) // 2
    y = (size - work.height) // 2
    canvas.alpha_composite(work, (x, y))
    return canvas
