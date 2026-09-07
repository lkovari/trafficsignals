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
CAR = (0xEE, 0xF1, 0xF4)
VEST = (0xF5, 0xC4, 0x00)


def rgba(rgb: tuple[int, int, int], a: int = 255) -> tuple[int, int, int, int]:
    return rgb + (a,)


def disk(draw: ImageDraw.ImageDraw, xy: tuple[float, float], radius: float, fill) -> None:
    x, y = xy
    draw.ellipse([x - radius, y - radius, x + radius, y + radius], fill=fill)


def outlined_disk(
    draw: ImageDraw.ImageDraw, xy: tuple[float, float], radius: float, fill, outline_width: float
) -> None:
    disk(draw, xy, radius + outline_width, rgba(BLACK))
    disk(draw, xy, radius, fill)


def thick_line(
    draw: ImageDraw.ImageDraw, a: tuple[float, float], b: tuple[float, float], width: int, fill
) -> None:
    draw.line([a, b], fill=fill, width=width)
    disk(draw, a, width / 2, fill)
    disk(draw, b, width / 2, fill)


def arrow(
    draw: ImageDraw.ImageDraw, start: tuple[float, float], end: tuple[float, float], width: int, fill
) -> None:
    thick_line(draw, start, end, width, fill)
    dx = end[0] - start[0]
    dy = end[1] - start[1]
    mag = max(1e-6, math.hypot(dx, dy))
    ux, uy = dx / mag, dy / mag
    px, py = -uy, ux
    length = width * 2.6
    spread = width * 1.8
    left = (end[0] - ux * length + px * spread, end[1] - uy * length + py * spread)
    right = (end[0] - ux * length - px * spread, end[1] - uy * length - py * spread)
    draw.polygon([end, left, right], fill=fill)


def rotate(cx: float, cy: float, x: float, y: float, ang: float) -> tuple[float, float]:
    cos_a, sin_a = math.cos(ang), math.sin(ang)
    dx, dy = x - cx, y - cy
    return cx + dx * cos_a - dy * sin_a, cy + dx * sin_a + dy * cos_a


def octagon(draw: ImageDraw.ImageDraw, cx: float, cy: float, radius: float, fill) -> None:
    pts = []
    for i in range(8):
        a = math.radians(22.5 + i * 45)
        pts.append((cx + radius * math.cos(a), cy + radius * math.sin(a)))
    draw.polygon(pts, fill=fill)


def stop_mark(draw: ImageDraw.ImageDraw, cx: float, cy: float, radius: float = 36) -> None:
    octagon(draw, cx, cy, radius + 5, rgba(BLACK))
    octagon(draw, cx, cy, radius, rgba(SIGN_RED))
    octagon(draw, cx, cy, radius * 0.42, rgba(WHITE))


def arc_arrow(
    draw: ImageDraw.ImageDraw,
    cx: float,
    cy: float,
    radius: float,
    start_deg: float,
    end_deg: float,
    width: int,
    fill,
) -> None:
    steps = 18
    pts = []
    for i in range(steps + 1):
        t = i / steps
        ang = math.radians(start_deg + (end_deg - start_deg) * t)
        pts.append((cx + radius * math.cos(ang), cy + radius * math.sin(ang)))
    for a, b in zip(pts[:-1], pts[1:]):
        thick_line(draw, a, b, width, fill)
    arrow(draw, pts[-3], pts[-1], width, fill)


def car_top(
    draw: ImageDraw.ImageDraw,
    cx: float,
    cy: float,
    heading_deg: float,
    scale: float = 1.0,
    fill: tuple[int, int, int] = CAR,
) -> None:
    ang = math.radians(heading_deg)
    length = 70 * scale
    width = 38 * scale
    local = [
        (length * 0.55, 0.0),
        (length * 0.22, width * 0.52),
        (-length * 0.48, width * 0.48),
        (-length * 0.48, -width * 0.48),
        (length * 0.22, -width * 0.52),
    ]
    pts = [rotate(cx, cy, cx + x, cy + y, ang) for x, y in local]
    draw.polygon(pts, fill=rgba(BLACK))
    inner = [
        (length * 0.46, 0.0),
        (length * 0.16, width * 0.38),
        (-length * 0.40, width * 0.36),
        (-length * 0.40, -width * 0.36),
        (length * 0.16, -width * 0.38),
    ]
    draw.polygon([rotate(cx, cy, cx + x, cy + y, ang) for x, y in inner], fill=rgba(fill))
    glass = [
        (length * 0.22, 0.0),
        (length * 0.02, width * 0.22),
        (-length * 0.08, width * 0.20),
        (-length * 0.08, -width * 0.20),
        (length * 0.02, -width * 0.22),
    ]
    draw.polygon([rotate(cx, cy, cx + x, cy + y, ang) for x, y in glass], fill=rgba(SIGN_BLUE))


