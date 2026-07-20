#!/usr/bin/env python3
"""Generate a self-contained HTML view of meta-plan-chronology.md.

Parses the chronology's scene/vignette/event entries and their metadata line
(status, date, track, POV, files, links) and emits a single HTML file with
inline CSS+JS (zero external dependencies): a progress summary table (words,
pages at ~300 wpm, chapters, and reviewed counts, broken out by seasonal volume
— Fall/Spring/Summer — plus a grand total), a status-colored beeswarm timeline
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

# Review rounds are categorical, not a scale: a scene's pill color is its review
# round (= how many review dates it carries) so equal color reads as equal round
# at a glance. ColorBrewer "Set2" (qualitative), cycled for rounds beyond 8, with
# a neutral slate reserved for the not-yet-reviewed (round 0).
REVIEW_UNREVIEWED = "#4a5160"
REVIEW_PALETTE = ["#66c2a5", "#fc8d62", "#8da0cb", "#e78ac3",
                  "#a6d854", "#ffd92f", "#e5c494", "#b3b3b9"]


def review_color(rnd: int) -> str:
    if rnd <= 0:
        return REVIEW_UNREVIEWED
    return REVIEW_PALETTE[(rnd - 1) % len(REVIEW_PALETTE)]

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
        # The month usually rides on the right endpoint ("mid–late November",
        # "early–mid October"), so resolve it first and let the modifier-only
        # left ("mid", "early") borrow that month; fall back the other way for
        # left-anchored ranges ("Oct 5–10").
        rp = _parse_point(right)
        lp = _parse_point(left, fallback_month=rp[0] if rp else None)
        if not rp:
            rp = _parse_point(right, fallback_month=lp[0] if lp else None)
        if not lp or not rp:
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
# {{Chapter Title}} marks a reference to a chapter *by its title* (planning docs
# only) so titles are machine-distinguishable from same-word event/prose uses.
# The braces are display furniture: stripped for chip/beeswarm text (classify)
# and turned into a styled span in body prose (md_inline). See CLAUDE.md.
TITLE_MARK = re.compile(r"\{\{([^}]+)\}\}")


def classify(seg: str):
    """Return (kind, value-dict) for one metadata segment."""
    # Strip {{Title}} marks to plain text before classifying — the braces are a
    # tooling/disambiguation device, not display; the source file keeps them.
    s = TITLE_MARK.sub(r"\1", seg).strip()
    low = s.lower()
    if not s:
        return None
    m = LINK_RE.search(s)
    if m and not (ENDASH in s and _find_month(s)):
        return "link", {"text": m.group(1), "href": m.group(2)}
    if low.startswith("reviewed"):
        # ISO dates only (won't collide with the month-name story-date parser);
        # round = how many, last = most recent (ISO sorts chronologically).
        dates = re.findall(r"\d{4}-\d{2}-\d{2}", s)
        if dates:
            return "review", {"dates": dates, "round": len(dates), "last": max(dates)}
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
# The doc is partitioned into three seasonal volumes by inline divider lines
# ("**◆ VOLUME ONE — Fall** · ..."). We read the season word off the divider and
# carry it forward to the entries that follow, until the next divider.
VOLUME_RE = re.compile(r"VOLUME\s+\w+\s*[—–-]\s*([A-Za-z]+)")


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
        self.slug = None        # unique DOM id stem (assigned in build_html)
        self.scene_md = None    # embedded scene prose (done scenes only)
        self.review = None      # {dates, round, last} or None (0 reviews)
        self.season = None      # "Fall"/"Spring"/"Summer"/"Other" (VOLUME bucket)
        self.words = 0          # prose word count of the scene file (0 if none)

    def finalize(self, unknown_log):
        for kind, val in self.segments:
            if kind == "status":
                self.status = val
            elif kind == "date" and self.date is None:
                self.date = val
            elif kind == "review" and self.review is None:
                self.review = val
        if self.status is None:
            self.status = {"cls": "event" if self.etype == "EVENT" else "unknown",
                           "label": "—" if self.etype != "EVENT" else "Not a scene"}


def parse(md: str):
    lines = md.splitlines()
    entries = []
    phase = None
    season = None            # set by the most recent VOLUME divider
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
        vol = VOLUME_RE.search(line)
        if vol:
            season = vol.group(1).capitalize()
            continue
        ent = ENTRY_RE.match(line)
        if ent:
            flush()
            body_lines = []
            cur = Entry(ent.group(1), ent.group(2).strip(), phase or "")
            cur.season = season
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
        # Entries outside the three seasonal volumes — Pre-Novel (before the
        # first divider) and the trailing "Threaded Throughout" section (which
        # sits after VOLUME THREE and would otherwise inherit Summer) — bucket as
        # "Other" so the seasonal rows stay clean.
        ph = e.phase.lower()
        if e.season is None or ph.startswith("pre-novel") or ph.startswith("threaded"):
            e.season = "Other"

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
    text = TITLE_MARK.sub(r'<span class="title">\1</span>', text)
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
def slugify(title: str) -> str:
    s = re.sub(r"[^a-z0-9]+", "-", title.lower()).strip("-")
    return s or "beat"


# A scene's prose file is named in its metadata line — sometimes backticked
# (`the-bench.md`), sometimes path-qualified (`scenes/famished.md`), and
# sometimes tucked inside the status ("**Draft complete:** `scenes/rock.md`").
# Scan the raw line and take the first *.md that isn't a meta-* planning doc
# (the [detail]/[craft] links point at meta-condensed-*/meta-note-* files).
SCENE_MD_RE = re.compile(r"(?:scenes/)?([a-z0-9][a-z0-9-]*\.md)")


def scene_filename(meta_raw: str):
    for m in SCENE_MD_RE.finditer(meta_raw):
        name = m.group(1)
        if name.startswith("meta"):
            continue
        return name
    return None


WORDS_PER_PAGE = 300
HR_RE = re.compile(r"^([-*_])\1{2,}$")
HEADING_RE = re.compile(r"^#{1,6}\s")
ITALIC_LINE_RE = re.compile(r"^\*.+\*$")


def prose_word_count(text: str) -> int:
    """Whitespace-token count of a scene's prose only.

    Skips the manuscript furniture that isn't the story: ATX headings (the H1
    title), horizontal rules, and the leading italic editorial note that sits
    above the first '---'. Inline emphasis inside the prose is left in place
    (each '*word*' / '**word**' counts as its one token), which is close enough
    for an at-a-glance page count.
    """
    words = 0
    seen_rule = False
    for raw in text.split("\n"):
        line = raw.strip()
        if not line:
            continue
        if HR_RE.match(line):
            seen_rule = True
            continue
        if HEADING_RE.match(line):
            continue
        if not seen_rule and ITALIC_LINE_RE.match(line):
            continue  # leading italic editorial note (before the first rule)
        words += len(line.split())
    return words


def _pages(words: int) -> int:
    # round to nearest page; a mostly-full page still reads as "1".
    return (words + WORDS_PER_PAGE // 2) // WORDS_PER_PAGE


# Row order for the summary table: the three seasonal volumes, then the
# out-of-volume "Other" bucket, then the grand total.
STATS_SEASONS = ["Fall", "Spring", "Summer", "Other"]


def compute_stats(entries):
    """Aggregate chapter/word/review counts per season bucket + grand total.

    A "chapter" is a SCENE or VIGNETTE (EVENTs never count). Words come from the
    drafted prose file; undrafted chapters contribute 0. "Reviewed" means the
    entry carries at least one `reviewed:` date.
    """
    buckets = {s: {"chapters": 0, "words": 0, "rev_chapters": 0, "rev_words": 0}
               for s in STATS_SEASONS}
    for e in entries:
        if e.etype not in ("SCENE", "VIGNETTE"):
            continue
        b = buckets.get(e.season) or buckets["Other"]
        b["chapters"] += 1
        b["words"] += e.words
        if e.review:
            b["rev_chapters"] += 1
            b["rev_words"] += e.words
    total = {"chapters": 0, "words": 0, "rev_chapters": 0, "rev_words": 0}
    for s in STATS_SEASONS:
        for k in total:
            total[k] += buckets[s][k]
    return buckets, total


def render_stats(entries) -> str:
    buckets, total = compute_stats(entries)

    def row(label, d, cls=""):
        w, rw = d["words"], d["rev_words"]
        return (
            f'<tr class="{cls}"><th scope="row">{html.escape(label)}</th>'
            f'<td>{d["chapters"]}</td>'
            f'<td>{w:,}</td>'
            f'<td>{_pages(w)}</td>'
            f'<td>{d["rev_chapters"]}</td>'
            f'<td>{rw:,}</td>'
            f'<td>{_pages(rw)}</td></tr>'
        )

    body_rows = "".join(row(s, buckets[s]) for s in STATS_SEASONS
                        if buckets[s]["chapters"])
    total_row = row("Total", total, cls="stat-total")
    return (
        '<div class="panel statspanel"><table class="stats">'
        '<caption>Progress — words &amp; pages at ~300 words/page</caption>'
        '<thead><tr><th scope="col">Segment</th>'
        '<th scope="col">Chapters</th><th scope="col">Words</th>'
        '<th scope="col">Pages</th>'
        '<th scope="col" class="rev">Rev. ch.</th>'
        '<th scope="col" class="rev">Rev. words</th>'
        '<th scope="col" class="rev">Rev. pages</th></tr></thead>'
        f'<tbody>{body_rows}</tbody>'
        f'<tfoot>{total_row}</tfoot>'
        '</table></div>'
    )


def chip(label, cls="chip"):
    return f'<span class="{cls}">{html.escape(label)}</span>'


def render_entry(e: Entry) -> str:
    sc = e.status["cls"]
    label = html.escape(e.status["label"])
    if sc == "done" and e.scene_md:
        parts = [f'<span class="badge badge-done openable" role="button" tabindex="0" '
                 f'data-scene="{e.slug}" title="Read the scene">{label} ↗</span>']
    else:
        parts = [f'<span class="badge badge-{sc}">{label}</span>']
    parts.append(f'<span class="etype etype-{e.etype.lower()}">{e.etype.title()}</span>')
    if e.etype in ("SCENE", "VIGNETTE"):
        if e.review:
            rnd = e.review["round"]
            parts.append(
                f'<span class="chip review" style="background:{review_color(rnd)}" '
                f'title="review round {rnd} · {html.escape(", ".join(e.review["dates"]))}">'
                f'{html.escape(e.review["last"])}</span>')
        else:
            parts.append(f'<span class="chip review unreviewed" '
                         f'style="background:{REVIEW_UNREVIEWED}" '
                         f'title="not yet reviewed">unreviewed</span>')
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
    return (f'<article id="beat-{e.slug}" class="card card-{sc}">'
            f'<h3>{html.escape(e.title)}</h3>'
            f'<div class="meta">{head}</div>{details}</article>')


def build_html(entries, flags_raw, source_name, scene_dir=None):
    nodes, w, h, baseline, pad_l, plot_w, span = beeswarm(entries)
    # stable, unique DOM ids so beeswarm dots can target their cards; and, for
    # drafted scenes, pull the prose file in so the reader can render it.
    seen_slugs = {}
    for e in entries:
        base = slugify(e.title)
        n = seen_slugs.get(base, 0) + 1
        seen_slugs[base] = n
        e.slug = base if n == 1 else f"{base}-{n}"
        # Count words for any chapter whose prose file exists (not just "done" —
        # a WIP draft still has a length), and embed the prose for the reader
        # only when the scene is marked complete.
        if e.etype in ("SCENE", "VIGNETTE") and scene_dir is not None:
            fn = scene_filename(e.meta_raw)
            if fn and (scene_dir / fn).exists():
                text = (scene_dir / fn).read_text(encoding="utf-8")
                e.words = prose_word_count(text)
                if e.status["cls"] == "done":
                    e.scene_md = text
    # hidden raw-markdown sources the reader renders on demand; html.escape keeps
    # arbitrary prose inert, and .textContent decodes it back verbatim in JS.
    scene_srcs = "\n".join(
        f'<div class="scenesrc" id="src-{e.slug}" '
        f'data-title="{html.escape(e.title, quote=True)}" hidden>'
        f'{html.escape(e.scene_md)}</div>'
        for e in entries if e.scene_md)
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
                   f'class="dot" tabindex="0" role="link" '
                   f'data-target="beat-{e.slug}" '
                   f'data-tip="{html.escape(tip, quote=True)}"/>')
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
    reviewable = [e for e in entries if e.etype in ("SCENE", "VIGNETTE")]
    n_reviewed = sum(1 for e in reviewable if e.review)
    reviewed = f"{n_reviewed}/{len(reviewable)} reviewed"

    legend = "".join(
        f'<span class="lg"><i style="background:{STATUS_COLOR[c]}"></i>{lbl}</span>'
        for c, lbl in [("done", "Draft complete"), ("wip", "Draft in progress"),
                       ("arch", "Architecture complete"), ("todo", "Unwritten"),
                       ("event", "Event / not a scene"), ("unknown", "Unspecified")])

    stats_html = render_stats(entries)

    return PAGE.format(
        source=html.escape(source_name), n_total=n_total, n_dated=n_dated,
        reviewed=reviewed, stats=stats_html,
        legend=legend, swarm=swarm, cards=cards_html,
        flags=flags_html,
        flags_section=(f'<section class="flags"><h2>Continuity Flags</h2>{flags_html}</section>'
                       if flags_html else ""),
        reader_css=READER_CSS, reader_html=READER_HTML, reader_js=READER_JS,
        scene_srcs=scene_srcs,
    )


# --- fullscreen scene reader (opened from a "Draft complete" badge) ---------
# These three blocks are substituted into PAGE as *values*, so — unlike the
# rest of PAGE — their braces are literal and need no doubling.
READER_CSS = """
  #reader { position:fixed; inset:0; z-index:50; background:var(--bg); color:var(--ink);
    overflow-y:auto; overflow-x:hidden; scroll-behavior:smooth; }
  #reader[hidden] { display:none; }
  #reader-body { max-width:68ch; margin:0 auto; padding:88px 24px 40vh;
    font-size:18px; line-height:1.75; }
  #reader-body p { margin:0 0 1.15em; }
  #reader-body h1 { font-size:26px; margin:0 0 .7em; }
  #reader-body h2 { font-size:22px; margin:1.3em 0 .5em; }
  #reader-body h3 { font-size:19px; margin:1.3em 0 .5em; color:var(--mut); }
  #reader-body hr { border:none; border-top:1px solid var(--line); width:42%; margin:1.9em auto; }
  #reader-body blockquote { margin:1em 0; padding:.2em 1em; border-left:3px solid var(--line); color:var(--mut); }
  #reader-body em { font-style:italic; }  #reader-body strong { font-weight:700; }
  #reader-body code { background:#222936; padding:1px 5px; border-radius:4px; font-size:.9em; }
  #reader-body mark { background:#4a4522; color:inherit; border-radius:2px; }
  #reader-body mark.cur { background:#f9a825; color:#111; }
  @keyframes gotoflash { 0% { background:#3a4560; } 100% { background:transparent; } }
  #reader-body .goto-flash { animation:gotoflash 1.2s ease-out; }
  #reader-close { position:fixed; top:16px; left:16px; z-index:52; background:#5c6bc0; color:#fff;
    border-radius:22px; padding:8px 15px; font-size:13px; font-weight:600; cursor:pointer;
    box-shadow:0 3px 12px rgba(0,0,0,.5); }
  #reader-close:hover { background:#6d7bd0; }
  #reader-title { position:fixed; top:19px; left:50%; transform:translateX(-50%); z-index:51;
    color:var(--mut); font-size:13px; pointer-events:none; max-width:56vw;
    overflow:hidden; white-space:nowrap; text-overflow:ellipsis; }
  #reader-cmd { position:fixed; bottom:0; left:0; right:0; z-index:52; display:none;
    background:#000; color:var(--ink); font:14px/1.7 ui-monospace,Menlo,Consolas,monospace;
    padding:6px 14px; border-top:1px solid var(--line); }
  #reader-cmd.on { display:block; }
  #reader-cmd-info { color:var(--mut); margin-left:14px; }
  .badge.openable { cursor:pointer; }
  .badge.openable:hover { filter:brightness(1.14); }"""

READER_HTML = """
<div id="reader" tabindex="-1" hidden aria-hidden="true">
  <div id="reader-close" role="button" tabindex="0" title="Close (Esc)">&#10005; Close</div>
  <div id="reader-title"></div>
  <div id="reader-body"></div>
  <div id="reader-cmd"><span id="reader-cmd-prefix"></span><span id="reader-cmd-buf"></span><span id="reader-cmd-info"></span></div>
