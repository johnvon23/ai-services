"""Render the favicon set from the decision-node mark.

Run from the repo root:  python3 scripts/make-favicons.py

Writes favicon.svg, favicon.ico (16, 32, 48) and apple-touch-icon.png (180)
to the repo root. The mark is drawn from the shapes below on a 64-unit grid,
so the SVG and the bitmaps always match. Needs Pillow.

The mark: grey boxes are the steps a system runs, the coral diamond is the
flowchart decision point where a person steps in.
"""
from pathlib import Path

from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parent.parent

# theme tokens, kept in step with _page.css
GROUND = "#0B0D12"
GREY = "#5C6472"
CORAL = "#FF5A48"

TILE_RADIUS = 14
LINE_WIDTH = 3.5
# (x, y, size) of each step box, radius 3
BOXES = [(4, 25, 14), (46, 8, 12), (46, 44, 12)]
# connector polylines: into the diamond, and the two branches out of it
LINES = [[(17, 32), (25, 32)], [(43, 32), (52, 32), (52, 21)], [(52, 32), (52, 43)]]
DIAMOND = [(34, 22), (44, 32), (34, 42), (24, 32)]


def svg(radius=TILE_RADIUS):
    lines = "".join(
        "M" + "L".join(f"{x} {y}" for x, y in pts) for pts in LINES
    )
    boxes = "".join(
        f'<rect x="{x}" y="{y}" width="{s}" height="{s}" rx="3" fill="{GREY}"/>'
        for x, y, s in BOXES
    )
    diamond = "M" + "L".join(f"{x} {y}" for x, y in DIAMOND) + "Z"
    return (
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64" '
        'role="img" aria-label="Systems with Judgment">\n'
        f'  <rect width="64" height="64" rx="{radius}" fill="{GROUND}"/>\n'
        f'  <path d="{lines}" fill="none" stroke="{GREY}" stroke-width="{LINE_WIDTH}" '
        'stroke-linecap="round" stroke-linejoin="round"/>\n'
        f"  {boxes}\n"
        f'  <path d="{diamond}" fill="{CORAL}"/>\n'
        "</svg>\n"
    )


def render(size, radius=TILE_RADIUS, mark_scale=1.0):
    """Draw the tile at 16x and downsample, so edges come out antialiased."""
    ss = 16
    big = size * ss
    u = big / 64                      # pixels per grid unit
    off = big * (1 - mark_scale) / 2  # centring offset when the mark shrinks
    k = u * mark_scale

    def p(x, y):
        return (off + x * k, off + y * k)

    img = Image.new("RGBA", (big, big), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    d.rounded_rectangle((0, 0, big - 1, big - 1), radius=radius * u, fill=GROUND)

    w = LINE_WIDTH * k
    for pts in LINES:
        pts = [p(x, y) for x, y in pts]
        d.line(pts, fill=GREY, width=round(w), joint="curve")
        for cx, cy in pts:  # round caps and joins
            d.ellipse((cx - w / 2, cy - w / 2, cx + w / 2, cy + w / 2), fill=GREY)
    for x, y, s in BOXES:
        d.rounded_rectangle((*p(x, y), *p(x + s, y + s)), radius=3 * k, fill=GREY)
    d.polygon([p(x, y) for x, y in DIAMOND], fill=CORAL)

    return img.resize((size, size), Image.LANCZOS)


def main():
    (ROOT / "favicon.svg").write_text(svg())

    icons = [render(s) for s in (16, 32, 48)]
    icons[-1].save(ROOT / "favicon.ico", sizes=[(16, 16), (32, 32), (48, 48)],
                   append_images=icons[:-1])

    # iOS rounds the corners itself, so the touch icon is a full square with
    # the mark pulled in from the edges
    render(180, radius=0, mark_scale=0.8).convert("RGB").save(
        ROOT / "apple-touch-icon.png")

    print("wrote favicon.svg, favicon.ico, apple-touch-icon.png")


if __name__ == "__main__":
    main()
