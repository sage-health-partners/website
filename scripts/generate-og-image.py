#!/usr/bin/env python3
"""Generate Sage Health OG share image (1200x630).

Minimal design — subtle dark vertical gradient, brand leaf mark, PT Serif wordmark,
single tagline. Follows brand-guide.html. No SVG rasterizer dependency: the leaf is
drawn directly with Pillow by sampling the bezier/arc path from favicon.svg and
rendered with 4× supersample anti-aliasing.
"""
from __future__ import annotations

import math
from pathlib import Path

from PIL import Image, ImageChops, ImageDraw, ImageFont

# ─── Brand tokens (from brand-guide.html) ────────────────────────────────────
W, H = 1200, 630
BG_TOP = (11, 19, 16)         # #0b1310 — hero gradient top
BG_BOT = (4, 8, 6)            # #040806 — hero gradient bottom
LEAF = (122, 184, 109)        # #7ab86d — accent-bright
INK = (255, 255, 255)
INK_SOFT = (255, 255, 255, 178)  # ~70% white

FONT_PT_SERIF = "/System/Library/Fonts/Supplemental/PTSerif.ttc"
FONT_PT_SERIF_BOLD_INDEX = 3  # TTC order: 0=Regular, 1=Italic, 2=BoldItalic, 3=Bold
FONT_SF_FALLBACKS = [
    "/System/Library/Fonts/SFNS.ttf",
    "/System/Library/Fonts/Helvetica.ttc",
    "/Library/Fonts/Arial.ttf",
]

OUTPUT = Path(__file__).resolve().parent.parent / "images" / "og-image.png"


# ─── Background ──────────────────────────────────────────────────────────────
def vertical_gradient(size, top, bot):
    w, h = size
    strip = Image.new("RGB", (1, h))
    for y in range(h):
        t = y / (h - 1)
        strip.putpixel((0, y), (
            round(top[0] + (bot[0] - top[0]) * t),
            round(top[1] + (bot[1] - top[1]) * t),
            round(top[2] + (bot[2] - top[2]) * t),
        ))
    return strip.resize((w, h), Image.BILINEAR)


# ─── Leaf path sampling (from favicon.svg, 32×32 viewBox) ────────────────────
def _cubic(p0, p1, p2, p3, n=60):
    out = []
    for i in range(n + 1):
        t = i / n
        u = 1 - t
        x = u**3 * p0[0] + 3 * u**2 * t * p1[0] + 3 * u * t**2 * p2[0] + t**3 * p3[0]
        y = u**3 * p0[1] + 3 * u**2 * t * p1[1] + 3 * u * t**2 * p2[1] + t**3 * p3[1]
        out.append((x, y))
    return out


def _arc_half(cx, cy, r, start_angle, end_angle, n=80):
    """Sample a circular arc (counter-clockwise in y-down → dips downward)."""
    out = []
    for i in range(n + 1):
        t = i / n
        a = start_angle + (end_angle - start_angle) * t
        out.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    return out


def leaf_outline_points():
    """Outline of the leaf body in the 32×32 viewBox of favicon.svg."""
    # M16 3 → C10.67 8.33, 8 12.33, 8 17.67
    left = _cubic((16, 3), (10.67, 8.33), (8, 12.33), (8, 17.67))
    # a8 8 0 0 0 16 0  → arc from (8, 17.67) to (24, 17.67), dipping down to (16, 25.67)
    # In y-down: counter-clockwise (sweep=0) from angle π → π/2 → 0 goes through y=cy+r.
    arc = _arc_half(16, 17.67, 8, math.pi, 0)
    # c0 -5.34, -2.67 -9.34, -8 -14.67  → cubic from (24, 17.67) back to (16, 3)
    right = _cubic((24, 17.67), (24, 12.33), (21.33, 8.33), (16, 3))
    return left + arc[1:] + right[1:]


def leaf_stem_points():
    """The vertical stem: M16 29 V 14.67 (drawn at 60% opacity)."""
    return [(16, 29), (16, 14.67)]


