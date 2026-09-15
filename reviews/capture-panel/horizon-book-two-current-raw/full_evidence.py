#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = ["openai>=1.40", "openai-codex"]
# ///
from __future__ import annotations

from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import date
from pathlib import Path
import hashlib
import os
import sys

REPO = Path(__file__).resolve().parents[3]
os.chdir(REPO)
sys.path.insert(0, str(REPO / 'tools'))

import authorship_audit  # noqa: E402
import cold_read  # noqa: E402

ROOT = REPO / 'reviews' / 'capture-panel' / 'horizon-book-two-current-raw'
PANEL = REPO / 'reviews' / 'capture-panel'
PERSONAS = ['romance-graduate', 'fsog-refugee', 'consent-sensitive']
MODELS = ['claude-opus-4-8', 'gpt-5.6-sol', 'gpt-5.5']
PROTOCOL = 'book-two-current-raw-full-evidence-v1'

REVISED_JACKET = (ROOT / 'INSTRUMENT.md').read_text(encoding='utf-8').split('## Revised Book Two jacket\n\n',1)[1].split('\n## Volume Three ending/reveal/fallout packet',1)[0].strip()
VOLUME_THREE_ENDING_PACKET = (ROOT / 'INSTRUMENT.md').read_text(encoding='utf-8').split('## Volume Three ending/reveal/fallout packet\n\n',1)[1].split('\n## Arm A questions',1)[0].strip()
BOOK_TWO_PACKET_PATH = ROOT / 'VOLUME_TWO_RAW_GAP_PACKET.md'
BOOK_TWO_PACKET = BOOK_TWO_PACKET_PATH.read_text(encoding='utf-8')

QUESTIONS = '''Answer in your persona. You have all of the information below in one sitting: your own Volume One interview, the revised Book Two jacket, the chronology-ordered current Book Two raw-prose + sourced-gap-summary packet, and the intended late-Book-Three reveal/fallout packet. Label F1 through F8.

F1 — Commercial verdict: after all this, do you keep reading through Book Three to the reveal? yes/no/only-if. Do not answer as a craft advisor; answer as this reader.

F2 — Does the revised Book Two jacket set a fair contract for escalation-without-reckoning, or would you still feel misled by the Book Two curtain?

F3 — Does the current Book Two material earn the delay better or worse than the jacket alone? Name the exact drafted scenes or gap-summary beats that decide it.

F4 — Does the intended late reveal + no-road-back crash-out + Cassie debrief answer the Pace/Randi accountability problem, or is the delay still too long?

F5 — What must the remaining Book Two pages do, short of reveal, to keep you from deciding the book has joined the con?

F6 — What must early/mid Book Three do before the reveal, if anything, to keep you from quitting before the planned crash-out?

F7 — What is your concrete DNF line?

F8 — One-sentence final condition or breaking point.
'''

def clean(text: str) -> str:
    return '\n'.join(line.rstrip() for line in text.strip().splitlines()) + '\n'

def digest(text: str) -> str:
    return hashlib.sha256(text.encode()).hexdigest()[:12]

def persona_system(persona: str) -> str:
    core = (PANEL / 'prompts' / 'core.md').read_text(encoding='utf-8')
    pers = (PANEL / 'personas' / f'{persona}.md').read_text(encoding='utf-8')
    attention = core.split('You will be given up to four chapters', 1)[0].rstrip()
    return attention + '\n\n' + pers.strip() + '\n\nYou are answering a full-evidence continuation/horizon interview as this reader after Volume One. Stay in persona. Be candid about purchase, trust, anger, and DNF lines. Do not be patient out of politeness. Do not raise contraception, STI, pregnancy, or safer-sex logistics.\n'

def prior_path(model: str, persona: str) -> Path:
    return PANEL / model / f'{persona}--volume-dag-interview.md'

