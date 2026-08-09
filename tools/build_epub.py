#!/usr/bin/env python3
"""Build the Volume 1 test epub from scenes/ in chronology order.

Implements the packaging spec in meta/meta-blurb.md ("Test-epub assembly"):

    cover -> blurb page (BEFORE the title page) -> title page -> copyright
    -> chapters (Volume One, story order = chronology list order)
    -> note to test readers -> metadata

Sources, all parsed at build time so the docs stay authoritative:
  - meta/meta-plan-chronology.md  chapter inventory + order (the VOLUME ONE
                                  section; SCENE/VIGNETTE entries only)
  - meta/meta-blurb.md            blurb page text (## Test-epub blurb) and the
                                  metadata description (## Explicit / ### Short)
  - scenes/<slug>.md              prose (H1 title and the leading italic
                                  editorial note above the first --- are
                                  stripped; interior --- become scene breaks)
  - images/cover.png              cover image — a symlink naming the currently
                                  chosen cover asset (retarget the link to
                                  switch covers; no builder change needed)

No decorative page backgrounds: CSS background images fight reader theming
and pagination (dark-mode contrast, Calibre partial/inconsistent renders) —
parchment treatment dropped 2026-07-27.

Deterministic: same inputs -> same output bytes (fixed zip timestamps; the
package UUID is derived from the content; dcterms:modified comes from the
newest input commit), so rebuilds are diffable. --reader is the deliberate
exception: each recipient's copy is stamped with their name, so two readers'
copies of identical prose differ by design. A rebuild for the *same* reader
is still reproducible.

Usage:
    tools/build_epub.py
    tools/build_epub.py --list          # preview the chapter roster, no build
    tools/build_epub.py --reader "Jane Doe <jane@example.com>"
Defaults: cover images/cover.png, output build/a-polite-invitation.epub
(the date/sha build stamp lives on the copyright page, not in the filename).
A Volume One chapter whose prose file is missing aborts the build (--allow-missing
to override) — a test reader must never receive a silently incomplete book.
"""
from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import re
import subprocess
import sys
import uuid
import zipfile
from pathlib import Path

VOLUME_TITLE = "A Polite Invitation"
BOOK_TITLE = "A Polite Invitation (With a Long Spoon, Book 1)"
SERIES_NAME = "With a Long Spoon"
SERIES_INDEX = "1"
LANGUAGE = "en-US"
COPYRIGHT_YEAR = "2026"
# One line only on the copyright page besides boilerplate (spec: no itemized
# content-warning list for the test round; the blurb self-selects).
COPYRIGHT_NOTICE = "An erotic novel, for adult readers."
DRAFT_NOTICE = "Test-reader draft — please don’t share or distribute."
WEBSITE = "helenriversbooks.com"
CONTACT_EMAIL = "helen@helenriversbooks.com"

# Back matter (spec: asks live here, never up front — first read unshaped,
# reflection directed). Edit freely; this text lives nowhere else.
NOTE_TO_READERS_TITLE = "A Note to Test Readers"


def note_to_readers(reader=None):
    """The back-matter note, addressed to this copy's recipient if there is one.

    Personalised deliberately: the greeting is warmer, and it puts the
    identification somewhere a reader actually reads, rather than on a
    copyright page they skip.
    """
    greeting = "Thank you for reading."
    if reader and reader["first_name"]:
        greeting = f"{reader['first_name']}, thank you for reading."
    paras = [
        f"{greeting} This is a test draft of Book One — you are "
        "among its first readers, and what you noticed matters more to me than "
        "what you think I want to hear.",
        "Two questions I care about most:",
        "• Did you keep falling for Pace — and enjoying the brunches — "
        "even though you knew?",
        "• Was there a point where the warmth curdled?",
        "Beyond those: where you put the book down, what you skipped, what you "
        "didn’t believe, and anything that pulled you out. All of it helps.",
        f"Write to me at {CONTACT_EMAIL}. — Helen Rivers",
    ]
    if reader:
        paras.append(f"This copy was prepared for {reader['label']}. "
                     "Please don’t pass it on.")
    return paras

