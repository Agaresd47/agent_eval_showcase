from __future__ import annotations

import html
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent
CONTEXT_PATH = ROOT / "context.json"
OUTPUT_PATH = ROOT / "index.html"


STYLE = """
  body {
    font-family: var(--font-sans);
    background: var(--color-bg);
    color: var(--color-fg-1);
    line-height: var(--leading-normal);
  }
  a { color: var(--color-accent); text-decoration: none; }
  a:hover { color: var(--color-accent-hover); }
  code {
    font-family: var(--font-mono);
    font-size: 12px;
    background: var(--color-surface-2);
    padding: 1px 4px;
    border-radius: 3px;
    color: var(--color-fg-1);
  }
  .wrap { max-width: 1120px; margin: 0 auto; padding: 0 var(--space-6); }
  .topbar {
    height: var(--nav-height);
    border-bottom: 1px solid var(--color-border);
    background: var(--color-surface);
    display: flex; align-items: center;
    position: sticky; top: 0; z-index: 50;
  }
  .topbar .wrap { width: 100%; display: flex; align-items: center; justify-content: space-between; gap: var(--space-6); }
  .topbar .brand { display: flex; align-items: center; gap: var(--space-3); font-weight: var(--font-medium); }
  .topbar .brand .mark {
    width: 22px; height: 22px; border-radius: var(--radius-sm);
    background: var(--color-accent); position: relative;
  }
  .topbar .brand .mark::after {
    content: ""; position: absolute; inset: 4px;
    border: 1.5px solid #fff; border-radius: 2px;
    border-bottom-color: transparent; border-right-color: transparent;
    transform: rotate(45deg);
  }
  .topbar nav { display: flex; gap: var(--space-5); font-size: var(--text-sm); }
  .topbar nav a { color: var(--color-fg-2); padding: 6px 0; }
  .topbar nav a:hover { color: var(--color-fg-1); }
  .topbar .meta { font-family: var(--font-mono); font-size: var(--text-xs); color: var(--color-fg-3); }
  .hero {
    padding: var(--space-12) 0 var(--space-10);
    border-bottom: 1px solid var(--color-border);
    background:
      radial-gradient(circle at 88% 10%, var(--color-accent-subtle) 0, transparent 45%),
      var(--color-bg);
  }
  .hero .eyebrow {
    font-family: var(--font-mono); font-size: var(--text-xs);
    color: var(--color-accent); letter-spacing: var(--tracking-wide);
    margin-bottom: var(--space-3);
    display: flex; align-items: center; gap: var(--space-2);
  }
  .hero .eyebrow .dot {
    width: 6px; height: 6px; border-radius: 999px;
    background: var(--color-accent);
    box-shadow: 0 0 0 4px var(--color-accent-subtle);
  }
  .hero h1 {
    font-size: 44px; line-height: 1.05;
    letter-spacing: -0.02em; font-weight: var(--font-semibold);
    max-width: 820px; margin-bottom: var(--space-4);
  }
  .hero h1 .accent { color: var(--color-accent); }
  .hero .lede {
    max-width: 760px;
    font-size: var(--text-md);
    line-height: var(--leading-relaxed);
    color: var(--color-fg-2);
    margin-bottom: var(--space-6);
  }
  .hero .lede strong { color: var(--color-fg-1); font-weight: var(--font-medium); }
  .stat-strip {
    display: grid;
    grid-template-columns: repeat(4, minmax(0, 1fr));
    gap: var(--space-2);
    border-top: 1px solid var(--color-border);
    padding-top: var(--space-5);
  }
  .stat .num {
    font-family: var(--font-mono); font-size: 24px;
    font-weight: var(--font-medium); color: var(--color-fg-1);
    letter-spacing: -0.01em;
  }
  .stat .label { margin-top: 2px; color: var(--color-fg-3); font-size: var(--text-xs); }
  section.block {
    padding: var(--space-12) 0;
    border-bottom: 1px solid var(--color-border);
  }
  section.block.tight { padding: var(--space-8) 0; }
  .section-head {
    display: grid;
    grid-template-columns: 180px 1fr;
    gap: var(--space-6);
    align-items: baseline;
    margin-bottom: var(--space-6);
  }
  .section-head .kicker {
    font-family: var(--font-mono); font-size: var(--text-xs);
    color: var(--color-fg-3); letter-spacing: var(--tracking-wide);
  }
  .section-head h2 {
    font-size: 26px; letter-spacing: -0.015em; margin-bottom: var(--space-2);
  }
  .section-head .sub {
    color: var(--color-fg-2); font-size: var(--text-base);
    line-height: var(--leading-relaxed); max-width: 760px;
  }
  .problem-grid {
    display: grid; grid-template-columns: repeat(3, 1fr);
    gap: var(--space-3);
  }
  .problem-card {
    background: var(--color-surface);
    border: 1px solid var(--color-border);
    border-radius: var(--radius-md);
    padding: var(--space-5);
  }
  .problem-card.is { border-color: var(--color-accent-muted); background: var(--color-accent-subtle); }
  .problem-card h3 {
    font-family: var(--font-mono); font-size: var(--text-xs);
    letter-spacing: var(--tracking-wide); text-transform: uppercase;
    color: var(--color-fg-3); margin-bottom: var(--space-3);
  }
  .problem-card.is h3 { color: var(--color-accent); }
  .problem-card p { color: var(--color-fg-2); font-size: var(--text-sm); line-height: var(--leading-relaxed); }
  .problem-card.is p { color: var(--color-fg-1); }
  .arch {
    background: var(--color-surface);
    border: 1px solid var(--color-border);
    border-radius: var(--radius-lg);
    box-shadow: var(--shadow-card);
    overflow: hidden;
  }
  .arch-layer {
    display: grid;
    grid-template-columns: 200px 1fr;
    gap: var(--space-5);
    padding: var(--space-5) var(--space-6);
    border-top: 1px solid var(--color-border);
    align-items: start;
  }
  .arch-layer:first-child { border-top: 0; }
  .arch-layer .label {
    display: flex; flex-direction: column; gap: 2px;
  }
  .arch-layer .label .num {
    font-family: var(--font-mono); font-size: var(--text-xs);
    color: var(--color-fg-3); letter-spacing: var(--tracking-wide);
  }
  .arch-layer .label .name { font-size: var(--text-base); font-weight: var(--font-medium); }
  .arch-layer .body { color: var(--color-fg-2); font-size: var(--text-sm); line-height: var(--leading-relaxed); }
  .arch-layer .chips { display: flex; flex-wrap: wrap; gap: 4px; margin-top: var(--space-2); }
  .arch-chip {
    font-family: var(--font-mono); font-size: 11px;
    padding: 2px 7px; border-radius: var(--radius-sm);
    background: var(--color-bg); color: var(--color-fg-2);
    border: 1px solid var(--color-border);
  }
  .arch-layer.deterministic { background: #fafaf7; }
  .lane-toggle {
    display: inline-flex;
    border: 1px solid var(--color-border);
    border-radius: var(--radius-md);
    overflow: hidden; background: var(--color-surface);
    margin-bottom: var(--space-5);
  }
  .lane-toggle button {
    appearance: none; background: transparent; border: 0;
    padding: 7px 13px; font: inherit; font-size: var(--text-sm);
    color: var(--color-fg-2); cursor: pointer;
    font-family: var(--font-mono); transition: var(--transition-fast);
  }
  .lane-toggle button + button { border-left: 1px solid var(--color-border); }
  .lane-toggle button.active { background: var(--color-accent); color: #fff; }
  .lane-toggle button:hover:not(.active) { background: var(--color-surface-2); }
  .pipeline {
    background: var(--color-surface);
    border: 1px solid var(--color-border);
    border-radius: var(--radius-lg);
    padding: var(--space-6);
    box-shadow: var(--shadow-card);
  }
  .phase-row { display: grid; gap: var(--space-2); }
  .step {
    background: var(--color-bg);
    border: 1px solid var(--color-border);
    border-radius: var(--radius-md);
    padding: var(--space-2) var(--space-3);
    display: flex; align-items: center; gap: var(--space-3);
    transition: var(--transition-fast);
  }
  .step:hover { border-color: var(--color-accent-muted); background: var(--color-accent-subtle); }
  .step .ix {
    font-family: var(--font-mono); font-size: var(--text-xs);
    color: var(--color-fg-3); width: 24px;
    flex-shrink: 0; text-align: right;
  }
  .step .name {
    font-family: var(--font-mono); font-size: var(--text-sm);
    color: var(--color-fg-1); font-weight: var(--font-medium);
    min-width: 180px;
  }
  .step .what { color: var(--color-fg-2); font-size: var(--text-sm); }
  .step.critic { border-left: 3px solid var(--color-accent); }
  .step.deterministic { background: #fafaf7; position: relative; }
  .step.deterministic::after {
    content: "deterministic"; position: absolute; right: 12px;
    font-family: var(--font-mono); font-size: 10px;
    color: var(--color-verdict-safe-failure);
    background: var(--color-verdict-safe-failure-bg);
    border: 1px solid var(--color-verdict-safe-failure-border);
    padding: 1px 6px; border-radius: var(--radius-sm);
    letter-spacing: var(--tracking-wide);
  }
  .phase-label {
    display: flex; align-items: center; gap: var(--space-3);
    margin: var(--space-4) 0 var(--space-1);
    font-family: var(--font-mono); font-size: 11px;
    color: var(--color-fg-3); letter-spacing: var(--tracking-wide);
    text-transform: uppercase;
  }
  .phase-label::before, .phase-label::after { content: ""; height: 1px; background: var(--color-border); }
  .phase-label::before { width: 16px; }
  .phase-label::after  { flex: 1; }
  .phase-label:first-child { margin-top: 0; }
  .critics-fan { display: grid; grid-template-columns: repeat(2, 1fr); gap: var(--space-2); }
  .lane-pane { display: none; }
  .lane-pane.active { display: block; }
  .tree {
    background: var(--color-surface);
    border: 1px solid var(--color-border);
    border-radius: var(--radius-lg);
    padding: var(--space-6);
    box-shadow: var(--shadow-card);
    display: grid; gap: var(--space-2);
  }
  .gate {
    display: grid;
    grid-template-columns: 200px 1fr 180px;
    gap: var(--space-4);
    align-items: stretch;
    padding: var(--space-4);
    background: var(--color-bg);
    border: 1px solid var(--color-border);
    border-radius: var(--radius-md);
  }
  .gate .gate-label { display: flex; flex-direction: column; justify-content: center; gap: 2px; }
  .gate .gate-num { font-family: var(--font-mono); font-size: var(--text-xs); color: var(--color-fg-3); letter-spacing: var(--tracking-wide); }
  .gate .gate-title { font-size: var(--text-base); font-weight: var(--font-medium); }
  .gate .conds { display: grid; gap: 4px; align-content: center; }
  .gate .cond {
    font-family: var(--font-mono); font-size: var(--text-sm);
    color: var(--color-fg-2);
    background: var(--color-surface);
    border: 1px solid var(--color-border);
    border-radius: var(--radius-sm);
    padding: 5px 9px;
  }
  .gate .outcomes { display: grid; gap: 4px; align-content: center; }
  .outcome { display: flex; align-items: center; gap: 6px; font-size: var(--text-sm); font-family: var(--font-mono); }
  .outcome .arrow { color: var(--color-fg-3); }
  .pill {
    display: inline-flex; align-items: center; gap: 6px;
    padding: 2px 9px; border-radius: var(--radius-full);
    font-size: var(--text-xs); font-family: var(--font-mono);
    font-weight: var(--font-medium); border: 1px solid;
  }
  .pill.reject  { color: var(--color-verdict-unsafe-failure); background: var(--color-verdict-unsafe-failure-bg); border-color: var(--color-verdict-unsafe-failure-border); }
  .pill.support { color: var(--color-verdict-fragile-success); background: var(--color-verdict-fragile-success-bg); border-color: var(--color-verdict-fragile-success-border); }
  .pill.anchor  { color: var(--color-verdict-safe-success); background: var(--color-verdict-safe-success-bg); border-color: var(--color-verdict-safe-success-border); }
  .gate.terminal { background: var(--color-verdict-safe-success-bg); border-color: var(--color-verdict-safe-success-border); }
  .gate-connector { height: 12px; margin-left: 110px; border-left: 1.5px dashed var(--color-border-strong); }
  .samples { display: grid; grid-template-columns: repeat(3, 1fr); gap: var(--space-3); }
  .sample {
    background: var(--color-surface);
    border: 1px solid var(--color-border);
    border-radius: var(--radius-md);
    overflow: hidden; display: flex; flex-direction: column;
    box-shadow: var(--shadow-card);
  }
  .sample .sample-head {
    padding: var(--space-3) var(--space-4);
    border-bottom: 1px solid var(--color-border);
    display: flex; align-items: center; justify-content: space-between; gap: var(--space-2);
  }
  .sample .sample-file { font-family: var(--font-mono); font-size: var(--text-sm); color: var(--color-fg-1); font-weight: var(--font-medium); }
  .sample .sample-body { padding: var(--space-4); flex: 1; display: flex; flex-direction: column; gap: var(--space-3); }
  .sample .row { display: grid; grid-template-columns: 80px 1fr; gap: var(--space-2); font-size: var(--text-sm); }
  .sample .row .k { font-family: var(--font-mono); font-size: var(--text-xs); color: var(--color-fg-3); text-transform: uppercase; letter-spacing: var(--tracking-wide); padding-top: 2px; }
  .sample .row .v { color: var(--color-fg-1); font-family: var(--font-mono); font-size: var(--text-sm); }
  .sample .why { color: var(--color-fg-2); font-size: var(--text-sm); line-height: var(--leading-relaxed); }
  .sample .reason-codes { display: flex; flex-wrap: wrap; gap: 4px; }
  .reason-code {
    font-family: var(--font-mono); font-size: 11px;
    padding: 2px 6px; border-radius: var(--radius-sm);
    background: var(--color-surface-2); color: var(--color-fg-2);
    border: 1px solid var(--color-border);
  }
  .reason-code.pos { color: var(--color-verdict-safe-success); border-color: var(--color-verdict-safe-success-border); background: var(--color-verdict-safe-success-bg); }
  .reason-code.neg { color: var(--color-verdict-unsafe-failure); border-color: var(--color-verdict-unsafe-failure-border); background: var(--color-verdict-unsafe-failure-bg); }
  .reason-code.warn { color: var(--color-verdict-fragile-success); border-color: var(--color-verdict-fragile-success-border); background: var(--color-verdict-fragile-success-bg); }
  .why-grid {
    display: grid; grid-template-columns: repeat(3, 1fr);
    gap: var(--space-3);
  }
  .why-card {
    background: var(--color-surface);
    border: 1px solid var(--color-border);
    border-radius: var(--radius-md);
    padding: var(--space-5);
  }
  .why-card .num {
    font-family: var(--font-mono); font-size: var(--text-xs);
    color: var(--color-accent); letter-spacing: var(--tracking-wide);
    margin-bottom: var(--space-2);
  }
  .why-card h3 {
    font-size: var(--text-base); font-weight: var(--font-medium);
    margin-bottom: var(--space-2); letter-spacing: -0.01em;
  }
  .why-card p { color: var(--color-fg-2); font-size: var(--text-sm); line-height: var(--leading-relaxed); }
  .stack-grid {
    display: grid; grid-template-columns: repeat(3, 1fr);
    gap: var(--space-3);
  }
  .stack-card {
    background: var(--color-surface);
    border: 1px solid var(--color-border);
    border-radius: var(--radius-md);
    padding: var(--space-5);
    box-shadow: var(--shadow-card);
  }
  .stack-card h4 {
    font-family: var(--font-mono); font-size: var(--text-xs);
    color: var(--color-accent); letter-spacing: var(--tracking-wide);
    text-transform: uppercase; margin-bottom: var(--space-3);
    display: flex; justify-content: space-between; align-items: center;
  }
  .stack-card h4 .layer-num { color: var(--color-fg-3); }
  .stack-card ul { list-style: none; padding: 0; }
  .stack-card li {
    padding: 5px 0; font-size: var(--text-sm); color: var(--color-fg-2);
    border-top: 1px solid var(--color-border);
    line-height: var(--leading-snug);
  }
  .stack-card li:first-child { border-top: 0; }
  .versions {
    margin-top: var(--space-5);
    padding: var(--space-4) var(--space-5);
    background: var(--color-surface);
    border: 1px solid var(--color-border);
    border-radius: var(--radius-md);
    display: flex; flex-wrap: wrap; gap: 4px;
    align-items: center;
  }
  .versions .label {
    font-family: var(--font-mono); font-size: 11px;
    color: var(--color-fg-3); letter-spacing: var(--tracking-wide);
    text-transform: uppercase; margin-right: var(--space-2);
  }
  .artifacts-table {
    background: var(--color-surface);
    border: 1px solid var(--color-border);
    border-radius: var(--radius-md);
    overflow: hidden;
  }
  .art-row {
    display: grid;
    grid-template-columns: 240px 1fr;
    gap: var(--space-4);
    padding: var(--space-3) var(--space-5);
    border-top: 1px solid var(--color-border);
    align-items: baseline;
  }
  .art-row:first-child { border-top: 0; }
  .art-row:hover { background: var(--color-surface-2); }
  .art-row .file { font-family: var(--font-mono); font-size: var(--text-sm); color: var(--color-fg-1); }
  .art-row .desc { color: var(--color-fg-2); font-size: var(--text-sm); }
  footer { padding: var(--space-8) 0 var(--space-12); color: var(--color-fg-3); font-size: var(--text-sm); }
  footer .wrap { display: flex; justify-content: space-between; align-items: center; gap: var(--space-6); flex-wrap: wrap; }
  footer code { background: transparent; color: var(--color-fg-2); padding: 0; }
  @media (max-width: 920px) {
    .hero h1 { font-size: 32px; }
    .stat-strip { grid-template-columns: repeat(2, 1fr); row-gap: var(--space-3); }
    .section-head { grid-template-columns: 1fr; gap: var(--space-2); }
    .samples { grid-template-columns: 1fr; }
    .problem-grid { grid-template-columns: 1fr; }
    .topbar nav { display: none; }
    .arch-layer { grid-template-columns: 1fr; gap: var(--space-2); }
    .stack-grid { grid-template-columns: 1fr; }
    .why-grid { grid-template-columns: 1fr; }
    .critics-fan { grid-template-columns: 1fr; }
    .gate { grid-template-columns: 1fr; }
    .gate-connector { margin-left: 24px; }
  }
"""