def prompt(model: str, persona: str) -> str:
    prior = prior_path(model, persona)
    return f'''===== YOUR PRIOR VOLUME ONE INTERVIEW =====\nsource: {prior.relative_to(REPO)}\n\n{prior.read_text(encoding='utf-8')}\n===== END PRIOR INTERVIEW =====\n\n===== REVISED BOOK TWO JACKET COPY =====\n\n{REVISED_JACKET}\n===== END JACKET =====\n\n===== CURRENT BOOK TWO RAW-PROSE + SOURCED-GAP-SUMMARY PACKET =====\nsource: {BOOK_TWO_PACKET_PATH.relative_to(REPO)}\n\n{BOOK_TWO_PACKET}\n===== END BOOK TWO PACKET =====\n\n===== INTENDED VOLUME THREE REVEAL / FALLOUT ENDING PACKET =====\n\n{VOLUME_THREE_ENDING_PACKET}\n===== END ENDING PACKET =====\n\n{QUESTIONS}'''

def out_path(model: str, persona: str) -> Path:
    return ROOT / model / f'{persona}--arm-d-full-evidence.md'

def write_out(model: str, persona: str, system_sha: str, prompt_sha: str, answer: str) -> None:
    out = out_path(model, persona)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(f'# Book Two current raw horizon — {persona} · arm-d-full-evidence\n\n*model: {model} · persona: {persona} · arm: arm-d-full-evidence · protocol: {PROTOCOL} · sources: prior-volume-interview + revised-jacket + VOLUME_TWO_RAW_GAP_PACKET.md + ending-packet · system-sha: {system_sha} · prompt-sha: {prompt_sha} · run: {date.today().isoformat()}*\n\n{clean(answer)}', encoding='utf-8')

def validate(answer: str, label: str) -> str:
    text = clean(answer)
    if len(text) < 700:
        raise RuntimeError(f'suspiciously short {label}: {len(text)} chars')
    if 'F8' not in text:
        raise RuntimeError(f'malformed {label}: missing F8')
    return text

def call_model(model: str, system: str, p: str, label: str, codex_fn=None) -> str:
    if model.startswith('claude-'):
        return authorship_audit.run_claude(model, system, p, label)
    if codex_fn is None:
        raise RuntimeError('codex_fn required')
    return (codex_fn(prompt=p, model=model, label=label).get('output') or '')

def run_lane(model: str, persona: str, codex_fn=None) -> str:
    system = persona_system(persona)
    p = prompt(model, persona)
    answer = validate(call_model(model, system, p, f'horizon-full-{model}-{persona}', codex_fn), f'{model}·{persona}·full')
    write_out(model, persona, digest(system), digest(p), answer)
    return f'ok {model} {persona}'

def run_codex_model(model: str) -> list[str]:
    def one(persona: str) -> str:
        system = persona_system(persona)
        fn, close = cold_read.make_codex_agent_fn(system_prompt=system, effort='low')
        try:
            return run_lane(model, persona, codex_fn=fn)
        finally:
            close()
    out = []
    with ThreadPoolExecutor(max_workers=2) as pool:
        for fut in as_completed([pool.submit(one, p) for p in PERSONAS]):
            out.append(fut.result())
    return out

def main() -> None:
    failures = []
    results = []
    with ThreadPoolExecutor(max_workers=3) as pool:
        futs = [pool.submit(run_lane, 'claude-opus-4-8', p) for p in PERSONAS]
        futs += [pool.submit(run_codex_model, m) for m in ['gpt-5.6-sol', 'gpt-5.5']]
        for fut in as_completed(futs):
            try:
                res = fut.result()
                if isinstance(res, list):
                    results.extend(res); print(res, flush=True)
                else:
                    results.append(res); print(res, flush=True)
            except Exception as e:
                failures.append(str(e)); print('FAIL', e, flush=True)
    print('\nfinished', len(results), 'full-evidence lanes ok')
    if failures:
        print('failures:')
        for f in failures:
            print(' ', f)
        sys.exit(1)

if __name__ == '__main__':
    main()