MIDDOT = "·"
ENTRY_RE = re.compile(r"^###\s+\[(SCENE|VIGNETTE|EVENT)\]\s+(.*)$")
VOLUME_RE = re.compile(r"VOLUME\s+(\w+)\s*[—–-]")
# Same convention as chronology_html.py: the prose file is the first *.md in
# the metadata line that isn't a meta-* planning doc.
SCENE_MD_RE = re.compile(r"(?:scenes/)?([a-z0-9][a-z0-9-]*\.md)")
HR_RE = re.compile(r"^([-*_])\1{2,}$")


EMAIL_RE = re.compile(r"[^<>\s@]+@[^<>\s@]+\.[^<>\s@]+")


def slugify(s: str) -> str:
    s = re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")
    return s or "reader"


def parse_reader(spec: str) -> dict:
    """'Jane Doe <jane@ex.com>' | 'jane@ex.com' | 'Jane Doe' -> reader dict.

    A reader build is per-recipient by design, so it is deliberately NOT
    byte-identical to another reader's copy of the same prose — the whole
    point is that the copies differ. Builds for the *same* reader from the
    same inputs remain reproducible.
    """
    spec = spec.strip()
    if not spec:
        sys.exit("--reader was empty")
    m = EMAIL_RE.search(spec)
    email = m.group(0) if m else ""
    name = (spec[:m.start()] + spec[m.end():] if m else spec)
    name = name.replace("<", " ").replace(">", " ").strip(" ,;")
    name = re.sub(r"\s+", " ", name).strip()
    if not name and not email:
        sys.exit(f"could not parse --reader {spec!r}")
    if name and email:
        label = f"{name} ({email})"
    else:
        label = name or email
    return {"name": name, "email": email, "label": label,
            "first_name": name.split(" ")[0] if name else "",
            "slug": slugify(name) if name else slugify(email.split("@")[0])}


def canonical_title(raw: str) -> str:
    """Entry heading -> display title (drop any trailing parenthetical)."""
    return re.sub(r"\s*\([^)]*\)\s*$", "", raw).strip()


def parse_volume_one(md: str):
    """Return [(title, scene_filename_or_None), ...] in story order."""
    chapters = []
    volume = None
    pending = None  # (title,) awaiting its metadata line
    for line in md.splitlines():
        v = VOLUME_RE.search(line)
        if v:
            volume = v.group(1).upper()
            pending = None
            continue
        m = ENTRY_RE.match(line)
        if m:
            pending = None
            if volume == "ONE" and m.group(1) in ("SCENE", "VIGNETTE"):
                pending = canonical_title(m.group(2))
            continue
        if pending and line.strip().startswith("*") and MIDDOT in line:
            fn = None
            for fm in SCENE_MD_RE.finditer(line):
                if not fm.group(1).startswith("meta"):
                    fn = fm.group(1)
                    break
            chapters.append((pending, fn))
            pending = None
    return chapters


# --- blurb doc extraction ----------------------------------------------------
def _section(md: str, heading: str) -> str:
    """Text of a ## / ### section, up to the next heading of <= that level."""
    lines = md.splitlines()
    level = heading.split(" ", 1)[0].count("#")
    out, active = [], False
    for line in lines:
        if line.strip().startswith(heading):
            active = True
            continue
        if active and re.match(r"^#{1,%d}\s" % level, line):
            break
        if active:
            out.append(line)
    return "\n".join(out)


def blockquote_paragraphs(section: str):
    paras = []
    for line in section.splitlines():
        s = line.strip()
        if s.startswith(">"):
            s = s.lstrip(">").strip()
            if s:
                paras.append(s)
    return paras


def strip_emphasis(text: str) -> str:
    text = re.sub(r"\*\*([^*]+)\*\*", r"\1", text)
    text = re.sub(r"\*([^*]+)\*", r"\1", text)
    return text