SCRIPT = """
  (() => {
    const buttons = document.querySelectorAll('.lane-toggle button');
    const panes = document.querySelectorAll('.lane-pane');
    buttons.forEach(btn => {
      btn.addEventListener('click', () => {
        const lane = btn.getAttribute('data-lane');
        buttons.forEach(b => b.classList.toggle('active', b === btn));
        panes.forEach(p => p.classList.toggle('active', p.getAttribute('data-lane') === lane));
      });
    });
  })();
  document.querySelectorAll('a[href^="#"]').forEach(a => {
    a.addEventListener('click', e => {
      const id = a.getAttribute('href');
      if (id.length <= 1) return;
      const el = document.querySelector(id);
      if (!el) return;
      e.preventDefault();
      window.scrollTo({ top: el.offsetTop - 60, behavior: 'smooth' });
    });
  });
"""


def load_context() -> dict:
    return json.loads(CONTEXT_PATH.read_text(encoding="utf-8-sig"))


def esc(value: str | int | float) -> str:
    return html.escape(str(value), quote=True)


def section_head(block: dict) -> str:
    note_html = block.get("note_html")
    note = ""
    if note_html:
        note = (
            '<p class="sub" style="margin-top: var(--space-3); font-size: var(--text-sm); color: var(--color-fg-3);">'
            f"{note_html}</p>"
        )
    return (
        '<div class="section-head">'
        f'<div class="kicker">{esc(block["kicker"])}</div>'
        '<div>'
        f'<h2>{esc(block["title"])}</h2>'
        f'<p class="sub">{block["sub_html"]}</p>'
        f"{note}"
        "</div>"
        "</div>"
    )


