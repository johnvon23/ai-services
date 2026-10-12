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
The press page is hand-written HTML in `_press.body.html`, and the 404 page in
`_404.body.html`. Run `npm run build` after any of these changes. All pages share
one inlined stylesheet and script, assembled by `_assemble.py`. A template can
pull in a shared fragment with `{{include:_file.html}}`. `npm run check` confirms
the generated HTML is current and runs the copy checks.

## Deploys

The live site is **GitHub Pages**, serving the `main` branch as committed
(`CNAME` points `systemswithjudgment.com` at it). Pages are served as flat
files, so `press.html` answers at `/press` and `secondbrain.html` at
`/secondbrain`. `vercel.json` is kept for a possible Vercel move but is not what
serves the site today.

Every push to `main` runs `.github/workflows/build-pages.yml`, which rebuilds
the pages (including `404.html`, which GitHub Pages shows for any missing
address) from the Markdown copy, runs the checks, and commits the rebuilt HTML
back to `main` if it differs. So editing `index.md` or
`secondbrain.md` on GitHub and committing is enough to deploy a copy change;
running `npm run build` locally first just makes the bot commit a no-op.

## Booking

The Cal.com calendar sits at the end of the homepage, /secondbrain and /press
(`#book`). Its embed code lives once, in `_booking.html`, exactly as Cal.com
supplies it, together with the "Open the calendar in a new tab" link and its
label. To change the event, paste Cal.com's new embed code there and update
`bookingUrl` in `site-config.js`, which that link uses. The site checks fail if
the two disagree.

## Analytics

Every button click (`book_session_click`, with its placement), scroll depth,
the calendar scrolled into view (`calendar_viewed`), the calendar drawn by
Cal.com (`calendar_loaded`), a completed booking (`booking_completed`) and a
calendar that fails to load (`calendar_failed`) are pushed to
`window.dataLayer`. They also go to PostHog once `posthogKey` in
`site-config.js` holds a project key; while it is empty, no analytics script
loads. `posthogPersistence: "memory"` sets no cookies; `"localStorage+cookie"`
recognises returning visitors but may need a consent banner for EU visitors.

## Search

`sitemap.xml` lists the three public pages and `robots.txt` points to it. The
old design snapshot `index-b.html` carries a `noindex` tag so it stays out of
search results.

## Site checks

`npm run check` requires a few exact strings: the H1, the button label "Free
30-minute session", several section headings and the NDA sentence. Rewording
one of them on GitHub makes the deploy workflow fail, so change
`scripts/check-site.mjs` in the same commit.

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
