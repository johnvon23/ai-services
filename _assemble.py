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

# Social scrapers need absolute URLs; several reject relative ones outright.
site_url = "https://systemswithjudgment.com"
# Bump when the card art changes, so platforms refetch instead of serving
# the version they already cached.
og_image = f"{site_url}/assets/og-image.png?v=2"
og_image_alt = (
    "Systems with Judgment. AI systems for music companies. "
    "Grow the business, not the admin burden."
)

html = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>{title}</title>
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="description" content="{description}">
<link rel="canonical" href="{site_url}/">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Systems with Judgment">
<meta property="og:url" content="{site_url}/">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{description}">
<meta property="og:image" content="{og_image}">
<meta property="og:image:type" content="image/png">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="{og_image_alt}">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{title}">
<meta name="twitter:description" content="{description}">
<meta name="twitter:image" content="{og_image}">
<meta name="twitter:image:alt" content="{og_image_alt}">
<meta name="theme-color" content="#0B0D12">
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