def render_nav(groups: list[dict]) -> str:
    links = "".join(
        f'<a href="#{esc(group["id"])}">{esc(group["nav_label"])}</a>'
        for group in groups
    )
    return f"<nav>{links}</nav>"


def render_page_hero(data: dict) -> str:
    stats = "".join(
        '<div class="stat">'
        f'<div class="num">{esc(item["value"])}</div>'
        f'<div class="label">{esc(item["label"])}</div>'
        "</div>"
        for item in data["stats"]
    )
    return (
        '<section class="hero">'
        '<div class="wrap">'
        f'<div class="eyebrow"><span class="dot"></span>{esc(data["eyebrow"])}</div>'
        f'<h1>{data["heading_html"]}</h1>'
        f'<p class="lede">{data["lede_html"]}</p>'
        f'<p class="lede" style="font-size: var(--text-sm); color: var(--color-fg-3);">{data["caption_html"]}</p>'
        f'<div class="stat-strip">{stats}</div>'
        "</div>"
        "</section>"
    )


def render_problem_cards(block: dict) -> str:
    cards = []
    for item in block["items"]:
        cls = "problem-card is" if item.get("emphasis") else "problem-card"
        cards.append(
            f'<div class="{cls}">'
            f'<h3>{esc(item["title"])}</h3>'
            f'<p>{item["body_html"]}</p>'
            "</div>"
        )
    return f'<div class="problem-grid">{"".join(cards)}</div>'