def _inset_polygon(points, distance):
    """Shift each vertex `distance` pixels toward the polygon centroid.

    Approximates a proper polygon offset. For the leaf (roughly convex teardrop)
    this produces a uniformly inset boundary suitable for masking out the
    interior of a thick stroke.
    """
    cx = sum(p[0] for p in points) / len(points)
    cy = sum(p[1] for p in points) / len(points)
    out = []
    for x, y in points:
        dx, dy = cx - x, cy - y
        d = (dx * dx + dy * dy) ** 0.5
        if d < 1e-6:
            out.append((x, y))
        else:
            out.append((x + dx / d * distance, y + dy / d * distance))
    return out


def render_leaf(px, color, supersample=4):
    """Render the leaf at `px`×`px` using SSAA.

    Strategy: draw the filled outline polygon and the filled inset polygon as
    separate L-mode masks, then subtract — the difference is a clean stroke
    band of arbitrary thickness. Avoids Pillow's `draw.polygon(outline=, width=)`
    which stamps radial spokes from every vertex, and `draw.line(joint='curve')`
    whose dense elliptical joins bleed inward on tight curves.
    """
    s = supersample
    size = px * s
    scale = size / 32
    stroke_w = max(1, round(2.5 * scale))

    pts = [(x * scale, y * scale) for x, y in leaf_outline_points()]
    inner_pts = _inset_polygon(pts, stroke_w)

    outer_mask = Image.new("L", (size, size), 0)
    ImageDraw.Draw(outer_mask).polygon(pts, fill=255)
    inner_mask = Image.new("L", (size, size), 0)
    ImageDraw.Draw(inner_mask).polygon(inner_pts, fill=255)
    stroke_mask = ImageChops.subtract(outer_mask, inner_mask)

    leaf = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    leaf.paste(color + (255,), (0, 0), stroke_mask)

    # Stem: simple straight line, no joint artifacts. 60% opacity per favicon.svg.
    stem = [(x * scale, y * scale) for x, y in leaf_stem_points()]
    ImageDraw.Draw(leaf).line(stem, fill=color + (153,), width=stroke_w)

    return leaf.resize((px, px), Image.LANCZOS)


# ─── Type ────────────────────────────────────────────────────────────────────
def load_font(path, size, index=0):
    return ImageFont.truetype(path, size=size, index=index)


def find_sans(size):
    for p in FONT_SF_FALLBACKS:
        if Path(p).exists():
            try:
                return ImageFont.truetype(p, size=size)
            except OSError:
                continue
    return ImageFont.load_default()


def text_metrics(draw, s, font):
    l, t, r, b = draw.textbbox((0, 0), s, font=font)
    return (r - l, b - t, t)  # width, height, top-offset


# ─── Compose ─────────────────────────────────────────────────────────────────
def main():
    canvas = vertical_gradient((W, H), BG_TOP, BG_BOT).convert("RGBA")
    measure = ImageDraw.Draw(canvas)

    LEAF_PX = 104
    GAP_LEAF_NAME = 36
    GAP_NAME_TAG = 28
    name_font = load_font(FONT_PT_SERIF, 92, index=FONT_PT_SERIF_BOLD_INDEX)
    tag_font = find_sans(26)

    name = "Sage Health"
    tagline = "Your practice, operating at its full potential."

    name_w, name_h, name_top = text_metrics(measure, name, name_font)
    tag_w, tag_h, tag_top = text_metrics(measure, tagline, tag_font)

    stack_h = LEAF_PX + GAP_LEAF_NAME + name_h + GAP_NAME_TAG + tag_h
    y0 = (H - stack_h) // 2

    leaf = render_leaf(LEAF_PX, LEAF)
    canvas.paste(leaf, ((W - LEAF_PX) // 2, y0), leaf)

    draw = ImageDraw.Draw(canvas)
    draw.text(((W - name_w) // 2, y0 + LEAF_PX + GAP_LEAF_NAME - name_top),
              name, font=name_font, fill=INK)
    draw.text(((W - tag_w) // 2,
               y0 + LEAF_PX + GAP_LEAF_NAME + name_h + GAP_NAME_TAG - tag_top),
              tagline, font=tag_font, fill=INK_SOFT)

    canvas.convert("RGB").save(OUTPUT, "PNG", optimize=True)
    print(f"Wrote {OUTPUT} ({OUTPUT.stat().st_size // 1024} KB)")


if __name__ == "__main__":
    main()