def draw_roads(draw: ImageDraw.ImageDraw) -> None:
    draw.rectangle([0, 350, SIZE - 1, 674], fill=rgba(ROAD))
    draw.rectangle([350, 0, 674, SIZE - 1], fill=rgba(ROAD))
    dash = 40
    gap = 26
    x = 28
    while x < SIZE - 28:
        x_end = min(SIZE - 28, x + dash)
        if x_end > x:
            draw.rectangle([x, 504, x_end, 520], fill=rgba(ROAD_LINE))
        x += dash + gap
    y = 28
    while y < SIZE - 28:
        y_end = min(SIZE - 28, y + dash)
        if y_end > y:
            draw.rectangle([504, y, 520, y_end], fill=rgba(ROAD_LINE))
        y += dash + gap


def draw_officer_top(draw: ImageDraw.ImageDraw, facing: str = "north") -> tuple[float, float, float, float, float, float]:
    cx, cy = 512.0, 512.0
    angles = {"north": -math.pi / 2, "east": 0.0, "south": math.pi / 2, "west": math.pi}
    ang = angles[facing]
    ux, uy = math.cos(ang), math.sin(ang)
    px, py = -uy, ux
    torso = [
        (cx + ux * 78 + px * 40, cy + uy * 78 + py * 40),
        (cx + ux * 78 - px * 40, cy + uy * 78 - py * 40),
        (cx - ux * 70 - px * 50, cy - uy * 70 - py * 50),
        (cx - ux * 70 + px * 50, cy - uy * 70 + py * 50),
    ]
    under = [
        (cx + ux * 84 + px * 46, cy + uy * 84 + py * 46),
        (cx + ux * 84 - px * 46, cy + uy * 84 - py * 46),
        (cx - ux * 76 - px * 56, cy - uy * 76 - py * 56),
        (cx - ux * 76 + px * 56, cy - uy * 76 + py * 56),
    ]
    draw.polygon(under, fill=rgba(BLACK))
    draw.polygon(torso, fill=rgba(SIGN_BLUE))
    vest_a = (cx + ux * 18 + px * 36, cy + uy * 18 + py * 36)
    vest_b = (cx + ux * 18 - px * 36, cy + uy * 18 - py * 36)
    vest_c = (cx - ux * 10 - px * 40, cy - uy * 10 - py * 40)
    vest_d = (cx - ux * 10 + px * 40, cy - uy * 10 + py * 40)
    draw.polygon([vest_a, vest_b, vest_c, vest_d], fill=rgba(VEST))
    belt_a = (cx - ux * 8 + px * 42, cy - uy * 8 + py * 42)
    belt_b = (cx - ux * 8 - px * 42, cy - uy * 8 - py * 42)
    thick_line(draw, belt_a, belt_b, 14, rgba(WHITE))
    head = (cx + ux * 108, cy + uy * 108)
    outlined_disk(draw, head, 32, rgba(WHITE), 6)
    visor_c = (head[0] + ux * 22, head[1] + uy * 22)
    brim_a = (visor_c[0] + px * 28, visor_c[1] + py * 28)
    brim_b = (visor_c[0] - px * 28, visor_c[1] - py * 28)
    thick_line(draw, brim_a, brim_b, 12, rgba(BLACK))
    cap_a = (head[0] - ux * 10 + px * 22, head[1] - uy * 10 + py * 22)
    cap_b = (head[0] - ux * 10 - px * 22, head[1] - uy * 10 - py * 22)
    thick_line(draw, cap_a, cap_b, 16, rgba(WHITE))
    return cx, cy, ux, uy, px, py


