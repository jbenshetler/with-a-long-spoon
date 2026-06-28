#!/usr/bin/env python3
"""Generate a self-contained HTML view of meta-plan-chronology.md.

Parses the chronology's scene/vignette/event entries and their metadata line
(status, date, track, POV, files, links) and emits a single HTML file with
inline CSS+JS (zero external dependencies): a status-colored beeswarm timeline
across the academic year (hover a dot for the beat name), a phase-grouped card
list, and the Continuity Flags panel.

Deterministic: same input -> same output (no timestamps embedded), so it is
safe to commit and to diff. Re-run after any chronology edit to refresh.

Usage:
    tools/chronology_html.py [INPUT.md] [-o OUTPUT.html]
Defaults: INPUT = meta/meta-plan-chronology.md, OUTPUT = chronology.html
"""
from __future__ import annotations

import argparse
import datetime as dt
import html
import re
import sys
from pathlib import Path

# --- academic-year framing -------------------------------------------------
# Story runs ~Aug -> next Aug. We anchor day-0 at Aug 1 of an arbitrary base
# year so beats sort continuously across the Dec->Jan boundary. The base year
# is cosmetic (only month/day are shown); it just disambiguates ordering.
BASE_YEAR = 2024
ANCHOR = dt.date(BASE_YEAR, 8, 1)
YEAR_DAYS = 365

MONTHS = {
    "jan": 1, "january": 1, "feb": 2, "february": 2, "mar": 3, "march": 3,
    "apr": 4, "april": 4, "may": 5, "jun": 6, "june": 6, "jul": 7, "july": 7,
    "aug": 8, "august": 8, "sep": 9, "sept": 9, "september": 9,
    "oct": 10, "october": 10, "nov": 11, "november": 11, "dec": 12, "december": 12,
}
DAYS_IN_MONTH = {1: 31, 2: 28, 3: 31, 4: 30, 5: 31, 6: 30,
                 7: 31, 8: 31, 9: 30, 10: 31, 11: 30, 12: 31}

# Matched as a prefix (status words sometimes carry a trailing colon or an
# inline "(scenes/foo.md)"). Longest phrases first so the specific ones win.
STATUS_MATCH = [
    ("architecture complete, prose not drafted", "arch", "Architecture complete"),
    ("architecture complete", "arch", "Architecture complete"),
    ("draft complete", "done", "Draft complete"),
    ("draft in progress", "wip", "Draft in progress"),
    ("unwritten", "todo", "Unwritten"),
    ("not a scene", "event", "Not a scene"),
]
STATUS_COLOR = {
    "done": "#2e7d32", "wip": "#f9a825", "arch": "#5c6bc0", "todo": "#9e9e9e",
    "event": "#546e7a", "unknown": "#c0c0c0",
}

MIDDOT = "·"
ENDASH = "–"


# --- date resolution -------------------------------------------------------
def _offset(month: int, day: int) -> int:
    day = max(1, min(day, DAYS_IN_MONTH[month]))
    year = BASE_YEAR if month >= 8 else BASE_YEAR + 1
    return (dt.date(year, month, day) - ANCHOR).days


def _find_month(text: str):
    for tok in re.findall(r"[A-Za-z]+", text):
        n = MONTHS.get(tok.lower())
        if n:
            return n
    return None


def _modifier_day(text: str):
    low = text.lower()
    if "mid-late" in low or "mid" + ENDASH + "late" in low:
        return 20
    if "early" in low:
        return 7
    if "late" in low:
        return 23
    if "mid" in low:
        return 15
    return None


def _parse_point(text: str, fallback_month=None):
    """Parse one date token -> (month, day) or None."""
    month = _find_month(text) or fallback_month
    if not month:
        return None
    nums = re.findall(r"\b(\d{1,2})\b", text)
    if nums:
        return month, int(nums[0])
    mod = _modifier_day(text)
    return month, (mod if mod is not None else 15)


