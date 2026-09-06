#!/usr/bin/env python3
from __future__ import annotations

import math
import sys
from pathlib import Path

from PIL import Image, ImageDraw

sys.path.insert(0, str(Path(__file__).resolve().parent))

from palette import (
    BLACK,
    SIGN_BLUE,
    SIGN_RED,
    SIGN_YELLOW,
    WHITE,
    write_drawable_png,
)

SIZE = 1024
GO = (0x28, 0xA0, 0x3C)
ROAD = (0xC5, 0xC9, 0xCE)
ROAD_LINE = WHITE


def rgba(rgb: tuple[int, int, int], a: int = 255) -> tuple[int, int, int, int]:
    return rgb + (a,)


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


def stop_bar(draw: ImageDraw.ImageDraw, center: tuple[float, float], across: tuple[float, float], length: float, width: int) -> None:
    mag = max(1e-6, math.hypot(across[0], across[1]))
    ux, uy = across[0] / mag, across[1] / mag
    a = (center[0] - ux * length / 2, center[1] - uy * length / 2)
    b = (center[0] + ux * length / 2, center[1] + uy * length / 2)
    thick_line(draw, a, b, width, rgba(SIGN_RED))


def draw_roads(draw: ImageDraw.ImageDraw) -> None:
    draw.rectangle([0, 390, SIZE - 1, 634], fill=rgba(ROAD))
    draw.rectangle([390, 0, 634, SIZE - 1], fill=rgba(ROAD))
    dash = 36
    gap = 28
    x = 40
    while x < SIZE - 40:
        x_end = min(SIZE - 40, x + dash)
        if x_end > x:
            draw.rectangle([x, 504, x_end, 520], fill=rgba(ROAD_LINE))
        x += dash + gap
    y = 40
    while y < SIZE - 40:
        y_end = min(SIZE - 40, y + dash)
        if y_end > y:
            draw.rectangle([504, y, 520, y_end], fill=rgba(ROAD_LINE))
        y += dash + gap


def draw_officer_top(draw: ImageDraw.ImageDraw, facing: str = "north") -> None:
    cx, cy = 512.0, 512.0
    angles = {"north": -math.pi / 2, "east": 0.0, "south": math.pi / 2, "west": math.pi}
    ang = angles[facing]
    ux, uy = math.cos(ang), math.sin(ang)
    px, py = -uy, ux
    torso = [
        (cx + ux * 54 + px * 28, cy + uy * 54 + py * 28),
        (cx + ux * 54 - px * 28, cy + uy * 54 - py * 28),
        (cx - ux * 46 - px * 34, cy - uy * 46 - py * 34),
        (cx - ux * 46 + px * 34, cy - uy * 46 + py * 34),
    ]
    draw.polygon(torso, fill=rgba(SIGN_BLUE))
    belt_a = (cx - ux * 4 + px * 32, cy - uy * 4 + py * 32)
    belt_b = (cx - ux * 4 - px * 32, cy - uy * 4 - py * 32)
    thick_line(draw, belt_a, belt_b, 10, rgba(WHITE))
    head = (cx + ux * 78, cy + uy * 78)
    disk(draw, head, 26, rgba(BLACK))
    disk(draw, head, 22, rgba(WHITE))
    brim_a = (head[0] + px * 24, head[1] + py * 24)
    brim_b = (head[0] - px * 24, head[1] - py * 24)
    thick_line(draw, brim_a, brim_b, 8, rgba(WHITE))
    return cx, cy, ux, uy, px, py


def arms_out(draw: ImageDraw.ImageDraw, cx: float, cy: float, px: float, py: float) -> None:
    thick_line(draw, (cx + px * 28, cy + py * 28), (cx + px * 118, cy + py * 118), 18, rgba(SIGN_BLUE))
    thick_line(draw, (cx - px * 28, cy - py * 28), (cx - px * 118, cy - py * 118), 18, rgba(SIGN_BLUE))
    disk(draw, (cx + px * 118, cy + py * 118), 16, rgba(WHITE))
    disk(draw, (cx - px * 118, cy - py * 118), 16, rgba(WHITE))