def arms_out(draw: ImageDraw.ImageDraw, cx: float, cy: float, px: float, py: float) -> None:
    thick_line(draw, (cx + px * 36, cy + py * 36), (cx + px * 168, cy + py * 168), 26, rgba(BLACK))
    thick_line(draw, (cx - px * 36, cy - py * 36), (cx - px * 168, cy - py * 168), 26, rgba(BLACK))
    thick_line(draw, (cx + px * 36, cy + py * 36), (cx + px * 168, cy + py * 168), 20, rgba(SIGN_BLUE))
    thick_line(draw, (cx - px * 36, cy - py * 36), (cx - px * 168, cy - py * 168), 20, rgba(SIGN_BLUE))
    outlined_disk(draw, (cx + px * 168, cy + py * 168), 22, rgba(WHITE), 5)
    outlined_disk(draw, (cx - px * 168, cy - py * 168), 22, rgba(WHITE), 5)


def arms_down(
    draw: ImageDraw.ImageDraw, cx: float, cy: float, ux: float, uy: float, px: float, py: float
) -> None:
    l_end = (cx - ux * 88 + px * 42, cy - uy * 88 + py * 42)
    r_end = (cx - ux * 88 - px * 42, cy - uy * 88 - py * 42)
    thick_line(draw, (cx + px * 38, cy + py * 38), l_end, 22, rgba(BLACK))
    thick_line(draw, (cx - px * 38, cy - py * 38), r_end, 22, rgba(BLACK))
    thick_line(draw, (cx + px * 38, cy + py * 38), l_end, 16, rgba(SIGN_BLUE))
    thick_line(draw, (cx - px * 38, cy - py * 38), r_end, 16, rgba(SIGN_BLUE))
    outlined_disk(draw, l_end, 18, rgba(WHITE), 4)
    outlined_disk(draw, r_end, 18, rgba(WHITE), 4)


def canvas() -> tuple[Image.Image, ImageDraw.ImageDraw]:
    image = Image.new("RGBA", (SIZE, SIZE), rgba(WHITE))
    return image, ImageDraw.Draw(image)


def save(sign_id: str, image: Image.Image) -> None:
    write_drawable_png(sign_id, image)
    print(sign_id)


def go_from_east(draw: ImageDraw.ImageDraw) -> None:
    car_top(draw, 900, 470, 180, 1.15)
    arrow(draw, (820, 512), (690, 512), 28, rgba(GO))


def go_from_west(draw: ImageDraw.ImageDraw) -> None:
    car_top(draw, 124, 554, 0, 1.15)
    arrow(draw, (204, 512), (334, 512), 28, rgba(GO))


def stop_from_north(draw: ImageDraw.ImageDraw) -> None:
    car_top(draw, 470, 124, 90, 1.05)
    stop_mark(draw, 512, 220)


def stop_from_south(draw: ImageDraw.ImageDraw) -> None:
    car_top(draw, 554, 900, -90, 1.05)
    stop_mark(draw, 512, 804)


def stop_from_east(draw: ImageDraw.ImageDraw) -> None:
    car_top(draw, 900, 470, 180, 1.05)
    stop_mark(draw, 804, 512)


def stop_from_west(draw: ImageDraw.ImageDraw) -> None:
    car_top(draw, 124, 554, 0, 1.05)
    stop_mark(draw, 220, 512)


def draw_karokoldalra() -> None:
    image, draw = canvas()
    draw_roads(draw)
    cx, cy, _ux, _uy, px, py = draw_officer_top(draw, "north")
    arms_out(draw, cx, cy, px, py)
    go_from_west(draw)
    go_from_east(draw)
    stop_from_north(draw)
    stop_from_south(draw)
    save("rendori_karokoldalra", image)


def draw_alapallas() -> None:
    image, draw = canvas()
    draw_roads(draw)
    cx, cy, ux, uy, px, py = draw_officer_top(draw, "north")
    arms_down(draw, cx, cy, ux, uy, px, py)
    go_from_west(draw)
    go_from_east(draw)
    stop_from_north(draw)
    stop_from_south(draw)
    save("rendori_alapallas", image)


