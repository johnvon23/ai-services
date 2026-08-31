"""Render assets/og-image.png, the social share card, in the site's theme.

Run from the repo root:  python3 scripts/make-og-image.py

Needs Pillow. The two typefaces are downloaded from the Google Fonts repo into
.fontcache/ on first run, since the site itself only carries them as woff2 data
URIs inside _fonts.css, which Pillow cannot read.
"""
import math
import urllib.request
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent.parent
CACHE = ROOT / ".fontcache"
OUT = ROOT / "assets" / "og-image.png"
JOHN = ROOT / "assets" / "john-von-640.jpg"
TSOTNE = ROOT / "assets" / "tsotne-photo-640.jpg"

FONTS = {
    "SchibstedGrotesk[wght].ttf":
        "https://raw.githubusercontent.com/google/fonts/main/ofl/"
        "schibstedgrotesk/SchibstedGrotesk%5Bwght%5D.ttf",
    "FragmentMono-Regular.ttf":
        "https://raw.githubusercontent.com/google/fonts/main/ofl/"
        "fragmentmono/FragmentMono-Regular.ttf",
}

# theme tokens, kept in step with _page.css
GROUND = (11, 13, 18)
INK = (233, 236, 242)
MUTED = (197, 204, 214)
HAIRLINE = (31, 37, 48)
CORAL = (255, 90, 72)
PANEL = (16, 20, 28)

S = 3                       # supersample, downsampled at the end
W, H = 1200 * S, 630 * S
PAD = 72 * S
RULE_Y = H - PAD - 40 * S

FIELD_TOP = 220 * S
FIELD_BOT = 520 * S
ACCENT_FRAC = 0.38
LINES = 16
FADE_FROM, FADE_TO = 390 * S, RULE_Y - 90 * S


def font_path(name):
    CACHE.mkdir(exist_ok=True)
    path = CACHE / name
    if not path.exists():
        print("downloading", name)
        with urllib.request.urlopen(FONTS[name]) as r:
            path.write_bytes(r.read())
    return str(path)


def grotesk(px, weight=400):
    f = ImageFont.truetype(font_path("SchibstedGrotesk[wght].ttf"), px * S)
    try:
        f.set_variation_by_axes([weight])
    except Exception:
        pass
    return f


def mono(px):
    return ImageFont.truetype(font_path("FragmentMono-Regular.ttf"), px * S)


def tracked(draw, xy, text, font, fill, tracking):
    """Draw text with letter-spacing."""
    x, y = xy
    for ch in text:
        draw.text((x, y), ch, font=font, fill=fill)
        x += draw.textlength(ch, font=font) + tracking * S


def wave_y(base, amp, phase, n):
    """The same sine stack the live hero canvas draws."""
    return (
        base
        + math.sin(n * 9 + phase * 0.7) * amp * 0.55
        + math.sin(n * 23 + phase * 1.3) * amp * 0.3
        + math.sin(n * 4 + phase * 0.2) * amp * 0.4
    )


def circle_portrait(path, size, y_focus=0.5):
    src = Image.open(path).convert("RGB")
    w, h = src.size
    side = min(w, h)
    left = (w - side) // 2
    top = int((h - side) * y_focus)
    top = max(0, min(h - side, top))
    cropped = src.crop((left, top, left + side, top + side)).resize(
        (size, size), Image.LANCZOS
    )
    mask = Image.new("L", (size, size), 0)
    ImageDraw.Draw(mask).ellipse((1, 1, size - 2, size - 2), fill=255)
    out = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    out.paste(cropped, (0, 0))
    out.putalpha(mask)
    ring = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    ImageDraw.Draw(ring).ellipse(
        (1, 1, size - 2, size - 2), outline=HAIRLINE + (255,), width=max(2, S)
    )
    return Image.alpha_composite(out, ring)


img = Image.new("RGB", (W, H), GROUND)
d = ImageDraw.Draw(img)


def trace(base, amp, phase, colour, width):
    pts = [(px, wave_y(base, amp, phase, px / W)) for px in range(0, W + 1, 4 * S)]
    d.line(pts, fill=colour, width=width, joint="curve")


