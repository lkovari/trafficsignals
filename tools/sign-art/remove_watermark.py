#!/usr/bin/env python3
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
from PIL import Image

sys.path.insert(0, str(Path(__file__).resolve().parent))

from palette import SIGN_BLUE, SIGN_RED, WHITE, local_range


def remove_lk_watermark(image: Image.Image) -> Image.Image:
    arr = np.array(image.convert("RGB"))
    h, w = arr.shape[:2]
    r = arr[:, :, 0].astype(np.int16)
    g = arr[:, :, 1].astype(np.int16)
    b = arr[:, :, 2].astype(np.int16)
    lum = 0.299 * r + 0.587 * g + 0.114 * b
    white = (r >= 215) & (g >= 215) & (b >= 215)
    blue = (b > r + 16) & (b > g + 6) & (b >= 65) & (r < 145)
    black = (r <= 45) & (g <= 45) & (b <= 45)
    blue_frac = blue.mean(axis=1)
    if blue_frac.max() < 0.05:
        return Image.fromarray(arr, mode="RGB")
    blue_top = int(np.argmax(blue_frac > 0.12))
    y0 = max(0, blue_top - 2)
    y1 = min(h, blue_top + 20)
    side = max(3, int(round(0.03 * w)))
    x1 = min(w, max(side + 24, int(round(0.52 * w))))
    white_frac = white.mean(axis=1)
    blue_lum = float(np.median(lum[blue])) if blue.any() else 80.0
    wm = np.zeros((h, w), dtype=bool)
    for y in range(y0, y1):
        row_white = float(white_frac[y])
        for x in range(side, x1):
            if black[y, x]:
                continue
            if row_white >= 0.45:
                if not white[y, x] and not blue[y, x]:
                    wm[y, x] = True
                elif blue[y, x] and lum[y, x] > blue_lum + 16:
                    wm[y, x] = True
                continue
            if white[y, x] or (not blue[y, x]) or (lum[y, x] > blue_lum + 16):
                wm[y, x] = True
    if wm.sum() < 6:
        return Image.fromarray(arr, mode="RGB")
    ys, xs = np.where(wm)
    by0 = max(y0, int(ys.min()) - 1)
    by1 = min(y1, max(int(ys.max()) + 3, int(ys.min()) + 14))
    bx0 = max(side, int(xs.min()) - 1)
    bx1 = min(x1, max(int(xs.max()) + 4, int(xs.min()) + 60))
    near_blue = np.zeros((h, w), dtype=bool)
    pad = 3
    for dy in range(-pad, pad + 1):
        for dx in range(-pad, pad + 1):
            sy0, sy1 = max(0, dy), h + min(0, dy)
            sx0, sx1 = max(0, dx), w + min(0, dx)
            near_blue[sy0:sy1, sx0:sx1] |= blue[sy0 - dy : sy1 - dy, sx0 - dx : sx1 - dx]
    out = arr.copy()
    for y in range(by0, by1):
        row_white = float(white_frac[y])
        for x in range(bx0, bx1):
            if black[y, x]:
                continue
            if near_blue[y, x] and row_white < 0.45 and (white[y, x] or lum[y, x] > blue_lum + 12):
                out[y, x] = SIGN_BLUE
            elif (not white[y, x]) and (not blue[y, x]) and (not near_blue[y, x]):
                out[y, x] = WHITE
            elif (not white[y, x]) and (not blue[y, x]) and row_white >= 0.45:
                out[y, x] = WHITE
    return Image.fromarray(out, mode="RGB")


def snap_raster_photo(image: Image.Image) -> Image.Image:
    arr = np.array(image.convert("RGBA"))
    rgb = arr[:, :, :3]
    r = rgb[:, :, 0].astype(np.int16)
    g = rgb[:, :, 1].astype(np.int16)
    b = rgb[:, :, 2].astype(np.int16)
    mx = np.maximum(np.maximum(r, g), b)
    mn = np.minimum(np.minimum(r, g), b)
    chroma = mx - mn
    from palette import rgb_to_hsv_arrays

    hue, sat, val = rgb_to_hsv_arrays(rgb)
    base = (mx >= 22) & (mn <= 242) & (chroma >= 28) & (sat >= 0.28) & (val >= 0.16)
    yellow = (hue >= 38) & (hue <= 72)
    green = (hue > 72) & (hue <= 175)
    red = base & ~yellow & ~green & ((hue <= 16) | (hue >= 348))
    blue_hue = (hue >= 185) & (hue <= 262)
    blue = base & ~yellow & ~green & blue_hue & ~((val >= 0.72) & (sat <= 0.88))
    flat = local_range(rgb) < 36
    arr[flat & red, 0:3] = SIGN_RED
    arr[flat & blue, 0:3] = SIGN_BLUE
    return Image.fromarray(arr, mode="RGBA")
