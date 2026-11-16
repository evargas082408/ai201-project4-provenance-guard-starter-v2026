#!/usr/bin/env python3
"""
Score my five criteria (criteria.md) across three trials and call each one.

    python run_eval.py --label before          # first: the HTTP scenarios
    python check_criteria.py --label before    # then: this

Criteria 1, 2 and 3a are read off the newest `results/run_*_<label>.md` that
run_eval.py wrote: it already sent those texts three times, so this file only
counts. The rest can't be expressed as run_eval scenarios, so this file runs
them itself against the live service, three trials each:

    3b  every score 0.00–1.00 through scoring.score_to_label
    4   10 real submissions, each appealed by its own creator, then 3 appeals
        against made-up ids, all checked against GET /log
    5   the nine malformed bodies criterion 5 names (including a body that is a
        bare JSON list, which run_eval can't send), checked for status, JSON
        error field, exactly one `rejected` log entry each, and /ping after

A target has to hold in every trial; one bad trial is a MISSED.
Writes results/criteria_<stamp>_<label>.md.
"""

import argparse
import datetime as dt
import json
import re
import sys
import time
import uuid

import config
import scoring
import scenarios

URL = f"http://{config.HOST}:{config.PORT}"
TRIALS = 3


# ── reading run_eval's output ────────────────────────────────────────────────

def load_run(label: str) -> tuple[dict[str, list[list[dict]]], str]:
    """({scenario name: [trial1 results, trial2, trial3]}, file name) from the newest run file."""
    pattern = f"run_*_{label}.md" if label else "run_*.md"
    runs = sorted(config.RESULTS_DIR.glob(pattern))
    if not runs:
        sys.exit(f"No results/{pattern}. Run: python run_eval.py --label {label}")
    text = runs[-1].read_text(encoding="utf-8")
    out, current = {}, None
    for line_block in re.split(r"\n(?=### |\*\*Trial )", text):
        if line_block.startswith("### "):
            current = line_block.splitlines()[0][4:].strip()
            out[current] = []
        elif line_block.startswith("**Trial ") and current:
            body = line_block.split("```json", 1)[1].split("```", 1)[0]
            out[current].append(json.loads(body))
    return out, runs[-1].name


def c1(run):
    rows = []
    for t in run["my own writing"]:
        ai = sum(r.get("guess") == "ai" for r in t)
        human = sum(r.get("guess") == "human" for r in t)
        rows.append({"pass": ai == 0 and human >= 6,
                     "shown": f"{ai} ai / {human} human of {len(t)}",
                     "guesses": [r.get("guess") for r in t],
                     "scores": [r.get("confidence") for r in t]})
    return rows


def c2(run):
    rows = []
    for ai_t, hu_t in zip(run["clearly AI"], run["clearly human"]):
        ai = [r["confidence"] for r in ai_t if isinstance(r.get("confidence"), (int, float))]
        hu = [r["confidence"] for r in hu_t if isinstance(r.get("confidence"), (int, float))]
        if len(ai) < 5 or len(hu) < 5:
            rows.append({"pass": False, "shown": "missing scores", "ai": ai, "human": hu})
            continue
        gap = sum(ai) / len(ai) - sum(hu) / len(hu)
        above = sum(a > max(hu) for a in ai)
        rows.append({"pass": gap >= 0.30 and above >= 4,
                     "shown": f"gap {gap:.3f}, {above}/5 above",
                     "ai": ai, "human": hu})
    return rows


def c3(run):
    rows = []
    for t in run["label coverage"]:
        seen = sorted({r.get("guess") for r in t if r.get("guess")})
        sweep = {}
        for i in range(101):
            guess, _ = scoring.score_to_label(i / 100)
            sweep[guess] = sweep.get(guess, 0) + 1
        mapped = sum(v for k, v in sweep.items() if k in ("ai", "human", "unsure"))
        ok = {"ai", "human", "unsure"} <= set(seen) and mapped == 101
        rows.append({"pass": ok, "shown": f"{len(set(seen) & {'ai','human','unsure'})}/3 labels, {mapped}/101 mapped",
                     "labels_seen": seen, "sweep": sweep,
                     "guesses": [r.get("guess") for r in t]})
    return rows


# ── live checks ──────────────────────────────────────────────────────────────

def c4(requests, label):
    texts = [t for s in scenarios.SCENARIOS if s["name"] in ("clearly AI", "clearly human")
             for t in s["texts"]]
    rows = []
    for trial in range(1, TRIALS + 1):
        made = []
        for i, text in enumerate(texts, 1):
            creator = f"c4_{label}_{trial}_{i}"
            sub = requests.post(f"{URL}/submit", json={"text": text, "creator_id": creator}).json()
            app = requests.post(f"{URL}/appeal", json={
                "content_id": sub.get("content_id"), "creator_id": creator,
                "reasoning": f"criterion 4 check, trial {trial}, piece {i}"})
            made.append((sub, app.status_code, app.json()))
        fakes = [uuid.uuid4().hex for _ in range(3)]
        fake_codes = [requests.post(f"{URL}/appeal", json={
            "content_id": f, "creator_id": "c4_nobody", "reasoning": "fake"}).status_code
            for f in fakes]

        log = requests.get(f"{URL}/log").json()["entries"]
        good = 0
        details = []
        for sub, code, body in made:
            cid = sub.get("content_id")
            mine = [e for e in log if isinstance(e, dict) and e.get("content_id") == cid]
            decisions = [e for e in mine if e.get("status") == "decided" and "event" not in e]
            appeals = [e for e in mine if e.get("event") == "appeal"]
            untouched = (len(decisions) == 1
                         and decisions[0].get("combined_score") == sub.get("confidence")
                         and decisions[0].get("label") == sub.get("label"))
            ok = (code == 200 and body.get("status") == "under_review" and untouched
                  and len(appeals) == 1 and appeals[0].get("reasoning")
                  and appeals[0]["timestamp"] >= decisions[0]["timestamp"])
            good += bool(ok)
            details.append({"content_id": cid, "appeal_status": code, "ok": bool(ok)})
        fake_review = sum(1 for e in log if isinstance(e, dict)
                          and e.get("content_id") in fakes and e.get("status") == "under_review")
        fakes_404 = sum(c == 404 for c in fake_codes)
        rows.append({"pass": good == 10 and fakes_404 == 3 and fake_review == 0,
                     "shown": f"{good}/10 valid, {fakes_404}/3 fakes 404",
                     "fake_under_review_entries": fake_review, "valid": details,
                     "fake_codes": fake_codes})
    return rows


