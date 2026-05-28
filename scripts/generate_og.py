#!/usr/bin/env python3
"""Generate the Sage Health Open Graph image (1200x630 PNG)."""
from PIL import Image, ImageDraw, ImageFont
from pathlib import Path

W, H = 1200, 630
OUT = Path(__file__).resolve().parent.parent / "images" / "og-image.png"

BG_TOP = (26, 35, 24)        # #1a2318
BG_BOTTOM = (12, 18, 11)     # darker for subtle vertical gradient
TEAL = (13, 148, 136)        # #0D9488
WHITE = (255, 255, 255)
MUTED = (200, 210, 200)

TITLE = "Sage Health"
TAGLINE = "Your practice, operating at its full potential."

HELVETICA = "/System/Library/Fonts/Helvetica.ttc"
HELVETICA_NEUE = "/System/Library/Fonts/HelveticaNeue.ttc"

# Vertical gradient background
img = Image.new("RGB", (W, H), BG_TOP)
px = img.load()
for y in range(H):
    t = y / (H - 1)
    r = int(BG_TOP[0] + (BG_BOTTOM[0] - BG_TOP[0]) * t)
    g = int(BG_TOP[1] + (BG_BOTTOM[1] - BG_TOP[1]) * t)
    b = int(BG_TOP[2] + (BG_BOTTOM[2] - BG_TOP[2]) * t)
    for x in range(W):
        px[x, y] = (r, g, b)

draw = ImageDraw.Draw(img)

# Teal accent bar — short, centered above the title
bar_w, bar_h = 80, 5
bar_x = (W - bar_w) // 2
bar_y = 230
draw.rectangle([bar_x, bar_y, bar_x + bar_w, bar_y + bar_h], fill=TEAL)

# Title — Helvetica Bold (TTC index 1 is Bold for Helvetica.ttc on macOS)
try:
    title_font = ImageFont.truetype(HELVETICA, 120, index=1)
except OSError:
    title_font = ImageFont.truetype(HELVETICA, 120)

tagline_font = ImageFont.truetype(HELVETICA, 36)

# Center title
tb = draw.textbbox((0, 0), TITLE, font=title_font)
tw = tb[2] - tb[0]
th = tb[3] - tb[1]
title_x = (W - tw) // 2 - tb[0]
title_y = 270
draw.text((title_x, title_y), TITLE, font=title_font, fill=WHITE)

# Center tagline
gb = draw.textbbox((0, 0), TAGLINE, font=tagline_font)
gw = gb[2] - gb[0]
tagline_x = (W - gw) // 2 - gb[0]
tagline_y = title_y + th + 60
draw.text((tagline_x, tagline_y), TAGLINE, font=tagline_font, fill=MUTED)

# Save
OUT.parent.mkdir(parents=True, exist_ok=True)
img.save(OUT, "PNG", optimize=True)
print(f"Wrote {OUT} ({OUT.stat().st_size:,} bytes, {W}x{H})")
