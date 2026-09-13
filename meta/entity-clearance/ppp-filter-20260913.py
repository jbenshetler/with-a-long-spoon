#!/usr/bin/env python3
"""Filter used for the Miranda entity-clearance PPP extract (run 2026-09-13).

Invocation, once per source file, streaming (files never stored to disk):

  BASE=https://data.sba.gov/sites/default/files/distribution/SBA-OCA-2022-07-001
  for n in public_150k_plus_240930 public_up_to_150k_{1..12}_240930; do
      curl -s "$BASE/$n.csv" | python3 ppp-filter-20260913.py >> ppp-miranda-extract-20260913.csv
  done

Emits one row per PPP loan whose BorrowerName begins with the token MIRANDA:
  [BorrowerName, BorrowerCity, BorrowerState, CurrentApprovalAmount]

Notes that matter for reproducing the result:
  * The SBA CSVs are latin-1, NOT utf-8. Decoding as utf-8 raises
    UnicodeDecodeError on the first non-ASCII byte and silently truncates the
    scan — an earlier run of this scan failed exactly that way and returned 2
    rows instead of 1231.
  * Column 4 (0-based) is BorrowerName in every file; the header row is
    consumed and discarded per file.
  * \\bMIRANDA\\b anchors at the start, so it matches company names beginning
    with Miranda and personal names "Miranda Smith", but not "DeMiranda" or
    "Gaytan Miranda". The complementary substring search (see
    ppp-miranda-namehits-20260913.csv) catches those.
"""
import csv, sys, re
sys.stdin.reconfigure(encoding='latin-1', errors='replace')
csv.field_size_limit(10**7)
w = csv.writer(sys.stdout)
r = csv.reader(sys.stdin)
next(r, None)                      # discard header
for row in r:
    try:
        if len(row) > 14 and re.match(r'\s*MIRANDA\b', row[4], re.I):
            w.writerow([row[4], row[6], row[7], row[14]])
    except Exception:
        continue
