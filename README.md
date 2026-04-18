# QR Pages Site

A small Python-powered static site generator for GitHub Pages.

Recommended repository name: `qr-pages-site`

This project is designed for QR-code-friendly landing pages:

- today: text-only pages
- later: optional embedded YouTube videos
- hosting: GitHub Pages
- authoring/building: Python

## How it works

You edit page content in `content/pages.json`.

Then run:

```powershell
python build.py
```

That generates static HTML files into `docs/`, which GitHub Pages can publish directly.

## Suggested GitHub Pages setup

1. Create a GitHub repository.
2. Upload this project.
3. In GitHub, open `Settings` -> `Pages`.
4. Set the source to `Deploy from a branch`.
5. Choose your main branch and the `/docs` folder.
6. Save.

Your site will be published at a URL like:

`https://YOUR-USERNAME.github.io/YOUR-REPO/`

## Git setup

Once Git is installed on your machine, run these commands inside this folder:

```powershell
git init
git add .
git commit -m "Initial GitHub Pages site"
```

Then create a GitHub repository named `qr-pages-site` and connect it:

```powershell
git branch -M main
git remote add origin https://github.com/YOUR-USERNAME/qr-pages-site.git
git push -u origin main
```

## QR code flow

Each generated page gets its own URL, for example:

- `https://YOUR-USERNAME.github.io/YOUR-REPO/`
- `https://YOUR-USERNAME.github.io/YOUR-REPO/welcome.html`
- `https://YOUR-USERNAME.github.io/YOUR-REPO/event-info.html`

You can turn any of those URLs into a QR code and print/share them.

## Content format

Each page in `content/pages.json` supports:

- `slug`: filename, like `welcome`
- `title`: page title
- `heading`: visible page heading
- `body`: list of text paragraphs
- `youtube_video_id`: optional YouTube video ID

If `slug` is `index`, the generator writes `docs/index.html`.

## Add a YouTube embed later

Set a `youtube_video_id` value on a page, for example:

```json
{
  "slug": "welcome",
  "title": "Welcome",
  "heading": "Welcome",
  "body": ["Hello from our QR page."],
  "youtube_video_id": "dQw4w9WgXcQ"
}
```

Then rebuild:

```powershell
python build.py
```