def resolve_date(seg: str):
    """Return (offset, display, precision) for a date-ish segment, else None."""
    s = seg.strip().lstrip("~").strip()
    if not s:
        return None
    if ENDASH in s:  # a range (ranges in this doc always use the en-dash)
        left, right = s.split(ENDASH, 1)
        lp = _parse_point(left)
        if not lp:
            return None
        rp = _parse_point(right, fallback_month=lp[0])
        if not rp:
            return None
        off = (_offset(*lp) + _offset(*rp)) // 2
        return off, "~" + s, "range"
    low = s.lower()
    pt = _parse_point(s)
    if not pt:
        return None
    off = _offset(*pt)
    if "week of" in low:
        prec = "week"
    elif re.search(r"\b\d{1,2}\b", s):
        prec = "day"
    else:
        prec = "month"
    return off, "~" + s, prec


# --- metadata segment classification ---------------------------------------
LINK_RE = re.compile(r"\[([^\]]+)\]\(([^)]+)\)")


def classify(seg: str):
    """Return (kind, value-dict) for one metadata segment."""
    s = seg.strip()
    low = s.lower()
    if not s:
        return None
    m = LINK_RE.search(s)
    if m and not (ENDASH in s and _find_month(s)):
        return "link", {"text": m.group(1), "href": m.group(2)}
    for phrase, cls, label in STATUS_MATCH:
        if low.startswith(phrase):
            return "status", {"cls": cls, "label": label}
    d = resolve_date(s)
    if d:
        return "date", {"offset": d[0], "display": d[1], "precision": d[2]}
    if low == "fb" or "satc" in low or "cassandra" in low or "track" in low:
        return "track", {"label": s}
    if "pov" in low:
        return "pov", {"label": s}
    if "`" in s or "scenes/" in s or s.endswith(".md"):
        return "file", {"label": s.replace("`", "")}
    if "page" in low:
        return "length", {"label": s}
    return "context", {"label": s}


# --- parsing the file ------------------------------------------------------
ENTRY_RE = re.compile(r"^###\s+\[(SCENE|VIGNETTE|EVENT)\]\s+(.*)$")
SECTION_RE = re.compile(r"^##\s+(.*)$")


class Entry:
    def __init__(self, etype, title, phase):
        self.etype = etype
        self.title = title
        self.phase = phase
        self.meta_raw = ""
        self.segments = []      # list of (kind, dict)
        self.body = ""
        # convenience
        self.status = None      # (cls, label)
        self.date = None        # dict or None

    def finalize(self, unknown_log):
        for kind, val in self.segments:
            if kind == "status":
                self.status = val
            elif kind == "date" and self.date is None:
                self.date = val
        if self.status is None:
            self.status = {"cls": "event" if self.etype == "EVENT" else "unknown",
                           "label": "—" if self.etype != "EVENT" else "Not a scene"}