def render_architecture(block: dict) -> str:
    layers = []
    for item in block["items"]:
        cls = "arch-layer deterministic" if item.get("deterministic") else "arch-layer"
        chips = "".join(f'<span class="arch-chip">{esc(chip)}</span>' for chip in item["chips"])
        layers.append(
            f'<div class="{cls}">'
            '<div class="label">'
            f'<div class="num">{esc(item["num"])}</div>'
            f'<div class="name">{esc(item["name"])}</div>'
            "</div>"
            f'<div class="body">{item["body_html"]}<div class="chips">{chips}</div></div>'
            "</div>"
        )
    return f'<div class="arch">{"".join(layers)}</div>'


def render_step(step: dict) -> str:
    classes = ["step"]
    if step.get("critic"):
        classes.append("critic")
    if step.get("deterministic"):
        classes.append("deterministic")
    return (
        f'<div class="{" ".join(classes)}">'
        f'<div class="ix">{esc(step["ix"])}</div>'
        f'<div class="name">{esc(step["name"])}</div>'
        f'<div class="what">{esc(step["what"])}</div>'
        "</div>"
    )


def render_pipeline(block: dict) -> str:
    button_parts = []
    for lane in block["lanes"]:
        active_attr = ' class="active"' if lane.get("active") else ""
        button_parts.append(
            f'<button{active_attr} data-lane="{esc(lane["id"])}">{esc(lane["label"])}</button>'
        )
    buttons = "".join(button_parts)
    panes = []
    for lane in block["lanes"]:
        pane_cls = "lane-pane active" if lane.get("active") else "lane-pane"
        parts = []
        for phase in lane["phases"]:
            parts.append(f'<div class="phase-label">{esc(phase["label"])}</div>')
            if phase["layout"] == "critic":
                critics = "".join(render_step(step) for step in phase["steps"])
                parts.append(f'<div class="critics-fan">{critics}</div>')
                if phase.get("followup_steps"):
                    followups = "".join(render_step(step) for step in phase["followup_steps"])
                    parts.append(f'<div class="phase-row" style="margin-top: var(--space-2);">{followups}</div>')
            else:
                steps = "".join(render_step(step) for step in phase["steps"])
                parts.append(f'<div class="phase-row">{steps}</div>')
        if lane.get("note_html"):
            parts.append(
                '<p style="color: var(--color-fg-3); font-size: var(--text-sm); margin-top: var(--space-4); font-family: var(--font-mono);">'
                f'{lane["note_html"]}</p>'
            )
        panes.append(f'<div class="{pane_cls}" data-lane="{esc(lane["id"])}">{"".join(parts)}</div>')
    return (
        f'<div class="lane-toggle" role="tablist">{buttons}</div>'
        f'<div class="pipeline">{"".join(panes)}</div>'
    )


