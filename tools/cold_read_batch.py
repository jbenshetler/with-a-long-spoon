#!/usr/bin/env python3
"""Batch cold-read runner for OMP/eval bridge.

Usage examples:
  python3 tools/cold_read_batch.py --model openrouter/x-ai/grok-4.5 --model-id grok-4.5 --scope fall
  python3 tools/cold_read_batch.py --model openai-codex/gpt-5.6-sol --model-id gpt-5.6-sol --scope fall --resume

This script is driven from an OMP eval cell that provides `agent(...)`.
It is intentionally importable; call `run_batch(...)` from eval.

Not a standalone CLI without the eval bridge.
"""

from __future__ import annotations

import json
import re
import time
from pathlib import Path

FALL_SCENES = [
    {"title": "The Bench", "slug": "the-bench"},
    {"title": "Standards", "slug": "standards"},
    {"title": "The Pointing Game", "slug": "the-pointing-game"},
    {"title": "See You Later", "slug": "see-you-later"},
    {"title": "Substitution", "slug": "substitution"},
    {"title": "The Long Way", "slug": "long-way"},
    {"title": "Water Wings", "slug": "water-wings"},
    {"title": "May I Choose", "slug": "may-i-choose"},
    {"title": "Off Six-Fourteen", "slug": "off-six-fourteen"},
    {"title": "Dear", "slug": "dear"},
    {"title": "Leave No Trace", "slug": "leave-no-trace"},
    {"title": "Rye", "slug": "rye"},
    {"title": "What to Wear", "slug": "what-to-wear"},
    {"title": "Two Towels", "slug": "two-towels"},
    {"title": "A Round", "slug": "a-round"},
    {"title": "Turned Up", "slug": "turned-up"},
    {"title": "How It's Done", "slug": "how-its-done"},
    {"title": "Famished", "slug": "famished"},
    {"title": "Toenails", "slug": "toenails"},
    {"title": "Fed", "slug": "fed"},
    {"title": "Peekaboo", "slug": "peekaboo"},
    {"title": "All Told", "slug": "all-told"},
    {"title": "Sorority", "slug": "sorority"},
    {"title": "Gone", "slug": "gone"},
    {"title": "Rock", "slug": "rock"},
    {"title": "Lesson", "slug": "lesson"},
    {"title": "Broken In", "slug": "broken-in"},
    {"title": "Hills and Valleys", "slug": "hills-and-valleys"},
    {"title": "A Recognized Method", "slug": "recognized-method"},
    {"title": "The Practice Room", "slug": "practice-room"},
    {"title": "We Find Out", "slug": "we-find-out"},
    {"title": "One Bite", "slug": "one-bite"},
    {"title": "Above Him", "slug": "above-him"},
    {"title": "School Nights", "slug": "school-nights"},
    {"title": "The Induction", "slug": "the-induction"},
    {"title": "The New Ordinary", "slug": "new-ordinary"},
    {"title": "In His Hands", "slug": "in-his-hands"},
    {"title": "All the Time", "slug": "all-the-time"},
    {"title": "The Outlier", "slug": "outlier"},
    {"title": "Cropped", "slug": "cropped"},
    {"title": "Seconds", "slug": "seconds"},
    {"title": "Under the Rug", "slug": "under-the-rug"},
    {"title": "Bare", "slug": "bare"},
    {"title": "Believe Me", "slug": "believe-me"},
    {"title": "Fairytale", "slug": "fairytale"},
    {"title": "Old Acquaintances", "slug": "old-acquaintances"},
    {"title": "The Usual", "slug": "the-usual"},
    {"title": "My Friend Randi", "slug": "my-friend-randi"},
    {"title": "Nothing Underneath", "slug": "nothing-underneath"},
]


def clean_scene_text(slug: str) -> str:
    raw = Path(f"scenes/{slug}.md").read_text()
    lines = raw.splitlines()
    start = 0
    if lines and lines[0].startswith("# "):
        start = 1
    divider = None
    for i in range(start, min(len(lines), start + 12)):
        if lines[i].strip() == "---":
            divider = i
            break
    body = lines[divider + 1 :] if divider is not None else lines[start:]
    if divider is None:
        while body and not body[0].strip():
            body.pop(0)
        if body and body[0].lstrip().startswith("*"):
            body.pop(0)
    body = [ln for ln in body if not ln.lstrip().startswith("[AI")]
    while body and not body[0].strip():
        body.pop(0)
    while body and not body[-1].strip():
        body.pop()
    text = "\n".join(body)
    if "[AI" in text:
        raise RuntimeError(f"AI marker survived in {slug}")
    return text


