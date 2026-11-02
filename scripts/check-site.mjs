import { access, readFile } from "node:fs/promises";

const requiredFiles = [
  "index.md",
  "secondbrain.md",
  "index.html",
  "press.html",
  "secondbrain.html",
  "404.html",
  "_booking.html",
  "_404.body.html",
  "_landing.body.html",
  "landing/music-tech.md",
  "music-tech.html",
  "sitemap.xml",
  "site-config.js",
  "vercel.json",
  "favicon.svg",
  "favicon.ico",
  "apple-touch-icon.png",
  "robots.txt",
  "assets/og-image.png",
  "assets/brain-icon.png",
  "assets/john-von.jpg",
  "assets/john-von-640.jpg",
  "assets/tsotne-photo-CQeDVvxh.jpg",
  "assets/tsotne-photo-640.jpg",
  "assets/logos/futureproof.png",
  "assets/logos/tunepal.png",
  "assets/logos/343-labs.png",
  "assets/logos/icon-collective.png",
  "assets/logos/icon-collective-mark.png",
  "assets/logos/native-instruments.svg"
];

for (const file of requiredFiles) {
  await access(file);
}

const html = await readFile("index.html", "utf8");
const markdown = await readFile("index.md", "utf8");
const press = await readFile("press.html", "utf8");
const secondbrain = await readFile("secondbrain.html", "utf8");
const notFound = await readFile("404.html", "utf8");
const landing = await readFile("music-tech.html", "utf8");
const booking = await readFile("_booking.html", "utf8");
const robots = await readFile("robots.txt", "utf8");
const sitemap = await readFile("sitemap.xml", "utf8");
const css = await readFile("_page.css", "utf8");
const configSource = await readFile("site-config.js", "utf8");
const vercelConfig = JSON.parse(await readFile("vercel.json", "utf8"));

const mainPages = [
  ["index.html", html],
  ["press.html", press],
  ["secondbrain.html", secondbrain],
  ["404.html", notFound]
];

const requiredCopy = [
  "Systems with Judgment",
  "AI systems for founders and small teams",
  "Free 30-minute session",
  "Grow the business.",
  "Not the busywork.",
  "Free opportunity map within 48 hours.",
  "Where the work usually gets stuck.",
  "Companies we’ve founded or worked at",
  "Bring us the messy version.",
  "The first two steps are free.",
  "Where we know the work best.",
  "How an engagement works.",
  "System we built",
  "Growth we led",
  "Program we ran",
  "Co-founder, CTO and CMO, TunePal",
  "More about John",
  "Customer data, contracts, and unreleased work stay private.",
  "What happens in the 30-minute session?",
  "Is the opportunity map free?",
  "Do you replace staff?",
  "FAQPage",
  "AI Systems for Founders and Small Teams",
  "my-cal-inline-30min",
  "https://app.cal.com/embed/embed.js",
  "john-von-seggern-czdmwr/30min",
  "data-book=\"header\"",
  "data-book=\"hero\"",
  "data-book=\"process\"",
  "data-book=\"cases\"",
  "data-book=\"calendar_tab\"",
  "href=\"/music-tech.html\"",
  "book_session_click",
  "scroll_depth",
  "calendar_viewed",
  "calendar_loaded",
  "booking_completed",
  "bookingSuccessfulV2"
];

if (!markdown.includes("<!-- copy:hero.heading -->")) {
  throw new Error("index.md is no longer the homepage copy source.");
}

const secondbrainMarkdown = await readFile("secondbrain.md", "utf8");
if (!secondbrainMarkdown.includes("<!-- copy:hero.heading -->")) {
  throw new Error("secondbrain.md is no longer the second brain copy source.");
}

for (const copy of requiredCopy) {
  if (!html.includes(copy)) {
    throw new Error(`Missing required page copy: ${copy}`);
  }
}

if (html.includes('class="logo-role"')) {
  throw new Error("The removed company-logo role tags are still present.");
}

if (configSource.includes("calendar.google.com") || configSource.includes("calendar.app.google")) {
  throw new Error("The retired Google Calendar booking configuration is still present.");
}