def render_pill(pill: dict) -> str:
    return f'<span class="pill {esc(pill["tone"])}">{esc(pill["label"])}</span>'


def render_decision_tree(block: dict) -> str:
    gates = []
    for index, gate in enumerate(block["gates"]):
        cls = "gate terminal" if gate.get("terminal") else "gate"
        conditions = "".join(f'<div class="cond">{item}</div>' for item in gate["conditions_html"])
        outcomes = []
        for outcome in gate["outcomes"]:
            text = f'{esc(outcome["text"])} ' if outcome.get("text") else ""
            arrow = f'<span class="arrow">{esc(outcome["arrow"])}</span>' if outcome.get("arrow") else ""
            pill = render_pill(outcome["pill"]) if outcome.get("pill") else ""
            outcomes.append(f'<div class="outcome">{text}{arrow}{pill}</div>')
        gates.append(
            f'<div class="{cls}">'
            '<div class="gate-label">'
            f'<div class="gate-num">{esc(gate["num"])}</div>'
            f'<div class="gate-title">{esc(gate["title"])}</div>'
            "</div>"
            f'<div class="conds">{conditions}</div>'
            f'<div class="outcomes">{"".join(outcomes)}</div>'
            "</div>"
        )
        if index < len(block["gates"]) - 1:
            gates.append('<div class="gate-connector"></div>')
    return f'<div class="tree">{"".join(gates)}</div>'


