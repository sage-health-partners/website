"""Generate a premium 1200x630 Open Graph image for Sage Health."""
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import math
import os

W, H = 1200, 630
SCALE = 2
SW, SH = W * SCALE, H * SCALE

DEEP = (15, 26, 15)
MID = (26, 35, 24)
TEAL = (13, 148, 136)
TEAL_SOFT = (45, 200, 180)
WHITE = (255, 255, 255)
SAGE_GRAY = (176, 196, 176)


def lerp(a, b, t):
    return tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(3))


def build_background(w, h):
    """Diagonal base gradient + radial teal glow behind center text."""
    img = Image.new("RGB", (w, h), DEEP)
    px = img.load()

    cx, cy = w * 0.5, h * 0.48
    max_d = math.hypot(w * 0.6, h * 0.6)
    glow_radius = max_d * 0.55

    for y in range(h):
        t_base = y / h
        base = lerp(DEEP, MID, t_base)
        for x in range(w):
            d = math.hypot(x - cx, y - cy)
            g = max(0.0, 1.0 - d / glow_radius)
            g = g ** 2.2 * 0.35
            r = int(base[0] + (TEAL[0] - base[0]) * g)
            gg = int(base[1] + (TEAL[1] - base[1]) * g)
            b = int(base[2] + (TEAL[2] - base[2]) * g)
            px[x, y] = (r, gg, b)
    return img


def add_dot_grid(img, spacing, radius, alpha):
    """Subtle dot mesh overlay."""
    w, h = img.size
    overlay = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)
    for y in range(spacing, h - spacing, spacing):
        for x in range(spacing, w - spacing, spacing):
            draw.ellipse(
                [x - radius, y - radius, x + radius, y + radius],
                fill=(255, 255, 255, alpha),
            )
    img.paste(overlay, (0, 0), overlay)
    return img


