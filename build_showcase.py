from __future__ import annotations

import argparse
import html
import json
import shutil
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent
SOURCE_REPO = ROOT.parent / "Agent_info_flow"

SUBPAGES = {
    "agent-eval": {
        "builder": ROOT / "agent-eval" / "build_showcase.py",
        "sync": [
            (
                SOURCE_REPO / "website_showcase" / "build_showcase.py",
                ROOT / "agent-eval" / "build_showcase.py",
            ),
            (
                SOURCE_REPO / "website_showcase" / "context.json",
                ROOT / "agent-eval" / "context.json",
            ),
            (
                SOURCE_REPO / "website_showcase" / "first_page_cn.json",
                ROOT / "agent-eval" / "first_page_cn.json",
            ),
            (
                SOURCE_REPO / "website_showcase" / "first_page_en.json",
                ROOT / "agent-eval" / "first_page_en.json",
            ),
        ],
    },
    "agent-dev": {
        "builder": ROOT / "agent-dev" / "build_showcase.py",
        "sync": [
            (
                SOURCE_REPO / "dev" / "agent dev showcase" / "build_showcase.py",
                ROOT / "agent-dev" / "build_showcase.py",
            ),
            (
                SOURCE_REPO / "dev" / "agent dev showcase" / "context.json",
                ROOT / "agent-dev" / "context.json",
            ),
            (
                SOURCE_REPO / "dev" / "agent dev showcase" / "tokens.css",
                ROOT / "agent-dev" / "tokens.css",
            ),
        ],
    },
}


def load_context() -> dict:
    return json.loads((ROOT / "index.json").read_text(encoding="utf-8"))


def sync_sources() -> list[str]:
    copied: list[str] = []
    for page in SUBPAGES.values():
        for source, target in page["sync"]:
            if not source.exists():
                raise FileNotFoundError(f"Missing source: {source}")
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source, target)
            copied.append(f"{source} -> {target}")
    return copied


def run_subpage_builders() -> list[str]:
    built: list[str] = []
    for slug, page in SUBPAGES.items():
        builder = page["builder"]
        if not builder.exists():
            raise FileNotFoundError(f"Missing builder for {slug}: {builder}")
        subprocess.run(
            [sys.executable, str(builder)],
            check=True,
            cwd=builder.parent,
        )
        built.append(slug)
    return built


def build_cards(projects: list[dict]) -> str:
    cards: list[str] = []
    for project in projects:
        points = "".join(
            f"<li>{html.escape(point)}</li>" for point in project.get("points", [])
        )
        cards.append(
            f"""
            <article class="card">
              <div class="eyebrow">{html.escape(project['eyebrow'])}</div>
              <h2>{html.escape(project['title'])}</h2>
              <p>{html.escape(project['description'])}</p>
              <ul>{points}</ul>
              <a class="cta" href="{html.escape(project['href'])}">进入页面</a>
            </article>
            """.strip()
        )
    return "\n".join(cards)


