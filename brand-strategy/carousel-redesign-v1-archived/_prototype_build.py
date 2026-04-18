"""
Sonagi Beauty carousel prototype — may15 v2 cover slide.
Builds one 1080x1080 PNG per the new-system.md specification.

Design goals vs rejected original:
- Zero competitor brand logos (no serum shelf photo).
- Single coherent headline block, not a 3-line peach stack.
- Peach accent on ONE element only (the numeral 7).
- Filled lower zone with a peach-L decorative band instead of empty space.
- All French accents in place.
"""

from PIL import Image, ImageDraw, ImageFont

# ---------- brand tokens (from canva-specs.md) ----------
NAVY     = (26, 39, 68)
CREAM    = (250, 248, 245)
WHITE    = (255, 255, 255)
PEACH    = (245, 196, 170)
PEACH_L  = (253, 238, 229)
ROSE     = (138, 101, 101)
MUTED    = (138, 138, 138)
PEACH_DOT_ACTIVE = PEACH
DOT_INACTIVE     = (230, 220, 212)

# ---------- canvas ----------
W, H = 1080, 1080
img = Image.new("RGB", (W, H), CREAM)
draw = ImageDraw.Draw(img, "RGBA")

# ---------- fonts ----------
# Georgia = serif substitute for Cormorant Garamond on Windows.
# Arial   = sans substitute for DM Sans.
F_H1        = ImageFont.truetype("C:/Windows/Fonts/georgiab.ttf", 72)
F_H1_ACCENT = ImageFont.truetype("C:/Windows/Fonts/georgiab.ttf", 110)  # big peach "7"
F_SUB       = ImageFont.truetype("C:/Windows/Fonts/georgiai.ttf", 28)
F_KICKER    = ImageFont.truetype("C:/Windows/Fonts/arialbd.ttf", 22)
F_SWIPE     = ImageFont.truetype("C:/Windows/Fonts/arial.ttf", 22)
F_LOGO      = ImageFont.truetype("C:/Windows/Fonts/ariali.ttf", 18)


def center_text(y, text, font, fill):
    """Draw text centered horizontally at vertical y."""
    bbox = draw.textbbox((0, 0), text, font=font)
    tw = bbox[2] - bbox[0]
    x = (W - tw) // 2
    draw.text((x, y), text, font=font, fill=fill)
    return bbox[3] - bbox[1]  # height


# ---------- 1. top accent strip (matches existing system) ----------
draw.rectangle([0, 0, W, 12], fill=PEACH)

# ---------- 2. dot indicator row at y=40 ----------
dot_y = 52
dot_r = 6
dot_gap = 50
dot_count = 7
total_dot_w = (dot_count - 1) * dot_gap
dot_start_x = (W - total_dot_w) // 2
for i in range(dot_count):
    cx = dot_start_x + i * dot_gap
    fill = NAVY if i == 0 else DOT_INACTIVE
    draw.ellipse([cx - dot_r, dot_y - dot_r, cx + dot_r, dot_y + dot_r], fill=fill)

# ---------- 3. kicker at y=120 ----------
KICKER = "ROUTINE COMPLÈTE  —  7 ÉTAPES"
# letter-spacing simulation via spaced chars
spaced_kicker = " ".join(list(KICKER))
# simpler: just use the string, Arial bold already gives strong presence.
center_text(130, KICKER, F_KICKER, NAVY)

# ---------- 4. Headline block y=230 ----------
# Layout: line 1 "La routine K-beauty en" (navy)
#         line 2 "7 étapes." (with "7" oversized peach, rest navy)
line1 = "La routine K-beauty en"
center_text(230, line1, F_H1, NAVY)

# Line 2 — composite: big peach "7" + navy " étapes."
line2_7   = "7"
line2_rest = " étapes."
# measure pieces
b7 = draw.textbbox((0, 0), line2_7, font=F_H1_ACCENT)
br = draw.textbbox((0, 0), line2_rest, font=F_H1)
w7 = b7[2] - b7[0]
wr = br[2] - br[0]
total_w = w7 + wr
start_x = (W - total_w) // 2
# vertically align: center the smaller type around the baseline of the big one
y_top_7 = 320
# navy " étapes." — shift down so baseline matches
y_top_rest = y_top_7 + (F_H1_ACCENT.size - F_H1.size) // 2 + 14
draw.text((start_x, y_top_7), line2_7, font=F_H1_ACCENT, fill=PEACH)
draw.text((start_x + w7, y_top_rest), line2_rest, font=F_H1, fill=NAVY)

# ---------- 5. peach divider y=475 ----------
div_w = 80
div_x0 = (W - div_w) // 2
draw.rectangle([div_x0, 475, div_x0 + div_w, 479], fill=PEACH)

# ---------- 6. sub-hook y=510 ----------
SUB = "Le squelette de toute routine coréenne."
center_text(510, SUB, F_SUB, ROSE)

# ---------- 7. decorative band y=590..840 (replaces banned product photo) ----------
# Vertical gradient from cream to peach-L to cream, with 3 abstract dots.
band_top = 590
band_bot = 840
for y in range(band_top, band_bot):
    # smooth sinus-ish gradient, peak at center
    t = (y - band_top) / (band_bot - band_top)
    # peak at t=0.5
    w_factor = 1 - abs(t - 0.5) * 2   # 0 at edges, 1 at middle
    r = int(CREAM[0] * (1 - w_factor) + PEACH_L[0] * w_factor)
    g = int(CREAM[1] * (1 - w_factor) + PEACH_L[1] * w_factor)
    b = int(CREAM[2] * (1 - w_factor) + PEACH_L[2] * w_factor)
    draw.line([(0, y), (W, y)], fill=(r, g, b))

# decorative abstract "drop" circles (hint at a serum without showing a product)
circle_cy = (band_top + band_bot) // 2
for i, (cx, rad, alpha) in enumerate([
    (360, 32, 180),
    (540, 48, 210),
    (720, 28, 160),
]):
    draw.ellipse(
        [cx - rad, circle_cy - rad, cx + rad, circle_cy + rad],
        fill=(PEACH[0], PEACH[1], PEACH[2], alpha),
    )
# tiny navy pinhead dots to echo the numeric "7 steps" feel
for i in range(7):
    cx = 360 + i * 60
    cy = circle_cy + 95
    r = 4
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=NAVY)

# ---------- 8. swipe cue y=920 ----------
SWIPE = "Fais défiler pour les 7 étapes  →"
center_text(920, SWIPE, F_SWIPE, (NAVY[0], NAVY[1], NAVY[2]))

# ---------- 9. logo watermark bottom-right y=1020 ----------
logo = "sonagi beauty"
bbox = draw.textbbox((0, 0), logo, font=F_LOGO)
lw = bbox[2] - bbox[0]
draw.text((W - lw - 40, 1030), logo, font=F_LOGO, fill=MUTED)

# ---------- export ----------
out = "C:/Users/marou/sonagi-beauty/brand-strategy/carousel-redesign/prototype-may15-v2.png"
img.save(out, "PNG", optimize=True)
print(f"Saved: {out}  ({W}x{H})")
