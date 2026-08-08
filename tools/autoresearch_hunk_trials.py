#!/usr/bin/env python3
"""Run one-at-a-time main-version hunk trials for a scene revision.

Each trial reverses exactly one ``main...tag`` hunk, regenerates the selected
cold-reader reviews, records model scores in a restartable Markdown log, commits
that checkpoint, then restores the tagged scene before proceeding.
"""
from __future__ import annotations

import argparse
import re
import subprocess
import tempfile
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
SCENE = Path("scenes/the-pointing-game.md")
MODELS = ("gpt-5.6-terra", "gpt-5.6-sol", "gpt-5.5")


def run(*args: str, capture: bool = False) -> str:
    result = subprocess.run(args, cwd=REPO, text=True, capture_output=capture, check=True)
    return result.stdout if capture else ""


def hunks(tag: str) -> list[dict[str, str]]:
    diff = run("git", "diff", "--unified=0", f"main...{tag}", "--", str(SCENE), capture=True)
    header, *chunks = re.split(r"(?=^@@ )", diff, flags=re.M)
    result = []
    for number, chunk in enumerate(chunks, 1):
        lines = chunk.splitlines()
        old = "\n".join(line[1:] for line in lines[1:] if line.startswith("-"))
        new = "\n".join(line[1:] for line in lines[1:] if line.startswith("+"))
        result.append({"number": str(number), "header": lines[0], "old": old, "new": new, "patch": header + chunk})
    return result


def score(model: str) -> tuple[int, int]:
    review = REPO / "reviews" / "cold-read" / model / "the-pointing-game.md"
    text = review.read_text()
    heat = re.search(r"^\*\*Heat:\*\*\s*(\d)", text, re.M)
    romance = re.search(r"^\*\*Romance:\*\*\s*(\d)", text, re.M)
    if not heat or not romance:
        raise RuntimeError(f"missing Heat/Romance score in {review}")
    return int(heat.group(1)), int(romance.group(1))


def append_log(log: Path, trial: dict[str, str], outcomes: dict[str, tuple[int, int]]) -> None:
    keep = all(romance >= 2 for _, romance in outcomes.values())
    old = trial["old"].replace("\n", " ")
    new = trial["new"].replace("\n", " ")
    lines = [
        f"\n### Main-hunk trial {trial['number']}\n",
        f"- Hunk: `{trial['header']}`\n",
        f"- Reverted only this hunk to `main`: `{old}`\n",
        f"- Retained tagged wording outside this hunk: `{new}`\n",
        "- Scores: " + "; ".join(
            f"{model} Heat {heat}/3, Romance {romance}/3" for model, (heat, romance) in outcomes.items()
        ) + ".\n",
        f"- Result: {'romance floor holds' if keep else 'romance floor fails'}; tagged scene restored before the next trial.\n",
    ]
    with log.open("a") as file:
        file.writelines(lines)


def commit_trial(number: str, log: Path) -> None:
    paths = [str(log), *[
        str(Path("reviews") / "cold-read" / model / filename)
        for model in MODELS
        for filename in ("the-pointing-game.md", "BATCH_STATS.json", "BATCH_RUNS.jsonl")
    ]]
    run("git", "add", *paths)
    run("git", "commit", "-m", f"Record pointing game main-hunk trial {number}")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--tag", required=True)
    parser.add_argument("--log", required=True, type=Path)
    parser.add_argument("--start", type=int, default=1)
    parser.add_argument("--stop", type=int, default=None)
    args = parser.parse_args()
    log = REPO / args.log
    trials = hunks(args.tag)
    stop = args.stop or len(trials)

    for trial in trials[args.start - 1 : stop]:
        marker = f"### Main-hunk trial {trial['number']}"
        if marker in log.read_text():
            continue
        with tempfile.NamedTemporaryFile("w", suffix=".patch", delete=False) as file:
            patch_path = Path(file.name)
            file.write(trial["patch"])
        outcomes = {}
        try:
            run("git", "apply", "--reverse", str(patch_path))
            for model in MODELS:
                run(
                    "uv", "run", "--python", "3.11", "--with", "openai-codex",
                    "tools/cold_read_openai.py", "--auth", "codex", "--model", model,
                    "--scope", "the-pointing-game", "--fresh", "--allow-volume-one-rewrite",
                )
                outcomes[model] = score(model)
        finally:
            patch_path.unlink(missing_ok=True)
            run("git", "restore", str(SCENE))
        append_log(log, trial, outcomes)
        commit_trial(trial["number"], args.log)


if __name__ == "__main__":
    main()
