from html import escape
from pathlib import Path
import json
import re
import sys


SITE_URL = "https://systemswithjudgment.com"
COPY_MARKER = re.compile(r"^<!--\s*copy:([a-z0-9_.-]+)\s*-->$")
COPY_PLACEHOLDER = re.compile(r"\{\{(copy|attr|entity):([a-z0-9_.-]+)\}\}")
EMPHASIS = re.compile(r"(?<!\*)\*([^*\n]+)\*(?!\*)")


class HomepageCopy:
    def __init__(self, values):
        self.values = values
        self.used = set()

    def raw(self, key):
        try:
            value = self.values[key]
        except KeyError as error:
            raise ValueError(f"Missing copy value in index.md: {key}") from error
        self.used.add(key)
        return value

    def inline_html(self, key):
        value = escape(self.raw(key))
        return EMPHASIS.sub(r"<em>\1</em>", value)

    def attribute(self, key):
        return escape(self.raw(key), quote=True)

    def entity(self, key):
        return "".join(
            f"&#{ord(character)};"
            if ord(character) > 127
            else escape(character, quote=True)
            for character in self.raw(key)
        )

    def assert_all_used(self):
        unused = sorted(set(self.values) - self.used)
        if unused:
            raise ValueError(
                "Copy values in index.md are not used by the homepage build: "
                + ", ".join(unused)
            )


def read_homepage_copy(path="index.md"):
    lines = Path(path).read_text(encoding="utf8").splitlines()
    values = {}

    for line_number, line in enumerate(lines):
        match = COPY_MARKER.fullmatch(line.strip())
        if not match:
            continue

        key = match.group(1)
        if key in values:
            raise ValueError(f"Duplicate copy key in {path}: {key}")

        value_lines = []
        for candidate in lines[line_number + 1 :]:
            if not candidate.strip():
                break
            value_lines.append(candidate.strip())

        if not value_lines:
            raise ValueError(
                f"Copy key {key} must be followed immediately by a paragraph"
            )
        values[key] = " ".join(value_lines)

    if not values:
        raise ValueError(f"No copy values found in {path}")

    return HomepageCopy(values)


def fill_homepage_template(copy):
    template = Path("_page.body.html").read_text(encoding="utf8").strip()

    def replace(match):
        mode, key = match.groups()
        if mode == "attr":
            return copy.attribute(key)
        if mode == "entity":
            return copy.entity(key)
        return copy.inline_html(key)

    body = COPY_PLACEHOLDER.sub(replace, template)
    if any(token in body for token in ("{{copy:", "{{attr:", "{{entity:")):
        raise ValueError("Unresolved copy placeholder in _page.body.html")
    return body


def build_homepage_jsonld(copy):
    questions = []
    for number in range(1, 7):
        questions.append(
            {
                "@type": "Question",
                "name": copy.raw(f"faq.question_{number}"),
                "acceptedAnswer": {
                    "@type": "Answer",
                    "text": copy.raw(f"faq.answer_{number}"),
                },
            }
        )

    return json.dumps(
        {
            "@context": "https://schema.org",
            "@graph": [
                {
                    "@type": ["Organization", "ProfessionalService"],
                    "@id": f"{SITE_URL}/#org",
                    "name": copy.raw("organization.name"),
                    "url": f"{SITE_URL}/",
                    "description": copy.raw("organization.description"),
                    "areaServed": "Music",
                    "founder": [
                        {"@id": f"{SITE_URL}/#john"},
                        {"@id": f"{SITE_URL}/#tsotne"},
                    ],
                },
                {
                    "@type": "Person",
                    "@id": f"{SITE_URL}/#john",
                    "name": copy.raw("founders.john.name"),
                    "url": "https://www.linkedin.com/in/johnvon/",
                    "sameAs": ["https://www.linkedin.com/in/johnvon/"],
                    "jobTitle": copy.raw("schema.founder_job_title"),
                    "worksFor": {"@id": f"{SITE_URL}/#org"},
                },
                {
                    "@type": "Person",
                    "@id": f"{SITE_URL}/#tsotne",
                    "name": copy.raw("founders.tsotne.name"),
                    "url": "https://www.linkedin.com/in/tsotnetunes/",
                    "sameAs": ["https://www.linkedin.com/in/tsotnetunes/"],
                    "jobTitle": copy.raw("schema.founder_job_title"),
                    "worksFor": {"@id": f"{SITE_URL}/#org"},
                },
                {
                    "@type": "FAQPage",
                    "@id": f"{SITE_URL}/#faq",
                    "mainEntity": questions,
                },
            ],
        },
        indent=2,
        ensure_ascii=False,
    ).replace("</", "<\\/")