def load_blurb(blurb_path: Path):
    """-> (body_paragraphs, tagline, comp_line, metadata_description)."""
    md = blurb_path.read_text(encoding="utf-8")
    paras = blockquote_paragraphs(_section(md, "## Test-epub blurb"))
    if len(paras) < 4:
        sys.exit(f"could not parse the Test-epub blurb section of {blurb_path} "
                 f"(expected >=4 blockquote paragraphs, got {len(paras)})")
    body, tagline, comp = paras[:-2], paras[-2], paras[-1]
    short = blockquote_paragraphs(_section(_section(md, "## Explicit"),
                                           "### Short"))
    if not short:
        sys.exit(f"could not parse the Explicit/Short blurb in {blurb_path}")
    return body, tagline, comp, strip_emphasis(" ".join(short))


# --- markdown -> xhtml --------------------------------------------------------
def esc(s: str) -> str:
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def inline(s: str) -> str:
    s = esc(s)
    s = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", s)
    s = re.sub(r"\*([^*]+)\*", r"<em>\1</em>", s)
    return s


def scene_body_html(text: str) -> str:
    """Scene .md -> chapter body html.

    Drops the H1 title and the leading italic editorial note above the first
    horizontal rule (and that rule itself); interior rules render as scene
    breaks. Each non-blank source line is one paragraph (house prose format).
    """
    out = []
    seen_rule = False
    started = False  # first prose paragraph emitted
    for raw in text.split("\n"):
        line = raw.strip()
        if not line:
            continue
        if HR_RE.match(line):
            if not seen_rule:
                seen_rule = True
                continue
            out.append('<p class="break">* * *</p>')
            started = False  # paragraph after a break is unindented
            continue
        if line.startswith("#"):
            continue
        if not seen_rule and re.match(r"^\*.+\*$", line):
            continue  # editorial note before the first rule
        cls = "" if started else ' class="first"'
        out.append(f"<p{cls}>{inline(line)}</p>")
        started = True
    return "\n".join(out)


XHTML = """<?xml version="1.0" encoding="utf-8"?>
<!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:epub="http://www.idpf.org/2007/ops" xml:lang="{lang}">
<head><title>{title}</title><link rel="stylesheet" type="text/css" href="style.css"/></head>
<body{bodyattr}>
{body}
</body>
</html>
"""

CSS = """\
body { margin: 1em; }
h1.chapter { text-align: center; font-size: 1.4em; margin: 3em 0 0.4em; }
p.chapnum { text-align: center; font-size: 0.85em; letter-spacing: 0.15em;
  text-transform: uppercase; margin: 0; color: #555; }
div.chapter-open { margin-bottom: 2.5em; }
p { margin: 0; text-indent: 1.3em; text-align: justify; }
p.first { text-indent: 0; }
p.break { text-indent: 0; text-align: center; margin: 1.2em 0; }
/* front & back matter */
.cover { text-align: center; margin: 0; padding: 0; }
.cover img { max-width: 100%; max-height: 100%; }
.blurb p, .frontmatter p, .backmatter p { text-indent: 0; text-align: left;
  margin: 0 0 1em; }
.blurb .tagline { text-align: center; font-style: italic; margin: 2.5em 0; }
.blurb .comp { font-size: 0.85em; font-style: italic; margin-top: 3em; }
.titlepage { text-align: center; margin-top: 20%; }
.titlepage h1 { font-size: 1.9em; letter-spacing: 0.06em; text-align: center; }
.titlepage .series { font-size: 0.8em; letter-spacing: 0.18em; margin: 0 0 3em; text-indent: 0; text-align: center; }
.titlepage h1 { margin-bottom: 4em; }
.titlepage .author { font-size: 1.1em; text-indent: 0; text-align: center; }
.copyright { margin-top: 60%; font-size: 0.85em; }
.copyright p { text-align: center; text-indent: 0; margin: 0 0 0.8em; }
.buildid { font-size: 0.8em; opacity: 0.7; }
.prepared { font-style: italic; }
.backmatter h1 { font-size: 1.2em; margin: 3em 0 1.5em; text-align: center; }
"""


