#!/usr/bin/env python3
from __future__ import annotations

import math
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

sys.path.insert(0, str(Path(__file__).resolve().parent))

from palette import BLACK, SIGN_RED, SIGN_YELLOW, WHITE, write_drawable_png

SIZE = 1024
GO = (0x28, 0xA0, 0x3C)
ASPHALT = (0x3A, 0x3F, 0x45)
CURB = (0xC5, 0xC9, 0xCE)


def rgba(rgb: tuple[int, int, int], a: int = 255) -> tuple[int, int, int, int]:
    return rgb + (a,)


def canvas() -> tuple[Image.Image, ImageDraw.ImageDraw]:
    image = Image.new("RGBA", (SIZE, SIZE), rgba(WHITE))
    return image, ImageDraw.Draw(image)


def save(sign_id: str, image: Image.Image) -> None:
    write_drawable_png(sign_id, image)
    print(sign_id)


def disk(draw: ImageDraw.ImageDraw, xy: tuple[float, float], radius: float, fill) -> None:
    x, y = xy
    draw.ellipse([x - radius, y - radius, x + radius, y + radius], fill=fill)


def thick_line(draw: ImageDraw.ImageDraw, a: tuple[float, float], b: tuple[float, float], width: int, fill) -> None:
    draw.line([a, b], fill=fill, width=width)
    disk(draw, a, width / 2, fill)
    disk(draw, b, width / 2, fill)


def arrow(draw: ImageDraw.ImageDraw, start: tuple[float, float], end: tuple[float, float], width: int, fill) -> None:
    thick_line(draw, start, end, width, fill)
    dx = end[0] - start[0]
    dy = end[1] - start[1]
    mag = max(1e-6, math.hypot(dx, dy))
    ux, uy = dx / mag, dy / mag
    px, py = -uy, ux
    length = width * 2.4
    spread = width * 1.7
    left = (end[0] - ux * length + px * spread, end[1] - uy * length + py * spread)
    right = (end[0] - ux * length - px * spread, end[1] - uy * length - py * spread)
    draw.polygon([end, left, right], fill=fill)


def housing(draw: ImageDraw.ImageDraw, box: list[float]) -> None:
    draw.rounded_rectangle(box, radius=36, fill=rgba(BLACK))


def draw_red_x() -> None:
    image, draw = canvas()
    housing(draw, [220, 180, 804, 844])
    cx, cy = 512.0, 512.0
    arm = 210
    width = 56
    thick_line(draw, (cx - arm, cy - arm), (cx + arm, cy + arm), width, rgba(SIGN_RED))
    thick_line(draw, (cx + arm, cy - arm), (cx - arm, cy + arm), width, rgba(SIGN_RED))
    save("fenyjelzo_savfoglaltsagpirosx", image)


def draw_green_arrow() -> None:
    image, draw = canvas()
    housing(draw, [220, 180, 804, 844])
    arrow(draw, (512, 250), (512, 760), 64, rgba(GO))
    save("fenyjelzo_savfoglaltsagzoldnyil", image)


def draw_amber_arrow() -> None:
    image, draw = canvas()
    housing(draw, [220, 180, 804, 844])
    arrow(draw, (360, 280), (680, 740), 58, rgba(SIGN_YELLOW))
    for i in range(3):
        y = 220 + i * 28
        thick_line(draw, (250, y), (310, y + 18), 8, rgba(SIGN_YELLOW))
    save("fenyjelzo_savfoglaltsagsarganyil", image)