for i in range(LINES):
    frac = i / (LINES - 1)
    band = math.exp(-(((frac - ACCENT_FRAC) / 0.4) ** 2))
    alpha = 0.06 + 0.20 * band
    trace(
        FIELD_TOP + (FIELD_BOT - FIELD_TOP) * frac,
        (5 + 26 * band) * S,
        i,
        tuple(round(GROUND[c] + (MUTED[c] - GROUND[c]) * alpha) for c in range(3)),
        max(1, round(1.1 * S)),
    )

trace(
    FIELD_TOP + (FIELD_BOT - FIELD_TOP) * ACCENT_FRAC,
    30 * S,
    ACCENT_FRAC * LINES,
    CORAL,
    round(2.2 * S),
)

fade = Image.new("L", (1, H), 0)
fd = ImageDraw.Draw(fade)
for y in range(H):
    t = (y - FADE_FROM) / (FADE_TO - FADE_FROM)
    fd.point((0, y), fill=max(0, min(255, int(t * 255))))
img = Image.composite(Image.new("RGB", (W, H), GROUND), img, fade.resize((W, H)))
d = ImageDraw.Draw(img)

face_size = 92 * S
john = circle_portrait(JOHN, face_size, y_focus=0.38)
tsotne = circle_portrait(TSOTNE, face_size, y_focus=0.5)
overlap = int(face_size * 0.28)
faces = Image.new("RGBA", (face_size * 2 - overlap, face_size), (0, 0, 0, 0))
faces.alpha_composite(john, (0, 0))
faces.alpha_composite(tsotne, (face_size - overlap, 0))
img = img.convert("RGBA")
img.alpha_composite(faces, (PAD, PAD + 4 * S))
d = ImageDraw.Draw(img)

text_x = PAD + faces.width + 28 * S
tracked(d, (text_x, PAD + 4 * S), "AI AUTOMATION FOR MUSIC COMPANIES", mono(18), CORAL, 3.0)

name_font = grotesk(52, 700)
name_y = PAD + 36 * S
d.text((text_x, name_y), "Systems with Judgment", font=name_font, fill=INK)
d.text(
    (text_x + d.textlength("Systems with Judgment", font=name_font) + 4 * S, name_y),
    "_", font=name_font, fill=CORAL,
)

line_font = grotesk(34, 400)
line_y = PAD + 108 * S
d.text((PAD, line_y), "Grow the business.", font=line_font, fill=MUTED)
d.text(
    (PAD + d.textlength("Grow the business. ", font=line_font), line_y),
    "Not the busywork.", font=grotesk(34, 700), fill=INK,
)

chips = [
    ("30+", "overnight tasks, every night"),
    ("3x", "online enrollment at Icon"),
    ("15K to 60K", "followers in 12 months"),
]
chip_y = line_y + 64 * S
chip_h = 78 * S
gap = 14 * S
chip_w = (W - PAD * 2 - gap * 2) // 3
chip_font = grotesk(26, 700)
chip_label = mono(14)

for i, (value, label) in enumerate(chips):
    x0 = PAD + i * (chip_w + gap)
    x1 = x0 + chip_w
    d.rectangle([x0, chip_y, x1, chip_y + chip_h], fill=PANEL, outline=HAIRLINE, width=S)
    d.text((x0 + 18 * S, chip_y + 12 * S), value, font=chip_font, fill=INK)
    d.text((x0 + 18 * S, chip_y + 44 * S), label, font=chip_label, fill=MUTED)

d.line([(PAD, RULE_Y), (W - PAD, RULE_Y)], fill=HAIRLINE, width=max(1, round(1.4 * S)))

foot = mono(18)
d.text((PAD, RULE_Y + 16 * S), "systemswithjudgment.com", font=foot, fill=MUTED)
credit = "John von Seggern & Tsotne Arbolishvili"
d.text(
    (W - PAD - d.textlength(credit, font=foot), RULE_Y + 16 * S),
    credit, font=foot, fill=MUTED,
)

img.convert("RGB").resize((1200, 630), Image.LANCZOS).save(OUT, "PNG", optimize=True)
print("wrote", OUT.relative_to(ROOT), OUT.stat().st_size, "bytes")
