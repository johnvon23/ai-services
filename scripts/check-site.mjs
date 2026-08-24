import { access, readFile } from "node:fs/promises";

const requiredFiles = [
  "index.html",
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
const configSource = await readFile("site-config.js", "utf8");
const vercelConfig = JSON.parse(await readFile("vercel.json", "utf8"));

const requiredCopy = [
  "Systems with Judgment",
  "AI systems for music companies",
  "Book a 30-minute working session",
  "Grow the business.",
  "Where the work usually gets stuck.",
  "Companies we've founded, led, or worked in",
  "Bring us the messy version.",
  "data-book=\"header\"",
  "data-book=\"hero\"",
  "data-book=\"final_cta\"",
  "book_session_click"
];

for (const copy of requiredCopy) {
  if (!html.includes(copy)) {
    throw new Error(`Missing required page copy: ${copy}`);
  }
}

const forbiddenCopy = [
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
  "student communication"
];

for (const copy of forbiddenCopy) {
  if (html.includes(copy)) {
    throw new Error(`Draft or retired copy is still present: ${copy}`);
  }
}

const h1Count = (html.match(/<h1(?:\s|>)/g) || []).length;
if (h1Count !== 1) {
  throw new Error(`Expected one H1, found ${h1Count}`);
}

if (vercelConfig.$schema !== "https://openapi.vercel.sh/vercel.json") {
  throw new Error("Vercel schema is missing or incorrect.");
}

if (/bookingUrl:\s*["']{2}/.test(configSource)) {
  console.warn("Warning: add the production scheduling URL to site-config.js before launch.");
}

console.log("Site checks passed.");