def arms_down(draw: ImageDraw.ImageDraw, cx: float, cy: float, ux: float, uy: float, px: float, py: float) -> None:
    thick_line(draw, (cx + px * 30, cy + py * 30), (cx - ux * 70 + px * 38, cy - uy * 70 + py * 38), 16, rgba(SIGN_BLUE))
    thick_line(draw, (cx - px * 30, cy - py * 30), (cx - ux * 70 - px * 38, cy - uy * 70 - py * 38), 16, rgba(SIGN_BLUE))
    disk(draw, (cx - ux * 70 + px * 38, cy - uy * 70 + py * 38), 14, rgba(WHITE))
    disk(draw, (cx - ux * 70 - px * 38, cy - uy * 70 - py * 38), 14, rgba(WHITE))


def canvas() -> tuple[Image.Image, ImageDraw.ImageDraw]:
    image = Image.new("RGBA", (SIZE, SIZE), rgba(WHITE))
    return image, ImageDraw.Draw(image)


def save(sign_id: str, image: Image.Image) -> None:
    write_drawable_png(sign_id, image)
    print(sign_id)


def draw_karokoldalra() -> None:
    image, draw = canvas()
    draw_roads(draw)
    cx, cy, ux, uy, px, py = draw_officer_top(draw, "north")
    arms_out(draw, cx, cy, px, py)
    arrow(draw, (70, 512), (250, 512), 22, rgba(GO))
    arrow(draw, (954, 512), (774, 512), 22, rgba(GO))
    stop_bar(draw, (512, 160), (1, 0), 150, 22)
    stop_bar(draw, (512, 864), (1, 0), 150, 22)
    save("rendori_karokoldalra", image)


def draw_alapallas() -> None:
    image, draw = canvas()
    draw_roads(draw)
    cx, cy, ux, uy, px, py = draw_officer_top(draw, "north")
    arms_down(draw, cx, cy, ux, uy, px, py)
    arrow(draw, (70, 512), (250, 512), 22, rgba(GO))
    arrow(draw, (954, 512), (774, 512), 22, rgba(GO))
    stop_bar(draw, (512, 160), (1, 0), 150, 22)
    stop_bar(draw, (512, 864), (1, 0), 150, 22)
    save("rendori_alapallas", image)


def draw_balramogott() -> None:
    image, draw = canvas()
    draw_roads(draw)
    cx, cy, ux, uy, px, py = draw_officer_top(draw, "north")
    thick_line(draw, (cx - px * 28, cy - py * 28), (cx - px * 110 - ux * 20, cy - py * 110 - uy * 20), 18, rgba(SIGN_BLUE))
    disk(draw, (cx - px * 110 - ux * 20, cy - py * 110 - uy * 20), 16, rgba(WHITE))
    thick_line(draw, (cx + px * 24, cy + py * 24), (cx + px * 40 - ux * 90, cy + py * 40 - uy * 90), 18, rgba(SIGN_BLUE))
    disk(draw, (cx + px * 40 - ux * 90, cy + py * 40 - uy * 90), 16, rgba(WHITE))
    arrow(draw, (900, 512), (700, 512), 20, rgba(GO))
    arrow(draw, (780, 470), (780, 280), 18, rgba(GO))
    arrow(draw, (780, 560), (780, 760), 18, rgba(GO))
    stop_bar(draw, (240, 512), (0, 1), 140, 22)
    stop_bar(draw, (512, 160), (1, 0), 140, 22)
    save("rendori_balramogott", image)


