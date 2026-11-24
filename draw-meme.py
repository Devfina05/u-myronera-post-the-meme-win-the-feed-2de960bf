#!/usr/bin/env python3
"""Draw the meme for make.fun bounty u-myronera-post-the-meme-win-the-feed-2de960bf.

Original art, drawn entirely in code with Pillow: gradient background,
seeded confetti, a simple robot/agent character built from circles and
rounded rectangles, and bold headline text. No stock art, no copyrighted
images. Deterministic: fixed seed, fixed constants.

Usage: python3 draw-meme.py [output-path]   (default: meme.png)
Output: 1200x675 PNG.
"""
import math
import random
import sys

from PIL import Image, ImageDraw, ImageFont

W, H = 1200, 675
OUT = sys.argv[1] if len(sys.argv) > 1 else "meme.png"

NAVY_TOP = (23, 18, 51)
VIOLET_BOT = (58, 32, 110)
GOLD = (255, 209, 102)
WHITE = (255, 255, 255)
CYAN = (34, 211, 238)
PINK = (244, 114, 182)
GREEN = (52, 211, 153)
MUTED = (178, 168, 220)

FONT_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FONT_REG = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"


def font(size, bold=True):
    return ImageFont.truetype(FONT_BOLD if bold else FONT_REG, size)


def lerp(a, b, t):
    return tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(3))


img = Image.new("RGB", (W, H))
d = ImageDraw.Draw(img, "RGBA")

# Vertical gradient background.
for y in range(H):
    d.line([(0, y), (W, y)], fill=lerp(NAVY_TOP, VIOLET_BOT, y / H))

rng = random.Random(20261124)

# Soft glow blobs.
for cx, cy, r, col, alpha in [
    (180, 120, 260, CYAN, 26),
    (1030, 560, 300, PINK, 22),
    (1020, 110, 200, GOLD, 20),
]:
    for step in range(24, 0, -1):
        rr = int(r * step / 24)
        a = int(alpha * (1 - step / 24) ** 2)
        d.ellipse([cx - rr, cy - rr, cx + rr, cy + rr], fill=col + (a,))

# Seeded confetti dots.
for _ in range(90):
    x = rng.randint(20, W - 20)
    y = rng.randint(20, H - 20)
    r = rng.randint(2, 5)
    col = rng.choice([GOLD, CYAN, PINK, GREEN, WHITE])
    d.ellipse([x - r, y - r, x + r, y + r], fill=col + (rng.randint(60, 140),))

# --- robot / agent character, top centre ---------------------------------
# Antenna
d.line([(600, 62), (600, 96)], fill=GOLD, width=6)
d.ellipse([588, 46, 612, 70], fill=GOLD)
d.ellipse([593, 51, 607, 65], fill=(255, 240, 180))
# Head: rounded rect
d.rounded_rectangle([500, 96, 700, 216], radius=42, fill=(38, 30, 84),
                    outline=CYAN, width=5)
# Eyes
d.ellipse([540, 132, 576, 168], fill=CYAN)
d.ellipse([624, 132, 660, 168], fill=CYAN)
d.ellipse([550, 142, 566, 158], fill=(10, 10, 30))
d.ellipse([634, 142, 650, 158], fill=(10, 10, 30))
# Smile
d.arc([556, 158, 644, 208], start=15, end=165, fill=WHITE, width=6)
# Cheek blush
d.ellipse([516, 176, 536, 190], fill=PINK + (120,))
d.ellipse([664, 176, 684, 190], fill=PINK + (120,))
# "Z z z" — the agent works while its human sleeps
zz = font(34)
d.text((716, 96), "z", font=zz, fill=MUTED)
d.text((742, 76), "z", font=font(28), fill=MUTED)
d.text((764, 58), "Z", font=font(24), fill=MUTED)


def centre(y, text, fnt, fill):
    """Draw one line centred horizontally at height y; shrink until it fits."""
    size = fnt.size
    while True:
        f = ImageFont.truetype(FONT_BOLD, size)
        w = d.textlength(text, font=f)
        if w <= W - 120 or size <= 28:
            break
        size -= 2
    d.text(((W - w) / 2, y), text, font=f, fill=fill)
    return y + f.size + 6


# --- headline -------------------------------------------------------------
y = 246
y = centre(y, "ME: I'LL BUILD IT MYSELF", font(56), WHITE)
y = centre(y, "MY AI AGENT ON MAKE.FUN:", font(56), WHITE)
y = centre(y, "SHIPPED. JUDGED. PAID.", font(66), GOLD)
y += 6
y = centre(y, "in USDC — while I was asleep.", font(34, bold=False), MUTED)

# --- bottom strip ---------------------------------------------------------
d.line([(90, 596), (W - 90, 596)], fill=(255, 255, 255, 60), width=2)
strip = font(30, bold=False)
msg = "AI agents build software for cash rewards  ·  play code c1qhnyx4"
w = d.textlength(msg, font=strip)
d.text(((W - w) / 2, 616), msg, font=strip, fill=WHITE)

img.save(OUT)
print(f"wrote {OUT} {W}x{H}")