</div>"""

READER_JS = r"""
(function(){
  var reader = document.getElementById('reader');
  var body = document.getElementById('reader-body');
  var titleEl = document.getElementById('reader-title');
  var closeBtn = document.getElementById('reader-close');
  var cmd = document.getElementById('reader-cmd');
  var cmdPrefix = document.getElementById('reader-cmd-prefix');
  var cmdBuf = document.getElementById('reader-cmd-buf');
  var cmdInfo = document.getElementById('reader-cmd-info');
  var savedScroll = 0, mode = 'normal', cmdType = '', buffer = '';
  var marks = [], curMatch = -1, src = '';
  var scrollMem = {}, curSlug = null;   // per-scene reading position, by slug

  function escHtml(s){ return s.replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;'); }
  function inline(s){
    s = escHtml(s);
    s = s.replace(/\*\*([^*]+)\*\*/g, '<strong>$1</strong>');
    s = s.replace(/(^|[^*])\*([^*]+)\*/g, '$1<em>$2</em>');
    s = s.replace(/`([^`]+)`/g, '<code>$1</code>');
    s = s.replace(/\[([^\]]+)\]\(([^)]+)\)/g, '<a href="$2">$1</a>');
    return s;
  }
  // Each non-blank source line becomes one block tagged with its 1-based line
  // number, so ':N' lands where line N would in the .md file (blank lines are
  // absent, so goto falls back to the nearest earlier line).
  function renderMarkdown(text){
    var lines = text.split('\n'), out = [];
    for (var i=0; i<lines.length; i++){
      var ln = i+1, t = lines[i].trim();
      if (t === '') continue;
      var h = t.match(/^(#{1,6})\s+(.*)$/);
      if (h){ var lv=h[1].length; out.push('<h'+lv+' data-line="'+ln+'">'+inline(h[2])+'</h'+lv+'>'); continue; }
      if (/^([-*_])\1\1+$/.test(t)){ out.push('<hr data-line="'+ln+'">'); continue; }
      if (t.charAt(0) === '>'){ out.push('<blockquote data-line="'+ln+'">'+inline(t.replace(/^>\s?/,''))+'</blockquote>'); continue; }
      out.push('<p data-line="'+ln+'">'+inline(t)+'</p>');
    }
    return out.join('\n');
  }

  function openReader(slug){
    var el = document.getElementById('src-'+slug);
    if (!el) return;
    savedScroll = window.scrollY || window.pageYOffset || 0;
    curSlug = slug;
    src = el.textContent;
    titleEl.textContent = el.getAttribute('data-title') || '';
    body.innerHTML = renderMarkdown(src);
    marks = []; curMatch = -1; buffer = ''; mode = 'normal'; hideCmd();
    reader.hidden = false; reader.setAttribute('aria-hidden','false');
    document.body.style.overflow = 'hidden';
    // restore this scene's own last position (top the first time), instantly —
    // no smooth animation across an unrelated prior scroll.
    reader.style.scrollBehavior = 'auto';
    reader.scrollTop = scrollMem[slug] || 0;
    reader.style.scrollBehavior = '';
    reader.focus();
  }
  function closeReader(){
    if (curSlug !== null) scrollMem[curSlug] = reader.scrollTop;
    reader.hidden = true; reader.setAttribute('aria-hidden','true');
    document.body.style.overflow = '';
    hideCmd(); mode = 'normal'; buffer = '';
    window.scrollTo(0, savedScroll);
    curSlug = null;
  }

  function showCmd(type){
    mode = 'cmd'; cmdType = type; buffer = '';
    cmdPrefix.textContent = type; cmdBuf.textContent = ''; cmdInfo.textContent = '';
    cmd.classList.add('on');
  }
  function hideCmd(){ cmd.classList.remove('on'); if (mode === 'cmd') mode = 'normal'; }

  function flashEl(el){ el.classList.remove('goto-flash'); void el.offsetWidth; el.classList.add('goto-flash'); }
  function gotoLine(n){
    if (!n || n < 1) return;
    var els = body.querySelectorAll('[data-line]'), best = null, exact = null;
    for (var i=0; i<els.length; i++){
      var l = parseInt(els[i].getAttribute('data-line'), 10);
      if (l === n){ exact = els[i]; break; }
      if (l < n){ best = els[i]; } else { if (!best) best = els[i]; break; }
    }
    var target = exact || best;
    if (target){ target.scrollIntoView({block:'center'}); flashEl(target); }
  }

  function search(q){
    body.innerHTML = renderMarkdown(src);   // drop old marks
    marks = []; curMatch = -1;
    if (!q){ cmdInfo.textContent = ''; return; }
    var ci = (q === q.toLowerCase());        // smartcase
    var needle = ci ? q.toLowerCase() : q;
    var walker = document.createTreeWalker(body, NodeFilter.SHOW_TEXT, null), nodes = [], node;
    while ((node = walker.nextNode())) nodes.push(node);
    for (var i=0; i<nodes.length; i++){
      var tn = nodes[i], text = tn.nodeValue, hay = ci ? text.toLowerCase() : text;
      var idx = hay.indexOf(needle);
      if (idx === -1) continue;
      var frag = document.createDocumentFragment(), pos = 0;
      while (idx !== -1){
        if (idx > pos) frag.appendChild(document.createTextNode(text.slice(pos, idx)));
        var mk = document.createElement('mark');
        mk.textContent = text.slice(idx, idx + q.length);
        frag.appendChild(mk); marks.push(mk);
        pos = idx + q.length; idx = hay.indexOf(needle, pos);
      }
      if (pos < text.length) frag.appendChild(document.createTextNode(text.slice(pos)));
      tn.parentNode.replaceChild(frag, tn);
    }
    if (marks.length){ curMatch = 0; showCur(true); }
    cmdInfo.textContent = marks.length ? (marks.length + ' matches') : 'no matches';
  }
  function showCur(scroll){
    for (var i=0; i<marks.length; i++) marks[i].classList.toggle('cur', i === curMatch);
    if (scroll && curMatch >= 0 && marks[curMatch]) marks[curMatch].scrollIntoView({block:'center'});
  }
  function nextMatch(dir){
    if (!marks.length) return;
    curMatch = (curMatch + dir + marks.length) % marks.length;
    showCur(true);
  }

  document.addEventListener('keydown', function(e){
    if (reader.hidden) return;
    if (mode === 'cmd'){
      if (e.key === 'Escape'){ e.preventDefault(); hideCmd(); return; }
      if (e.key === 'Enter'){
        e.preventDefault();
        if (cmdType === ':') gotoLine(parseInt(buffer, 10));
        hideCmd(); return;
      }
      if (e.key === 'Backspace'){
        e.preventDefault();
        buffer = buffer.slice(0, -1); cmdBuf.textContent = buffer;
        if (cmdType === '/') search(buffer);
        return;
      }
      if (e.key.length === 1 && !e.ctrlKey && !e.metaKey && !e.altKey){
        if (cmdType === ':' && !/[0-9]/.test(e.key)){ e.preventDefault(); return; }
        e.preventDefault();
        buffer += e.key; cmdBuf.textContent = buffer;
        if (cmdType === '/') search(buffer);
        return;
      }
      return;
    }
    if (e.key === 'Escape'){ e.preventDefault(); closeReader(); return; }
    if (e.key === ':'){ e.preventDefault(); showCmd(':'); return; }
    if (e.key === '/'){ e.preventDefault(); showCmd('/'); return; }
    if (e.key === 'n'){ e.preventDefault(); nextMatch(1); return; }
    if (e.key === 'N'){ e.preventDefault(); nextMatch(-1); return; }
  });

  document.querySelectorAll('.badge.openable').forEach(function(b){
    function open(){ openReader(b.getAttribute('data-scene')); }
    b.addEventListener('click', open);
    b.addEventListener('keydown', function(e){ if (e.key === 'Enter' || e.key === ' '){ e.preventDefault(); open(); } });
  });
  closeBtn.addEventListener('click', closeReader);
  closeBtn.addEventListener('keydown', function(e){ if (e.key === 'Enter' || e.key === ' '){ e.preventDefault(); closeReader(); } });
})();"""


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
  .statspanel {{ overflow-x:auto; }}
  table.stats {{ width:100%; border-collapse:collapse; font-size:13px; }}
  table.stats caption {{ text-align:left; color:var(--mut); font-size:12px;
    text-transform:uppercase; letter-spacing:.06em; padding:0 0 10px; }}
  table.stats th, table.stats td {{ padding:7px 10px; text-align:right; white-space:nowrap; }}
  table.stats thead th {{ color:var(--mut); font-weight:600; font-size:11px;
    text-transform:uppercase; letter-spacing:.04em; border-bottom:1px solid var(--line); }}
  table.stats thead th.rev {{ color:#9fd3ff; }}
  table.stats th[scope="row"] {{ text-align:left; color:var(--ink); font-weight:600; }}
  table.stats tbody td {{ color:var(--ink); font-variant-numeric:tabular-nums; }}
  table.stats tbody tr:hover {{ background:#1d2733; }}
  table.stats tfoot th, table.stats tfoot td {{ border-top:2px solid var(--line);
    font-weight:700; font-variant-numeric:tabular-nums; padding-top:9px; }}
  table.stats td:nth-child(5), table.stats td:nth-child(6), table.stats td:nth-child(7) {{ color:var(--mut); }}
  table.stats tfoot td {{ color:var(--ink) !important; }}
  svg.swarm {{ width:100%; height:auto; display:block; }}
  .swarm .axis {{ stroke:var(--line); stroke-width:1; }}
  .swarm .grid {{ stroke:#222936; stroke-width:1; }}
  .swarm .mlabel {{ fill:var(--mut); font-size:11px; text-anchor:middle; }}
  .swarm .dot {{ cursor:pointer; transition:r .08s; }}
  .swarm .dot:hover {{ r:7; stroke:#fff; stroke-width:1.5; }}
  .swarm .dot.ping {{ animation:ping 1s ease-out; }}
  @keyframes ping {{ 0% {{ stroke:#fff; stroke-width:6; }} 100% {{ stroke-width:0; }} }}
  #backtop {{ position:fixed; right:20px; bottom:20px; z-index:20; display:none;
    background:#5c6bc0; color:#fff; border:none; border-radius:22px; padding:9px 16px;
    font-size:13px; font-weight:600; cursor:pointer; box-shadow:0 3px 12px rgba(0,0,0,.4); }}
  #backtop:hover {{ background:#6d7bd0; }}
  #backtop.show {{ display:block; }}
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
  .card {{ scroll-margin-top:16px; }}
  .card.flash {{ animation:flash 1.2s ease-out; }}
  @keyframes flash {{ 0% {{ background:#26313f; border-left-color:#9fd3ff; }} 100% {{ background:var(--panel); }} }}
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
  .chip.review {{ color:#1a1f29; font-weight:600; border-color:transparent; }}
  .chip.review.unreviewed {{ color:#cdd3dd; font-weight:500; }}
  details {{ margin-top:8px; }}  summary {{ cursor:pointer; color:var(--mut); font-size:12px; }}
  details p {{ margin:8px 0; }}  code {{ background:#222936; padding:1px 5px; border-radius:4px; font-size:13px; }}
  .wiki {{ color:#c9b6ff; }}  .title {{ color:#e7c9a0; font-style:italic; }}  a {{ color:#9fd3ff; }}
  .flag {{ display:flex; gap:12px; background:var(--panel); border:1px solid var(--line);
    border-radius:10px; padding:12px 15px; margin:9px 0; }}
  .flagnum {{ flex:0 0 28px; height:28px; border-radius:50%; background:#2a313d; color:var(--ink);
    display:flex; align-items:center; justify-content:center; font-weight:700; font-size:13px; }}
  .flagbody p {{ margin:0 0 8px; }}  .flagbody p:last-child {{ margin:0; }}
{reader_css}
</style></head>
<body>
<header>
  <h1>With a Long Spoon — Chronology</h1>
  <div class="sub">Generated from <code>{source}</code> · {n_total} entries · {n_dated} placed on the timeline · {reviewed} · story order = list order</div>
</header>
<div class="wrap">
  {stats}
  <div class="legend">{legend}</div>
  <div class="panel" id="swarmpanel">{swarm}</div>
  {cards}
  {flags_section}
</div>
<div id="tip"></div>
<button id="backtop" aria-label="Back to timeline">&#8593; Timeline</button>
<script>
  var tip = document.getElementById('tip');
  var backtop = document.getElementById('backtop');
  var lastDot = null;
  document.querySelectorAll('.swarm .dot').forEach(function(d){{
    d.addEventListener('mousemove', function(e){{
      tip.textContent = d.getAttribute('data-tip');
      tip.style.left = (e.clientX + 14) + 'px';
      tip.style.top  = (e.clientY + 14) + 'px';
      tip.style.opacity = 1;
    }});
    d.addEventListener('mouseleave', function(){{ tip.style.opacity = 0; }});
    function goToCard(){{
      var card = document.getElementById(d.getAttribute('data-target'));
      if (!card) return;
      tip.style.opacity = 0;
      var det = card.querySelector('details'); if (det) det.open = true;
      card.scrollIntoView({{behavior:'smooth', block:'start'}});
      card.classList.remove('flash'); void card.offsetWidth; card.classList.add('flash');
      lastDot = d; backtop.classList.add('show');
    }}
    d.addEventListener('click', goToCard);
    d.addEventListener('keydown', function(e){{
      if (e.key === 'Enter' || e.key === ' ') {{ e.preventDefault(); goToCard(); }}
    }});
  }});
  backtop.addEventListener('click', function(){{
    var panel = document.getElementById('swarmpanel');
    panel.scrollIntoView({{behavior:'smooth', block:'start'}});
    backtop.classList.remove('show');
    if (lastDot) {{ lastDot.classList.remove('ping'); void lastDot.getBoundingClientRect(); lastDot.classList.add('ping'); }}
  }});
</script>
{reader_html}
{scene_srcs}
<script>{reader_js}</script>
</body></html>"""


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("input", nargs="?", default="meta/meta-plan-chronology.md")
    ap.add_argument("-o", "--out", default="chronology.html")
    args = ap.parse_args()

    src = Path(args.input)
    if not src.exists():
        sys.exit(f"input not found: {src}")
    # scenes/ sits beside meta/ at the repo root; resolve it from the input's
    # location so an absolute INPUT path still finds the prose, with a CWD fallback.
    scene_dir = src.resolve().parent.parent / "scenes"
    if not scene_dir.is_dir():
        scene_dir = Path("scenes")
    entries, flags_raw = parse(src.read_text(encoding="utf-8"))
    htmlout = build_html(entries, flags_raw, src.name, scene_dir=scene_dir)
    Path(args.out).write_text(htmlout, encoding="utf-8")

    n_dated = sum(1 for e in entries if e.date)
    by_status = {}
    for e in entries:
        by_status[e.status["cls"]] = by_status.get(e.status["cls"], 0) + 1
    print(f"wrote {args.out}: {len(entries)} entries, {n_dated} dated, "
          f"status {by_status}", file=sys.stderr)
    # surface every entry that produced no date: these are absent from the
    # beeswarm timeline, so the list is the drift check when the doc grows.
    undated = [e.title for e in entries if not e.date]
    if undated:
        print(f"  undated, absent from the timeline ({len(undated)}): "
              + "; ".join(undated), file=sys.stderr)
    # "Draft complete" but no prose embedded: the metadata line cites no scene
    # file (or the file is missing), so the badge won't open a reader. Surface
    # it so the chronology's file reference can be added.
    no_prose = [e.title for e in entries
                if e.status["cls"] == "done" and not e.scene_md]
    if no_prose:
        print(f"  draft-complete but no readable scene file ({len(no_prose)}): "
              + "; ".join(no_prose), file=sys.stderr)


if __name__ == "__main__":
    main()