def render_samples(block: dict) -> str:
    articles = []
    for item in block["items"]:
        rows = "".join(
            '<div class="row">'
            f'<div class="k">{esc(row["key"])}</div>'
            f'<div class="v">{esc(row["value"])}</div>'
            "</div>"
            for row in item["rows"]
        )
        codes = "".join(
            f'<span class="reason-code {esc(code["tone"])}">{esc(code["label"])}</span>'
            for code in item["reason_codes"]
        )
        articles.append(
            '<article class="sample">'
            '<div class="sample-head">'
            f'<div class="sample-file">{esc(item["file"])}</div>'
            f'{render_pill(item["verdict"])}'
            "</div>"
            '<div class="sample-body">'
            f"{rows}"
            f'<p class="why">{item["why_html"]}</p>'
            f'<div class="reason-codes">{codes}</div>'
            "</div>"
            "</article>"
        )
    return f'<div class="samples">{"".join(articles)}</div>'


def render_feature_cards(block: dict) -> str:
    cards = "".join(
        '<div class="why-card">'
        f'<div class="num">{esc(item["num"])}</div>'
        f'<h3>{esc(item["title"])}</h3>'
        f'<p>{item["body_html"]}</p>'
        "</div>"
        for item in block["items"]
    )
    return f'<div class="why-grid">{cards}</div>'