def draw_balramogott() -> None:
    image, draw = canvas()
    draw_roads(draw)
    cx, cy, ux, uy, px, py = draw_officer_top(draw, "north")
    left_hand = (cx - px * 150, cy - py * 150)
    right_hand = (cx + px * 36 - ux * 130, cy + py * 36 - uy * 130)
    thick_line(draw, (cx - px * 36, cy - py * 36), left_hand, 26, rgba(BLACK))
    thick_line(draw, (cx + px * 28, cy + py * 28), right_hand, 26, rgba(BLACK))
    thick_line(draw, (cx - px * 36, cy - py * 36), left_hand, 20, rgba(SIGN_BLUE))
    thick_line(draw, (cx + px * 28, cy + py * 28), right_hand, 20, rgba(SIGN_BLUE))
    outlined_disk(draw, left_hand, 22, rgba(WHITE), 5)
    outlined_disk(draw, right_hand, 22, rgba(WHITE), 5)
    car_top(draw, 900, 470, 180, 1.15)
    arrow(draw, (820, 470), (690, 470), 24, rgba(GO))
    arrow(draw, (780, 430), (780, 250), 22, rgba(GO))
    arc_arrow(draw, 512, 512, 210, 12, 88, 22, rgba(GO))
    stop_from_west(draw)
    stop_from_north(draw)
    stop_from_south(draw)
    save("rendori_balramogott", image)


def draw_balraelott() -> None:
    image, draw = canvas()
    draw_roads(draw)
    cx, cy, ux, uy, px, py = draw_officer_top(draw, "north")
    right_hand = (cx + ux * 150, cy + uy * 150)
    left_hand = (cx - px * 40 + ux * 110, cy - py * 40 + uy * 110)
    thick_line(draw, (cx + px * 24, cy + py * 24), right_hand, 26, rgba(BLACK))
    thick_line(draw, (cx - px * 32, cy - py * 32), left_hand, 26, rgba(BLACK))
    thick_line(draw, (cx + px * 24, cy + py * 24), right_hand, 20, rgba(SIGN_BLUE))
    thick_line(draw, (cx - px * 32, cy - py * 32), left_hand, 20, rgba(SIGN_BLUE))
    outlined_disk(draw, right_hand, 22, rgba(WHITE), 5)
    outlined_disk(draw, left_hand, 22, rgba(WHITE), 5)
    car_top(draw, 124, 554, 0, 1.15)
    arrow(draw, (204, 554), (334, 554), 24, rgba(GO))
    arrow(draw, (244, 594), (244, 770), 22, rgba(GO))
    arc_arrow(draw, 512, 512, 210, 168, 268, 22, rgba(GO))
    stop_from_east(draw)
    stop_from_north(draw)
    stop_from_south(draw)
    save("rendori_balraelott", image)


def draw_officer_side(
    draw: ImageDraw.ImageDraw,
    cx: float,
    cy: float,
    scale: float,
    left_hand: tuple[float, float],
    right_hand: tuple[float, float],
    vest: tuple[int, int, int] = VEST,
    helmet: bool = False,
) -> None:
    s = scale
    head = (cx, cy - 118 * s)
    outlined_disk(draw, head, 40 * s, rgba(WHITE), 6 * s)
    if helmet:
        draw.pieslice(
            [cx - 48 * s, cy - 178 * s, cx + 48 * s, cy - 88 * s],
            start=180,
            end=0,
            fill=rgba(VEST),
            outline=rgba(BLACK),
            width=max(3, int(5 * s)),
        )
    else:
        cap = [cx - 40 * s, cy - 172 * s, cx + 40 * s, cy - 132 * s]
        draw.rounded_rectangle(cap, radius=10 * s, fill=rgba(WHITE), outline=rgba(BLACK), width=max(3, int(5 * s)))
        draw.polygon(
            [
                (cx - 44 * s, cy - 132 * s),
                (cx + 48 * s, cy - 132 * s),
                (cx + 42 * s, cy - 118 * s),
                (cx - 40 * s, cy - 118 * s),
            ],
            fill=rgba(BLACK),
        )
    torso = [cx - 56 * s, cy - 92 * s, cx + 56 * s, cy + 78 * s]
    draw.rounded_rectangle(torso, radius=20 * s, fill=rgba(SIGN_BLUE), outline=rgba(BLACK), width=max(3, int(5 * s)))
    draw.rectangle([cx - 44 * s, cy - 70 * s, cx + 44 * s, cy + 28 * s], fill=rgba(vest))
    draw.rectangle([cx - 56 * s, cy - 6 * s, cx + 56 * s, cy + 16 * s], fill=rgba(WHITE))
    thick_line(draw, (cx - 20 * s, cy + 78 * s), (cx - 32 * s, cy + 188 * s), int(26 * s), rgba(BLACK))
    thick_line(draw, (cx + 20 * s, cy + 78 * s), (cx + 32 * s, cy + 188 * s), int(26 * s), rgba(BLACK))
    l_sh = (cx - 56 * s, cy - 68 * s)
    r_sh = (cx + 56 * s, cy - 68 * s)
    thick_line(draw, l_sh, left_hand, int(24 * s), rgba(BLACK))
    thick_line(draw, r_sh, right_hand, int(24 * s), rgba(BLACK))
    thick_line(draw, l_sh, left_hand, int(18 * s), rgba(SIGN_BLUE))
    thick_line(draw, r_sh, right_hand, int(18 * s), rgba(SIGN_BLUE))
    outlined_disk(draw, left_hand, 16 * s, rgba(WHITE), 5 * s)
    outlined_disk(draw, right_hand, 16 * s, rgba(WHITE), 5 * s)