def draw_balraelott() -> None:
    image, draw = canvas()
    draw_roads(draw)
    cx, cy, ux, uy, px, py = draw_officer_top(draw, "north")
    thick_line(draw, (cx + px * 20, cy + py * 20), (cx + ux * 110, cy + uy * 110), 18, rgba(SIGN_BLUE))
    disk(draw, (cx + ux * 110, cy + uy * 110), 16, rgba(WHITE))
    thick_line(draw, (cx - px * 24, cy - py * 24), (cx - px * 50 + ux * 70, cy - py * 50 + uy * 70), 18, rgba(SIGN_BLUE))
    disk(draw, (cx - px * 50 + ux * 70, cy - py * 50 + uy * 70), 16, rgba(WHITE))
    arrow(draw, (124, 512), (324, 512), 20, rgba(GO))
    arrow(draw, (244, 470), (244, 280), 18, rgba(GO))
    arrow(draw, (244, 560), (244, 760), 18, rgba(GO))
    stop_bar(draw, (784, 512), (0, 1), 140, 22)
    stop_bar(draw, (512, 864), (1, 0), 140, 22)
    save("rendori_balraelott", image)


def outlined_disk(draw: ImageDraw.ImageDraw, xy: tuple[float, float], radius: float, fill, outline_width: float) -> None:
    disk(draw, xy, radius + outline_width, rgba(BLACK))
    disk(draw, xy, radius, fill)


def draw_officer_side(
    draw: ImageDraw.ImageDraw,
    cx: float,
    cy: float,
    scale: float,
    left_hand: tuple[float, float],
    right_hand: tuple[float, float],
) -> None:
    s = scale
    head = (cx, cy - 118 * s)
    outlined_disk(draw, head, 36 * s, rgba(WHITE), 5 * s)
    cap = [cx - 36 * s, cy - 160 * s, cx + 36 * s, cy - 128 * s]
    draw.rounded_rectangle(cap, radius=8 * s, fill=rgba(WHITE), outline=rgba(BLACK), width=max(3, int(5 * s)))
    draw.polygon(
        [(cx - 40 * s, cy - 128 * s), (cx + 44 * s, cy - 128 * s), (cx + 38 * s, cy - 118 * s), (cx - 36 * s, cy - 118 * s)],
        fill=rgba(BLACK),
    )
    torso = [cx - 48 * s, cy - 90 * s, cx + 48 * s, cy + 70 * s]
    draw.rounded_rectangle(torso, radius=18 * s, fill=rgba(SIGN_BLUE), outline=rgba(BLACK), width=max(3, int(4 * s)))
    draw.rectangle([cx - 48 * s, cy - 8 * s, cx + 48 * s, cy + 10 * s], fill=rgba(WHITE))
    thick_line(draw, (cx - 18 * s, cy + 70 * s), (cx - 28 * s, cy + 170 * s), int(22 * s), rgba(BLACK))
    thick_line(draw, (cx + 18 * s, cy + 70 * s), (cx + 28 * s, cy + 170 * s), int(22 * s), rgba(BLACK))
    l_sh = (cx - 48 * s, cy - 70 * s)
    r_sh = (cx + 48 * s, cy - 70 * s)
    thick_line(draw, l_sh, left_hand, int(18 * s), rgba(SIGN_BLUE))
    thick_line(draw, r_sh, right_hand, int(18 * s), rgba(SIGN_BLUE))
    outlined_disk(draw, left_hand, 14 * s, rgba(WHITE), 4 * s)
    outlined_disk(draw, right_hand, 14 * s, rgba(WHITE), 4 * s)


def motion_arcs(draw: ImageDraw.ImageDraw, origin: tuple[float, float], toward: tuple[float, float], count: int = 3) -> None:
    dx = toward[0] - origin[0]
    dy = toward[1] - origin[1]
    mag = max(1e-6, math.hypot(dx, dy))
    ux, uy = dx / mag, dy / mag
    for i in range(count):
        t = 18 + i * 22
        a = (origin[0] + ux * t, origin[1] + uy * t)
        b = (a[0] + ux * 16, a[1] + uy * 16)
        arrow(draw, a, b, 8, rgba(SIGN_YELLOW))


def draw_karfuggoleges() -> None:
    image, draw = canvas()
    draw.rectangle([0, 820, SIZE - 1, SIZE - 1], fill=rgba(ROAD))
    draw_officer_side(draw, 512, 560, 1.15, (380, 620), (590, 220))
    disk(draw, (512, 140), 48, rgba(SIGN_YELLOW))
    save("rendori_karfuggoleges", image)


