import { access, readFile } from "node:fs/promises";

const requiredFiles = [
  "index.md",
  "index.html",
  "press.html",
  "site-config.js",
  "vercel.json",
  "favicon.svg",
  "robots.txt",
  "assets/og-image.png",
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
const configSource = await readFile("site-config.js", "utf8");
const vercelConfig = JSON.parse(await readFile("vercel.json", "utf8"));

const requiredCopy = [
  "Systems with Judgment",
  "AI systems for music companies",
  "Free 30-minute session",
  "Grow the business.",
  "Not the busywork.",
  "Where the work usually gets stuck.",
  "Companies we’ve founded, led, or built systems for",
  "Bring us the messy version.",
  "Built for your corner of the industry.",
  "How an engagement works.",
  "Unreleased music, artist contracts, and royalty data stay private.",
  "Do you replace staff?",
  "FAQPage",
  "AI Automation for Music Companies",
  "booking-embed",
  "data-book=\"header\"",
  "data-book=\"hero\"",
  "data-book=\"calendar_tab\"",
  "book_session_click",
  "scroll_depth"
];

if (!markdown.includes("<!-- copy:hero.heading -->")) {
  throw new Error("index.md is no longer the homepage copy source.");
}

for (const copy of requiredCopy) {
  if (!html.includes(copy)) {
    throw new Error(`Missing required page copy: ${copy}`);
  }
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
  "Not the admin burden."
];

for (const copy of forbiddenCopy) {
  for (const [name, source] of [["index.html", html], ["press.html", press]]) {
    if (source.includes(copy)) {
      throw new Error(`Draft or retired copy is still present in ${name}: ${copy}`);
    }
  }
}

for (const [name, source] of [["index.html", html], ["press.html", press]]) {
  const h1Count = (source.match(/<h1(?:\s|>)/g) || []).length;
  if (h1Count !== 1) {
    throw new Error(`Expected one H1 in ${name}, found ${h1Count}`);
  }
}

if (!html.includes("<h1>AI systems for music companies</h1>")) {
  throw new Error("Home H1 is no longer “AI systems for music companies”.");
}

if (!html.includes('href="/press"')) {
  throw new Error("The founder bio no longer links to the local press page.");
}

const requiredPressCopy = [
  "Where AI helps.",
  "LA Examiner",
  "CNET",
  "Cointelegraph",
  "data-book=\"press_cta\""
];

for (const copy of requiredPressCopy) {
  if (!press.includes(copy)) {
    throw new Error(`Missing required press page copy: ${copy}`);
  }
}

if (vercelConfig.$schema !== "https://openapi.vercel.sh/vercel.json") {
  throw new Error("Vercel schema is missing or incorrect.");
}

if (/bookingUrl:\s*["']{2}/.test(configSource)) {
  console.warn("Warning: add the production scheduling URL to site-config.js before launch.");
}

console.log("Site checks passed.");
