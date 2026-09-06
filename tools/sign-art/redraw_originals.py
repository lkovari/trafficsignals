#!/usr/bin/env python3
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFont

sys.path.insert(0, str(Path(__file__).resolve().parent))

from palette import (
    DRAWABLE,
    PNG_DIR,
    ROOT,
    SIGN_BLUE,
    SIGN_RED,
    SNAPPED_SVG_DIR,
    SVG_DIR,
    WHITE,
    rasterize_svg,
    snap_raster,
    snap_svg_text,
    write_drawable_png,
)
from unify_palette import render_from_svg

DIN = Path("/System/Library/Fonts/Supplemental/DIN Alternate Bold.ttf")
ARIAL = Path("/System/Library/Fonts/Supplemental/Arial Bold.ttf")
FONT_PATH = DIN if DIN.exists() else ARIAL
SS = 4
SIZE = 1024
WORK = SIZE * SS


def font(size: int) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(str(FONT_PATH), size)


def rasterize_named(code: str, width: int = 1400) -> Image.Image:
    source = SVG_DIR / f"Hungary_road_sign_{code}.svg"
    snapped = SNAPPED_SVG_DIR / source.name
    SNAPPED_SVG_DIR.mkdir(parents=True, exist_ok=True)
    snapped.write_text(snap_svg_text(source.read_text(encoding="utf-8", errors="replace")), encoding="utf-8")
    png_path = PNG_DIR / f"redraw_{code}.png"
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
    return image.crop((int(xs.min()), int(ys.min()), int(xs.max()) + 1, int(ys.max()) + 1)).convert("RGBA")


def down(image: Image.Image) -> Image.Image:
    return image.resize((SIZE, SIZE), Image.Resampling.LANCZOS)


def text_size(draw: ImageDraw.ImageDraw, text: str, used: ImageFont.ImageFont) -> tuple[int, int]:
    box = draw.textbbox((0, 0), text, font=used)
    return box[2] - box[0], box[3] - box[1]


