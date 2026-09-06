#!/usr/bin/env python3
from __future__ import annotations

import math
import sys
from pathlib import Path

from PIL import Image, ImageDraw

sys.path.insert(0, str(Path(__file__).resolve().parent))

from palette import ASPHALT, ROOT, SIGN_BLUE, SIGN_RED, SIGN_YELLOW, WHITE

SCALE = 0.76
CX = 54.0
CY = 54.0
VIEW = 108.0


def xform(x: float, y: float) -> tuple[float, float]:
    return CX + SCALE * (x - CX), CY + SCALE * (y - CY)


def xform_r(r: float) -> float:
    return r * SCALE


def fmt(value: float) -> str:
    return f"{value:.2f}".rstrip("0").rstrip(".")


def circle_path(cx: float, cy: float, r: float) -> str:
    x0 = cx - r
    return f"M{fmt(x0)},{fmt(cy)} a{fmt(r)},{fmt(r)} 0 1,0 {fmt(2 * r)},0 a{fmt(r)},{fmt(r)} 0 1,0 {fmt(-2 * r)},0"


def write_vector() -> None:
    t1 = xform(54, 22)
    t2 = xform(79, 63)
    t3 = xform(29, 63)
    y1 = xform(54, 25.4)
    y2 = xform(75.8, 60.2)
    y3 = xform(32.2, 60.2)
    bar = xform(51.8, 34)
    bar_w, bar_h = xform_r(4.4), xform_r(13)
    dot = xform(51.8, 49.6)
    dot_s = xform_r(4.4)
    red_c = xform(38, 69)
    red_outer = xform_r(17)
    red_fill = xform_r(16)
    red_inner = xform_r(10.8)
    blue_c = xform(70, 69)
    blue_outer = xform_r(17)
    blue_fill = xform_r(16)
    a1 = xform(70, 56.2)
    a2 = xform(80.4, 67.6)
    a3 = xform(74.3, 67.6)
    a4 = xform(74.3, 81)
    a5 = xform(65.7, 81)
    a6 = xform(65.7, 67.6)
    a7 = xform(59.6, 67.6)

    xml = f"""<?xml version="1.0" encoding="utf-8"?>
<vector xmlns:android="http://schemas.android.com/apk/res/android"
    android:width="108dp"
    android:height="108dp"
    android:viewportWidth="108"
    android:viewportHeight="108">
    <path
        android:fillColor="#1B1F24"
        android:pathData="M{fmt(t1[0])},{fmt(t1[1])} L{fmt(t2[0])},{fmt(t2[1])} L{fmt(t3[0])},{fmt(t3[1])} Z" />
    <path
        android:fillColor="#F5C400"
        android:pathData="M{fmt(y1[0])},{fmt(y1[1])} L{fmt(y2[0])},{fmt(y2[1])} L{fmt(y3[0])},{fmt(y3[1])} Z" />
    <path
        android:fillColor="#1B1F24"
        android:pathData="M{fmt(bar[0])},{fmt(bar[1])}h{fmt(bar_w)}v{fmt(bar_h)}h-{fmt(bar_w)}z" />
    <path
        android:fillColor="#1B1F24"
        android:pathData="M{fmt(dot[0])},{fmt(dot[1])}h{fmt(dot_s)}v{fmt(dot_s)}h-{fmt(dot_s)}z" />
    <path
        android:fillColor="#1B1F24"
        android:pathData="{circle_path(red_c[0], red_c[1], red_outer)}" />
    <path
        android:fillColor="#C8102E"
        android:pathData="{circle_path(red_c[0], red_c[1], red_fill)}" />
    <path
        android:fillColor="#FFFFFF"
        android:pathData="{circle_path(red_c[0], red_c[1], red_inner)}" />
    <path
        android:fillColor="#1B1F24"
        android:pathData="{circle_path(blue_c[0], blue_c[1], blue_outer)}" />
    <path
        android:fillColor="#0050A0"
        android:pathData="{circle_path(blue_c[0], blue_c[1], blue_fill)}" />
    <path
        android:fillColor="#FFFFFF"
        android:pathData="M{fmt(a1[0])},{fmt(a1[1])} L{fmt(a2[0])},{fmt(a2[1])} H{fmt(a3[0])} V{fmt(a4[1])} H{fmt(a5[0])} V{fmt(a6[1])} H{fmt(a7[0])} Z" />
</vector>
"""
    dest = ROOT / "app/src/main/res/drawable/ic_launcher_foreground.xml"
    dest.write_text(xml, encoding="utf-8")