def page(title: str, body: str, lang: str = LANGUAGE, bodyattr: str = "") -> str:
    return XHTML.format(title=esc(title), body=body, lang=lang,
                        bodyattr=bodyattr)


# --- epub assembly -------------------------------------------------------------
def build(chapters, blurb, cover_path: Path, author: str, out_path: Path,
          modified: str, build_id: str = "", reader=None):
    body_paras, tagline, comp, description = blurb
    files = []  # (id, href, media-type, properties, content_bytes, in_spine)

    def add(fid, href, mt, content, props=None, spine=True):
        data = content.encode("utf-8") if isinstance(content, str) else content
        files.append((fid, href, mt, props, data, spine))

    cover_ext = cover_path.suffix.lower().lstrip(".")
    cover_mt = {"png": "image/png", "jpg": "image/jpeg",
                "jpeg": "image/jpeg"}.get(cover_ext)
    if not cover_mt:
        sys.exit(f"unsupported cover image type: {cover_path}")
    add("cover-image", f"cover.{cover_ext}", cover_mt, cover_path.read_bytes(),
        props="cover-image", spine=False)

    # No decorative page background: CSS background images fight reader
    # theming (white dark-mode text over a pale image) and pagination
    # (partial/inconsistent renders in Calibre, bleed in Apple Books).
    add("cover", "cover.xhtml", "application/xhtml+xml", page(
        "Cover",
        f'<div class="cover"><img src="cover.{cover_ext}" '
        f'alt="{esc(BOOK_TITLE)}"/></div>'))

    # Blurb page — before the title page (simulates the retail listing).
    blurb_html = ['<div class="blurb frontmatter">']
    blurb_html += [f"<p>{inline(p)}</p>" for p in body_paras]
    blurb_html.append(f'<p class="tagline">{inline(tagline)}</p>')
    blurb_html.append(f'<p class="comp">{inline(comp)}</p>')
    blurb_html.append("</div>")
    add("blurb", "blurb.xhtml", "application/xhtml+xml",
        page("About This Book", "\n".join(blurb_html)))

    add("titlepage", "titlepage.xhtml", "application/xhtml+xml", page(
        BOOK_TITLE,
        '<div class="titlepage frontmatter">'
        f'<p class="series">{esc(SERIES_NAME.upper())} · BOOK ONE</p>'
        f"<h1>{esc(VOLUME_TITLE)}</h1>"
        f'<p class="author">{esc(author)}</p></div>'))

    add("copyright", "copyright.xhtml", "application/xhtml+xml", page(
        "Copyright",
        '<div class="copyright frontmatter">'
        f"<p>Copyright © {COPYRIGHT_YEAR} {esc(author)}. "
        "All rights reserved.</p>"
        "<p>This is a work of fiction. Names, characters, places, and "
        "incidents are products of the author’s imagination or are used "
        "fictitiously. All characters depicted are adults.</p>"
        "<p>This book contains explicit sexual content and is intended "
        "for adult readers.</p>"
        f"<p>{esc(COPYRIGHT_NOTICE)}</p>"
        f"<p>{esc(WEBSITE)}</p>"
        f"<p>{esc(DRAFT_NOTICE)}</p>"
        + (f'<p class="prepared">Prepared for {esc(reader["label"])}.</p>'
           if reader else "")
        + (f'<p class="buildid">Draft {esc(build_id)}</p>' if build_id else "")
        + "</div>"))

    toc = []  # (href, label) — chapters + back matter
    for i, (title, path) in enumerate(chapters, 1):
        href = f"ch{i:03d}.xhtml"
        body = (f'<div class="chapter-open"><p class="chapnum">Chapter {i}'
                f"</p><h1 class=\"chapter\">{esc(title)}</h1></div>\n"
                + scene_body_html(path.read_text(encoding="utf-8")))
        add(f"ch{i:03d}", href, "application/xhtml+xml", page(title, body))
        toc.append((href, f"{i} · {title}"))

    note = ['<div class="backmatter">',
            f"<h1>{esc(NOTE_TO_READERS_TITLE)}</h1>"]
    note += [f"<p>{inline(p)}</p>" for p in note_to_readers(reader)]
    note.append("</div>")
    add("note", "note.xhtml", "application/xhtml+xml",
        page(NOTE_TO_READERS_TITLE, "\n".join(note)))
    toc.append(("note.xhtml", NOTE_TO_READERS_TITLE))

    add("css", "style.css", "text/css", CSS, spine=False)

    # nav (epub3) + ncx (older readers)
    nav_items = "\n".join(f'<li><a href="{h}">{esc(t)}</a></li>'
                          for h, t in toc)
    nav = page("Contents", f"""<nav epub:type="toc" id="toc"><h1>Contents</h1>
<ol>
{nav_items}
</ol></nav>
<nav epub:type="landmarks" hidden="hidden"><ol>
<li><a epub:type="cover" href="cover.xhtml">Cover</a></li>
<li><a epub:type="bodymatter" href="ch001.xhtml">Begin Reading</a></li>
</ol></nav>""")
    add("nav", "nav.xhtml", "application/xhtml+xml", nav, props="nav",
        spine=False)

    digest = hashlib.sha256()
    for _, href, _, _, data, _ in files:
        digest.update(href.encode()) or digest.update(data)
    book_id = uuid.uuid5(uuid.NAMESPACE_URL,
                         "with-a-long-spoon:" + digest.hexdigest())

    nav_points = "\n".join(
        f'<navPoint id="np{i}" playOrder="{i}"><navLabel><text>{esc(t)}</text>'
        f'</navLabel><content src="{h}"/></navPoint>'
        for i, (h, t) in enumerate(toc, 1))
    ncx = f"""<?xml version="1.0" encoding="utf-8"?>
<ncx xmlns="http://www.daisy.org/z3986/2005/ncx/" version="2005-1">
<head><meta name="dtb:uid" content="urn:uuid:{book_id}"/></head>
<docTitle><text>{esc(BOOK_TITLE)}</text></docTitle>
<navMap>
{nav_points}
</navMap></ncx>
"""
    add("ncx", "toc.ncx", "application/x-dtbncx+xml", ncx, spine=False)

    manifest = "\n".join(
        f'<item id="{fid}" href="{href}" media-type="{mt}"'
        + (f' properties="{props}"' if props else "") + "/>"
        for fid, href, mt, props, _, _ in files)
    spine = "\n".join(f'<itemref idref="{fid}"/>'
                      for fid, _, _, _, _, sp in files if sp)
    opf = f"""<?xml version="1.0" encoding="utf-8"?>
<package xmlns="http://www.idpf.org/2007/opf" version="3.0"
         unique-identifier="bookid">
<metadata xmlns:dc="http://purl.org/dc/elements/1.1/">
<dc:identifier id="bookid">urn:uuid:{book_id}</dc:identifier>
<dc:title>{esc(BOOK_TITLE)}</dc:title>
<dc:creator id="creator">{esc(author)}</dc:creator>
<dc:language>{LANGUAGE}</dc:language>
<dc:description>{esc(description)}</dc:description>
<meta property="dcterms:modified">{modified}</meta>
<meta property="belongs-to-collection" id="series">{esc(SERIES_NAME)}</meta>
<meta refines="#series" property="collection-type">series</meta>
<meta refines="#series" property="group-position">{SERIES_INDEX}</meta>
<meta name="calibre:series" content="{esc(SERIES_NAME)}"/>
<meta name="calibre:series_index" content="{SERIES_INDEX}"/>
<meta name="cover" content="cover-image"/>
{f'<meta property="wals:build">{esc(build_id)}</meta>' if build_id else ""}
{f'<meta property="wals:recipient">{esc(reader["label"])}</meta>' if reader else ""}
</metadata>
<manifest>
{manifest}
</manifest>
<spine toc="ncx">
{spine}
</spine>
</package>
"""

    out_path.parent.mkdir(parents=True, exist_ok=True)
    # Fixed zip timestamps -> byte-identical rebuilds from identical inputs.
    stamp = (1980, 1, 1, 0, 0, 0)
    with zipfile.ZipFile(out_path, "w") as zf:
        zi = zipfile.ZipInfo("mimetype", date_time=stamp)
        zf.writestr(zi, "application/epub+zip",
                    compress_type=zipfile.ZIP_STORED)
        zi = zipfile.ZipInfo("META-INF/container.xml", date_time=stamp)
        zf.writestr(zi, """<?xml version="1.0" encoding="utf-8"?>
<container version="1.0" xmlns="urn:oasis:names:tc:opendocument:xmlns:container">
<rootfiles><rootfile full-path="OEBPS/content.opf"
 media-type="application/oebps-package+xml"/></rootfiles>
</container>
""", compress_type=zipfile.ZIP_DEFLATED)
        zi = zipfile.ZipInfo("OEBPS/content.opf", date_time=stamp)
        zf.writestr(zi, opf, compress_type=zipfile.ZIP_DEFLATED)
        for _, href, _, _, data, _ in files:
            zi = zipfile.ZipInfo(f"OEBPS/{href}", date_time=stamp)
            zf.writestr(zi, data, compress_type=zipfile.ZIP_DEFLATED)
    return book_id


