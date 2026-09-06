#!/usr/bin/env python3
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
from PIL import Image

sys.path.insert(0, str(Path(__file__).resolve().parent))

from palette import (
    DRAWABLE,
    PNG_DIR,
    ROOT,
    SNAPPED_SVG_DIR,
    SVG_DIR,
    WHITE,
    rasterize_svg,
    snap_raster,
    snap_svg_text,
)

VECTOR_DIR = ROOT / "app/src/main/res/drawable"
BLUE = "#0050A0"
RED = "#C8102E"
WHITE_HEX = "#FFFFFF"
BLACK = "#1B1F24"
YELLOW = "#F5C400"
GREEN = "#28A03C"
CANVAS = 1024


def circ(cx: float, cy: float, r: float) -> str:
    return f"M{cx - r},{cy} a{r},{r} 0 1,0 {2 * r},0 a{r},{r} 0 1,0 {-2 * r},0"


def rounded_square(x: float, y: float, size: float, radius: float) -> str:
    inner = size - 2 * radius
    return (
        f"M{x + radius},{y} h{inner} a{radius},{radius} 0 0,1 {radius},{radius} "
        f"v{inner} a{radius},{radius} 0 0,1 -{radius},{radius} "
        f"h-{inner} a{radius},{radius} 0 0,1 -{radius},-{radius} "
        f"v-{inner} a{radius},{radius} 0 0,1 {radius},-{radius} z"
    )


def vector(*paths: str) -> str:
    body = "\n".join(paths)
    return f"""<?xml version="1.0" encoding="utf-8"?>
<vector xmlns:android="http://schemas.android.com/apk/res/android"
    android:width="512dp"
    android:height="512dp"
    android:viewportWidth="108"
    android:viewportHeight="108">
{body}
</vector>
"""


def fill(color: str, data: str) -> str:
    return f'    <path\n        android:fillColor="{color}"\n        android:pathData="{data}" />'


ICONS = {
    "kategoria_elsobseg": vector(
        fill(RED, "M10,14 L98,14 L54,100 Z"),
        fill(WHITE_HEX, "M26,26 L82,26 L54,82 Z"),
    ),
    "kategoria_utasitastado": vector(
        fill(BLUE, circ(54, 54, 44)),
        fill(WHITE_HEX, "M54,22 L80,54 H64 V86 H44 V54 H28 Z"),
    ),
    "kategoria_tilalmi": vector(
        fill(RED, circ(54, 54, 44)),
        fill(WHITE_HEX, "M26,47 h56 v14 H26 Z"),
    ),
    "kategoria_veszely": vector(
        fill(RED, "M54,8 L102,96 L6,96 Z"),
        fill(WHITE_HEX, "M54,26 L88,88 L20,88 Z"),
        fill(BLACK, "M51,40 h6 v28 h-6 z"),
        fill(BLACK, "M51,72 h6 v8 h-6 z"),
    ),
    "kategoria_tajekoztato": vector(
        fill(BLUE, rounded_square(8, 8, 92, 10)),
        fill(WHITE_HEX, circ(54, 32, 8)),
        fill(WHITE_HEX, "M46,42 h16 v22 H46 Z"),
        fill(WHITE_HEX, "M30,44 h16 v7 H30 Z"),
        fill(WHITE_HEX, "M62,44 h16 v7 H62 Z"),
        fill(WHITE_HEX, "M46,64 h7 v24 h-7 z"),
        fill(WHITE_HEX, "M55,64 h7 v24 h-7 z"),
    ),
    "kategoria_utburkolati": vector(
        fill(BLACK, rounded_square(8, 8, 92, 10)),
        fill(WHITE_HEX, "M18,18 L90,18 L54,92 Z"),
        fill(BLACK, "M30,30 L78,30 L54,76 Z"),
    ),
    "kategoria_fenyjelzo": vector(
        fill(BLACK, rounded_square(34, 8, 40, 10)),
        fill(RED, circ(54, 26, 10)),
        fill(YELLOW, circ(54, 54, 10)),
        fill(GREEN, circ(54, 82, 10)),
    ),
}


