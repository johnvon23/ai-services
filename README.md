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

Edit `index.md` to change any homepage text and `secondbrain.md` to change
the second brain page, then run `npm run build` to regenerate `index.html` and
`secondbrain.html`. Keep the `copy:` comments in place; the paragraph below each
comment is the editable value. Markdown emphasis such as `*this*` is supported.

For layout or behavior changes, edit `_page.body.html` (homepage template),
`_secondbrain.body.html` (second brain template), `_page.css`, or `_page.js`.
The press page is hand-written HTML in `_press.body.html`. Run `npm run build`
after any of these changes. All three pages share one inlined stylesheet and
script, assembled by `_assemble.py`. `npm run check` confirms the generated HTML
is current and runs the copy checks.

## Deploys

The live site is **GitHub Pages**, serving the `main` branch as committed
(`CNAME` points `systemswithjudgment.com` at it). Pages are served as flat
files, so `press.html` answers at `/press` and `secondbrain.html` at
`/secondbrain`. `vercel.json` is kept for a possible Vercel move but is not what
serves the site today.

Every push to `main` runs `.github/workflows/build-pages.yml`, which rebuilds
the three pages from the Markdown copy, runs the checks, and commits the
rebuilt HTML back to `main` if it differs. So editing `index.md` or
`secondbrain.md` on GitHub and committing is enough to deploy a copy change;
running `npm run build` locally first just makes the bot commit a no-op.

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