def car_side(
    draw: ImageDraw.ImageDraw,
    x: float,
    y: float,
    w: float,
    h: float,
    police: bool = False,
    facing_right: bool = True,
) -> None:
    body = [x, y, x + w, y + h]
    draw.rounded_rectangle(body, radius=18, fill=rgba(WHITE), outline=rgba(BLACK), width=7)
    cabin = (0x3A, 0x6B, 0x9A) if police else (0x7A, 0x88, 0x96)
    draw.polygon(
        [(x + w * 0.18, y), (x + w * 0.32, y - h * 0.42), (x + w * 0.68, y - h * 0.42), (x + w * 0.82, y)],
        fill=rgba(cabin),
    )
    stripe_fill = SIGN_BLUE if police else (0x9A, 0xA3, 0xAB)
    draw.rectangle([x, y + h * 0.38, x + w, y + h * 0.62], fill=rgba(stripe_fill))
    disk(draw, (x + w * 0.22, y + h + 8), 22, rgba(BLACK))
    disk(draw, (x + w * 0.78, y + h + 8), 22, rgba(BLACK))
    disk(draw, (x + w * 0.22, y + h + 8), 10, rgba(ROAD))
    disk(draw, (x + w * 0.78, y + h + 8), 10, rgba(ROAD))
    light_x = x + w - 16 if facing_right else x + 16
    disk(draw, (light_x, y + h * 0.28), 8, rgba(SIGN_YELLOW))
    if police:
        bar = [x + w * 0.32, y - h * 0.62, x + w * 0.68, y - h * 0.42]
        draw.rounded_rectangle(bar, radius=8, fill=rgba(BLACK))
        disk(draw, (x + w * 0.40, y - h * 0.52), 10, rgba(SIGN_BLUE))
        disk(draw, (x + w * 0.50, y - h * 0.52), 10, rgba(SIGN_RED))
        disk(draw, (x + w * 0.60, y - h * 0.52), 10, rgba(SIGN_BLUE))


def traffic_light(draw: ImageDraw.ImageDraw, cx: float, cy: float, lit: str) -> None:
    draw.rounded_rectangle([cx - 40, cy - 110, cx + 40, cy + 110], radius=22, fill=rgba(BLACK))
    colors = {"red": SIGN_RED, "yellow": SIGN_YELLOW, "green": GO}
    positions = {"red": cy - 68, "yellow": cy, "green": cy + 68}
    for name, yy in positions.items():
        fill = colors[name] if name == lit else (0x3A, 0x3F, 0x45)
        outlined_disk(draw, (cx, yy), 24, rgba(fill), 3)


def stop_disc(draw: ImageDraw.ImageDraw, cx: float, cy: float, r: float) -> None:
    disk(draw, (cx, cy), r + 8, rgba(BLACK))
    disk(draw, (cx, cy), r, rgba(WHITE))
    disk(draw, (cx, cy), r * 0.78, rgba(SIGN_RED))