BAD_BODIES = [
    ("text missing", {"creator_id": "c5_missing"}),
    ("text empty", {"text": "", "creator_id": "c5_empty"}),
    ("text whitespace", {"text": "   \n\t  ", "creator_id": "c5_space"}),
    ("text null", {"text": None, "creator_id": "c5_null"}),
    ("text a number", {"text": 42, "creator_id": "c5_number"}),
    ("body a JSON list", ["text", "creator_id"]),
    ("creator_id missing", {"text": "A perfectly normal sentence about the weather. And then another one about lunch."}),
    ("text 20,001 chars", {"text": "a" * 20001, "creator_id": "c5_20001"}),
    ("text 50,000 words", {"text": "word " * 50000, "creator_id": "c5_50k"}),
]


def c5(requests):
    rows = []
    for trial in range(1, TRIALS + 1):
        before = len(requests.get(f"{URL}/log").json()["entries"])
        results = []
        for name, body in BAD_BODIES:
            r = requests.post(f"{URL}/submit", json=body)
            try:
                payload = r.json()
            except ValueError:
                payload = None
            results.append({"case": name, "status": r.status_code,
                            "error": payload.get("error") if isinstance(payload, dict) else None})
        new = requests.get(f"{URL}/log").json()["entries"][before:]
        rejected = sum(1 for e in new if isinstance(e, dict) and e.get("status") == "rejected")
        ping = requests.post(f"{URL}/ping", json={"message": "c5"}).status_code == 200
        fivexx = sum(r["status"] >= 500 for r in results)
        fourxx_json = sum(400 <= r["status"] < 500 and bool(r["error"]) for r in results)
        limited = sum(r["status"] == 429 for r in results)
        rows.append({"pass": fivexx == 0 and fourxx_json == 9 and rejected == 9 and len(new) == 9
                     and ping and limited == 0,
                     "shown": f"{fourxx_json}/9 JSON 4xx, {fivexx} 5xx, {rejected} rejected logged, ping {'ok' if ping else 'FAIL'}",
                     "rate_limited": limited, "results": results})
        if trial < TRIALS:
            # Two of the nine have no usable creator_id, so they count against
            # this machine's address. Spread the trials out so a 429 can't
            # stand in for the route's own refusal.
            time.sleep(25)
    return rows


# ── report ───────────────────────────────────────────────────────────────────

TARGETS = {
    1: ("My writing shouldn't get called AI", "0 ai and ≥6 human of 10"),
    2: ("AI and human writing get different scores", "gap ≥ 0.30 and ≥4/5 AI above all human"),
    3: ("All three labels work", "3/3 labels seen, 101/101 scores mapped"),
    4: ("Valid appeals work and get saved", "10/10 valid, 3/3 fakes 404, 0 fake reviews"),
    5: ("Bad requests don't crash the service", "9/9 JSON 4xx, 0 5xx, 9 rejected logged, ping ok"),
}


def main():
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--label", default="")
    args = parser.parse_args()
    import requests

    run, run_name = load_run(args.label)
    print(f"reading {run_name}; running criteria 4 and 5 live (this takes a few minutes)")
    time.sleep(61)  # let run_eval's per-address requests age out of the 1-minute window
    results = {1: c1(run), 2: c2(run), 3: c3(run), 4: c4(requests, args.label or "x"), 5: c5(requests)}

    stamp = dt.datetime.now().strftime("%Y-%m-%d_%H%M")
    label = f"_{args.label}" if args.label else ""
    path = config.RESULTS_DIR / f"criteria_{stamp}{label}.md"
    lines = [f"# Criteria check{f' — {args.label}' if args.label else ''}", "",
             "- Produced by: `check_criteria.py::main`",
             f"- Criteria 1–3a from `results/{run_name}` (`run_eval.py::main`); 3b, 4, 5 run live",
             f"- {TRIALS} trials · {dt.datetime.now().strftime('%Y-%m-%d %H:%M')}", "",
             "| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |", "|---|---|---|---|---|---|"]
    for n, rows in results.items():
        name, target = TARGETS[n]
        verdict = "MET" if all(r["pass"] for r in rows) else "MISSED"
        lines.append(f"| {n}. {name} | {target} | " + " | ".join(r["shown"] for r in rows) + f" | {verdict} |")
    print("\n".join(lines[-7:]))
    lines += ["", "---", "", "## Per-trial detail", ""]
    for n, rows in results.items():
        lines += [f"### Criterion {n}", ""]
        for i, r in enumerate(rows, 1):
            lines += [f"**Trial {i}**", "", "```json", json.dumps(r, indent=2, ensure_ascii=False), "```", ""]
    path.write_text("\n".join(lines), encoding="utf-8")
    print(f"\nWrote {path.relative_to(config.ROOT)}")


if __name__ == "__main__":
    main()
