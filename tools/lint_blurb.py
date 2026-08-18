#!/usr/bin/env python3
"""Detect when the jacket source changed but the derived reader packet wasn't refreshed.

The cover/blurb has ONE downstream copy the cold-read reader is actually fed:
`reviews/_harness/volume-packets.toml`. Its source of truth is `meta/meta-blurb.md`
(+ `meta/meta-cover.md`). When the source changes and the packet isn't regenerated, the
reader gets stale copy (this is how the retired "trap" tagline lingered). This lint pins
a checksum of the source into the packet so that drift fails the pre-commit hook until
the packet is refreshed and re-stamped.

Usage:
  tools/lint_blurb.py            # check; exit 1 on drift
  tools/lint_blurb.py --update   # re-stamp blurb_source_sha256 to the current source
"""
import hashlib
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
SOURCES = [REPO / "meta/meta-blurb.md", REPO / "meta/meta-cover.md"]
PACKET = REPO / "reviews/_harness/volume-packets.toml"
KEY = "blurb_source_sha256"


def source_sha() -> str:
    h = hashlib.sha256()
    for p in SOURCES:
        h.update(b"\x00" + p.name.encode())
        h.update(p.read_bytes() if p.exists() else b"")
    return h.hexdigest()


def recorded(text: str):
    m = re.search(rf'{KEY}\s*=\s*"([0-9a-f]+)"', text)
    return m.group(1) if m else None


def main() -> int:
    cur = source_sha()
    text = PACKET.read_text()
    rec = recorded(text)

    if "--update" in sys.argv:
        line = f'{KEY} = "{cur}"'
        if rec is None:
            out, done = [], False
            for ln in text.splitlines(keepends=True):
                if not done and ln.lstrip().startswith("["):
                    out.append(line + "\n\n")
                    done = True
                out.append(ln)
            text = "".join(out) if done else line + "\n" + text
        else:
            text = re.sub(rf'{KEY}\s*=\s*"[0-9a-f]+"', line, text)
        PACKET.write_text(text)
        print(f"lint_blurb: stamped {KEY} = {cur}")
        return 0

    if rec is None:
        print(f"lint_blurb: no {KEY} in {PACKET.name}; run tools/lint_blurb.py --update",
              file=sys.stderr)
        return 1
    if cur != rec:
        print(
            "lint_blurb: JACKET SOURCE CHANGED but the reader packet wasn't refreshed.\n"
            f"  source (meta-blurb.md + meta-cover.md): {cur}\n"
            f"  packet ({PACKET.name}):                 {rec}\n"
            "  -> update the packet's blurb to match the source, then re-stamp:\n"
            "     tools/lint_blurb.py --update",
            file=sys.stderr,
        )
        return 1
    print("lint_blurb: packet in sync with jacket source")
    return 0


if __name__ == "__main__":
    sys.exit(main())
