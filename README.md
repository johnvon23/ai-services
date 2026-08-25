# Systems with Judgment — AI Systems for Music Companies

A static landing page for John von Seggern and Tsotne Arbolishvili’s AI systems work with music companies.

## Local preview

Requires Node.js 20+ and Python 3.

```sh
npm run build
npm run check
npm run dev
```

Then open `http://localhost:3000`.

Edit `_page.body.html` (home), `_press.body.html` (press), `_page.css`, and
`_page.js`, then run `npm run build` to regenerate `index.html` and `press.html`.
Both pages share one inlined stylesheet and script, assembled by `_assemble.py`.
`vercel.json` sets `cleanUrls`, so `press.html` is served at `/press`.

The booking link lives in `site-config.js`. Both call-to-action buttons use this one value.

## Social share card

`assets/og-image.png` is generated, not hand-drawn. Regenerate it after any
brand change:

```sh
python3 scripts/make-og-image.py
```

It needs Pillow, and caches the two typefaces in `.fontcache/` on first run.
The colours at the top of the script mirror the tokens in `_page.css`.

## Previous design

`index-b.html` is a self-contained snapshot of the earlier cream-and-serif
page, kept for reference. It is not linked from the site.