def parse_response(raw_output):
    parsed = raw_output
    if isinstance(raw_output, str):
        try:
            parsed = json.loads(raw_output)
        except Exception:
            parsed = raw_output
    if isinstance(parsed, dict):
        return (
            parsed.get("response")
            or parsed.get("text")
            or parsed.get("output")
            or json.dumps(parsed, ensure_ascii=False, indent=2)
        ).strip()
    return str(parsed).strip()


def split_reader(text: str):
    carry_pattern = re.compile(
        r"(?im)^\s*(?:#{1,3}\s*)?(?:\*\*)?Carry[- ]forward state:?(?:\*\*)?\s*$"
    )
    matches = list(carry_pattern.finditer(text))
    if not matches:
        return text.strip(), ""
    m = matches[0]
    before = text[: m.start()].strip()
    after = text[m.end() :].strip()
    reader_pattern = re.compile(
        r"(?im)^\s*(?:#{1,3}\s*)?(?:\*\*)?Reader reaction:?(?:\*\*)?\s*$"
    )
    before = reader_pattern.sub("", before, count=1).strip()
    return before, after


def extract_usage(agent_id: str):
    sessions = Path.home() / ".omp/agent/sessions"
    matches = list(sessions.rglob(f"{agent_id}.jsonl"))
    if not matches:
        return None
    p = max(matches, key=lambda x: x.stat().st_mtime)
    totals = {
        "input": 0,
        "output": 0,
        "cacheRead": 0,
        "cacheWrite": 0,
        "totalTokens": 0,
        "reasoningTokens": 0,
        "cost": 0.0,
        "promptTokens": 0,
        "nonMessageTokens": 0,
        "duration_ms": 0.0,
        "turns": 0,
        "jsonl": str(p),
    }
    for line in p.read_text().splitlines():
        if not line.strip():
            continue
        r = json.loads(line)
        if r.get("type") != "message":
            continue
        m = r.get("message") or {}
        if m.get("role") != "assistant" or "usage" not in m:
            continue
        u = m["usage"]
        c = u.get("cost") or {}
        totals["input"] += u.get("input") or 0
        totals["output"] += u.get("output") or 0
        totals["cacheRead"] += u.get("cacheRead") or 0
        totals["cacheWrite"] += u.get("cacheWrite") or 0
        totals["totalTokens"] += u.get("totalTokens") or 0
        totals["reasoningTokens"] += u.get("reasoningTokens") or 0
        totals["cost"] += float((c.get("total") if isinstance(c, dict) else 0) or 0)
        totals["duration_ms"] += float(m.get("duration") or 0)
        totals["turns"] += 1
        cs = m.get("contextSnapshot") or {}
        pt = cs.get("promptTokens") or 0
        if pt >= totals["promptTokens"]:
            totals["promptTokens"] = pt
            totals["nonMessageTokens"] = cs.get("nonMessageTokens") or 0
    return totals


def has_valid_review(path: Path) -> bool:
    if not path.exists():
        return False
    txt = path.read_text()
    if "## Carry-forward state" not in txt:
        return False
    return bool(txt.split("## Carry-forward state", 1)[1].strip())


def write_review(out_dir: Path, model_id: str, model_selector: str, scene, response_text, predecessor, provider_label: str = "OMP"):
    reader, carry = split_reader(response_text)
    if not reader or not carry:
        raise ValueError(
            f"missing sections for {scene['slug']}: reader={len(reader)} carry={len(carry)}"
        )
    path = out_dir / f"{scene['slug']}.md"
    predecessor_label = predecessor if predecessor else "— (opening, cold)"
    content = (
        f"# Cold read — {scene['title']}\n\n"
        f"*scene: scenes/{scene['slug']}.md · model: {model_id} ({provider_label}: {model_selector}) · "
        f"read after: {predecessor_label}*\n\n"
        f"## Reader reaction\n\n{reader}\n\n"
        f"## Carry-forward state\n\n{carry}\n"
    )
    path.write_text(content)
    return path, carry


