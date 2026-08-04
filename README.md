# AI Operations for Education

A focused, static landing page for John von Seggern and Tsotne Arbolishvili's AI operations work with independent education companies.

## Before the production launch

Add the full scheduling URL to `site-config.js`:

```js
window.SITE_CONFIG = {
  bookingUrl: "https://your-scheduling-page.example"
};
```

Both call-to-action buttons use this one value. While it is blank, the page shows a temporary contact message instead of sending visitors to a broken link.

## Preview and verify

Requirements: Node.js 20 or newer and Python 3.

```sh
npm run check
npm run dev
```

Then open `http://localhost:3000`.

## Push to GitHub

This directory is initialized on the `main` branch with an initial commit. Create an empty GitHub repository, then connect and push it:

```sh
git remote add origin https://github.com/YOUR-ACCOUNT/YOUR-REPOSITORY.git
git push -u origin main
```

## Deploy on Vercel

1. In Vercel, choose **Add New Project** and import the GitHub repository.
2. Leave the framework preset as **Other**.
3. Leave the build command and output directory blank; the repository is a static site.
4. Deploy.
5. Add the custom domain when ready.

`vercel.json` keeps URLs clean and adds basic browser security headers. No secrets or environment variables are required.