def draw_gyorsitas() -> None:
    image, draw = canvas()
    draw.rectangle([0, 820, SIZE - 1, SIZE - 1], fill=rgba(ROAD))
    hand = (620, 470)
    draw_officer_side(draw, 430, 560, 1.15, (300, 680), hand)
    motion_arcs(draw, hand, (430, 490))
    save("rendori_gyorsitas", image)


def draw_lassitas() -> None:
    image, draw = canvas()
    draw.rectangle([0, 820, SIZE - 1, SIZE - 1], fill=rgba(ROAD))
    hand = (640, 360)
    draw_officer_side(draw, 430, 560, 1.15, (300, 680), hand)
    arrow(draw, (700, 250), (700, 340), 12, rgba(SIGN_YELLOW))
    arrow(draw, (700, 520), (700, 430), 12, rgba(SIGN_YELLOW))
    save("rendori_lassitas", image)


def stop_disc(draw: ImageDraw.ImageDraw, cx: float, cy: float, r: float) -> None:
    disk(draw, (cx, cy), r + 6, rgba(BLACK))
    disk(draw, (cx, cy), r, rgba(WHITE))
    disk(draw, (cx, cy), r * 0.86, rgba(SIGN_RED))


def draw_megallitotarcsa() -> None:
    image, draw = canvas()
    draw.rectangle([0, 820, SIZE - 1, SIZE - 1], fill=rgba(ROAD))
    disc = (640, 250)
    draw_officer_side(draw, 430, 560, 1.15, (300, 680), (600, 300))
    stop_disc(draw, disc[0], disc[1], 92)
    save("rendori_megallitotarcsa", image)


def draw_megallitasjarmubol() -> None:
    image, draw = canvas()
    draw.rectangle([0, 640, SIZE - 1, SIZE - 1], fill=rgba(ROAD))
    body = [140, 430, 780, 640]
    draw.rounded_rectangle(body, radius=28, fill=rgba(WHITE), outline=rgba(BLACK), width=8)
    draw.rectangle([140, 500, 780, 560], fill=rgba(SIGN_BLUE))
    draw.polygon([(780, 470), (900, 540), (900, 640), (780, 640)], fill=rgba(WHITE), outline=rgba(BLACK))
    draw.line([(780, 470), (900, 540), (900, 640), (780, 640)], fill=rgba(BLACK), width=8)
    disk(draw, (260, 660), 48, rgba(BLACK))
    disk(draw, (700, 660), 48, rgba(BLACK))
    disk(draw, (260, 660), 22, rgba(ROAD))
    disk(draw, (700, 660), 22, rgba(ROAD))
    disk(draw, (430, 400), 28, rgba(SIGN_BLUE))
    disk(draw, (510, 400), 28, rgba(SIGN_RED))
    stop_disc(draw, 820, 280, 80)
    thick_line(draw, (760, 480), (800, 340), 14, rgba(BLACK))
    save("rendori_megallitasjarmubol", image)


def draw_jelzoor() -> None:
    image, draw = canvas()
    draw.rectangle([0, 820, SIZE - 1, SIZE - 1], fill=rgba(ROAD))
    draw_officer_side(draw, 400, 560, 1.1, (280, 680), (560, 320))
    draw.rectangle([388, 430, 412, 700], fill=rgba(SIGN_YELLOW))
    stop_disc(draw, 620, 240, 100)
    thick_line(draw, (620, 340), (620, 760), 18, rgba(BLACK))
    disk(draw, (620, 760), 22, rgba(BLACK))
    save("rendori_jelzoor", image)


def main() -> None:
    draw_karokoldalra()
    draw_karfuggoleges()
    draw_balramogott()
    draw_balraelott()
    draw_alapallas()
    draw_gyorsitas()
    draw_lassitas()
    draw_megallitotarcsa()
    draw_megallitasjarmubol()
    draw_jelzoor()


if __name__ == "__main__":
    main()
