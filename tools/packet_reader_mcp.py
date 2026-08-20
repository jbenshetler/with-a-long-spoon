#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = ["mcp>=2.0"]
# ///
"""Sandboxed reading-packet MCP server for the blind grounded cold reader.

This is the *only* tool the `blind-reader-grounded` subagent is given — it has no
`Read`, no `Bash`, no filesystem access of its own. The server can physically
open files **only** inside a per-read reading-packet directory, so blindness is
enforced by the tool itself, not by instruction or a post-hoc audit:

  base jail   — every path is resolved and asserted to live under
                <repo>/reviews/cold-read/.packets/ ; anything else is refused.
  capability  — a packet is addressed by an unguessable 32-hex-char token
                (secrets.token_hex(16)); there is NO "list all packets" tool, so
                a reader that was handed one token cannot enumerate or reach any
                other packet — it cannot read another chapter's packet (i.e.
                cannot read ahead), and cannot reach meta/, the raw spoiler-headed
                scenes/, or any other file in the repo.

The harness (cold_read_grounded.py --emit-packet) mints a token dir containing
only that read's sanctioned, cleaned inputs (jacket, checkpoint, window scenes,
this chapter) and hands the reader its token.

Registered durably in the repo's .mcp.json; BASE is derived from this file's
location, so it needs no env and travels across clones.
"""
from __future__ import annotations

import re
from pathlib import Path

from mcp.server import MCPServer

REPO = Path(__file__).resolve().parent.parent
BASE = (REPO / "reviews" / "cold-read" / ".packets").resolve()
REVIEWS_ROOT = (REPO / "reviews" / "cold-read").resolve()

_TOKEN_RE = re.compile(r"^[0-9a-f]{32}$")
_NAME_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]*$")

# Reader-review format contract (reader reactions only — never checkpoints/oracle
# answers, which route to deeper paths). Enforced with in-context retries: a
# rejection costs the reader one short re-emit turn, not a re-read, so the cap is
# cheap. After _MAX_FORMAT_RETRIES rejections the write is accepted with a warning
# marker rather than discarded — the prose reaction is the expensive part.
_MAX_FORMAT_RETRIES = 2
_REQUIRED_BLOCK = (
    ("**Heat:** N", re.compile(r"\*\*Heat:\*\*\s*[0-3]\b")),
    ("**Romance:** N", re.compile(r"\*\*Romance:\*\*\s*[0-3]\b")),
    ("**Cast present**", re.compile(r"\*\*Cast present", re.IGNORECASE)),
)


def _is_reader_review(dest: Path) -> bool:
    """True only for reviews/cold-read/<model-id>/<slug>.md — the reader-reaction
    lane. Checkpoints (<model>/checkpoints/ck-*.md) and oracle outputs live deeper
    and carry no structured block."""
    return dest.parent.parent == REVIEWS_ROOT and not dest.name.startswith("ck-")

mcp = MCPServer(name="packet", version="1.0")


def _packet_dir(packet_id: str) -> Path:
    if not _TOKEN_RE.match(packet_id or ""):
        raise ValueError("invalid packet id")
    d = (BASE / packet_id).resolve()
    # Defense in depth behind the token regex: never escape the base jail.
    if d.parent != BASE or not d.is_dir():
        raise ValueError("unknown packet")
    return d


@mcp.tool(
    description="List the files in your reading packet, in the order you must read "
    "them. Call this first with the packet id you were given."
)
def list_packet(packet_id: str) -> str:
    d = _packet_dir(packet_id)
    # Dotfiles (.dest/.header) are internal routing markers — never listed or readable.
    names = sorted(p.name for p in d.iterdir() if p.is_file() and not p.name.startswith("."))
    return "\n".join(names)


@mcp.tool(
    description="Return the full text of one file from your reading packet. "
    "`name` must be a bare filename from list_packet (no paths)."
)
def read_packet(packet_id: str, name: str) -> str:
    d = _packet_dir(packet_id)
    if not _NAME_RE.match(name or "") or "/" in name or "\\" in name:
        raise ValueError("invalid file name")
    f = (d / name).resolve()
    if f.parent != d or not f.is_file():
        raise ValueError("no such file in this packet")
    return f.read_text(encoding="utf-8")


@mcp.tool(
    description="Save your finished output (your Reader reaction, or your checkpoint) to "
    "your packet's pre-assigned destination. Call this ONCE, at the very end, with your "
    "complete output text as `text` and nothing else — no preamble, no headings you were "
    "not asked for. Returns a confirmation."
)
def write_output(packet_id: str, text: str) -> str:
    d = _packet_dir(packet_id)
    dest_file = d / ".dest"
    if not dest_file.is_file():
        raise ValueError("this packet has no output destination")
    rel = dest_file.read_text(encoding="utf-8").strip()
    header = (d / ".header").read_text(encoding="utf-8") if (d / ".header").is_file() else ""
    dest = (REPO / rel).resolve()
    # Jail: writes are permitted ONLY under reviews/cold-read/, and only to a .md file.
    if REVIEWS_ROOT not in dest.parents or dest.suffix != ".md":
        raise ValueError("destination not permitted")
    body = (text or "").strip()
    if body.lower().startswith("tool_uses:"):
        body = body.split("\n", 1)[1].lstrip() if "\n" in body else ""
    # Drop a reader-emitted section heading; the destination header already has one.
    body = re.sub(r"(?is)^\s*#{1,3}\s*(?:reader reaction|checkpoint)\b[^\n]*\n+", "", body, count=1).strip()
    if len(body) < 200:
        raise ValueError("output too short to save")
    if _is_reader_review(dest):
        missing = [label for label, rx in _REQUIRED_BLOCK if not rx.search(body)]
        if missing:
            attempts_f = d / ".attempts"
            try:
                attempts = int(attempts_f.read_text(encoding="utf-8"))
            except (FileNotFoundError, ValueError):
                attempts = 0
            attempts += 1
            attempts_f.write_text(str(attempts), encoding="utf-8")
            if attempts <= _MAX_FORMAT_RETRIES:
                raise ValueError(
                    "output rejected — missing required structured-block lines: "
                    + ", ".join(missing)
                    + ". Re-send your COMPLETE output (do not shorten the Reader "
                    "reaction) ending with the full structured block: Cast present, "
                    "Heat, Romance, Motifs & images, Symbolism, Characterization, "
                    "Pace — with Heat and Romance as integers 0-3."
                )
            body += (
                "\n\n<!-- format-warning: accepted after "
                f"{_MAX_FORMAT_RETRIES} format retries; still missing: "
                + ", ".join(missing) + " -->"
            )
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(header + body + "\n", encoding="utf-8")
    return f"saved {len(body)} chars to {rel}"


if __name__ == "__main__":
    mcp.run(transport="stdio")