def parse(md: str):
    lines = md.splitlines()
    entries = []
    phase = None
    flags_raw = []
    in_flags = False
    cur = None
    body_lines = []

    def flush():
        if cur is not None:
            cur.body = "\n".join(body_lines).strip()
            entries.append(cur)

    for line in lines:
        sec = SECTION_RE.match(line)
        if sec:
            flush()
            cur = None
            body_lines = []
            phase = sec.group(1).strip()
            in_flags = phase.lower().startswith("continuity flags")
            continue
        if in_flags:
            flags_raw.append(line)
            continue
        ent = ENTRY_RE.match(line)
        if ent:
            flush()
            body_lines = []
            cur = Entry(ent.group(1), ent.group(2).strip(), phase or "")
            continue
        if cur is not None:
            # the metadata line is the first content line after the heading; the
            # italics wrap only its leading date/context part, with status, file
            # and links following after the closing '*', so don't require it to
            # end with '*' — just start with one and carry the '·' separator.
            if not cur.meta_raw and not body_lines:
                if line.strip() == "":
                    continue
                if line.strip().startswith("*") and MIDDOT in line:
                    cur.meta_raw = line.strip()
                    segs = []
                    for seg in cur.meta_raw.split(MIDDOT):
                        seg = seg.strip().strip("*").strip()
                        c = classify(seg)
                        if c is not None:
                            segs.append(c)
                    cur.segments = segs
                    continue
            body_lines.append(line)
    flush()

    unknown = []
    for e in entries:
        e.finalize(unknown)

    # The story spans one academic year (Aug -> next Aug), so both endpoints
    # land in August. A single Aug->Jul axis would collapse them. The file is
    # in story order, so walk it and bump a year counter at the single Jul->Aug
    # wrap (late-cycle -> early-cycle), making offsets monotonic across the year.
    year_off, prev_smi = 0, None
    for e in entries:
        if not e.date:
            continue
        cyc = e.date["offset"]                       # 0..364 within one cycle
        rmonth = (ANCHOR + dt.timedelta(days=cyc)).month
        smi = (rmonth - 8) % 12                       # story-month index, Aug=0
        if prev_smi is not None and prev_smi >= 8 and smi <= 1:
            year_off += 1
        prev_smi = smi
        e.date["offset"] = year_off * YEAR_DAYS + cyc
    return entries, "\n".join(flags_raw).strip()


# --- beeswarm layout (computed here, emitted as static SVG) -----------------
def beeswarm(entries, width=1080, pad_l=44, pad_r=20, top=18, dot_r=5, gap=12):
    plot_w = width - pad_l - pad_r
    dated = [e for e in entries if e.date]
    dated.sort(key=lambda e: e.date["offset"])
    span = max((e.date["offset"] for e in dated), default=YEAR_DAYS) or YEAR_DAYS
    levels = []  # last x placed at each level
    nodes = []
    for e in dated:
        x = pad_l + (e.date["offset"] / span) * plot_w
        lvl = 0
        while lvl < len(levels) and x - levels[lvl] < gap:
            lvl += 1
        if lvl == len(levels):
            levels.append(x)
        else:
            levels[lvl] = x
        nodes.append((e, x, lvl))
    height = top + (len(levels) + 1) * gap + 26
    baseline = height - 26
    return nodes, width, height, baseline, pad_l, plot_w, span


def month_ticks(pad_l, plot_w, span):
    ticks = []
    cur = dt.date(BASE_YEAR, 8, 1)
    while (cur - ANCHOR).days <= span + 18:
        off = (cur - ANCHOR).days
        x = pad_l + (off / span) * plot_w
        ticks.append((x, cur.strftime("%b")))
        y, m = (cur.year, cur.month + 1) if cur.month < 12 else (cur.year + 1, 1)
        cur = dt.date(y, m, 1)
    return ticks


# --- inline markdown -> html ------------------------------------------------
def md_inline(text: str) -> str:
    text = html.escape(text)
    text = re.sub(r"\[\[([^\]]+)\]\]", r'<span class="wiki">\1</span>', text)
    text = LINK_RE.sub(r'<a href="\2">\1</a>', text)
    text = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", text)
    text = re.sub(r"\*([^*]+)\*", r"<em>\1</em>", text)
    text = re.sub(r"`([^`]+)`", r"<code>\1</code>", text)
    return text


def md_block(text: str) -> str:
    out = []
    for para in re.split(r"\n\s*\n", text):
        para = para.strip()
        if para:
            out.append("<p>" + md_inline(para).replace("\n", "<br>") + "</p>")
    return "\n".join(out)


def render_flags(raw: str) -> str:
    items = re.split(r"(?m)^(?=\d+\.\s)", raw)
    cards = []
    for it in items:
        it = it.strip()
        if not it:
            continue
        m = re.match(r"(\d+)\.\s*(.*)", it, re.S)
        if not m:
            continue
        num, rest = m.group(1), m.group(2).strip()
        cards.append(
            f'<div class="flag"><span class="flagnum">{num}</span>'
            f'<div class="flagbody">{md_block(rest)}</div></div>'
        )
    return "\n".join(cards)