def rasterize_named(code: str, width: int = 1400) -> Image.Image:
    source = SVG_DIR / f"Hungary_road_sign_{code}.svg"
    snapped = SNAPPED_SVG_DIR / source.name
    SNAPPED_SVG_DIR.mkdir(parents=True, exist_ok=True)
    snapped.write_text(snap_svg_text(source.read_text(encoding="utf-8", errors="replace")), encoding="utf-8")
    png_path = PNG_DIR / f"category_{code}.png"
    if not rasterize_svg(snapped, png_path, width=width):
        raise RuntimeError(f"rasterize failed {code}")
    return snap_raster(Image.open(png_path))


def crop_visible(image: Image.Image, drop_dark_corners: bool) -> Image.Image:
    arr = np.array(image.convert("RGBA"))
    rgb = arr[:, :, :3]
    alpha = arr[:, :, 3]
    visible = alpha > 16
    if drop_dark_corners:
        visible &= rgb.max(axis=2) > 22
    ys, xs = np.where(visible)
    if ys.size == 0:
        return image
    return image.crop((int(xs.min()), int(ys.min()), int(xs.max()) + 1, int(ys.max()) + 1))


def fit(image: Image.Image, box: int) -> Image.Image:
    work = image.convert("RGBA")
    work.thumbnail((box, box), Image.Resampling.LANCZOS)
    return work


def write_category_png(name: str, image: Image.Image) -> None:
    xml = VECTOR_DIR / f"{name}.xml"
    if xml.exists():
        xml.unlink()
    for leftover in DRAWABLE.glob(f"{name}.*"):
        leftover.unlink()
    dest = VECTOR_DIR / f"{name}.png"
    image.convert("RGBA").save(dest, format="PNG", optimize=True)


def render_additional() -> None:
    main = crop_visible(rasterize_named("D-001", 1200), drop_dark_corners=True)
    plate = crop_visible(rasterize_named("H-012", 1200), drop_dark_corners=False)
    canvas = Image.new("RGBA", (CANVAS, CANVAS), WHITE + (255,))
    main_fit = fit(main, 640)
    plate_fit = fit(plate, 760)
    if plate_fit.height > 230:
        scale = 230 / plate_fit.height
        plate_fit = plate_fit.resize(
            (max(1, int(plate_fit.width * scale)), 230),
            Image.Resampling.LANCZOS,
        )
    gap = 28
    total_h = main_fit.height + gap + plate_fit.height
    top = (CANVAS - total_h) // 2
    canvas.alpha_composite(main_fit, ((CANVAS - main_fit.width) // 2, top))
    canvas.alpha_composite(
        plate_fit,
        ((CANVAS - plate_fit.width) // 2, top + main_fit.height + gap),
    )
    write_category_png("kategoria_kiegeszito", canvas)


def render_route_type() -> None:
    diamond = crop_visible(rasterize_named("B-003", 1400), drop_dark_corners=True)
    motorway = crop_visible(rasterize_named("E-016", 1200), drop_dark_corners=True)
    canvas = Image.new("RGBA", (CANVAS, CANVAS), WHITE + (255,))
    diamond_fit = fit(diamond, 820)
    motorway_fit = fit(motorway, 430)
    canvas.alpha_composite(diamond_fit, (48, 70))
    canvas.alpha_composite(motorway_fit, (CANVAS - motorway_fit.width - 36, CANVAS - motorway_fit.height - 40))
    write_category_png("kategoria_utvonaltipus", canvas)


def main() -> None:
    VECTOR_DIR.mkdir(parents=True, exist_ok=True)
    for name, xml in ICONS.items():
        (VECTOR_DIR / f"{name}.xml").write_text(xml, encoding="utf-8")
        for leftover in DRAWABLE.glob(f"{name}.*"):
            leftover.unlink()
        png_default = VECTOR_DIR / f"{name}.png"
        if png_default.exists():
            png_default.unlink()
        print(name)
    render_additional()
    print("kategoria_kiegeszito")
    render_route_type()
    print("kategoria_utvonaltipus")


if __name__ == "__main__":
    main()
