from __future__ import annotations

import json
from html import escape
from pathlib import Path


ROOT = Path(__file__).parent
CONTENT_FILE = ROOT / "content" / "pages.json"
OUTPUT_DIR = ROOT / "docs"


def build_navigation(pages: list[dict[str, object]]) -> str:
    links: list[str] = []
    for page in pages:
        slug = str(page["slug"]).strip()
        if slug == "index":
            continue

        href = f"{escape(slug)}.html"
        label = escape(str(page["title"]))
        links.append(f'          <li><a href="{href}">{label}</a></li>')

    if not links:
        return ""

    joined_links = "\n".join(links)
    return f"""
      <section class="nav-block" aria-labelledby="pages-title">
        <h2 id="pages-title">Pages</h2>
        <ul class="page-list">
{joined_links}
        </ul>
      </section>"""


def render_page(page: dict[str, object], navigation_html: str) -> str:
    title = escape(str(page["title"]))
    heading = escape(str(page["heading"]))
    paragraphs = page.get("body", [])
    youtube_video_id = str(page.get("youtube_video_id", "") or "").strip()

    body_html = "\n".join(
        f"        <p>{escape(str(paragraph))}</p>" for paragraph in paragraphs
    )

    video_html = ""
    if youtube_video_id:
        embed_url = f"https://www.youtube.com/embed/{escape(youtube_video_id)}"
        video_html = f"""
      <section class="video-block" aria-labelledby="video-title">
        <h2 id="video-title">Video</h2>
        <div class="video-frame">
          <iframe
            src="{embed_url}"
            title="Embedded YouTube video"
            loading="lazy"
            allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share"
            allowfullscreen
          ></iframe>
        </div>
      </section>"""

    return f"""<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>{title}</title>
    <style>
      :root {{
        --page-bg: #f5f1e8;
        --card-bg: #fffdf8;
        --text: #1f1b16;
        --muted: #5c5147;
        --accent: #a33b20;
        --border: #dccfbe;
      }}

      * {{
        box-sizing: border-box;
      }}

      body {{
        margin: 0;
        font-family: Georgia, "Times New Roman", serif;
        background:
          radial-gradient(circle at top right, rgba(163, 59, 32, 0.08), transparent 30%),
          linear-gradient(180deg, #f8f4ec 0%, var(--page-bg) 100%);
        color: var(--text);
      }}

      .shell {{
        min-height: 100vh;
        display: grid;
        place-items: center;
        padding: 24px;
      }}

      .card {{
        width: min(720px, 100%);
        background: var(--card-bg);
        border: 1px solid var(--border);
        border-radius: 20px;
        padding: 32px 24px;
        box-shadow: 0 16px 40px rgba(31, 27, 22, 0.08);
      }}

      h1 {{
        margin-top: 0;
        margin-bottom: 16px;
        font-size: clamp(2rem, 6vw, 3rem);
        line-height: 1.05;
      }}

      p {{
        font-size: 1.1rem;
        line-height: 1.7;
        color: var(--muted);
      }}

      .home-link {{
        display: inline-block;
        margin-top: 12px;
        color: var(--accent);
        text-decoration: none;
        font-weight: bold;
      }}

      .nav-block {{
        margin-top: 28px;
        padding-top: 20px;
        border-top: 1px solid var(--border);
      }}

      .page-list {{
        margin: 0;
        padding-left: 20px;
      }}

      .page-list a {{
        color: var(--accent);
      }}

      .video-block {{
        margin-top: 32px;
      }}

      .video-block h2 {{
        margin-bottom: 12px;
      }}

      .video-frame {{
        position: relative;
        width: 100%;
        padding-top: 56.25%;
        overflow: hidden;
        border-radius: 16px;
        background: #000;
      }}

      .video-frame iframe {{
        position: absolute;
        inset: 0;
        width: 100%;
        height: 100%;
        border: 0;
      }}
    </style>
  </head>
  <body>
    <main class="shell">
      <article class="card">
        <h1>{heading}</h1>
{body_html}
{navigation_html}
        <a class="home-link" href="./index.html">Back to home</a>{video_html}
      </article>
    </main>
  </body>
</html>
"""


def output_path_for_slug(slug: str) -> Path:
    filename = "index.html" if slug == "index" else f"{slug}.html"
    return OUTPUT_DIR / filename


def main() -> None:
    pages = json.loads(CONTENT_FILE.read_text(encoding="utf-8"))
    OUTPUT_DIR.mkdir(exist_ok=True)
    navigation_html = build_navigation(pages)

    for page in pages:
        slug = str(page["slug"]).strip()
        if not slug:
            raise ValueError("Each page must include a non-empty slug.")

        page_navigation_html = navigation_html if slug == "index" else ""
        output_path = output_path_for_slug(slug)
        html = render_page(page, page_navigation_html)
        output_path.write_text(html, encoding="utf-8")
        print(f"Generated {output_path.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
