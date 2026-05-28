"""Generate a brand-correct 1200x630 Open Graph image for Sage Health.

Brand spec sources (single source of truth):
- ../FrontDeskFramework/brand-guide.html  -> colors, gradients, type rules
- ../favicon.svg                          -> leaf logomark path
- ../styles.css :root                     -> CSS tokens

Design follows the brand guide's Technology / social-card surface:
- Dark base (#0b1310 -> #040806) + radial glows (green NW, indigo SE)
- AI gradient (#7ab86d -> #4dd4ac -> #818cf8) on the climax word
- PT Serif Bold wordmark + headline (brand display face)
- Stroked leaf logomark traced from favicon.svg, glowing on dark
"""
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import math
import os

# ─────────────────────────────────────────────────────────────────────────
# Canvas
# ─────────────────────────────────────────────────────────────────────────
W, H = 1200, 630
SCALE = 2                       # render at 2x then downsample (crisp AA)
SW, SH = W * SCALE, H * SCALE

# ─────────────────────────────────────────────────────────────────────────
# Brand tokens (RGB) — pulled directly from brand-guide.html :root
# ─────────────────────────────────────────────────────────────────────────
# Dark technology surface
BG_TOP        = (0x0b, 0x13, 0x10)   # #0b1310  hero top
BG_BOT        = (0x04, 0x08, 0x06)   # #040806  hero bottom

# Greens
GREEN         = (0x2d, 0x5a, 0x27)   # #2d5a27  primary green
GREEN_MID     = (0x3d, 0x75, 0x35)   # #3d7535
ACCENT        = (0x5c, 0x9e, 0x52)   # #5c9e52
ACCENT_BRIGHT = (0x7a, 0xb8, 0x6d)   # #7ab86d  leaf on dark

# AI gradient stops (linear-gradient(135deg, ...))
GRAD_AI_TEXT  = [
    (0x7a, 0xb8, 0x6d),              # #7ab86d  green
    (0x4d, 0xd4, 0xac),              # #4dd4ac  teal
    (0x81, 0x8c, 0xf8),              # #818cf8  indigo
]
GRAD_AI       = [
    (0x5c, 0x9e, 0x52),
    (0x2d, 0x8c, 0x9e),
    (0x63, 0x66, 0xf1),
]
INDIGO_GLOW   = (0x63, 0x66, 0xf1)   # #6366f1  indigo for SE radial

# Ink on dark
WHITE         = (255, 255, 255)
INK_SOFT      = (255, 255, 255)      # alpha applied later
INK_MUTED     = (255, 255, 255)

PT_SERIF_PATH = "/System/Library/Fonts/Supplemental/PTSerif.ttc"


# ─────────────────────────────────────────────────────────────────────────
# Fonts — PT Serif (TTC indices: 0=Reg, 1=Italic, 2=BoldItalic, 3=Bold)
# ─────────────────────────────────────────────────────────────────────────
def serif(size, bold=True):
    if os.path.exists(PT_SERIF_PATH):
        try:
            return ImageFont.truetype(PT_SERIF_PATH, size, index=3 if bold else 0)
        except Exception:
            pass
    # Fallback: Georgia / system serif
    for p in [
        "/System/Library/Fonts/Supplemental/Georgia Bold.ttf" if bold else "/System/Library/Fonts/Supplemental/Georgia.ttf",
        "/System/Library/Fonts/Times.ttc",
    ]:
        if os.path.exists(p):
            try:
                return ImageFont.truetype(p, size)
            except Exception:
                continue
    return ImageFont.load_default()


def sans(size, bold=False):
    candidates = (
        ["/System/Library/Fonts/HelveticaNeue.ttc"]
        + (["/System/Library/Fonts/Supplemental/Arial Bold.ttf"] if bold else
           ["/System/Library/Fonts/Supplemental/Arial.ttf"])
        + ["/System/Library/Fonts/Helvetica.ttc"]
    )
    for p in candidates:
        if os.path.exists(p):
            try:
                return ImageFont.truetype(p, size)
            except Exception:
                continue
    return ImageFont.load_default()


# ─────────────────────────────────────────────────────────────────────────
# Background — dark vertical gradient + radial glows + dot grid
# ─────────────────────────────────────────────────────────────────────────
def lerp(a, b, t):
    return tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(3))


