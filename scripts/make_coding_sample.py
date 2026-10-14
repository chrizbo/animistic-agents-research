"""
make_coding_sample.py — draw a blinded sample of failures for hand-coding.

Picks N failed conversations at random from each of two conditions, shuffles
them together, and gives them neutral ids (F01, F02, ...). Writes:

    hand-coding/items.json  what the coding page shows: the customer's goal,
                            the expected writes, and the conversation. No
                            condition, task id, trial, or automatic label.
    hand-coding/key.csv     the unblinding key (id → condition, task, trial,
                            automatic label). Don't open it until coding is done.

Usage:
    python3 scripts/make_coding_sample.py results/mvt-2026-10-07/ --conditions A C --n 30
"""

import argparse
import csv
import json
import random
from pathlib import Path

from failures import WRITE_TOOLS, classify, load  # same directory

TASKS = Path("tau2-bench/data/tau2/domains/retail/tasks.json")
RESULT_CHARS = 600  # tool results are long JSON; enough to see what came back


def fmt_call(call: dict) -> str:
    args = ", ".join(f"{k}={json.dumps(v)}" for k, v in (call.get("arguments") or {}).items())
    return f"{call['name']}({args})"


def turns(sim: dict) -> list[dict]:
    out = []
    for m in sim["messages"]:
        role, text = m["role"], (m.get("content") or "").strip()
        if role == "user":
            out.append({"who": "customer", "text": text.replace("###STOP###", "").strip(),
                        "ended": "###STOP###" in text})
        elif role == "assistant":
            calls = [fmt_call(c) for c in m.get("tool_calls") or []]
            writes = [c["name"] in WRITE_TOOLS for c in m.get("tool_calls") or []]
            if text or calls:
                out.append({"who": "agent", "text": text, "calls": calls, "write": any(writes)})
        elif role == "tool":
            body = text if len(text) <= RESULT_CHARS else text[:RESULT_CHARS] + " …"
            out.append({"who": "tool", "text": body, "error": bool(m.get("error"))})
    return out


def main():
    p = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    p.add_argument("results_dir", type=Path)
    p.add_argument("--conditions", nargs="+", default=["A", "C"])
    p.add_argument("--n", type=int, default=30)
    p.add_argument("--seed", type=int, default=20261013)
    p.add_argument("--out", type=Path, default=Path("hand-coding"))
    args = p.parse_args()

    tasks = {t["id"]: t for t in json.loads(TASKS.read_text())}
    rng = random.Random(args.seed)
    picked = []
    for path in sorted([*args.results_dir.glob("*.json"), *args.results_dir.glob("*.json.gz")]):
        cond = next((c for c in args.conditions if f"_cond{c.lower()}_" in path.name), None)
        if cond:
            failed = [s for s in load(path) if s["reward_info"]["reward"] != 1.0]
            picked += [(cond, s) for s in rng.sample(failed, args.n)]
    rng.shuffle(picked)

    items, key = [], []
    for i, (cond, sim) in enumerate(picked, 1):
        item_id = f"F{i:02d}"
        task = tasks[sim["task_id"]]
        ins = task["user_scenario"]["instructions"]
        expected = [a for a in task["evaluation_criteria"]["actions"] if a["name"] in WRITE_TOOLS]
        items.append({
            "id": item_id,
            "goal": ins.get("reason_for_call") or "",
            "persona": ins.get("task_instructions") or "",
            "expected": [fmt_call(a) for a in expected],
            "actual": [fmt_call(c) for c in sim["messages"] and
                       [c for m in sim["messages"] if m["role"] == "assistant"
                        for c in m.get("tool_calls") or [] if c["name"] in WRITE_TOOLS]],
            "turns": turns(sim),
        })
        key.append({"id": item_id, "condition": cond, "task_id": sim["task_id"],
                    "trial": sim["trial"], "auto_label": classify(sim)})

    args.out.mkdir(exist_ok=True)
    (args.out / "items.json").write_text(json.dumps(items, ensure_ascii=False))
    with open(args.out / "key.csv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(key[0]))
        w.writeheader()
        w.writerows(key)
    print(f"Wrote {len(items)} items to {args.out}/items.json "
          f"({(args.out / 'items.json').stat().st_size // 1024} KB) and the key to {args.out}/key.csv")


if __name__ == "__main__":
    main()