def render_stack(block: dict) -> str:
    cards = []
    for card in block["cards"]:
        items = "".join(f'<li>{item}</li>' for item in card["items_html"])
        cards.append(
            '<div class="stack-card">'
            f'<h4><span>{esc(card["title"])}</span><span class="layer-num">{esc(card["num"])}</span></h4>'
            f"<ul>{items}</ul>"
            "</div>"
        )
    versions = "".join(f'<span class="reason-code">{esc(item)}</span>' for item in block["versions"])
    return (
        f'<div class="stack-grid">{"".join(cards)}</div>'
        f'<div class="versions"><span class="label">{esc(block["versions_label"])}</span>{versions}</div>'
    )


def render_artifacts(block: dict) -> str:
    rows = "".join(
        '<div class="art-row">'
        f'<div class="file">{esc(item["file"])}</div>'
        f'<div class="desc">{esc(item["desc"])}</div>'
        "</div>"
        for item in block["items"]
    )
    return f'<div class="artifacts-table">{rows}</div>'


def render_block(block: dict) -> str:
    kind = block["kind"]
    if kind == "problem-cards":
        return render_problem_cards(block)
    if kind == "architecture":
        return render_architecture(block)
    if kind == "pipeline":
        return render_pipeline(block)
    if kind == "decision-tree":
        return render_decision_tree(block)
    if kind == "samples":
        return render_samples(block)
    if kind == "feature-cards":
        return render_feature_cards(block)
    if kind == "stack":
        return render_stack(block)
    if kind == "artifacts":
        return render_artifacts(block)
    raise ValueError(f"Unsupported block kind: {kind}")


