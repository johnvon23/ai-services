from pathlib import Path

fonts = Path("_fonts.css").read_text(encoding="utf8").strip()
css = Path("_page.css").read_text(encoding="utf8")
body = Path("_page.body.html").read_text(encoding="utf8").strip()
js = Path("_page.js").read_text(encoding="utf8")

jsonld = """{
  "@context": "https://schema.org",
  "@type": "ProfessionalService",
  "name": "Systems with Judgment",
  "description": "Systems with Judgment helps growing music companies reduce recurring work, connect disconnected systems, and find opportunities to save time or recover revenue.",
  "areaServed": "Music",
  "founder": [
    { "@type": "Person", "name": "John von Seggern", "url": "https://www.linkedin.com/in/johnvon/" },
    { "@type": "Person", "name": "Tsotne Arbolishvili", "url": "https://www.linkedin.com/in/tsotnetunes/" }
  ]
}"""

title = "Systems with Judgment | AI Systems for Music Companies"
description = (
    "Systems with Judgment helps growing music companies reduce recurring work, "
    "connect disconnected systems, and find opportunities to save time or recover revenue."
)

html = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>{title}</title>
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="description" content="{description}">
<link rel="canonical" href="/">
<meta property="og:type" content="website">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{description}">
<meta property="og:image" content="/assets/og-image.png">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{title}">
<meta name="twitter:description" content="{description}">
<meta name="twitter:image" content="/assets/og-image.png">
<meta name="theme-color" content="#F4F2ED">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<script type="application/ld+json">
{jsonld}
</script>
<script>
(function () {{
  try {{
    if (!window.matchMedia('(prefers-reduced-motion: reduce)').matches) {{
      document.documentElement.classList.add('wf-play');
    }}
  }} catch (e) {{}}
}})();
</script>
<style>
{fonts}

{css}
</style>
</head>
{body}
<script src="/site-config.js"></script>
<script>
{js}
</script>
</body>
</html>
"""

Path("index.html").write_text(html, encoding="utf8", newline="\n")
print("wrote index.html", Path("index.html").stat().st_size)