def draw_karfuggoleges() -> None:
    image, draw = canvas()
    draw.rectangle([0, 820, SIZE - 1, SIZE - 1], fill=rgba(ROAD))
    draw_officer_side(draw, 260, 560, 1.25, (120, 700), (300, 160))
    traffic_light(draw, 860, 240, "yellow")
    car_side(draw, 430, 720, 200, 80)
    stop_mark(draw, 400, 760, 28)
    car_side(draw, 720, 560, 180, 70)
    arrow(draw, (760, 500), (900, 430), 18, rgba(GO))
    save("rendori_karfuggoleges", image)


def draw_gyorsitas() -> None:
    image, draw = canvas()
    draw.rectangle([0, 820, SIZE - 1, SIZE - 1], fill=rgba(ROAD))
    chest = (280.0, 500.0)
    hand = (560.0, 400.0)
    draw_officer_side(draw, 280, 560, 1.25, (150, 710), hand)
    for t in (0.22, 0.48, 0.74):
        start = (hand[0] + (chest[0] - hand[0]) * t + 210 * (1.0 - t), hand[1] + (chest[1] - hand[1]) * t)
        end = (hand[0] + (chest[0] - hand[0]) * (t + 0.18), hand[1] + (chest[1] - hand[1]) * (t + 0.18))
        arrow(draw, start, end, 20, rgba(SIGN_YELLOW))
    car_side(draw, 620, 690, 250, 96, facing_right=False)
    arrow(draw, (860, 640), (640, 640), 22, rgba(GO))
    save("rendori_gyorsitas", image)


def draw_lassitas() -> None:
    image, draw = canvas()
    draw.rectangle([0, 820, SIZE - 1, SIZE - 1], fill=rgba(ROAD))
    hand = (600, 300)
    draw_officer_side(draw, 280, 560, 1.25, (150, 710), hand)
    arrow(draw, (730, 140), (730, 280), 22, rgba(SIGN_YELLOW))
    arrow(draw, (730, 560), (730, 420), 22, rgba(SIGN_YELLOW))
    thick_line(draw, (690, 300), (770, 300), 12, rgba(SIGN_YELLOW))
    car_side(draw, 620, 700, 250, 90)
    arrow(draw, (640, 660), (720, 660), 14, rgba(GO))
    arrow(draw, (760, 660), (820, 660), 10, rgba(GO))
    save("rendori_lassitas", image)


def draw_megallitotarcsa() -> None:
    image, draw = canvas()
    draw.rectangle([0, 820, SIZE - 1, SIZE - 1], fill=rgba(ROAD))
    disc = (730, 240)
    draw_officer_side(draw, 280, 560, 1.25, (140, 710), (540, 310))
    stop_disc(draw, disc[0], disc[1], 150)
    car_side(draw, 560, 700, 280, 100)
    stop_mark(draw, 520, 750, 32)
    save("rendori_megallitotarcsa", image)


def draw_megallitasjarmubol() -> None:
    image, draw = canvas()
    draw.rectangle([0, 720, SIZE - 1, SIZE - 1], fill=rgba(ROAD))
    car_side(draw, 40, 500, 470, 150, police=True)
    stop_disc(draw, 760, 250, 120)
    thick_line(draw, (480, 540), (680, 340), 18, rgba(BLACK))
    arrow(draw, (900, 110), (900, 210), 16, rgba(SIGN_YELLOW))
    arrow(draw, (900, 430), (900, 330), 16, rgba(SIGN_YELLOW))
    car_side(draw, 620, 640, 240, 88)
    stop_mark(draw, 590, 690, 30)
    save("rendori_megallitasjarmubol", image)


def draw_jelzoor() -> None:
    image, draw = canvas()
    draw.rectangle([0, 820, SIZE - 1, SIZE - 1], fill=rgba(ROAD))
    draw.rectangle([48, 760, 300, 820], fill=rgba(SIGN_RED))
    draw.rectangle([48, 700, 300, 760], fill=rgba(WHITE))
    draw.rectangle([48, 640, 300, 700], fill=rgba(SIGN_RED))
    orange = (0xE8, 0x5D, 0x00)
    draw_officer_side(draw, 400, 560, 1.15, (270, 700), (540, 340), vest=orange, helmet=True)
    stop_disc(draw, 780, 210, 130)
    thick_line(draw, (780, 340), (780, 800), 22, rgba(BLACK))
    disk(draw, (780, 808), 26, rgba(BLACK))
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