def render_group(group: dict) -> str:
    body_parts = [section_head(group)]
    for block in group["blocks"]:
        body_parts.append(render_block(block))
    block_cls = "block tight" if group.get("tight") else "block"
    return (
        f'<section class="{block_cls}" id="{esc(group["id"])}">'
        '<div class="wrap">'
        f'{"".join(body_parts)}'
        "</div>"
        "</section>"
    )


def render_footer(data: dict) -> str:
    return (
        "<footer>"
        '<div class="wrap">'
        f'<div>{data["left_html"]}</div>'
        f'<div>{data["right_html"]}</div>'
        "</div>"
        "</footer>"
    )


def build_page(context: dict) -> str:
    body = "".join(
        [
            '<header class="topbar"><div class="wrap"><div class="brand"><span class="mark"></span>'
            f'<span>{esc(context["meta"]["brand_title"])}</span></div>{render_nav(context["groups"])}'
            f'<div class="meta">{esc(context["meta"]["top_meta"])}</div></div></header>',
            render_page_hero(context["page_hero"]),
            *(render_group(group) for group in context["groups"]),
            render_footer(context["footer"]),
        ]
    )
    return f"""<!doctype html>
<html lang="zh-CN">
<head>
<meta charset="utf-8" />
<meta name="viewport" content="width=device-width, initial-scale=1" />
<title>{esc(context["meta"]["page_title"])}</title>
<meta name="description" content="{esc(context["meta"]["description"])}" />
<link rel="stylesheet" href="tokens.css" />
<style>
{STYLE}
</style>
</head>
<body>
{body}
<script>
{SCRIPT}
</script>
</body>
</html>
"""


def main() -> None:
    context = load_context()
    OUTPUT_PATH.write_text(build_page(context), encoding="utf-8")


if __name__ == "__main__":
    main()