def git_build_info(root: Path, inputs) -> dict:
    """Identify the build from git alone, so it stays deterministic.

    Returns the short HEAD sha (suffixed '+dirty' when any input has
    uncommitted changes) and the most recent commit date among the inputs —
    i.e. how current the *content* is, independent of when it was packaged.
    Falls back to file mtimes outside a git checkout.
    """
    def git(*a):
        return subprocess.run(("git", "-C", str(root)) + a,
                              capture_output=True, text=True).stdout.strip()

    sha = git("rev-parse", "--short", "HEAD")
    if not sha:
        newest = max(p.stat().st_mtime for p in inputs)
        return {"sha": None,
                "source_date": dt.datetime.fromtimestamp(
                    newest, tz=dt.timezone.utc).strftime("%Y-%m-%d"),
                "modified": dt.datetime.fromtimestamp(
                    newest, tz=dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")}

    rel = [str(p.resolve().relative_to(root)) for p in inputs]
    # The builder shapes the output as much as the prose does, so uncommitted
    # changes to it make the sha a lie too.
    rel.append(str(Path(__file__).resolve().relative_to(root)))
    dirty = bool(git("status", "--porcelain", "--", *rel))

    newest = 0
    for r in rel:
        ct = git("log", "-1", "--format=%ct", "--", r)
        if ct:
            newest = max(newest, int(ct))
    if not newest:                       # nothing committed yet
        newest = int(max(p.stat().st_mtime for p in inputs))

    when = dt.datetime.fromtimestamp(newest, tz=dt.timezone.utc)
    return {"sha": sha + ("+dirty" if dirty else ""),
            "source_date": when.strftime("%Y-%m-%d"),
            "modified": when.strftime("%Y-%m-%dT%H:%M:%SZ")}


def record_recipient(root: Path, reader, build_id, out_path: Path, book_id):
    """Append the copy to build/RECIPIENTS.tsv — which build went to whom.

    Lives in build/ because build/ is gitignored: this file holds real names
    and email addresses and must never reach the repo.
    """
    ledger = root / "build/RECIPIENTS.tsv"
    new = not ledger.exists()
    when = dt.datetime.now(tz=dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    with ledger.open("a", encoding="utf-8") as fh:
        if new:
            fh.write("built_at\tname\temail\tbuild\tfile\tuuid\n")
        fh.write("\t".join([when, reader["name"], reader["email"], build_id,
                            out_path.name, str(book_id)]) + "\n")
    return ledger


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    root = Path(__file__).resolve().parent.parent
    ap.add_argument("--author", default="Helen Rivers",
                    help="author/pen name for the title, copyright and "
                         "metadata (default: Helen Rivers, the decided pen "
                         "name — see meta/meta-plan-pen-name.md)")
    ap.add_argument("--chronology", type=Path,
                    default=root / "meta/meta-plan-chronology.md")
    ap.add_argument("--blurb", type=Path, default=root / "meta/meta-blurb.md")
    ap.add_argument("--scenes", type=Path, default=root / "scenes")
    ap.add_argument("--cover", type=Path,
                    default=root / "images/cover.png",
                    help="cover image (default: images/cover.png, a symlink "
                         "pointing at the currently chosen cover asset)")
    ap.add_argument("-o", "--out", type=Path, default=None,
                    help="output path (default: build/a-polite-invitation.epub, "
                         "or -<reader-slug> with --reader; the build stamp "
                         "lives inside the file either way)")
    ap.add_argument("--reader", default=None, metavar="'Name <email>'",
                    help="identify the test reader this copy is for: stamps "
                         "the copyright page, the note to test readers, and "
                         "the epub metadata, names the file, and records the "
                         "copy in build/RECIPIENTS.tsv. Accepts "
                         "'Jane Doe <jane@ex.com>', a bare email, or a name")
    ap.add_argument("--stamped-name", action="store_true",
                    help="append -<source-date>-<sha> to the filename, to keep "
                         "several builds of different drafts side by side")
    ap.add_argument("--list", action="store_true",
                    help="print the chapter roster and exit without building")
    ap.add_argument("--allow-missing", action="store_true",
                    help="build even if Volume One chapters lack prose files")
    args = ap.parse_args()

    for p in (args.chronology, args.blurb, args.cover):
        if not p.exists():
            sys.exit(f"missing input: {p}")

    entries = parse_volume_one(args.chronology.read_text(encoding="utf-8"))
    if not entries:
        sys.exit("no Volume One chapters found in the chronology")

    chapters, missing = [], []
    for title, fn in entries:
        path = args.scenes / fn if fn else None
        if path is not None and path.exists():
            chapters.append((title, path))
        else:
            missing.append(f"{title}" + (f"  (cited: {fn})" if fn
                                         else "  (no scene file cited)"))

    if args.list:
        for i, (title, path) in enumerate(chapters, 1):
            print(f"{i:3d}. {title}  [{path.name}]")
        for m in missing:
            print(f"  !! missing prose: {m}")
        return

    if missing and not args.allow_missing:
        sys.exit("Volume One chapters without prose files "
                 f"({len(missing)}):\n  " + "\n  ".join(missing)
                 + "\nUse --allow-missing to build without them.")

    blurb = load_blurb(args.blurb)
    inputs = [args.chronology, args.blurb, args.cover] + [p for _, p in chapters]
    info = git_build_info(root, inputs)
    build_id = (f"{info['source_date']} · {info['sha']}" if info["sha"]
                else info["source_date"])

    reader = parse_reader(args.reader) if args.reader else None

    out = args.out
    if out is None:
        stem = "a-polite-invitation"
        if reader:
            stem += f"-{reader['slug']}"
        if args.stamped_name and info["sha"]:
            stem += f"-{info['source_date']}-{info['sha'].replace('+', '-')}"
        out = root / f"build/{stem}.epub"
    out.parent.mkdir(parents=True, exist_ok=True)

    book_id = build(chapters, blurb, args.cover, args.author, out,
                    info["modified"], build_id, reader)
    if reader:
        record_recipient(root, reader, build_id, out, book_id)
    words = sum(len(p.read_text(encoding="utf-8").split())
                for _, p in chapters)
    print(f"wrote {out}: {len(chapters)} chapters, ~{words:,} words, "
          f"build {build_id}, id urn:uuid:{book_id}", file=sys.stderr)
    if reader:
        print(f"  prepared for {reader['label']} "
              "— recorded in build/RECIPIENTS.tsv", file=sys.stderr)
    if args.author == "Anonymous":
        print("  note: author defaulted to 'Anonymous' — pass --author "
              "\"Pen Name\"", file=sys.stderr)
    for m in missing:
        print(f"  !! built WITHOUT: {m}", file=sys.stderr)


if __name__ == "__main__":
    main()