const forbiddenCopy = [
  "—", // em dash, banned in all copy
  "The Placeholder Agency",
  "Draft for review",
  "Book a free call",
  "Get started",
  "Request a demo",
  "Subtle Data",
  "Every school is different. The goal is the same.",
  "AI operations for education",
  "education companies",
  "Enrollment operations",
  "student communication",
  "Not the admin burden.",
  "AI systems for music companies",
  "royalty",
  "built systems for"
];

for (const copy of forbiddenCopy) {
  for (const [name, source] of mainPages) {
    if (source.includes(copy)) {
      throw new Error(`Draft or retired copy is still present in ${name}: ${copy}`);
    }
  }
}

for (const [name, source] of mainPages) {
  const h1Count = (source.match(/<h1(?:\s|>)/g) || []).length;
  if (h1Count !== 1) {
    throw new Error(`Expected one H1 in ${name}, found ${h1Count}`);
  }
}

if (!html.includes("<h1>AI systems for founders and small teams</h1>")) {
  throw new Error("Home H1 is no longer “AI systems for founders and small teams”.");
}

for (const [name, source] of mainPages) {
  if (!source.includes('href="/secondbrain"')) {
    throw new Error(`Footer link to /secondbrain is missing from ${name}`);
  }
}

if (!html.includes('href="/press"')) {
  throw new Error("The founder bio no longer links to the local press page.");
}

const requiredPressCopy = [
  "Where AI helps.",
  "LA Examiner",
  "CNET",
  "Cointelegraph",
  "my-cal-inline-30min"
];

for (const copy of requiredPressCopy) {
  if (!press.includes(copy)) {
    throw new Error(`Missing required press page copy: ${copy}`);
  }
}

const requiredSecondBrainCopy = [
  "Your company’s second brain.",
  "Explained through ours.",
  "A chatbot answers. A second brain works.",
  "What it does for a company.",
  "class=\"hero-brain\"",
  "Nova, from the inside.",
  "A day in Nova’s life.",
  "The rules that make it trustworthy.",
  "What Nova can’t do.",
  "How we’d build yours.",
  "my-cal-inline-30min",
  "\"@type\": \"Article\""
];

for (const copy of requiredSecondBrainCopy) {
  if (!secondbrain.includes(copy)) {
    throw new Error(`Missing required second brain page copy: ${copy}`);
  }
}

// The FAQ shown on the page and the FAQ in the structured data must match.
const faqStart = html.indexOf('id="faq"');
const faqSection = html.slice(faqStart, html.indexOf("</section>", faqStart));
const faqShown = (faqSection.match(/<details>/g) || []).length;
const faqData = (html.match(/"@type": "Question"/g) || []).length;
if (faqShown === 0 || faqShown !== faqData) {
  throw new Error(`The FAQ shows ${faqShown} questions but its structured data has ${faqData}; add or remove the <details> in _page.body.html to match index.md.`);
}

// Readability: no text under 13px, no spaced capitals, no blinking cursor.
for (const match of css.matchAll(/font-size:\s*([\d.]+)(rem|px)/g)) {
  const px = parseFloat(match[1]) * (match[2] === "rem" ? 16 : 1);
  if (px < 13) {
    throw new Error(`_page.css sets text smaller than 13px: ${match[0]}`);
  }
}
if (/text-transform:\s*uppercase/.test(css)) {
  throw new Error("_page.css sets spaced capitals (text-transform: uppercase); use sentence case.");
}
if (/blink/.test(css)) {
  throw new Error("_page.css has a blinking animation again.");
}

// One booking calendar: every page that books shows the same Cal.com event,
// from _booking.html, and the fallback link in site-config.js points at it.
const calLink = (booking.match(/calLink:\s*"([^"]+)"/) || [])[1];
if (!calLink) {
  throw new Error("_booking.html no longer names a Cal.com calLink.");
}
if (!configSource.includes(calLink)) {
  throw new Error(`site-config.js bookingUrl does not point at the embedded event ${calLink}.`);
}

const usecaseSlugs = [
  "record-labels", "publishers", "distributors", "venues-and-promoters",
  "artists-and-managers", "schools-and-education"
];
const landingSlugs = ["music-tech"];