def build_press_jsonld():
    return json.dumps(
        {
            "@context": "https://schema.org",
            "@type": "CollectionPage",
            "name": "Press and interviews",
            "url": f"{SITE_URL}/press",
            "about": {
                "@type": "Person",
                "name": "John von Seggern",
                "url": "https://www.linkedin.com/in/johnvon/",
                "sameAs": ["https://www.linkedin.com/in/johnvon/"],
            },
            "isPartOf": {
                "@type": "WebSite",
                "name": "Systems with Judgment",
                "url": f"{SITE_URL}/",
            },
        },
        indent=2,
        ensure_ascii=False,
    )


def render_html(
    *, title, description, path, body, structured_data, site_name, og_image_alt
):
    fonts = Path("_fonts.css").read_text(encoding="utf8").strip()
    css = Path("_page.css").read_text(encoding="utf8")
    js = Path("_page.js").read_text(encoding="utf8")

    # Social scrapers need absolute URLs. The query string is bumped when the
    # card art changes so platforms fetch the new version.
    og_image = f"{SITE_URL}/assets/og-image.png?v=3"

    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>{escape(title)}</title>
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="description" content="{escape(description, quote=True)}">
<link rel="canonical" href="{SITE_URL}{path}">
<meta property="og:type" content="website">
<meta property="og:site_name" content="{escape(site_name, quote=True)}">
<meta property="og:url" content="{SITE_URL}{path}">
<meta property="og:title" content="{escape(title, quote=True)}">
<meta property="og:description" content="{escape(description, quote=True)}">
<meta property="og:image" content="{og_image}">
<meta property="og:image:type" content="image/png">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="{escape(og_image_alt, quote=True)}">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{escape(title, quote=True)}">
<meta name="twitter:description" content="{escape(description, quote=True)}">
<meta name="twitter:image" content="{og_image}">
<meta name="twitter:image:alt" content="{escape(og_image_alt, quote=True)}">
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


def write_or_check(path, html, check_only):
    output = Path(path)
    if check_only:
        if not output.exists() or output.read_text(encoding="utf8") != html:
            raise SystemExit(
                f"{path} is out of date. Run `npm run build` and commit the result."
            )
        return

    output.write_text(html, encoding="utf8", newline="\n")
    print("wrote", path, output.stat().st_size)


def main():
    unknown_args = [arg for arg in sys.argv[1:] if arg != "--check"]
    if unknown_args:
        raise SystemExit(f"Unknown argument: {unknown_args[0]}")
    check_only = "--check" in sys.argv[1:]

    copy = read_homepage_copy()
    home_body = fill_homepage_template(copy)
    home_jsonld = build_homepage_jsonld(copy)
    home_html = render_html(
        title=copy.raw("page.title"),
        description=copy.raw("page.description"),
        path="/",
        body=home_body,
        structured_data=home_jsonld,
        site_name=copy.raw("organization.name"),
        og_image_alt=copy.raw("page.share_image_alt"),
    )
    copy.assert_all_used()

    press_title = "Press and Interviews | John von Seggern | Systems with Judgment"
    press_description = (
        "Selected press, interviews, and podcasts with John von Seggern on where AI "
        "genuinely helps, where it oversells itself, and what still needs a person in the loop."
    )
    press_body = Path("_press.body.html").read_text(encoding="utf8").strip()
    press_html = render_html(
        title=press_title,
        description=press_description,
        path="/press",
        body=press_body,
        structured_data=build_press_jsonld(),
        site_name="Systems with Judgment",
        og_image_alt=(
            "John von Seggern and Tsotne Arbolishvili. AI automation for music companies. "
            "30+ overnight tasks, 3x Icon enrollment, 15K to 60K followers."
        ),
    )

    write_or_check("index.html", home_html, check_only)
    write_or_check("press.html", press_html, check_only)
    if check_only:
        print("Built pages are up to date.")


if __name__ == "__main__":
    main()
