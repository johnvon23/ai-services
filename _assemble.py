from pathlib import Path
import json

fonts = Path("_fonts.css").read_text(encoding="utf8").strip()
css = Path("_page.css").read_text(encoding="utf8")
js = Path("_page.js").read_text(encoding="utf8")

site_url = "https://systemswithjudgment.com"

jsonld = json.dumps(
    {
        "@context": "https://schema.org",
        "@graph": [
            {
                "@type": ["Organization", "ProfessionalService"],
                "@id": f"{site_url}/#org",
                "name": "Systems with Judgment",
                "url": f"{site_url}/",
                "description": (
                    "AI automation for music companies. We automate royalty statements, "
                    "release checklists, booking inquiries, and reporting inside the tools "
                    "you already use."
                ),
                "areaServed": "Music",
                "founder": [
                    {"@id": f"{site_url}/#john"},
                    {"@id": f"{site_url}/#tsotne"},
                ],
            },
            {
                "@type": "Person",
                "@id": f"{site_url}/#john",
                "name": "John von Seggern",
                "url": "https://www.linkedin.com/in/johnvon/",
                "sameAs": ["https://www.linkedin.com/in/johnvon/"],
                "jobTitle": "Founder",
                "worksFor": {"@id": f"{site_url}/#org"},
            },
            {
                "@type": "Person",
                "@id": f"{site_url}/#tsotne",
                "name": "Tsotne Arbolishvili",
                "url": "https://www.linkedin.com/in/tsotnetunes/",
                "sameAs": ["https://www.linkedin.com/in/tsotnetunes/"],
                "jobTitle": "Founder",
                "worksFor": {"@id": f"{site_url}/#org"},
            },
            {
                "@type": "FAQPage",
                "@id": f"{site_url}/#faq",
                "mainEntity": [
                    {
                        "@type": "Question",
                        "name": "Do you replace staff?",
                        "acceptedAnswer": {
                            "@type": "Answer",
                            "text": "No. Your team keeps judgment, money, and artist communication.",
                        },
                    },
                    {
                        "@type": "Question",
                        "name": "What tools do you work with?",
                        "acceptedAnswer": {
                            "@type": "Answer",
                            "text": (
                                "CRMs, email, spreadsheets, royalty portals, and project tools. "
                                "We build inside the stack you already use."
                            ),
                        },
                    },
                    {
                        "@type": "Question",
                        "name": "How long until something is live?",
                        "acceptedAnswer": {
                            "@type": "Answer",
                            "text": "A pilot is typically live in 2 to 4 weeks.",
                        },
                    },
                    {
                        "@type": "Question",
                        "name": "What does it cost?",
                        "acceptedAnswer": {
                            "@type": "Answer",
                            "text": (
                                "The working session is free. Pilot pricing is quoted after "
                                "the opportunity map, once we know the workflow."
                            ),
                        },
                    },
                    {
                        "@type": "Question",
                        "name": "What about our unreleased music and contracts?",
                        "acceptedAnswer": {
                            "@type": "Answer",
                            "text": (
                                "We are happy to sign an NDA before the first call. Unreleased "
                                "music, artist contracts, and royalty data stay in your accounts."
                            ),
                        },
                    },
                    {
                        "@type": "Question",
                        "name": "Do we need anyone technical on our side?",
                        "acceptedAnswer": {
                            "@type": "Answer",
                            "text": "No.",
                        },
                    },
                ],
            },
        ],
    },
    indent=2,
    ensure_ascii=False,
)

press_jsonld = json.dumps(
    {
        "@context": "https://schema.org",
        "@type": "CollectionPage",
        "name": "Press and interviews",
        "url": f"{site_url}/press",
        "about": {
            "@type": "Person",
            "name": "John von Seggern",
            "url": "https://www.linkedin.com/in/johnvon/",
            "sameAs": ["https://www.linkedin.com/in/johnvon/"],
        },
        "isPartOf": {
            "@type": "WebSite",
            "name": "Systems with Judgment",
            "url": f"{site_url}/",
        },
    },
    indent=2,
    ensure_ascii=False,
)

# Social scrapers need absolute URLs; several reject relative ones outright.
# Bump when the card art changes, so platforms refetch instead of serving
# the version they already cached.
og_image = f"{site_url}/assets/og-image.png?v=3"
og_image_alt = (
    "John von Seggern and Tsotne Arbolishvili. AI automation for music companies. "
    "30+ overnight tasks, 3x Icon enrollment, 15K to 60K followers."
)


def render(title, description, path, body_file, out_file, structured_data):
    body = Path(body_file).read_text(encoding="utf8").strip()
    html = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>{title}</title>
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="description" content="{description}">
<link rel="canonical" href="{site_url}{path}">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Systems with Judgment">
<meta property="og:url" content="{site_url}{path}">
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
{structured_data}
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
    Path(out_file).write_text(html, encoding="utf8", newline="\n")
    print("wrote", out_file, Path(out_file).stat().st_size)


render(
    title="AI Automation for Music Companies | Systems with Judgment",
    description=(
        "AI automation for music companies. We automate royalty statements, release "
        "checklists, booking inquiries, and reporting inside the tools you already use. "
        "Never the songwriting."
    ),
    path="/",
    body_file="_page.body.html",
    out_file="index.html",
    structured_data=jsonld,
)

render(
    title="Press and Interviews | John von Seggern | Systems with Judgment",
    description=(
        "Selected press, interviews, and podcasts with John von Seggern on where AI "
        "genuinely helps, where it oversells itself, and what still needs a person in the loop."
    ),
    path="/press",
    body_file="_press.body.html",
    out_file="press.html",
    structured_data=press_jsonld,
)