const bookingPages = [
  ["index.html", html],
  ["press.html", press],
  ["secondbrain.html", secondbrain]
];
for (const slug of [...usecaseSlugs, ...landingSlugs]) {
  bookingPages.push([`${slug}.html`, await readFile(`${slug}.html`, "utf8")]);
}

for (const [name, source] of bookingPages) {
  if (!source.includes(`calLink: "${calLink}"`)) {
    throw new Error(`${name} does not carry the booking calendar from _booking.html.`);
  }
  for (const id of ["book", "my-cal-inline-30min", "booking-fallback"]) {
    const count = source.split(`id="${id}"`).length - 1;
    if (count !== 1) {
      throw new Error(`${name} should have exactly one #${id}, found ${count}.`);
    }
  }
  if (!source.includes('href="#book"')) {
    throw new Error(`${name} has no booking button that stays on the page.`);
  }
  if (source.includes("—")) {
    throw new Error(`${name} contains an em dash.`);
  }
  if (/\{\{(?:copy|attr|entity|include):/.test(source)) {
    throw new Error(`Unresolved placeholder in ${name}`);
  }
  const ids = [...source.matchAll(/\bid="([^"]+)"/g)].map(match => match[1]);
  if (ids.length !== new Set(ids).size) {
    throw new Error(`Duplicate IDs in ${name}`);
  }
  for (const [, target] of source.matchAll(/href="#([^"]+)"/g)) {
    if (!ids.includes(target)) throw new Error(`Broken anchor #${target} in ${name}`);
  }
}

for (const slug of [...usecaseSlugs, ...landingSlugs]) {
  const page = await readFile(`${slug}.html`, "utf8");
  if (!html.includes(`href="/${slug}.html"`)) throw new Error(`Missing homepage link: ${slug}`);
  if ((page.match(/<h1(?:\s|>)/g) || []).length !== 1) throw new Error(`Expected one H1: ${slug}`);
  if (!page.includes(`href="https://systemswithjudgment.com/${slug}.html"`)) throw new Error(`Missing canonical: ${slug}`);
  if (!page.includes(">Free 30-minute session<")) throw new Error(`Missing the booking button label: ${slug}`);
}

// The landing page repeats the referral one-pager's promise.
for (const copy of [
  "AI automation for music, audio tech and education teams",
  "within 48 hours",
  "Where we’d look first.",
  "Schools and course platforms",
  "The first two steps are free."
]) {
  if (!landing.includes(copy)) {
    throw new Error(`music-tech.html no longer carries the one-pager copy: ${copy}`);
  }
}

// Search: the sitemap lists every public page; the 404 page and the old
// design snapshot stay out of search results.
if (!robots.includes("Sitemap: https://systemswithjudgment.com/sitemap.xml")) {
  throw new Error("robots.txt no longer points at the sitemap.");
}
const sitemapPaths = ["/", "/secondbrain", "/press", ...[...usecaseSlugs, ...landingSlugs].map(slug => `/${slug}.html`)];
for (const path of sitemapPaths) {
  if (!sitemap.includes(`<loc>https://systemswithjudgment.com${path}</loc>`)) {
    throw new Error(`sitemap.xml is missing ${path}`);
  }
}
const oldDesign = await readFile("index-b.html", "utf8");
if (!oldDesign.includes('<meta name="robots" content="noindex">')) {
  throw new Error("index-b.html (the old design snapshot) must stay out of search results.");
}
if (!notFound.includes('<meta name="robots" content="noindex">')) {
  throw new Error("404.html must stay out of search results.");
}

if (vercelConfig.$schema !== "https://openapi.vercel.sh/vercel.json") {
  throw new Error("Vercel schema is missing or incorrect.");
}

if (/bookingUrl:\s*["']{2}/.test(configSource)) {
  console.warn("Warning: add the production scheduling URL to site-config.js before launch.");
}

if (/posthogKey:\s*["']{2}/.test(configSource)) {
  console.warn("Note: analytics is off until a PostHog project key is added to site-config.js.");
}

console.log("Site checks passed: homepage, press, second brain, 404, six industry pages, the music-tech landing page, sitemap.");
