#!/usr/bin/env python3
# Copyright (c) 2026 AIperture-Labs <xavier.beheydt@gmail.com>
# SPDX-License-Identifier: MPL-2.0
# Contributors:
#   Copyright (c) 2026 Claude Code (Claude Opus 5.5)
"""Render the organization roadmap as an SVG from GitHub milestones.

Milestones named `M<n> · <name>` are read from the repositories in $REPOS
(comma-separated `owner/repo`) and drawn on a timeline. With no milestone
found, the output file is left untouched.

    REPOS=AIperture-Labs/AetherEngine GH_TOKEN=... python3 scripts/roadmap.py
    python3 scripts/roadmap.py --data milestones.json   # offline preview
"""

import argparse
import datetime
import json
import os
import re
import sys
import urllib.request
from html import escape

OUT = "profile/roadmap.svg"
W, H = 880, 292
PAD = 48
TRACK_Y = 150
MAX_NODES = 6


def fetch(repo, token):
    req = urllib.request.Request(
        f"https://api.github.com/repos/{repo}/milestones?state=all&per_page=100",
        headers={"Accept": "application/vnd.github+json"}
        | ({"Authorization": f"Bearer {token}"} if token else {}),
    )
    with urllib.request.urlopen(req) as r:
        return [
            {
                "repo": repo.split("/")[1],
                "title": m["title"],
                "state": m["state"],
                "open": m["open_issues"],
                "closed": m["closed_issues"],
            }
            for m in json.load(r)
        ]


def parse(m):
    match = re.match(r"M(\d+)\s*[·:\-–]?\s*(.*)", m["title"])
    return (int(match[1]), match[2] or m["title"]) if match else None


def visible(ms):
    """Ordered milestones, windowed around the first open one."""
    ms = sorted((m | {"n": p[0], "name": p[1]} for m in ms if (p := parse(m))),
                key=lambda m: (m["n"], m["repo"]))
    active = next((i for i, m in enumerate(ms) if m["state"] == "open"), len(ms))
    start = max(0, min(active - 1, len(ms) - MAX_NODES))
    return ms[start:start + MAX_NODES], active - start


def wrap(text, width=18):
    lines, line = [], ""
    for word in text.split():
        if line and len(line) + 1 + len(word) > width:
            lines.append(line)
            line = word
        else:
            line = f"{line} {word}".strip()
    lines.append(line)
    return lines[:2]


