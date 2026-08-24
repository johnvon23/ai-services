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
MUTED = (152, 160, 176)
HAIRLINE = (31, 37, 48)
CORAL = (255, 90, 72)

S = 3                       # supersample, downsampled at the end
W, H = 1200 * S, 630 * S
PAD = 84 * S
RULE_Y = H - PAD - 46 * S

FIELD_TOP = 296 * S
FIELD_BOT = 566 * S
ACCENT_FRAC = 0.44          # keeps the coral line clear of the footer text
LINES = 16
FADE_FROM, FADE_TO = 470 * S, RULE_Y - 6 * S


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


img = Image.new("RGB", (W, H), GROUND)
d = ImageDraw.Draw(img)


def trace(base, amp, phase, colour, width):
    pts = [(px, wave_y(base, amp, phase, px / W)) for px in range(0, W + 1, 4 * S)]
    d.line(pts, fill=colour, width=width, joint="curve")


# signal field, swelling around the accent line
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

# fade the field out before the rule so the credits sit on clean ground
fade = Image.new("L", (1, H), 0)
fd = ImageDraw.Draw(fade)
for y in range(H):
    t = (y - FADE_FROM) / (FADE_TO - FADE_FROM)
    fd.point((0, y), fill=max(0, min(255, int(t * 255))))
img = Image.composite(Image.new("RGB", (W, H), GROUND), img, fade.resize((W, H)))
d = ImageDraw.Draw(img)

y = PAD
tracked(d, (PAD, y), "AI SYSTEMS FOR MUSIC COMPANIES", mono(21), CORAL, 3.4)

y += 58 * S
name_font = grotesk(76, 700)
d.text((PAD, y), "Systems with Judgment", font=name_font, fill=INK)
d.text(
    (PAD + d.textlength("Systems with Judgment", font=name_font) + 4 * S, y),
    "_", font=name_font, fill=CORAL,
)

y += 108 * S
line_font = grotesk(38, 400)
d.text((PAD, y), "Grow the business.", font=line_font, fill=MUTED)
d.text(
    (PAD + d.textlength("Grow the business. ", font=line_font), y),
    "Not the admin burden.", font=grotesk(38, 700), fill=INK,
)

d.line([(PAD, RULE_Y), (W - PAD, RULE_Y)], fill=HAIRLINE, width=max(1, round(1.4 * S)))

foot = mono(20)
d.text((PAD, RULE_Y + 20 * S), "systemswithjudgment.com", font=foot, fill=MUTED)
credit = "John von Seggern & Tsotne Arbolishvili"
d.text(
    (W - PAD - d.textlength(credit, font=foot), RULE_Y + 20 * S),
    credit, font=foot, fill=MUTED,
)

img.resize((1200, 630), Image.LANCZOS).save(OUT, "PNG", optimize=True)
print("wrote", OUT.relative_to(ROOT), OUT.stat().st_size, "bytes")