def build_background(w, h):
    """Vertical dark gradient + green NW radial glow + indigo SE radial glow.

    Mirrors the brand guide hero/social surfaces:
    .ctx-hero { background: linear-gradient(180deg,#0b1310 0%,#040806 100%);
                background: radial-gradient(circle at 15% 20%, rgba(92,158,82,.08), transparent 50%),
                            radial-gradient(circle at 85% 75%, rgba(99,102,241,.06), transparent 50%); }
    Intensities bumped slightly for OG legibility at small thumbnail sizes.
    """
    img = Image.new("RGB", (w, h), BG_BOT)
    px = img.load()

    # Glow centers (per brand guide percentages)
    g_cx, g_cy = w * 0.15, h * 0.20      # green NW
    i_cx, i_cy = w * 0.85, h * 0.75      # indigo SE
    g_radius   = math.hypot(w, h) * 0.55
    i_radius   = math.hypot(w, h) * 0.55

    for y in range(h):
        base = lerp(BG_TOP, BG_BOT, y / h)
        for x in range(w):
            # Green glow (rgba(92,158,82,.18) at center, falls off to transparent)
            dg = math.hypot(x - g_cx, y - g_cy) / g_radius
            wg = max(0.0, 1.0 - dg) ** 2.2 * 0.22
            # Indigo glow (rgba(99,102,241,.14))
            di = math.hypot(x - i_cx, y - i_cy) / i_radius
            wi = max(0.0, 1.0 - di) ** 2.2 * 0.18

            r = int(base[0] + (ACCENT[0]      - base[0]) * wg + (INDIGO_GLOW[0] - base[0]) * wi)
            g = int(base[1] + (ACCENT[1]      - base[1]) * wg + (INDIGO_GLOW[1] - base[1]) * wi)
            b = int(base[2] + (ACCENT[2]      - base[2]) * wg + (INDIGO_GLOW[2] - base[2]) * wi)
            px[x, y] = (min(r, 255), min(g, 255), min(b, 255))
    return img


def add_dot_grid(img, spacing, radius, alpha):
    """Very faint dot mesh — the brand uses a subtle texture overlay."""
    w, h = img.size
    overlay = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(overlay)
    for y in range(spacing, h - spacing, spacing):
        for x in range(spacing, w - spacing, spacing):
            d.ellipse([x - radius, y - radius, x + radius, y + radius],
                      fill=(255, 255, 255, alpha))
    img.paste(overlay, (0, 0), overlay)
    return img


# ─────────────────────────────────────────────────────────────────────────
# Leaf logomark — traced from favicon.svg
# Path (viewBox 0 0 32 32):
#   M16 3 C 10.67 8.33, 8 12.33, 8 17.67
#   a 8 8 0 0 0 16 0
#   c 0 -5.34, -2.67 -9.34, -8 -14.67 Z
# Stem: M16 29 V 14.67 (opacity .6)
# ─────────────────────────────────────────────────────────────────────────
def _cubic(p0, p1, p2, p3, n):
    out = []
    for i in range(n + 1):
        t = i / n
        mt = 1 - t
        x = mt**3 * p0[0] + 3 * mt**2 * t * p1[0] + 3 * mt * t**2 * p2[0] + t**3 * p3[0]
        y = mt**3 * p0[1] + 3 * mt**2 * t * p1[1] + 3 * mt * t**2 * p2[1] + t**3 * p3[1]
        out.append((x, y))
    return out


def _leaf_points(samples=80):
    """Return outline points of the leaf in viewBox (0..32) coordinates."""
    # Left cubic: (16,3) -> (8,17.67)  via controls (10.67,8.33), (8,12.33)
    left = _cubic((16, 3), (10.67, 8.33), (8, 12.33), (8, 17.67), samples)

    # Arc: semicircle centered (16, 17.67), radius 8, from (8,17.67) going
    # through bottom (16, 25.67) to (24, 17.67). In SVG with sweep=0 from
    # (8,17.67) -> (24,17.67), the arc bulges downward.
    arc = []
    for i in range(1, samples + 1):
        theta = math.pi + (math.pi * i / samples)   # π -> 2π (left -> right via bottom)
        arc.append((16 + 8 * math.cos(theta), 17.67 + 8 * math.sin(theta)))

    # Right cubic: (24,17.67) -> (16,3) via controls (24,12.33), (21.33,8.33)
    right = _cubic((24, 17.67), (24, 12.33), (21.33, 8.33), (16, 3), samples)

    return left + arc[1:] + right[1:]