def run_batch(
    *,
    agent_fn,
    model_selector: str,
    model_id: str,
    scenes=None,
    resume: bool = True,
    max_attempts: int = 5,
    label_prefix: str = "BlindBatch",
    budget_usd: float | None = None,
    provider_label: str = "OMP",
):
    """agent_fn(prompt, model, label) -> result dict with output/text/id, and
    optionally a `usage` dict (input/output/cost/…). If `usage` is present it is
    used directly (the direct-API path); otherwise usage is read post-hoc from the
    OMP session jsonl via extract_usage().

    Cost safety: if `budget_usd` is set, the batch ABORTS (raises) the moment a
    scene's actual cost exceeds it, or a call comes back marked `incomplete`
    (hit its output cap). Combined with the caller's per-call max_output_tokens
    cap and a low `max_attempts`, this bounds per-scene spend."""
    scenes = list(scenes or FALL_SCENES)
    out_dir = Path("reviews/cold-read") / model_id
    out_dir.mkdir(parents=True, exist_ok=True)

    carry = ""
    predecessor = None
    log = []

    # Seed carry-forward when the run starts mid-book (e.g. a scoped `gone..` run).
    # The first scene's predecessor lives outside `scenes`, so the reader would
    # otherwise read it cold as the opening. Load the predecessor's carry-forward
    # from its review on disk; refuse rather than fabricate an opening read.
    full_slugs = [s["slug"] for s in FALL_SCENES]
    if scenes and scenes[0]["slug"] in full_slugs:
        pos = full_slugs.index(scenes[0]["slug"])
        if pos > 0:
            pred_slug = full_slugs[pos - 1]
            pred_file = out_dir / f"{pred_slug}.md"
            if not has_valid_review(pred_file):
                raise RuntimeError(
                    f"cannot seed carry-forward for {scenes[0]['slug']}: predecessor "
                    f"'{pred_slug}' has no review in {out_dir}. Start the run from the "
                    f"opening, or ensure {pred_slug}.md exists first."
                )
            carry = pred_file.read_text().split("## Carry-forward state", 1)[1].strip()
            predecessor = pred_slug

    for idx, scene in enumerate(scenes, 1):
        existing = out_dir / f"{scene['slug']}.md"
        if resume and has_valid_review(existing):
            carry = existing.read_text().split("## Carry-forward state", 1)[1].strip()
            predecessor = scene["slug"]
            rec = {
                "slug": scene["slug"],
                "title": scene["title"],
                "path": str(existing),
                "status": "skipped-existing",
                "usage": None,
                "attempt": 0,
                "wall_s": 0,
            }
            log.append(rec)
            print(
                json.dumps(
                    {
                        "n": idx,
                        "of": len(scenes),
                        "slug": scene["slug"],
                        "status": "skipped-existing",
                        "carry_chars": len(carry),
                    }
                ),
                flush=True,
            )
            continue

        clean = clean_scene_text(scene["slug"])
        prior_block = carry if carry.strip() else "empty — opening chapter"
        if predecessor and not carry.strip():
            raise RuntimeError(f"empty prior carry before {scene['slug']}")
        base_prompt = (
            f"TITLE:\n{scene['title']}\n\n"
            f"PRIOR READER-STATE (authoritative memory from every earlier chapter):\n{prior_block}\n\n"
            f"OUTPUT PRIORITY:\nKeep `### Reader reaction` concise. Always complete "
            f"`### Carry-forward state` in full; if space is tight, shorten the reaction, "
            f"never the carry-forward.\n\n"
            f"CHAPTER TEXT:\n{clean}\n"
        )

        ok = False
        usage = None
        for attempt in range(1, max_attempts + 1):
            prompt = base_prompt
            if attempt > 1:
                prompt += (
                    "\n\nFORMAT REMINDER: Return exactly two top-level sections headed "
                    "`### Reader reaction` and `### Carry-forward state`. The carry-forward "
                    "section must be a full updated memory, not empty."
                )
            # unique label every attempt/time to avoid artifact collisions
            label = (
                f"{label_prefix}_{model_id}_{scene['slug'].replace('-', '_')}"
                f"_try{attempt}_{int(time.time())}"
            )
            try:
                t0 = time.time()
                result = agent_fn(prompt=prompt, model=model_selector, label=label)
                wall = time.time() - t0
                response_text = parse_response(result.get("output") or result.get("text"))
                reader, parsed = split_reader(response_text)
                if reader and parsed:
                    path, carry = write_review(
                        out_dir, model_id, model_selector, scene, response_text, predecessor, provider_label
                    )
                    predecessor = scene["slug"]
                    usage = result.get("usage") or extract_usage(result.get("id") or label)
                    rec = {
                        "slug": scene["slug"],
                        "title": scene["title"],
                        "path": str(path),
                        "agent": result.get("id"),
                        "attempt": attempt,
                        "status": "generated",
                        "wall_s": round(wall, 1),
                        "response_chars": len(response_text),
                        "carry_chars": len(carry),
                        "usage": usage,
                    }
                    log.append(rec)
                    print(
                        json.dumps(
                            {
                                "n": idx,
                                "of": len(scenes),
                                "slug": scene["slug"],
                                "status": "generated",
                                "attempt": attempt,
                                "cost": None if not usage else round(usage["cost"], 6),
                                "input": None if not usage else usage["input"],
                                "output": None if not usage else usage["output"],
                                "totalTokens": None if not usage else usage["totalTokens"],
                                "promptTokens": None if not usage else usage["promptTokens"],
                                "carry_chars": len(carry),
                            }
                        ),
                        flush=True,
                    )
                    ok = True
                    break
                print(
                    f"invalid sections {scene['slug']} attempt={attempt} "
                    f"reader={len(reader)} carry={len(parsed)}",
                    flush=True,
                )
            except Exception as e:
                print(
                    f"exception {scene['slug']} attempt={attempt}: {type(e).__name__}: {e}",
                    flush=True,
                )
                time.sleep(min(30, 5 * attempt))
                continue
            # brief pause between invalid-section retries
            time.sleep(2 * attempt)
        if not ok:
            raise RuntimeError(
                f"failed {scene['slug']}; completed={[r['slug'] for r in log if r.get('status')=='generated']}"
            )
        # Cost safety: abort the whole batch on an over-budget or capped (incomplete) scene.
        if usage:
            if usage.get("incomplete"):
                raise RuntimeError(
                    f"response incomplete on {scene['slug']} (hit the output cap). "
                    f"Raise --budget-usd or lower --effort, then re-run with --resume."
                )
            if budget_usd is not None and float(usage.get("cost") or 0) > budget_usd:
                raise RuntimeError(
                    f"budget exceeded on {scene['slug']}: "
                    f"${float(usage['cost']):.4f} > ${budget_usd:.2f} — aborting batch."
                )

    gen = [r for r in log if r.get("status") == "generated"]
    summary = {
        "model_selector": model_selector,
        "model_id": model_id,
        "completed": len(log),
        "generated": len(gen),
        "skipped": sum(1 for r in log if r.get("status") == "skipped-existing"),
        "total_cost": sum((r.get("usage") or {}).get("cost", 0) for r in gen),
        "total_input": sum((r.get("usage") or {}).get("input", 0) for r in gen),
        "total_output": sum((r.get("usage") or {}).get("output", 0) for r in gen),
        "total_tokens": sum((r.get("usage") or {}).get("totalTokens", 0) for r in gen),
        "per_chapter": [
            {
                "slug": r["slug"],
                "title": r["title"],
                "status": r.get("status"),
                "cost": None if not r.get("usage") else r["usage"]["cost"],
                "input": None if not r.get("usage") else r["usage"]["input"],
                "output": None if not r.get("usage") else r["usage"]["output"],
                "totalTokens": None if not r.get("usage") else r["usage"]["totalTokens"],
                "promptTokens": None if not r.get("usage") else r["usage"]["promptTokens"],
                "reasoningTokens": None if not r.get("usage") else r["usage"]["reasoningTokens"],
                "cacheRead": None if not r.get("usage") else r["usage"]["cacheRead"],
                "duration_s": None
                if not r.get("usage")
                else round(r["usage"]["duration_ms"] / 1000, 1),
                "wall_s": r.get("wall_s"),
                "path": r["path"],
            }
            for r in log
        ],
    }
    stats_path = out_dir / "BATCH_STATS.json"
    stats_path.write_text(json.dumps(summary, indent=2) + "\n")
    print(json.dumps({"summary_path": str(stats_path), **{k: summary[k] for k in (
        "completed","generated","skipped","total_cost","total_input","total_output","total_tokens"
    )}}, indent=2), flush=True)
    return summary