def draw_time_token(draw: ImageDraw.ImageDraw, x: int, baseline: int, hour: str, minute: str, big: ImageFont.ImageFont, small: ImageFont.ImageFont) -> int:
    draw.text((x, baseline), hour, font=big, fill=(0, 0, 0, 255), anchor="ls")
    x += int(big.getlength(hour)) + max(4, big.size // 18)
    draw.text((x, baseline - int(small.size * 0.62)), minute, font=small, fill=(0, 0, 0, 255), anchor="ls")
    return x + int(small.getlength(minute))


def make_time_plate(start: tuple[str, str], end: tuple[str, str], width: int, height: int) -> Image.Image:
    plate = Image.new("RGBA", (width, height), (255, 255, 255, 255))
    draw = ImageDraw.Draw(plate)
    border = max(6, height // 16)
    draw.rectangle([0, 0, width - 1, height - 1], outline=(0, 0, 0, 255), width=border)
    big = font(int(height * 0.46))
    small = font(int(height * 0.22))
    dash = "–"
    probe = ImageDraw.Draw(Image.new("RGBA", (8, 8)))
    dash_w = int(big.getlength(dash))
    hour_w, _ = text_size(probe, start[0], big)
    min_w, _ = text_size(probe, start[1], small)
    token_w = hour_w + max(4, big.size // 18) + min_w
    total = token_w * 2 + dash_w + int(height * 0.22)
    x = (width - total) // 2
    baseline = int(height * 0.72)
    x = draw_time_token(draw, x, baseline, start[0], start[1], big, small)
    x += int(height * 0.08)
    draw.text((x, baseline), dash, font=big, fill=(0, 0, 0, 255), anchor="ls")
    x += dash_w + int(height * 0.08)
    draw_time_token(draw, x, baseline, end[0], end[1], big, small)
    return plate


def stack_circle_and_plate(code: str, start: tuple[str, str], end: tuple[str, str], sign_id: str) -> None:
    sign = crop_visible(rasterize_named(code, 1600), drop_dark_corners=True)
    canvas = Image.new("RGBA", (SIZE, SIZE), WHITE + (255,))
    sign_box = 720
    sign_fit = sign.copy()
    sign_fit.thumbnail((sign_box, sign_box), Image.Resampling.LANCZOS)
    plate = make_time_plate(start, end, 620, 168)
    gap = 22
    total = sign_fit.height + gap + plate.height
    top = (SIZE - total) // 2
    canvas.alpha_composite(sign_fit, ((SIZE - sign_fit.width) // 2, top))
    canvas.alpha_composite(plate, ((SIZE - plate.width) // 2, top + sign_fit.height + gap))
    write_drawable_png(sign_id, canvas)


def disk(draw: ImageDraw.ImageDraw, xy: tuple[float, float], radius: float, fill) -> None:
    x, y = xy
    draw.ellipse([x - radius, y - radius, x + radius, y + radius], fill=fill)


def thick_polyline(draw: ImageDraw.ImageDraw, points: list[tuple[float, float]], width: int, fill) -> None:
    draw.line(points, fill=fill, width=width, joint="curve")
    radius = width / 2
    disk(draw, points[0], radius, fill)
    disk(draw, points[-1], radius, fill)


def arrow_head(draw: ImageDraw.ImageDraw, tip: tuple[float, float], direction: tuple[float, float], length: float, width: float, fill) -> None:
    dx, dy = direction
    mag = max(1e-6, (dx * dx + dy * dy) ** 0.5)
    ux, uy = dx / mag, dy / mag
    px, py = -uy, ux
    base_x = tip[0] - ux * length
    base_y = tip[1] - uy * length
    left = (base_x + px * width / 2, base_y + py * width / 2)
    right = (base_x - px * width / 2, base_y - py * width / 2)
    draw.polygon([tip, left, right], fill=fill)


def dashed_line(draw: ImageDraw.ImageDraw, x: float, y0: float, y1: float, width: int, dash: int, gap: int, fill) -> None:
    y = y0
    while y < y1:
        y_end = min(y1, y + dash)
        thick_polyline(draw, [(x, y), (x, y_end)], width, fill)
        y = y_end + gap


def speed_badge(text: str, diameter: int, ended: bool = False) -> Image.Image:
    badge = Image.new("RGBA", (diameter, diameter), (0, 0, 0, 0))
    draw = ImageDraw.Draw(badge)
    ring = max(6, diameter // 14)
    draw.ellipse([1, 1, diameter - 2, diameter - 2], fill=SIGN_BLUE + (255,), outline=WHITE + (255,), width=ring)
    used = font(int(diameter * 0.46))
    dummy = ImageDraw.Draw(Image.new("RGBA", (8, 8)))
    tw, th = text_size(dummy, text, used)
    box = dummy.textbbox((0, 0), text, font=used)
    draw.text(
        ((diameter - tw) / 2 - box[0], (diameter - th) / 2 - box[1] + diameter * 0.02),
        text,
        font=used,
        fill=WHITE + (255,),
    )
    if ended:
        pad = int(diameter * 0.12)
        slash_w = max(10, diameter // 7)
        draw.line([(pad, diameter - pad), (diameter - pad, pad)], fill=WHITE + (255,), width=slash_w + max(6, diameter // 28))
        draw.line([(pad, diameter - pad), (diameter - pad, pad)], fill=SIGN_RED + (255,), width=slash_w)
    return badge


def paste_center(base: Image.Image, overlay: Image.Image, cx: float, cy: float) -> None:
    x = int(round(cx - overlay.width / 2))
    y = int(round(cy - overlay.height / 2))
    base.alpha_composite(overlay, (x, y))


def blue_square_canvas() -> tuple[Image.Image, ImageDraw.ImageDraw, int, int]:
    image = Image.new("RGBA", (WORK, WORK), SIGN_BLUE + (255,))
    draw = ImageDraw.Draw(image)
    inner = int(WORK * 0.045)
    draw.rectangle(
        [inner, inner, WORK - 1 - inner, WORK - 1 - inner],
        outline=WHITE + (255,),
        width=max(12, WORK // 64),
    )
    return image, draw, 0, inner


def finish_square(image: Image.Image, sign_id: str) -> None:
    write_drawable_png(sign_id, down(image))


def draw_up_arrow(draw: ImageDraw.ImageDraw, x: float, y_top: float, y_bottom: float, shaft: int) -> None:
    head_len = shaft * 1.15
    head_w = shaft * 2.05
    shaft_top = y_top + head_len * 0.62
    thick_polyline(draw, [(x, y_bottom), (x, shaft_top)], shaft, WHITE + (255,))
    arrow_head(draw, (x, y_top), (0, -1), head_len, head_w, WHITE + (255,))


def render_lane_begin(sign_id: str = "kulonleges_kiegeszitosavkezdete50", with_speed: bool = True) -> None:
    image, draw, _, inner = blue_square_canvas()
    left_x = WORK * 0.34
    right_x = WORK * 0.68
    top = inner + WORK * 0.10
    bottom = WORK - inner - WORK * 0.08
    shaft = int(WORK * 0.11)
    edge = max(10, WORK // 90)
    split = WORK * 0.58
    thick_polyline(draw, [(inner + WORK * 0.06, bottom), (inner + WORK * 0.06, top + WORK * 0.04)], edge, WHITE + (255,))
    thick_polyline(
        draw,
        [
            (WORK - inner - WORK * 0.06, split),
            (WORK - inner - WORK * 0.06, top + WORK * 0.04),
        ],
        edge,
        WHITE + (255,),
    )
    dashed_line(draw, (left_x + right_x) / 2, split, top + WORK * 0.08, max(8, WORK // 110), int(WORK * 0.045), int(WORK * 0.028), WHITE + (255,))
    draw_up_arrow(draw, left_x, top, bottom, shaft)
    curve = [
        (left_x + shaft * 0.15, split + WORK * 0.12),
        (left_x + (right_x - left_x) * 0.45, split + WORK * 0.02),
        (right_x, split - WORK * 0.08),
        (right_x, top + shaft * 1.05),
    ]
    thick_polyline(draw, curve, shaft, WHITE + (255,))
    arrow_head(draw, (right_x, top), (0, -1), shaft * 1.15, shaft * 2.05, WHITE + (255,))
    if with_speed:
        paste_center(image, speed_badge("50", int(WORK * 0.22)), left_x, WORK * 0.58)
    finish_square(image, sign_id)


def render_lane_end(sign_id: str = "kulonleges_kiegeszitosavvege50", with_speed: bool = True) -> None:
    image, draw, _, inner = blue_square_canvas()
    left_x = WORK * 0.38
    right_x = WORK * 0.72
    top = inner + WORK * 0.10
    bottom = WORK - inner - WORK * 0.08
    shaft = int(WORK * 0.11)
    edge = max(10, WORK // 90)
    merge = WORK * 0.42
    thick_polyline(draw, [(inner + WORK * 0.08, bottom), (inner + WORK * 0.08, top + WORK * 0.04)], edge, WHITE + (255,))
    thick_polyline(
        draw,
        [
            (WORK - inner - WORK * 0.05, bottom - WORK * 0.02),
            (WORK - inner - WORK * 0.05, merge + WORK * 0.12),
            (left_x + shaft * 0.9, merge - WORK * 0.02),
        ],
        edge,
        WHITE + (255,),
    )
    dashed_line(draw, (left_x + right_x) / 2, merge + WORK * 0.18, WORK * 0.78, max(8, WORK // 110), int(WORK * 0.045), int(WORK * 0.028), WHITE + (255,))
    draw_up_arrow(draw, left_x, top, bottom, shaft)
    curve = [
        (right_x, bottom - WORK * 0.04),
        (right_x, merge + WORK * 0.10),
        (left_x + shaft * 0.35, merge - WORK * 0.06),
    ]
    thick_polyline(draw, curve, shaft, WHITE + (255,))
    if with_speed:
        paste_center(image, speed_badge("50", int(WORK * 0.24), ended=True), left_x, WORK * 0.62)
    finish_square(image, sign_id)


def render_lane_speeds() -> None:
    image, draw, _, inner = blue_square_canvas()
    xs = (WORK * 0.26, WORK * 0.50, WORK * 0.76)
    top = inner + WORK * 0.10
    bottom = WORK - inner - WORK * 0.08
    shaft = int(WORK * 0.09)
    split = WORK * 0.62
    draw_up_arrow(draw, xs[0], top, bottom, shaft)
    thick_polyline(draw, [(xs[1], split), (xs[1], top + shaft * 1.05)], shaft, WHITE + (255,))
    arrow_head(draw, (xs[1], top), (0, -1), shaft * 1.15, shaft * 2.05, WHITE + (255,))
    curve = [
        (xs[1] + shaft * 0.1, split + WORK * 0.04),
        (xs[1] + (xs[2] - xs[1]) * 0.55, split - WORK * 0.04),
        (xs[2], split - WORK * 0.14),
        (xs[2], top + shaft * 1.05),
    ]
    thick_polyline(draw, curve, shaft, WHITE + (255,))
    arrow_head(draw, (xs[2], top), (0, -1), shaft * 1.15, shaft * 2.05, WHITE + (255,))
    thick_polyline(draw, [(xs[1], bottom), (xs[1], split)], shaft, WHITE + (255,))
    dashed_line(draw, (xs[0] + xs[1]) / 2, top + WORK * 0.08, bottom - WORK * 0.04, max(7, WORK // 120), int(WORK * 0.04), int(WORK * 0.024), WHITE + (255,))
    dashed_line(draw, (xs[1] + xs[2]) / 2, top + WORK * 0.08, split - WORK * 0.02, max(7, WORK // 120), int(WORK * 0.04), int(WORK * 0.024), WHITE + (255,))
    paste_center(image, speed_badge("80", int(WORK * 0.19)), xs[0], WORK * 0.52)
    paste_center(image, speed_badge("50", int(WORK * 0.19)), xs[1], WORK * 0.42)
    finish_square(image, "kulonleges_forgalmisavoklegkisebbsebessege")


def extract_dark_icon(code: str) -> Image.Image:
    source = rasterize_named(code, 1600)
    arr = np.array(source.convert("RGB"))
    white = arr.min(axis=2) > 220
    ys, xs = np.where(white)
    cy = float(ys.mean())
    cx = float(xs.mean())
    rad = float(np.quantile(np.sqrt((xs - cx) ** 2 + (ys - cy) ** 2), 0.82))
    yy, xx = np.ogrid[: arr.shape[0], : arr.shape[1]]
    inner = np.sqrt((xx - cx) ** 2 + (yy - cy) ** 2) < rad * 0.90
    icon = inner & (arr.max(axis=2) < 50)
    ys, xs = np.where(icon)
    y0, y1 = int(ys.min()), int(ys.max()) + 1
    x0, x1 = int(xs.min()), int(xs.max()) + 1
    out = np.zeros((y1 - y0, x1 - x0, 4), dtype=np.uint8)
    out[icon[y0:y1, x0:x1]] = (255, 255, 255, 255)
    return Image.fromarray(out, "RGBA")


def extract_white_bus() -> Image.Image:
    return extract_dark_icon("C-042")


def render_bus_circle(sign_id: str, ended: bool) -> None:
    canvas = Image.new("RGBA", (SIZE, SIZE), WHITE + (255,))
    draw = ImageDraw.Draw(canvas)
    cx = cy = SIZE / 2
    radius = SIZE * 0.44
    draw.ellipse([cx - radius, cy - radius, cx + radius, cy + radius], fill=SIGN_BLUE + (255,))
    rim = max(8, SIZE // 48)
    draw.ellipse(
        [cx - radius + rim * 0.2, cy - radius + rim * 0.2, cx + radius - rim * 0.2, cy + radius - rim * 0.2],
        outline=WHITE + (255,),
        width=rim,
    )
    bus = extract_white_bus()
    bus_w = int(SIZE * 0.62)
    scale = bus_w / bus.width
    bus = bus.resize((bus_w, max(1, int(bus.height * scale))), Image.Resampling.LANCZOS)
    paste_center(canvas, bus, cx, cy + SIZE * 0.02)
    if ended:
        overlay = Image.new("RGBA", (SIZE, SIZE), (0, 0, 0, 0))
        slash = ImageDraw.Draw(overlay)
        pad = int(SIZE * 0.18)
        slash_w = max(28, SIZE // 16)
        slash.line([(pad, SIZE - pad), (SIZE - pad, pad)], fill=WHITE + (255,), width=slash_w + 10)
        slash.line([(pad, SIZE - pad), (SIZE - pad, pad)], fill=SIGN_RED + (255,), width=slash_w)
        mask = Image.new("L", (SIZE, SIZE), 0)
        ImageDraw.Draw(mask).ellipse(
            [cx - radius + rim, cy - radius + rim, cx + radius - rim, cy + radius - rim],
            fill=255,
        )
        overlay.putalpha(Image.fromarray(np.minimum(np.array(overlay.split()[-1]), np.array(mask)), mode="L"))
        canvas.alpha_composite(overlay)
    write_drawable_png(sign_id, canvas)


def write_from_code(sign_id: str, code: str) -> None:
    source = SVG_DIR / f"Hungary_road_sign_{code}.svg"
    if not render_from_svg(sign_id, source):
        raise RuntimeError(f"svg render failed {code}")


def stack_signs(top: Image.Image, bottom: Image.Image, sign_id: str) -> None:
    canvas = Image.new("RGBA", (SIZE, SIZE), WHITE + (255,))
    top_fit = crop_visible(top, drop_dark_corners=True)
    bot_fit = crop_visible(bottom, drop_dark_corners=False)
    top_fit.thumbnail((720, 720), Image.Resampling.LANCZOS)
    bot_fit.thumbnail((560, 280), Image.Resampling.LANCZOS)
    gap = 24
    total = top_fit.height + gap + bot_fit.height
    y = (SIZE - total) // 2
    canvas.alpha_composite(top_fit, ((SIZE - top_fit.width) // 2, y))
    canvas.alpha_composite(bot_fit, ((SIZE - bot_fit.width) // 2, y + top_fit.height + gap))
    write_drawable_png(sign_id, canvas)


def render_except_two_way(sign_id: str, plate_code: str) -> None:
    main = rasterize_named("E-012", 1400)
    plate = crop_visible(rasterize_named(plate_code, 1400), drop_dark_corners=False)
    draw = ImageDraw.Draw(plate)
    h = plate.height
    w = plate.width
    arrow = max(8, h // 14)
    left_x = int(w * 0.10)
    right_x = int(w * 0.90)
    y0 = int(h * 0.58)
    y1 = int(h * 0.88)
    draw.polygon([(left_x, y0), (left_x - arrow, y0 + arrow), (left_x + arrow, y0 + arrow)], fill=(0, 0, 0, 255))
    draw.rectangle([left_x - arrow // 3, y0 + arrow - 2, left_x + arrow // 3, y1], fill=(0, 0, 0, 255))
    draw.polygon([(right_x, y1), (right_x - arrow, y1 - arrow), (right_x + arrow, y1 - arrow)], fill=(0, 0, 0, 255))
    draw.rectangle([right_x - arrow // 3, y0, right_x + arrow // 3, y1 - arrow + 2], fill=(0, 0, 0, 255))
    stack_signs(main, plate, sign_id)


def render_blue_p_icon(sign_id: str, icon: Image.Image, plus: bool) -> None:
    image, draw, margin, inner = blue_square_canvas()
    used = font(int(WORK * 0.28))
    label = "P+" if plus else "P"
    dummy = ImageDraw.Draw(Image.new("RGBA", (8, 8)))
    tw, th = text_size(dummy, label, used)
    box = dummy.textbbox((0, 0), label, font=used)
    draw.text(
        ((WORK - tw) / 2 - box[0], WORK * 0.18 - box[1]),
        label,
        font=used,
        fill=WHITE + (255,),
    )
    icon_w = int(WORK * 0.46)
    scale = icon_w / max(1, icon.width)
    icon = icon.resize((icon_w, max(1, int(icon.height * scale))), Image.Resampling.LANCZOS)
    paste_center(image, icon, WORK / 2, WORK * 0.68)
    finish_square(image, sign_id)


def white_icon_from_sign(code: str) -> Image.Image:
    source = crop_visible(rasterize_named(code, 1400), drop_dark_corners=True)
    arr = np.array(source.convert("RGBA"))
    rgb = arr[:, :, :3]
    white = (rgb.min(axis=2) > 200) & (arr[:, :, 3] > 20)
    ys, xs = np.where(white)
    y0, y1 = int(ys.min()), int(ys.max()) + 1
    x0, x1 = int(xs.min()), int(xs.max()) + 1
    out = np.zeros((y1 - y0, x1 - x0, 4), dtype=np.uint8)
    out[white[y0:y1, x0:x1]] = (255, 255, 255, 255)
    return Image.fromarray(out, "RGBA")


def render_permit() -> None:
    image, draw, _, inner = blue_square_canvas()
    cx = WORK / 2
    cy = WORK * 0.38
    arm = WORK * 0.09
    thick = WORK * 0.085
    draw.rectangle([cx - arm * 2.2, cy - thick / 2, cx + arm * 2.2, cy + thick / 2], fill=SIGN_RED + (255,))
    draw.rectangle([cx - thick / 2, cy - arm * 2.2, cx + thick / 2, cy + arm * 2.2], fill=SIGN_RED + (255,))
    used = font(int(WORK * 0.07))
    for i, line in enumerate(("VÁRAKOZÁSI", "ENGEDÉLY")):
        dummy = ImageDraw.Draw(Image.new("RGBA", (8, 8)))
        tw, th = text_size(dummy, line, used)
        box = dummy.textbbox((0, 0), line, font=used)
        draw.text(
            ((WORK - tw) / 2 - box[0], WORK * 0.62 + i * WORK * 0.10 - box[1]),
            line,
            font=used,
            fill=WHITE + (255,),
        )
    finish_square(image, "kulonleges_varakozasiengedely")


def render_parking_ahead() -> None:
    image, draw, _, _ = blue_square_canvas()
    used = font(int(WORK * 0.34))
    dummy = ImageDraw.Draw(Image.new("RGBA", (8, 8)))
    tw, th = text_size(dummy, "P", used)
    box = dummy.textbbox((0, 0), "P", font=used)
    draw.text(((WORK - tw) / 2 - box[0], WORK * 0.16 - box[1]), "P", font=used, fill=WHITE + (255,))
    arrow_y = WORK * 0.68
    thick_polyline(draw, [(WORK * 0.62, arrow_y), (WORK * 0.28, arrow_y)], int(WORK * 0.045), WHITE + (255,))
    arrow_head(draw, (WORK * 0.24, arrow_y), (-1, 0), WORK * 0.08, WORK * 0.10, WHITE + (255,))
    dist = font(int(WORK * 0.09))
    draw.text((WORK * 0.66, arrow_y), "250 m", font=dist, fill=WHITE + (255,), anchor="lm")
    finish_square(image, "kulonleges_parkoloelorejelzes")


def render_parking_truck() -> None:
    image, draw, _, inner = blue_square_canvas()
    used = font(int(WORK * 0.32))
    dummy = ImageDraw.Draw(Image.new("RGBA", (8, 8)))
    tw, th = text_size(dummy, "P", used)
    box = dummy.textbbox((0, 0), "P", font=used)
    draw.text((WORK * 0.16 - box[0], WORK * 0.14 - box[1]), "P", font=used, fill=WHITE + (255,))
    panel_w, panel_h = int(WORK * 0.46), int(WORK * 0.32)
    px, py = int(WORK * 0.48), int(WORK * 0.52)
    draw.rounded_rectangle([px, py, px + panel_w, py + panel_h], radius=int(WORK * 0.02), fill=WHITE + (255,))
    truck = extract_dark_icon("C-007")
    arr = np.array(truck)
    if arr.shape[2] == 4:
        visible = arr[:, :, 3] > 20
        arr[visible, 0:3] = (27, 31, 36)
        truck = Image.fromarray(arr, "RGBA")
    truck.thumbnail((int(panel_w * 0.78), int(panel_h * 0.55)), Image.Resampling.LANCZOS)
    image.alpha_composite(truck, (px + (panel_w - truck.width) // 2, py + int(panel_h * 0.08)))
    label = font(int(WORK * 0.055))
    draw.text((px + panel_w / 2, py + panel_h * 0.78), "7,5 t", font=label, fill=SIGN_BLUE + (255,), anchor="mm")
    finish_square(image, "kulonleges_parkoloamegjeloltjarmunek")


def render_lane_arrows_grid() -> None:
    image, draw, _, inner = blue_square_canvas()
    shaft = int(WORK * 0.048)
    length = WORK * 0.16
    top_y = WORK * 0.48
    top_xs = [WORK * x for x in (0.18, 0.34, 0.50, 0.66, 0.82)]
    dirs = [(-0.42, -1.0), (-0.42, -1.0), (0.0, -1.0), (0.0, -1.0), (0.42, -1.0)]
    for x, d in zip(top_xs, dirs):
        mag = (d[0] * d[0] + d[1] * d[1]) ** 0.5
        ux, uy = d[0] / mag, d[1] / mag
        base = (x, top_y)
        tip = (x + ux * length, top_y + uy * length)
        thick_polyline(draw, [base, (tip[0] - ux * shaft * 0.7, tip[1] - uy * shaft * 0.7)], shaft, WHITE + (255,))
        arrow_head(draw, tip, (ux, uy), shaft * 1.25, shaft * 2.1, WHITE + (255,))
    bot_y = WORK * 0.86
    bot_len = WORK * 0.20
    bot_xs = [WORK * x for x in (0.28, 0.50, 0.72)]
    bot_dirs = [(-0.42, -1.0), (0.0, -1.0), (0.0, -1.0)]
    for x, d in zip(bot_xs, bot_dirs):
        mag = (d[0] * d[0] + d[1] * d[1]) ** 0.5
        ux, uy = d[0] / mag, d[1] / mag
        base = (x, bot_y)
        tip = (x + ux * bot_len, bot_y + uy * bot_len)
        thick_polyline(draw, [base, (tip[0] - ux * shaft * 0.7, tip[1] - uy * shaft * 0.7)], shaft, WHITE + (255,))
        arrow_head(draw, tip, (ux, uy), shaft * 1.25, shaft * 2.1, WHITE + (255,))
    branch_tip = (bot_xs[2] + WORK * 0.12, bot_y - WORK * 0.16)
    thick_polyline(draw, [(bot_xs[2], bot_y - WORK * 0.06), (branch_tip[0] - 8, branch_tip[1] + 8)], shaft, WHITE + (255,))
    arrow_head(draw, branch_tip, (0.7, -0.75), shaft * 1.1, shaft * 1.9, WHITE + (255,))
    finish_square(image, "kulonleges_besorolasirend3")


def render_cycle_link() -> None:
    image, draw, _, inner = blue_square_canvas()
    shaft = int(WORK * 0.09)
    cx = WORK * 0.50
    draw_up_arrow(draw, cx, inner + WORK * 0.08, WORK * 0.48, shaft)
    thick_polyline(draw, [(cx, WORK * 0.36), (cx - WORK * 0.22, WORK * 0.22)], shaft, WHITE + (255,))
    arrow_head(draw, (cx - WORK * 0.24, WORK * 0.20), (-0.7, -0.7), shaft * 1.1, shaft * 1.8, WHITE + (255,))
    thick_polyline(draw, [(cx + WORK * 0.22, WORK * 0.40), (cx + shaft * 0.2, WORK * 0.48)], shaft, WHITE + (255,))
    bike = white_icon_from_sign("D-023")
    bike.thumbnail((int(WORK * 0.42), int(WORK * 0.28)), Image.Resampling.LANCZOS)
    paste_center(image, bike, WORK / 2, WORK * 0.70)
    box = int(WORK * 0.06)
    draw.rectangle([WORK / 2 - box / 2, WORK * 0.86, WORK / 2 + box / 2, WORK * 0.86 + box], fill=WHITE + (255,))
    finish_square(image, "kulonleges_kerekparoskozvetlenkapcsolat")


def watermark_residue(path: Path) -> int:
    arr = np.array(Image.open(path).convert("RGB"))
    height, width = arr.shape[:2]
    r = arr[:, :, 0].astype(np.int16)
    g = arr[:, :, 1].astype(np.int16)
    b = arr[:, :, 2].astype(np.int16)
    lum = 0.299 * r + 0.587 * g + 0.114 * b
    blue = (b > r + 16) & (b > g + 6) & (b >= 65) & (r < 145)
    if float(blue.mean()) < 0.02:
        return 0
    blue_frac = blue.mean(axis=1)
    hits = np.where(blue_frac > 0.12)[0]
    if hits.size == 0:
        return 0
    top = int(hits[0])
    y0 = top
    y1 = min(height, top + max(16, height // 16))
    x0 = max(0, int(0.02 * width))
    x1 = min(width, int(0.50 * width))
    region_blue = blue[y0:y1, x0:x1]
    if not region_blue.any():
        return 0
    white = (r[y0:y1, x0:x1] >= 215) & (g[y0:y1, x0:x1] >= 215) & (b[y0:y1, x0:x1] >= 215)
    med = float(np.median(lum[blue]))
    light = region_blue & ~white & (lum[y0:y1, x0:x1] > med + 18)
    return int(light.sum())


def scan_drawables() -> list[tuple[int, str, int, int]]:
    rows: list[tuple[int, str, int, int]] = []
    for path in sorted(DRAWABLE.glob("*.png")):
        if path.stem.startswith("kategoria_"):
            continue
        residue = watermark_residue(path)
        image = Image.open(path)
        if residue > 12:
            rows.append((residue, path.stem, image.width, image.height))
    rows.sort(reverse=True)
    return rows


def main() -> None:
    stack_circle_and_plate("D-027", ("09", "00"), ("19", "00"), "utasitastado_gyalogkerekparut919")
    print("utasitastado_gyalogkerekparut919")
    stack_circle_and_plate("D-025", ("06", "00"), ("09", "00"), "utasitastado_gyalogut69")
    print("utasitastado_gyalogut69")
    write_from_code("kulonleges_kiegeszitosavkezdete50", "E-001")
    print("kulonleges_kiegeszitosavkezdete50")
    write_from_code("kulonleges_kiegeszitosavvege50", "E-002")
    print("kulonleges_kiegeszitosavvege50")
    write_from_code("kulonleges_forgalmisavoklegkisebbsebessege", "E-003")
    write_from_code(
        "tajekoztato_kerekparosalltalhasznalhatoautobuszforgalmisav", "E-005"
    )
    print("kulonleges_forgalmisavoklegkisebbsebessege")
    write_from_code("utasitastado_kotelezohaladasiiranysalakban", "D-007")
    print("utasitastado_kotelezohaladasiiranysalakban")
    render_bus_circle("utasitastado_autobuszsav", ended=False)
    print("utasitastado_autobuszsav")
    render_bus_circle("utasitastado_autobuszsavvege", ended=True)
    print("utasitastado_autobuszsavvege")
    render_except_two_way("tajekoztato_egyiranyuforgalmuutkivevekerekpar", "H-089")
    print("tajekoztato_egyiranyuforgalmuutkivevekerekpar")
    render_except_two_way("tajekoztato_egyiranyuforgaluutkivevebusz", "H-086")
    print("tajekoztato_egyiranyuforgaluutkivevebusz")
    stack_signs(rasterize_named("E-046", 1400), rasterize_named("H-049", 1400), "kulonleges_parkolomozgasserultekreszere")
    print("kulonleges_parkolomozgasserultekreszere")
    render_blue_p_icon("kulonleges_parkoljesutazzautobusszal", extract_white_bus(), plus=True)
    print("kulonleges_parkoljesutazzautobusszal")
    render_blue_p_icon("kulonleges_parkoljesutazztrolibusszal", white_icon_from_sign("E-040"), plus=True)
    print("kulonleges_parkoljesutazztrolibusszal")
    render_blue_p_icon("kulonleges_parkoljesutazzvillamossal", white_icon_from_sign("E-041"), plus=True)
    print("kulonleges_parkoljesutazzvillamossal")
    metro = Image.new("RGBA", (400, 400), (0, 0, 0, 0))
    md = ImageDraw.Draw(metro)
    md.ellipse([20, 20, 380, 380], outline=(255, 255, 255, 255), width=28)
    mf = font(210)
    md.text((200, 210), "M", font=mf, fill=(255, 255, 255, 255), anchor="mm")
    render_blue_p_icon("kulonleges_parkoljesutazzmetroval", metro, plus=True)
    print("kulonleges_parkoljesutazzmetroval")
    render_permit()
    print("kulonleges_varakozasiengedely")
    render_parking_ahead()
    print("kulonleges_parkoloelorejelzes")
    render_parking_truck()
    print("kulonleges_parkoloamegjeloltjarmunek")
    render_lane_arrows_grid()
    print("kulonleges_besorolasirend3")
    render_cycle_link()
    print("kulonleges_kerekparoskozvetlenkapcsolat")
    render_lane_begin("tajekoztato_kapaszkodosav", with_speed=False)
    print("tajekoztato_kapaszkodosav")
    render_lane_end("tajekoztato_kapaszkodosavvege", with_speed=False)
    print("tajekoztato_kapaszkodosavvege")
    leftover = scan_drawables()
    print(f"watermark_hits={len(leftover)}")
    for residue, name, width, height in leftover[:40]:
        print(f"  {residue:5} {width}x{height} {name}")


if __name__ == "__main__":
    main()