def render_index(context: dict) -> str:
    stats = "\n".join(
        f"""
        <div class="stat">
          <div class="value">{html.escape(item['value'])}</div>
          <div class="label">{html.escape(item['label'])}</div>
        </div>
        """.strip()
        for item in context.get("highlights", [])
    )
    cards = build_cards(context.get("projects", []))
    site = context["site"]
    title = html.escape(site["title"])
    subtitle = html.escape(site["subtitle"])
    summary = html.escape(site["summary"])
    return f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>{title}</title>
  <style>
    :root {{
      --bg: #f4efe5;
      --surface: rgba(255, 252, 246, 0.9);
      --surface-strong: #fffdf8;
      --fg: #1f1b17;
      --muted: #6a6258;
      --line: rgba(31, 27, 23, 0.12);
      --accent: #b84720;
      --accent-dark: #8c3114;
      --shadow: 0 20px 40px rgba(31, 27, 23, 0.08);
      --radius: 24px;
      --font-sans: "IBM Plex Sans", "Segoe UI", sans-serif;
      --font-mono: "IBM Plex Mono", "SFMono-Regular", monospace;
    }}

    * {{ box-sizing: border-box; }}
    body {{
      margin: 0;
      font-family: var(--font-sans);
      color: var(--fg);
      background:
        radial-gradient(circle at top left, rgba(184, 71, 32, 0.14), transparent 34%),
        radial-gradient(circle at top right, rgba(30, 85, 120, 0.12), transparent 28%),
        linear-gradient(180deg, #f9f4ec 0%, var(--bg) 100%);
      min-height: 100vh;
    }}

    a {{ color: inherit; }}

    .shell {{
      max-width: 1120px;
      margin: 0 auto;
      padding: 56px 24px 72px;
    }}

    .hero {{
      padding: 36px;
      border: 1px solid var(--line);
      border-radius: 32px;
      background: linear-gradient(180deg, rgba(255,255,255,0.76), rgba(255,255,255,0.92));
      box-shadow: var(--shadow);
      backdrop-filter: blur(12px);
    }}

    .kicker {{
      display: inline-flex;
      align-items: center;
      gap: 10px;
      font-size: 13px;
      letter-spacing: 0.16em;
      text-transform: uppercase;
      color: var(--muted);
    }}

    .kicker::before {{
      content: "";
      width: 10px;
      height: 10px;
      border-radius: 999px;
      background: var(--accent);
      box-shadow: 0 0 0 6px rgba(184, 71, 32, 0.14);
    }}

    h1 {{
      margin: 18px 0 14px;
      font-size: clamp(38px, 7vw, 74px);
      line-height: 0.98;
      letter-spacing: -0.04em;
    }}

    .subtitle {{
      margin: 0;
      font-size: 18px;
      color: var(--muted);
    }}

    .summary {{
      max-width: 760px;
      margin-top: 20px;
      font-size: 17px;
      line-height: 1.7;
      color: #372f29;
    }}

    .stats {{
      display: grid;
      grid-template-columns: repeat(3, minmax(0, 1fr));
      gap: 16px;
      margin-top: 28px;
    }}

    .stat {{
      padding: 18px 20px;
      border-radius: 20px;
      border: 1px solid var(--line);
      background: rgba(255, 255, 255, 0.72);
    }}

    .stat .value {{
      font-size: 30px;
      font-weight: 700;
      letter-spacing: -0.04em;
    }}

    .stat .label {{
      margin-top: 6px;
      font-size: 13px;
      color: var(--muted);
      text-transform: uppercase;
      letter-spacing: 0.08em;
    }}

    .grid {{
      display: grid;
      grid-template-columns: repeat(2, minmax(0, 1fr));
      gap: 22px;
      margin-top: 28px;
    }}

    .card {{
      padding: 28px;
      border-radius: var(--radius);
      border: 1px solid var(--line);
      background: var(--surface-strong);
      box-shadow: var(--shadow);
    }}

    .card .eyebrow {{
      font-size: 13px;
      color: var(--muted);
      text-transform: uppercase;
      letter-spacing: 0.12em;
    }}

    .card h2 {{
      margin: 10px 0 12px;
      font-size: 30px;
      letter-spacing: -0.03em;
    }}

    .card p {{
      margin: 0;
      color: #433b34;
      line-height: 1.7;
    }}

    .card ul {{
      margin: 18px 0 0;
      padding-left: 18px;
      color: var(--muted);
      line-height: 1.7;
    }}

    .cta {{
      display: inline-flex;
      align-items: center;
      justify-content: center;
      margin-top: 22px;
      padding: 12px 18px;
      border-radius: 999px;
      background: var(--accent);
      color: #fff7f2;
      text-decoration: none;
      font-weight: 600;
    }}

    .cta:hover {{
      background: var(--accent-dark);
    }}

    footer {{
      margin-top: 26px;
      color: var(--muted);
      font-size: 14px;
    }}

    code {{
      font-family: var(--font-mono);
      font-size: 0.95em;
    }}

    @media (max-width: 800px) {{
      .shell {{
        padding: 24px 16px 40px;
      }}

      .hero {{
        padding: 24px;
      }}

      .stats,
      .grid {{
        grid-template-columns: 1fr;
      }}
    }}
  </style>
</head>
<body>
  <main class="shell">
    <section class="hero">
      <div class="kicker">面试作品集入口</div>
      <h1>{title}</h1>
      <p class="subtitle">{subtitle}</p>
      <p class="summary">{summary}</p>
      <div class="stats">{stats}</div>
    </section>
    <section class="grid">{cards}</section>
    <footer>
      根入口页由 <code>index.json</code> 和 <code>build_showcase.py</code> 生成；两个子页面的源码与构建脚本也已经收进当前仓库，运行一次顶层构建即可重建三个页面。
    </footer>
  </main>
</body>
</html>
"""


def build_landing_page() -> Path:
    context = load_context()
    html_output = render_index(context)
    output_path = ROOT / "index.html"
    output_path.write_text(html_output, encoding="utf-8")
    return output_path


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--sync-sources",
        action="store_true",
        help="Refresh subpage source files from the sibling Agent_info_flow workspace.",
    )
    parser.add_argument(
        "--skip-subpages",
        action="store_true",
        help="Only rebuild the landing page.",
    )
    args = parser.parse_args()

    if args.sync_sources:
        for item in sync_sources():
            print(f"synced {item}")

    if not args.skip_subpages:
        for slug in run_subpage_builders():
            print(f"built {slug}")

    output_path = build_landing_page()
    print(f"built {output_path}")


if __name__ == "__main__":
    main()