def render(ms, active):
    n = len(ms)
    step = (W - 2 * PAD) / n
    xs = [PAD + step * (i + 0.5) for i in range(n)]
    ratio = lambda m: m["closed"] / ((m["open"] + m["closed"]) or 1)
    if active < n:
        fill_x = xs[active] if active == 0 else xs[active - 1] + (xs[active] - xs[active - 1]) * max(ratio(ms[active]), 0.15)
        fill_x = max(fill_x, xs[0])
    else:
        fill_x = xs[-1]
    today = datetime.date.today().isoformat()

    o = [f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="AIperture Labs roadmap">
<defs>
  <linearGradient id="beam" gradientUnits="userSpaceOnUse" x1="{PAD}" x2="{W - PAD}" y1="0" y2="0"><stop offset="0" stop-color="#38bdf8"/><stop offset="1" stop-color="#a78bfa"/></linearGradient>
  <radialGradient id="halo"><stop offset="0" stop-color="#7dd3fc" stop-opacity=".55"/><stop offset="1" stop-color="#7dd3fc" stop-opacity="0"/></radialGradient>
  <pattern id="grid" width="22" height="22" patternUnits="userSpaceOnUse"><path d="M22 0H0V22" fill="none" stroke="#1b2333" stroke-width="1"/></pattern>
  <clipPath id="card"><rect width="{W}" height="{H}" rx="16"/></clipPath>
  <filter id="glow" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="3"/></filter>
</defs>
<style>
  .mono {{ font-family: ui-monospace, SFMono-Regular, Menlo, Consolas, monospace; }}
  .sans {{ font-family: -apple-system, "Segoe UI", Helvetica, Arial, sans-serif; }}
  .pulse {{ animation: pulse 2.4s ease-in-out infinite; transform-box: fill-box; transform-origin: center; }}
  @keyframes pulse {{ 0%,100% {{ opacity: .35; transform: scale(.8); }} 50% {{ opacity: 1; transform: scale(1.25); }} }}
  .spin {{ animation: spin 1.6s linear infinite; transform-box: fill-box; transform-origin: center; }}
  @keyframes spin {{ to {{ transform: rotate(360deg); }} }}
  .flow {{ animation: flow 1.2s linear infinite; }}
  @keyframes flow {{ to {{ stroke-dashoffset: -28; }} }}
  .scan {{ animation: scan 6s linear infinite; }}
  @keyframes scan {{ from {{ transform: translateX(-120px); }} to {{ transform: translateX({W + 120}px); }} }}
</style>
<g clip-path="url(#card)">
  <rect width="{W}" height="{H}" fill="#0b0f17"/>
  <rect width="{W}" height="{H}" fill="url(#grid)" opacity=".7"/>
  <rect class="scan" x="0" y="0" width="120" height="{H}" fill="url(#beam)" opacity=".035"/>
</g>
<rect x=".5" y=".5" width="{W - 1}" height="{H - 1}" rx="15.5" fill="none" stroke="#243047"/>
<text x="{PAD - 16}" y="44" class="mono" font-size="11" letter-spacing="3" fill="#38bdf8">// ROADMAP</text>
<text x="{PAD - 16}" y="72" class="sans" font-size="22" font-weight="600" fill="#e6edf3">AIperture Labs</text>
<text x="{W - PAD + 16}" y="44" class="mono" font-size="11" fill="#5b6b85" text-anchor="end">updated {today}</text>
<line x1="{xs[0]}" y1="{TRACK_Y}" x2="{xs[-1]}" y2="{TRACK_Y}" stroke="#243047" stroke-width="2" stroke-dasharray="2 6" stroke-linecap="round"/>
<line x1="{xs[0]}" y1="{TRACK_Y}" x2="{fill_x:.1f}" y2="{TRACK_Y}" stroke="url(#beam)" stroke-width="3" stroke-linecap="round" filter="url(#glow)" opacity=".8"/>
<line x1="{xs[0]}" y1="{TRACK_Y}" x2="{fill_x:.1f}" y2="{TRACK_Y}" stroke="url(#beam)" stroke-width="2" stroke-linecap="round"/>
<line class="flow" x1="{xs[0]}" y1="{TRACK_Y}" x2="{fill_x:.1f}" y2="{TRACK_Y}" stroke="#e0f2fe" stroke-width="2" stroke-dasharray="4 24" stroke-linecap="round" opacity=".8"/>
''']
    for i, (m, x) in enumerate(zip(ms, xs)):
        done, cur = m["state"] == "closed", i == active
        total = m["open"] + m["closed"]
        if done:
            o.append(f'<circle cx="{x:.1f}" cy="{TRACK_Y}" r="11" fill="#38bdf8"/>'
                     f'<path d="M{x - 5:.1f} {TRACK_Y}l3.5 3.5 6.5-7" fill="none" stroke="#0b0f17" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"/>')
        elif cur:
            o.append(f'<circle class="pulse" cx="{x:.1f}" cy="{TRACK_Y}" r="24" fill="url(#halo)"/>'
                     f'<circle class="spin" cx="{x:.1f}" cy="{TRACK_Y}" r="17" fill="none" stroke="#7dd3fc" stroke-width="2" stroke-linecap="round" stroke-dasharray="22 85"/>'
                     f'<circle cx="{x:.1f}" cy="{TRACK_Y}" r="11" fill="#0b0f17" stroke="#7dd3fc" stroke-width="2.5"/>'
                     f'<circle cx="{x:.1f}" cy="{TRACK_Y}" r="4.5" fill="#7dd3fc"/>')
        else:
            o.append(f'<circle cx="{x:.1f}" cy="{TRACK_Y}" r="9" fill="#0b0f17" stroke="#33415c" stroke-width="2"/>')
        tone = "#e6edf3" if done or cur else "#8b98ad"
        o.append(f'<text x="{x:.1f}" y="{TRACK_Y - 30}" class="mono" font-size="12" font-weight="700" text-anchor="middle" fill="{"#7dd3fc" if cur else "#38bdf8" if done else "#5b6b85"}">M{m["n"]}</text>')
        for j, line in enumerate(wrap(m["name"])):
            o.append(f'<text x="{x:.1f}" y="{TRACK_Y + 38 + j * 18}" class="sans" font-size="14" font-weight="{600 if cur else 500}" text-anchor="middle" fill="{tone}">{escape(line)}</text>')
        bar_y, bw = TRACK_Y + 82, 64
        o.append(f'<rect x="{x - bw / 2:.1f}" y="{bar_y}" width="{bw}" height="3" rx="1.5" fill="#1e293b"/>')
        if total:
            o.append(f'<rect x="{x - bw / 2:.1f}" y="{bar_y}" width="{bw * ratio(m):.1f}" height="3" rx="1.5" fill="url(#beam)"/>')
        label = f'{m["closed"]}/{total} issues' if total else ("done" if done else "planned")
        o.append(f'<text x="{x:.1f}" y="{bar_y + 20}" class="mono" font-size="10.5" text-anchor="middle" fill="#8b98ad">{label}</text>')
        o.append(f'<text x="{x:.1f}" y="{bar_y + 36}" class="mono" font-size="10" text-anchor="middle" fill="#4a5872">{escape(m["repo"])}</text>')
    o.append("</svg>\n")
    return "\n".join(o)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--data", help="read milestones from a JSON file instead of the API")
    args = ap.parse_args()
    if args.data:
        ms = json.load(open(args.data))
    else:
        token = os.environ.get("GH_TOKEN")
        ms = [m for r in os.environ["REPOS"].split(",") if r.strip() for m in fetch(r.strip(), token)]
    shown, active = visible(ms)
    if not shown:
        print("no M<n> milestone found, roadmap left unchanged", file=sys.stderr)
        return
    svg = render(shown, active)
    undated = lambda t: re.sub(r"updated \d{4}-\d{2}-\d{2}", "", t)
    if os.path.exists(OUT) and undated(open(OUT).read()) == undated(svg):
        return  # only the date would change: no daily commit
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w") as f:
        f.write(svg)


if __name__ == "__main__":
    main()