def write_svg() -> str:
    t1 = xform(54, 22)
    t2 = xform(79, 63)
    t3 = xform(29, 63)
    y1 = xform(54, 25.4)
    y2 = xform(75.8, 60.2)
    y3 = xform(32.2, 60.2)
    bar = xform(51.8, 34)
    bar_w, bar_h = xform_r(4.4), xform_r(13)
    dot = xform(51.8, 49.6)
    dot_s = xform_r(4.4)
    red_c = xform(38, 69)
    red_outer = xform_r(17)
    red_fill = xform_r(16)
    red_inner = xform_r(10.8)
    blue_c = xform(70, 69)
    blue_outer = xform_r(17)
    blue_fill = xform_r(16)
    a1 = xform(70, 56.2)
    a2 = xform(80.4, 67.6)
    a3 = xform(74.3, 67.6)
    a4 = xform(74.3, 81)
    a5 = xform(65.7, 81)
    a6 = xform(65.7, 67.6)
    a7 = xform(59.6, 67.6)
    svg = f"""<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" width="108" height="108" viewBox="0 0 108 108">
  <rect width="108" height="108" fill="#1B1F24"/>
  <polygon points="{fmt(t1[0])},{fmt(t1[1])} {fmt(t2[0])},{fmt(t2[1])} {fmt(t3[0])},{fmt(t3[1])}" fill="#1B1F24"/>
  <polygon points="{fmt(y1[0])},{fmt(y1[1])} {fmt(y2[0])},{fmt(y2[1])} {fmt(y3[0])},{fmt(y3[1])}" fill="#F5C400"/>
  <rect x="{fmt(bar[0])}" y="{fmt(bar[1])}" width="{fmt(bar_w)}" height="{fmt(bar_h)}" fill="#1B1F24"/>
  <rect x="{fmt(dot[0])}" y="{fmt(dot[1])}" width="{fmt(dot_s)}" height="{fmt(dot_s)}" fill="#1B1F24"/>
  <circle cx="{fmt(red_c[0])}" cy="{fmt(red_c[1])}" r="{fmt(red_outer)}" fill="#1B1F24"/>
  <circle cx="{fmt(red_c[0])}" cy="{fmt(red_c[1])}" r="{fmt(red_fill)}" fill="#C8102E"/>
  <circle cx="{fmt(red_c[0])}" cy="{fmt(red_c[1])}" r="{fmt(red_inner)}" fill="#FFFFFF"/>
  <circle cx="{fmt(blue_c[0])}" cy="{fmt(blue_c[1])}" r="{fmt(blue_outer)}" fill="#1B1F24"/>
  <circle cx="{fmt(blue_c[0])}" cy="{fmt(blue_c[1])}" r="{fmt(blue_fill)}" fill="#0050A0"/>
  <polygon points="{fmt(a1[0])},{fmt(a1[1])} {fmt(a2[0])},{fmt(a2[1])} {fmt(a3[0])},{fmt(a3[1])} {fmt(a4[0])},{fmt(a4[1])} {fmt(a5[0])},{fmt(a5[1])} {fmt(a6[0])},{fmt(a6[1])} {fmt(a7[0])},{fmt(a7[1])}" fill="#FFFFFF"/>
</svg>
"""
    dest = ROOT / "tools/sign-art/launcher.svg"
    dest.write_text(svg, encoding="utf-8")
    return svg