# --- HTML assembly ----------------------------------------------------------
def chip(label, cls="chip"):
    return f'<span class="{cls}">{html.escape(label)}</span>'


def render_entry(e: Entry) -> str:
    sc = e.status["cls"]
    parts = [f'<span class="badge badge-{sc}">{html.escape(e.status["label"])}</span>']
    parts.append(f'<span class="etype etype-{e.etype.lower()}">{e.etype.title()}</span>')
    if e.date:
        prec = e.date["precision"]
        parts.append(f'<span class="chip date" title="precision: {prec}">'
                     f'{html.escape(e.date["display"])} <i>{prec}</i></span>')
    for kind, val in e.segments:
        if kind == "track":
            parts.append(chip(val["label"], "chip track"))
        elif kind == "pov":
            parts.append(chip(val["label"], "chip pov"))
        elif kind == "length":
            parts.append(chip(val["label"], "chip len"))
        elif kind == "context":
            parts.append(chip(val["label"], "chip ctx"))
        elif kind == "file":
            parts.append(chip(val["label"], "chip file"))
        elif kind == "link":
            parts.append(f'<a class="chip link" href="{html.escape(val["href"])}">'
                         f'{html.escape(val["text"])}</a>')
    head = " ".join(parts)
    body = md_block(e.body) if e.body else ""
    details = (f'<details><summary>notes</summary>{body}</details>' if body else "")
    return (f'<article class="card card-{sc}">'
            f'<h3>{html.escape(e.title)}</h3>'
            f'<div class="meta">{head}</div>{details}</article>')


def build_html(entries, flags_raw, source_name):
    nodes, w, h, baseline, pad_l, plot_w, span = beeswarm(entries)
    ticks = month_ticks(pad_l, plot_w, span)

    # beeswarm svg
    svg = [f'<svg viewBox="0 0 {w} {h}" class="swarm" role="img" '
           f'aria-label="beat density timeline">']
    svg.append(f'<line x1="{pad_l}" y1="{baseline}" x2="{pad_l+plot_w}" '
               f'y2="{baseline}" class="axis"/>')
    for x, lbl in ticks:
        svg.append(f'<line x1="{x:.1f}" y1="14" x2="{x:.1f}" y2="{baseline}" class="grid"/>')
        svg.append(f'<text x="{x:.1f}" y="{baseline+16}" class="mlabel">{lbl}</text>')
    for e, x, lvl in nodes:
        cy = baseline - 8 - lvl * 12
        color = STATUS_COLOR[e.status["cls"]]
        tip = f'{e.title}  ({e.date["display"]}, {e.date["precision"]})'
        svg.append(f'<circle cx="{x:.1f}" cy="{cy:.1f}" r="5" fill="{color}" '
                   f'class="dot" data-tip="{html.escape(tip, quote=True)}"/>')
    svg.append("</svg>")
    swarm = "\n".join(svg)

    # phase-grouped cards (document order of phases)
    order, seen = [], set()
    for e in entries:
        if e.phase not in seen:
            seen.add(e.phase)
            order.append(e.phase)
    sections = []
    for ph in order:
        group = [e for e in entries if e.phase == ph]
        if not group:
            continue
        sections.append(f'<section class="phase"><h2>{html.escape(ph)}</h2>'
                        + "\n".join(render_entry(e) for e in group) + "</section>")
    cards_html = "\n".join(sections)

    flags_html = render_flags(flags_raw) if flags_raw else ""
    n_total = len(entries)
    n_dated = sum(1 for e in entries if e.date)

    legend = "".join(
        f'<span class="lg"><i style="background:{STATUS_COLOR[c]}"></i>{lbl}</span>'
        for c, lbl in [("done", "Draft complete"), ("wip", "Draft in progress"),
                       ("arch", "Architecture complete"), ("todo", "Unwritten"),
                       ("event", "Event / not a scene"), ("unknown", "Unspecified")])

    return PAGE.format(
        source=html.escape(source_name), n_total=n_total, n_dated=n_dated,
        legend=legend, swarm=swarm, cards=cards_html,
        flags=flags_html,
        flags_section=(f'<section class="flags"><h2>Continuity Flags</h2>{flags_html}</section>'
                       if flags_html else ""),
    )