def draw_leaf(img, cx, cy, height_px, color, glow=True):
    """Render the brand leaf at given center / height, with optional glow halo."""
    # viewBox is 32 tall; the leaf body spans roughly y=3..25.67 (~22.67 units).
    # Stem extends to y=29 (so full mark height = 26 units). We size so the full
    # mark including stem matches height_px.
    full_h_units = 29 - 3
    scale = height_px / full_h_units

    # Render into a transparent layer sized generously
    pad = int(height_px * 0.4)
    box_w = int(32 * scale) + pad * 2
    box_h = int(29 * scale) + pad * 2
    layer = Image.new("RGBA", (box_w, box_h), (0, 0, 0, 0))
    ld = ImageDraw.Draw(layer)

    ox = pad - int(0 * scale)               # viewBox-origin x in layer
    oy = pad - int(0 * scale)

    def vb_to_px(p):
        return (ox + p[0] * scale, oy + p[1] * scale)

    outline = [vb_to_px(p) for p in _leaf_points(samples=120)]
    outline.append(outline[0])              # close

    stroke_w = max(2, int(2.5 * scale))     # matches favicon stroke-width 2.5
    ld.line(outline, fill=color + (255,), width=stroke_w, joint="curve")

    # Stem at 0.6 opacity
    stem_top = vb_to_px((16, 14.67))
    stem_bot = vb_to_px((16, 29))
    stem_alpha = int(255 * 0.6)
    ld.line([stem_top, stem_bot], fill=color + (stem_alpha,),
            width=stroke_w, joint="curve")

    # Glow halo: blur a brighter copy underneath
    if glow:
        halo_src = Image.new("RGBA", (box_w, box_h), (0, 0, 0, 0))
        hd = ImageDraw.Draw(halo_src)
        # rgba(122,184,109,.35) per brand guide drop-shadow
        halo_color = ACCENT_BRIGHT + (int(255 * 0.35),)
        hd.line(outline, fill=halo_color, width=stroke_w + 4, joint="curve")
        hd.line([stem_top, stem_bot], fill=halo_color,
                width=stroke_w + 4, joint="curve")
        halo = halo_src.filter(ImageFilter.GaussianBlur(radius=int(height_px * 0.18)))
        # Paste halo first, then sharp leaf on top
        img.alpha_composite(halo, (cx - box_w // 2, cy - box_h // 2))

    img.alpha_composite(layer, (cx - box_w // 2, cy - box_h // 2))
    return img


# ─────────────────────────────────────────────────────────────────────────
# Gradient text — the AI gradient applied across a text mask
# ─────────────────────────────────────────────────────────────────────────
def draw_gradient_text(img, text, font, xy, stops, angle_deg=20):
    """Draw text filled with a multi-stop linear gradient.

    `stops` is a list of RGB tuples; gradient is laid along `angle_deg`
    (per brand guide: 135deg linear-gradient → maps to a slight downward slope
    across the text). 0deg = left→right.
    """
    # Build a mask of the text
    bbox = ImageDraw.Draw(Image.new("L", (1, 1))).textbbox((0, 0), text, font=font)
    tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]

    # Pad mask so anti-aliased edges aren't clipped
    pad = max(8, int(font.size * 0.1))
    mask = Image.new("L", (tw + pad * 2, th + pad * 2), 0)
    md = ImageDraw.Draw(mask)
    md.text((pad - bbox[0], pad - bbox[1]), text, font=font, fill=255)

    # Build the gradient fill at the same size
    mw, mh = mask.size
    grad = Image.new("RGB", (mw, mh))
    gpx = grad.load()
    # 135deg in CSS = top-left → bottom-right. Direction vector:
    a = math.radians(angle_deg)
    dx, dy = math.cos(a), math.sin(a)
    # Project each pixel onto the direction; normalize 0..1 across the bbox
    proj_min = 0
    proj_max = mw * dx + mh * dy
    if proj_max == 0:
        proj_max = mw
    n_stops = len(stops)
    for y in range(mh):
        for x in range(mw):
            t = (x * dx + y * dy - proj_min) / (proj_max - proj_min)
            t = max(0.0, min(1.0, t))
            # Pick segment between stops
            seg = t * (n_stops - 1)
            i0 = int(seg)
            i1 = min(i0 + 1, n_stops - 1)
            ft = seg - i0
            gpx[x, y] = lerp(stops[i0], stops[i1], ft)

    # Composite gradient onto img using mask
    grad_rgba = grad.convert("RGBA")
    grad_rgba.putalpha(mask)
    x0, y0 = xy
    img.alpha_composite(grad_rgba, (int(x0 - pad + bbox[0]), int(y0 - pad + bbox[1])))
    return tw, th


# ─────────────────────────────────────────────────────────────────────────
# Main composition
# ─────────────────────────────────────────────────────────────────────────
def main():
    print("→ Background (dark + green NW glow + indigo SE glow)…")
    img = build_background(SW, SH).convert("RGBA")

    print("→ Dot grid texture…")
    img = add_dot_grid(img, spacing=int(48 * SCALE / 2), radius=int(SCALE * 1.0),
                       alpha=14)

    # ─── Top: logo lockup (leaf + wordmark) ────────────────────────────
    print("→ Logo lockup (leaf + PT Serif wordmark)…")
    lockup_y     = int(SH * 0.135)
    leaf_h_px    = int(78 * SCALE)
    wordmark_pt  = int(56 * SCALE)
    wordmark_font = serif(wordmark_pt, bold=True)

    wordmark = "Sage Health"
    # Measure wordmark
    d_probe = ImageDraw.Draw(img)
    wm_bbox = d_probe.textbbox((0, 0), wordmark, font=wordmark_font)
    wm_w = wm_bbox[2] - wm_bbox[0]
    wm_h = wm_bbox[3] - wm_bbox[1]

    gap = int(20 * SCALE)
    leaf_w_render = int(leaf_h_px * (32 / 29))      # ~viewBox aspect, mark ≈ wide as tall
    total_w = leaf_w_render + gap + wm_w
    lockup_x = (SW - total_w) // 2

    leaf_cx = lockup_x + leaf_w_render // 2
    leaf_cy = lockup_y
    img = draw_leaf(img, leaf_cx, leaf_cy, leaf_h_px, ACCENT_BRIGHT, glow=True)

    wm_x = lockup_x + leaf_w_render + gap - wm_bbox[0]
    wm_y = lockup_y - wm_h // 2 - wm_bbox[1]
    d = ImageDraw.Draw(img)
    d.text((wm_x, wm_y), wordmark, font=wordmark_font, fill=WHITE + (255,))

    # ─── Eyebrow accent line + tag (small, centered above headline) ────
    eyebrow = "INTELLIGENT  OPERATIONS  FOR  INDEPENDENT  PRACTICES"
    eyebrow_font = sans(int(15 * SCALE), bold=True)
    eb_bbox = d.textbbox((0, 0), eyebrow, font=eyebrow_font)
    eb_w = eb_bbox[2] - eb_bbox[0]
    eb_x = (SW - eb_w) // 2 - eb_bbox[0]
    eb_y = int(SH * 0.30)
    d.text((eb_x, eb_y), eyebrow, font=eyebrow_font,
           fill=ACCENT_BRIGHT + (235,))

    # Thin accent line under eyebrow
    line_w = int(48 * SCALE)
    line_h = max(1, int(1.5 * SCALE))
    line_y = eb_y + (eb_bbox[3] - eb_bbox[1]) + int(14 * SCALE)
    line_x = (SW - line_w) // 2
    d.rectangle([line_x, line_y, line_x + line_w, line_y + line_h],
                fill=ACCENT_BRIGHT + (180,))

    # ─── Headline (two lines, AI-gradient on climax) ───────────────────
    # Auto-fit: shrink font until line 2 fits within MAX_HEAD_W of the canvas
    # (we have to fit "operating at its full potential." cleanly).
    print("→ Headline (PT Serif Bold + AI gradient)…")
    line1 = "Your practice,"
    line2 = "operating at its full potential."
    MAX_HEAD_W = int(SW * 0.86)         # leave generous safe margins

    head_pt = int(92 * SCALE)
    while head_pt > int(40 * SCALE):
        head_font = serif(head_pt, bold=True)
        probe = d.textbbox((0, 0), line2, font=head_font)
        if (probe[2] - probe[0]) <= MAX_HEAD_W:
            break
        head_pt -= int(2 * SCALE)
    print(f"   resolved headline size: {head_pt // SCALE}pt @1x")

    l1_bbox = d.textbbox((0, 0), line1, font=head_font)
    l1_w = l1_bbox[2] - l1_bbox[0]
    l1_h = l1_bbox[3] - l1_bbox[1]

    l2_bbox = d.textbbox((0, 0), line2, font=head_font)
    l2_w = l2_bbox[2] - l2_bbox[0]
    l2_h = l2_bbox[3] - l2_bbox[1]

    line_gap = int(8 * SCALE)
    headline_top = line_y + line_h + int(36 * SCALE)

    # Line 1 — white
    l1_x = (SW - l1_w) // 2 - l1_bbox[0]
    l1_y = headline_top - l1_bbox[1]
    # Subtle shadow for depth
    shadow_layer = Image.new("RGBA", (SW, SH), (0, 0, 0, 0))
    sd = ImageDraw.Draw(shadow_layer)
    sd.text((l1_x + int(2 * SCALE), l1_y + int(4 * SCALE)),
            line1, font=head_font, fill=(0, 0, 0, 110))
    shadow_layer = shadow_layer.filter(ImageFilter.GaussianBlur(radius=int(6 * SCALE)))
    img = Image.alpha_composite(img, shadow_layer)
    d = ImageDraw.Draw(img)
    d.text((l1_x, l1_y), line1, font=head_font, fill=WHITE + (255,))

    # Line 2 — AI gradient
    l2_x = (SW - l2_w) // 2 - l2_bbox[0]
    l2_y = headline_top + l1_h + line_gap - l2_bbox[1]
    # Indigo soft halo behind gradient text for that "drop-shadow" glow
    halo_layer = Image.new("RGBA", (SW, SH), (0, 0, 0, 0))
    hd = ImageDraw.Draw(halo_layer)
    hd.text((l2_x, l2_y), line2, font=head_font,
            fill=(0x81, 0x8c, 0xf8, 70))
    halo_layer = halo_layer.filter(ImageFilter.GaussianBlur(radius=int(14 * SCALE)))
    img = Image.alpha_composite(img, halo_layer)
    draw_gradient_text(img, line2, head_font, (l2_x, l2_y), GRAD_AI_TEXT,
                       angle_deg=18)

    # ─── Sub-tagline (sans-serif, muted) ───────────────────────────────
    d = ImageDraw.Draw(img)
    lede_font = sans(int(28 * SCALE), bold=False)
    lede = "Expert evaluation.  Standardized processes.  AI agents."
    ld_bbox = d.textbbox((0, 0), lede, font=lede_font)
    ld_w = ld_bbox[2] - ld_bbox[0]
    ld_x = (SW - ld_w) // 2 - ld_bbox[0]
    ld_y = l2_y + l2_h + int(36 * SCALE)
    d.text((ld_x, ld_y), lede, font=lede_font,
           fill=WHITE + (180,))

    # ─── Bottom-right: domain mark ─────────────────────────────────────
    domain_font = sans(int(16 * SCALE), bold=True)
    domain = "sagehealth.ai"
    dm_bbox = d.textbbox((0, 0), domain, font=domain_font)
    dm_w = dm_bbox[2] - dm_bbox[0]
    dm_x = SW - dm_w - int(60 * SCALE) - dm_bbox[0]
    dm_y = SH - int(56 * SCALE) - dm_bbox[1]
    d.text((dm_x, dm_y), domain, font=domain_font,
           fill=WHITE + (140,))

    # ─── Bottom-left: tiny brand bullet pill (optional spec) ───────────
    bullet_font = sans(int(13 * SCALE), bold=True)
    bullet = "HOUSTON · DALLAS"
    bl_bbox = d.textbbox((0, 0), bullet, font=bullet_font)
    bl_x = int(60 * SCALE) - bl_bbox[0]
    bl_y = SH - int(54 * SCALE) - bl_bbox[1]
    # accent dot
    dot_r = int(5 * SCALE)
    d.ellipse([bl_x - dot_r * 4, bl_y + (bl_bbox[3] - bl_bbox[1]) // 2 - dot_r,
               bl_x - dot_r * 2, bl_y + (bl_bbox[3] - bl_bbox[1]) // 2 + dot_r],
              fill=ACCENT_BRIGHT + (220,))
    d.text((bl_x, bl_y), bullet, font=bullet_font, fill=WHITE + (140,))

    # ─── Downsample to final 1200×630 for crisp anti-aliasing ──────────
    print("→ Downsampling 2x → 1x with Lanczos…")
    img = img.convert("RGB")
    img = img.resize((W, H), Image.LANCZOS)

    out_path = os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        "images", "og-image.png",
    )
    img.save(out_path, "PNG", optimize=True)
    print(f"✓ Saved {out_path} ({W}x{H})")


if __name__ == "__main__":
    main()