def draw_icon(size: int) -> Image.Image:
    image = Image.new("RGB", (size, size), ASPHALT)
    draw = ImageDraw.Draw(image)
    s = size / VIEW

    def p(x: float, y: float) -> tuple[float, float]:
        nx, ny = xform(x, y)
        return nx * s, ny * s

    def pr(r: float) -> float:
        return xform_r(r) * s

    def poly(points: list[tuple[float, float]], fill: tuple[int, int, int]) -> None:
        draw.polygon([p(x, y) for x, y in points], fill=fill)

    def circ(cx: float, cy: float, r: float, fill: tuple[int, int, int]) -> None:
        x, y = p(cx, cy)
        rr = pr(r)
        draw.ellipse((x - rr, y - rr, x + rr, y + rr), fill=fill)

    poly([(54, 22), (79, 63), (29, 63)], ASPHALT)
    poly([(54, 25.4), (75.8, 60.2), (32.2, 60.2)], SIGN_YELLOW)
    bx, by = p(51.8, 34)
    bw, bh = pr(4.4), pr(13)
    draw.rectangle((bx, by, bx + bw, by + bh), fill=ASPHALT)
    dx, dy = p(51.8, 49.6)
    ds = pr(4.4)
    draw.rectangle((dx, dy, dx + ds, dy + ds), fill=ASPHALT)
    circ(38, 69, 17, ASPHALT)
    circ(38, 69, 16, SIGN_RED)
    circ(38, 69, 10.8, WHITE)
    circ(70, 69, 17, ASPHALT)
    circ(70, 69, 16, SIGN_BLUE)
    poly([(70, 56.2), (80.4, 67.6), (74.3, 67.6), (74.3, 81), (65.7, 81), (65.7, 67.6), (59.6, 67.6)], WHITE)
    return image


def write_mipmaps() -> None:
    sizes = {
        "mdpi": 48,
        "hdpi": 72,
        "xhdpi": 96,
        "xxhdpi": 144,
        "xxxhdpi": 192,
    }
    master = draw_icon(1024)
    res = ROOT / "app/src/main/res"
    for density, size in sizes.items():
        folder = res / f"mipmap-{density}"
        folder.mkdir(parents=True, exist_ok=True)
        scaled = master.resize((size, size), Image.Resampling.LANCZOS)
        scaled.save(folder / "ic_launcher.png", format="PNG", optimize=True)
        scaled.save(folder / "ic_launcher_round.png", format="PNG", optimize=True)
    store = master.resize((512, 512), Image.Resampling.LANCZOS)
    dest = ROOT / "docs/icon.png"
    dest.parent.mkdir(parents=True, exist_ok=True)
    store.save(dest, format="PNG", optimize=True)


def write_safezone_preview() -> None:
    size = 512
    icon = draw_icon(size)
    mask = Image.new("L", (size, size), 0)
    draw = ImageDraw.Draw(mask)
    r = 33.0 / 108.0 * size
    cx = cy = size / 2
    draw.ellipse((cx - r, cy - r, cx + r, cy + r), fill=255)
    preview = Image.new("RGB", (size, size), (80, 80, 80))
    preview.paste(icon, mask=mask)
    out = ROOT / "tools/sign-art/cache/launcher_safezone_preview.png"
    out.parent.mkdir(parents=True, exist_ok=True)
    preview.save(out, format="PNG")
    farthest = 0.0
    for x, y, rad in [(38, 69, 17), (70, 69, 17), (54, 22, 0), (79, 63, 0), (29, 63, 0)]:
        nx, ny = xform(x, y)
        dist = math.hypot(nx - CX, ny - CY) + xform_r(rad)
        farthest = max(farthest, dist)
    print(f"farthest_from_center={farthest:.2f} safe_r=30")


def main() -> None:
    write_vector()
    write_svg()
    write_mipmaps()
    write_safezone_preview()
    print("launcher written")


if __name__ == "__main__":
    main()