def bike(draw: ImageDraw.ImageDraw, cx: float, cy: float, scale: float, fill) -> None:
    r = 22 * scale
    thick_line(draw, (cx - 38 * scale, cy + 8 * scale), (cx + 34 * scale, cy + 8 * scale), int(7 * scale), fill)
    disk(draw, (cx - 34 * scale, cy + 22 * scale), r, fill)
    disk(draw, (cx - 34 * scale, cy + 22 * scale), r * 0.45, rgba(BLACK))
    disk(draw, (cx + 34 * scale, cy + 22 * scale), r, fill)
    disk(draw, (cx + 34 * scale, cy + 22 * scale), r * 0.45, rgba(BLACK))
    thick_line(draw, (cx - 34 * scale, cy + 22 * scale), (cx, cy - 8 * scale), int(7 * scale), fill)
    thick_line(draw, (cx + 34 * scale, cy + 22 * scale), (cx, cy - 8 * scale), int(7 * scale), fill)
    thick_line(draw, (cx, cy - 8 * scale), (cx, cy - 28 * scale), int(7 * scale), fill)
    thick_line(draw, (cx, cy - 28 * scale), (cx + 22 * scale, cy - 28 * scale), int(7 * scale), fill)
    disk(draw, (cx, cy - 36 * scale), 8 * scale, fill)


def draw_cycle_signal() -> None:
    image, draw = canvas()
    housing(draw, [340, 80, 684, 944])
    colors = [SIGN_RED, SIGN_YELLOW, GO]
    ys = [240, 512, 784]
    for color, y in zip(colors, ys):
        disk(draw, (512, y), 108, color)
        bike(draw, 512, y + 8, 1.35, rgba(BLACK) if color != SIGN_YELLOW else rgba(BLACK))
    save("fenyjelzo_kerekparos", image)


def road_edge(draw: ImageDraw.ImageDraw) -> None:
    draw.rectangle([0, 0, SIZE - 1, SIZE - 1], fill=rgba(CURB))
    draw.polygon([(70, 0), (SIZE - 1, 0), (SIZE - 1, SIZE - 1), (280, SIZE - 1)], fill=rgba(ASPHALT))


def draw_yellow_solid() -> None:
    image, draw = canvas()
    road_edge(draw)
    thick_line(draw, (210, 40), (400, 984), 28, rgba(SIGN_YELLOW))
    save("utburkolat_megallasitilalomsargavonal", image)


def draw_yellow_broken() -> None:
    image, draw = canvas()
    road_edge(draw)
    x0, y0 = 210.0, 40.0
    x1, y1 = 400.0, 984.0
    dx, dy = x1 - x0, y1 - y0
    mag = math.hypot(dx, dy)
    ux, uy = dx / mag, dy / mag
    pos = 0.0
    on = 70.0
    off = 48.0
    while pos < mag:
        start = (x0 + ux * pos, y0 + uy * pos)
        end_pos = min(mag, pos + on)
        end = (x0 + ux * end_pos, y0 + uy * end_pos)
        thick_line(draw, start, end, 28, rgba(SIGN_YELLOW))
        pos += on + off
    save("utburkolat_varakozasitilalomsargavonal", image)


def draw_bus_wordmark() -> None:
    image, draw = canvas()
    draw.rectangle([0, 0, SIZE - 1, SIZE - 1], fill=rgba(ASPHALT))
    dash = 56
    gap = 40
    for y in (180, 820):
        x = 40
        while x < SIZE - 40:
            x_end = min(SIZE - 40, x + dash)
            draw.rectangle([x, y, x_end, y + 24], fill=rgba(WHITE))
            x += dash + gap
    font = None
    for path in (
        "/System/Library/Fonts/Supplemental/Arial Bold.ttf",
        "/System/Library/Fonts/Supplemental/Arial.ttf",
        "/Library/Fonts/Arial Bold.ttf",
    ):
        try:
            font = ImageFont.truetype(path, 210)
            break
        except OSError:
            continue
    if font is None:
        font = ImageFont.load_default()
    text = "BUSZ"
    bbox = draw.textbbox((0, 0), text, font=font)
    tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
    draw.text(((SIZE - tw) / 2, (SIZE - th) / 2 - 30), text, fill=rgba(WHITE), font=font)
    save("utburkolat_buszfelirat", image)


def main() -> None:
    draw_red_x()
    draw_green_arrow()
    draw_amber_arrow()
    draw_cycle_signal()
    draw_yellow_solid()
    draw_yellow_broken()
    draw_bus_wordmark()


if __name__ == "__main__":
    main()