def draw_leaf(img, cx, cy, size, color):
    """Stylized leaf using two arcs (ellipses clipped) and a central vein."""
    w, h = img.size
    leaf_layer = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(leaf_layer)

    leaf_w = size
    leaf_h = int(size * 2.0)

    leaf_img = Image.new("RGBA", (leaf_w * 2, leaf_h * 2), (0, 0, 0, 0))
    ld = ImageDraw.Draw(leaf_img)

    ld.ellipse([0, 0, leaf_w * 2, leaf_h * 2], fill=color + (255,))
    ld.polygon(
        [(0, leaf_h * 2), (leaf_w * 2, 0), (leaf_w * 2, leaf_h * 2)],
        fill=(0, 0, 0, 0),
    )

    vein_color = (255, 255, 255, 90)
    ld.line(
        [(leaf_w * 2 - 10, 10), (10, leaf_h * 2 - 10)],
        fill=vein_color,
        width=max(2, size // 30),
    )

    leaf_img = leaf_img.rotate(-20, resample=Image.BICUBIC, expand=True)
    lw, lh = leaf_img.size
    leaf_layer.paste(leaf_img, (cx - lw // 2, cy - lh // 2), leaf_img)
    img.paste(leaf_layer, (0, 0), leaf_layer)
    return img


def load_font(size, bold=True):
    """Try system fonts in order of preference."""
    candidates_bold = [
        "/System/Library/Fonts/Helvetica.ttc",
        "/System/Library/Fonts/HelveticaNeue.ttc",
        "/System/Library/Fonts/Supplemental/Arial Bold.ttf",
        "/Library/Fonts/Arial Bold.ttf",
        "/System/Library/Fonts/SFNS.ttf",
    ]
    candidates_reg = [
        "/System/Library/Fonts/HelveticaNeue.ttc",
        "/System/Library/Fonts/Helvetica.ttc",
        "/System/Library/Fonts/Supplemental/Arial.ttf",
        "/Library/Fonts/Arial.ttf",
        "/System/Library/Fonts/SFNS.ttf",
    ]
    paths = candidates_bold if bold else candidates_reg
    for p in paths:
        if os.path.exists(p):
            try:
                if bold and p.endswith(".ttc"):
                    return ImageFont.truetype(p, size, index=1)
                return ImageFont.truetype(p, size)
            except Exception:
                continue
    return ImageFont.load_default()


def draw_centered_text(draw, text, font, y, color, w):
    bbox = draw.textbbox((0, 0), text, font=font)
    tw = bbox[2] - bbox[0]
    th = bbox[3] - bbox[1]
    x = (w - tw) // 2 - bbox[0]
    draw.text((x, y), text, font=font, fill=color)
    return th


def add_bottom_accent(img, color, height_px):
    """Teal-to-transparent fade bar across bottom edge."""
    w, h = img.size
    bar = Image.new("RGBA", (w, height_px), (0, 0, 0, 0))
    px = bar.load()
    for y in range(height_px):
        alpha = int(220 * (1 - y / height_px) ** 1.5)
        for x in range(w):
            edge_fade = 1.0
            if x < w * 0.1:
                edge_fade = x / (w * 0.1)
            elif x > w * 0.9:
                edge_fade = (w - x) / (w * 0.1)
            px[x, y] = (color[0], color[1], color[2], int(alpha * edge_fade))
    img.paste(bar, (0, h - height_px), bar)
    return img


def main():
    print("Building background...")
    img = build_background(SW, SH)

    print("Adding dot grid texture...")
    img = add_dot_grid(img, spacing=44, radius=2, alpha=18)

    img = img.convert("RGBA")

    print("Drawing leaf icon...")
    leaf_cx = SW // 2
    leaf_cy = int(SH * 0.26)
    img = draw_leaf(img, leaf_cx, leaf_cy, size=70, color=TEAL)

    print("Rendering text...")
    draw = ImageDraw.Draw(img)

    title_font = load_font(180, bold=True)
    tagline_font = load_font(54, bold=False)

    title = "Sage Health"
    bbox = draw.textbbox((0, 0), title, font=title_font)
    tw = bbox[2] - bbox[0]
    th = bbox[3] - bbox[1]
    title_y = int(SH * 0.36)
    title_x = (SW - tw) // 2 - bbox[0]

    shadow = Image.new("RGBA", (SW, SH), (0, 0, 0, 0))
    sd = ImageDraw.Draw(shadow)
    sd.text((title_x + 4, title_y + 6), title, font=title_font, fill=(0, 0, 0, 120))
    shadow = shadow.filter(ImageFilter.GaussianBlur(radius=8))
    img = Image.alpha_composite(img, shadow)

    draw = ImageDraw.Draw(img)
    draw.text((title_x, title_y), title, font=title_font, fill=WHITE + (255,))

    line_y = title_y + th + 60
    line_w = 400
    line_x = (SW - line_w) // 2
    line_thickness = 5
    draw.rectangle(
        [line_x, line_y, line_x + line_w, line_y + line_thickness],
        fill=TEAL + (255,),
    )

    glow = Image.new("RGBA", (SW, SH), (0, 0, 0, 0))
    gd = ImageDraw.Draw(glow)
    gd.rectangle(
        [line_x - 20, line_y - 8, line_x + line_w + 20, line_y + line_thickness + 8],
        fill=TEAL + (90,),
    )
    glow = glow.filter(ImageFilter.GaussianBlur(radius=14))
    img = Image.alpha_composite(img, glow)
    draw = ImageDraw.Draw(img)
    draw.rectangle(
        [line_x, line_y, line_x + line_w, line_y + line_thickness],
        fill=TEAL + (255,),
    )

    tagline = "Your practice, operating at its full potential."
    tagline_y = line_y + line_thickness + 50
    bbox2 = draw.textbbox((0, 0), tagline, font=tagline_font)
    tw2 = bbox2[2] - bbox2[0]
    tagline_x = (SW - tw2) // 2 - bbox2[0]
    draw.text((tagline_x, tagline_y), tagline, font=tagline_font, fill=SAGE_GRAY + (255,))

    print("Adding bottom accent...")
    img = add_bottom_accent(img, TEAL, height_px=int(SH * 0.04))

    print("Downsampling for crisp anti-aliasing...")
    img = img.convert("RGB")
    img = img.resize((W, H), Image.LANCZOS)

    out_path = os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        "images",
        "og-image.png",
    )
    img.save(out_path, "PNG", optimize=True)
    print(f"Saved: {out_path} ({W}x{H})")


if __name__ == "__main__":
    main()