PAGE = """<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Chronology — With a Long Spoon</title>
<style>
  :root {{ --bg:#11141a; --panel:#1a1f29; --ink:#e7e9ee; --mut:#9aa3b2; --line:#2a313d; }}
  * {{ box-sizing:border-box; }}
  body {{ margin:0; background:var(--bg); color:var(--ink);
    font:15px/1.55 -apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Helvetica,Arial,sans-serif; }}
  header {{ padding:22px 28px 8px; }}
  h1 {{ margin:0 0 2px; font-size:22px; }}
  .sub {{ color:var(--mut); font-size:13px; }}
  .wrap {{ max-width:1140px; margin:0 auto; padding:0 28px 60px; }}
  .legend {{ display:flex; flex-wrap:wrap; gap:14px; margin:14px 0 6px; font-size:13px; color:var(--mut); }}
  .lg {{ display:flex; align-items:center; gap:6px; }}
  .lg i {{ width:12px; height:12px; border-radius:3px; display:inline-block; }}
  .panel {{ background:var(--panel); border:1px solid var(--line); border-radius:12px; padding:14px 16px; margin:10px 0 26px; }}
  svg.swarm {{ width:100%; height:auto; display:block; }}
  .swarm .axis {{ stroke:var(--line); stroke-width:1; }}
  .swarm .grid {{ stroke:#222936; stroke-width:1; }}
  .swarm .mlabel {{ fill:var(--mut); font-size:11px; text-anchor:middle; }}
  .swarm .dot {{ cursor:pointer; transition:r .08s; }}
  .swarm .dot:hover {{ r:7; stroke:#fff; stroke-width:1.5; }}
  #tip {{ position:fixed; pointer-events:none; background:#000; color:#fff; padding:5px 9px;
    border-radius:6px; font-size:12px; max-width:280px; opacity:0; transition:opacity .08s; z-index:9; }}
  .phase h2, .flags h2 {{ font-size:16px; color:var(--mut); text-transform:uppercase;
    letter-spacing:.06em; border-bottom:1px solid var(--line); padding-bottom:6px; margin:30px 0 14px; }}
  .card {{ background:var(--panel); border:1px solid var(--line); border-left:4px solid var(--line);
    border-radius:10px; padding:12px 15px; margin:9px 0; }}
  .card-done {{ border-left-color:#2e7d32; }}  .card-wip {{ border-left-color:#f9a825; }}
  .card-arch {{ border-left-color:#5c6bc0; }}  .card-todo {{ border-left-color:#9e9e9e; }}
  .card-event {{ border-left-color:#546e7a; }}  .card-unknown {{ border-left-color:#c0c0c0; }}
  .card h3 {{ margin:0 0 7px; font-size:16px; }}
  .meta {{ display:flex; flex-wrap:wrap; gap:6px; align-items:center; }}
  .badge {{ font-size:11px; font-weight:600; padding:2px 8px; border-radius:20px; color:#fff; }}
  .badge-done {{ background:#2e7d32; }} .badge-wip {{ background:#f9a825; color:#222; }}
  .badge-arch {{ background:#5c6bc0; }} .badge-todo {{ background:#9e9e9e; color:#222; }}
  .badge-event {{ background:#546e7a; }} .badge-unknown {{ background:#3a414e; color:var(--mut); }}
  .etype {{ font-size:11px; color:var(--mut); border:1px solid var(--line); border-radius:20px; padding:2px 8px; }}
  .chip {{ font-size:11.5px; color:var(--ink); background:#222936; border:1px solid var(--line);
    border-radius:6px; padding:2px 7px; text-decoration:none; }}
  .chip.date {{ background:#1d2733; }}  .chip.date i {{ color:var(--mut); font-style:normal; font-size:10px; }}
  .chip.track {{ color:#9fd3ff; }}  .chip.pov {{ color:#ffd59f; }}  .chip.file {{ color:#b6f0c4; font-family:ui-monospace,monospace; }}
  .chip.link {{ color:#c9b6ff; }}  .chip.link:hover {{ text-decoration:underline; }}
  .chip.ctx, .chip.len {{ color:var(--mut); }}
  details {{ margin-top:8px; }}  summary {{ cursor:pointer; color:var(--mut); font-size:12px; }}
  details p {{ margin:8px 0; }}  code {{ background:#222936; padding:1px 5px; border-radius:4px; font-size:13px; }}
  .wiki {{ color:#c9b6ff; }}  a {{ color:#9fd3ff; }}
  .flag {{ display:flex; gap:12px; background:var(--panel); border:1px solid var(--line);
    border-radius:10px; padding:12px 15px; margin:9px 0; }}
  .flagnum {{ flex:0 0 28px; height:28px; border-radius:50%; background:#2a313d; color:var(--ink);
    display:flex; align-items:center; justify-content:center; font-weight:700; font-size:13px; }}
  .flagbody p {{ margin:0 0 8px; }}  .flagbody p:last-child {{ margin:0; }}
</style></head>
<body>
<header>
  <h1>With a Long Spoon — Chronology</h1>
  <div class="sub">Generated from <code>{source}</code> · {n_total} entries · {n_dated} placed on the timeline · story order = list order</div>
</header>
<div class="wrap">
  <div class="legend">{legend}</div>
  <div class="panel">{swarm}</div>
  {cards}
  {flags_section}
</div>
<div id="tip"></div>
<script>
  var tip = document.getElementById('tip');
  document.querySelectorAll('.swarm .dot').forEach(function(d){{
    d.addEventListener('mousemove', function(e){{
      tip.textContent = d.getAttribute('data-tip');
      tip.style.left = (e.clientX + 14) + 'px';
      tip.style.top  = (e.clientY + 14) + 'px';
      tip.style.opacity = 1;
    }});
    d.addEventListener('mouseleave', function(){{ tip.style.opacity = 0; }});
  }});
</script>
</body></html>"""


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("input", nargs="?", default="meta/meta-plan-chronology.md")
    ap.add_argument("-o", "--out", default="chronology.html")
    args = ap.parse_args()

    src = Path(args.input)
    if not src.exists():
        sys.exit(f"input not found: {src}")
    entries, flags_raw = parse(src.read_text(encoding="utf-8"))
    htmlout = build_html(entries, flags_raw, src.name)
    Path(args.out).write_text(htmlout, encoding="utf-8")

    n_dated = sum(1 for e in entries if e.date)
    by_status = {}
    for e in entries:
        by_status[e.status["cls"]] = by_status.get(e.status["cls"], 0) + 1
    print(f"wrote {args.out}: {len(entries)} entries, {n_dated} dated, "
          f"status {by_status}", file=sys.stderr)
    # surface entries whose metadata produced no date and no status, so the
    # parser can be kept in sync as the doc grows.
    blind = [e.title for e in entries
             if not e.date and e.status["cls"] == "unknown"]
    if blind:
        print(f"  no date & no status ({len(blind)}): "
              + "; ".join(blind[:12]) + ("; ..." if len(blind) > 12 else ""),
              file=sys.stderr)


if __name__ == "__main__":
    main()
