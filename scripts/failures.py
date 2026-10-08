"""
failures.py — classify failed simulations by what the agent did wrong.

Compares each failed conversation's write calls against the task's expected
writes (from tau2's action_checks) and sorts it into one of four groups:

    under-action     no write, a transfer, or fewer writes than expected
    wrong details    the right write tool, with different arguments
    wrong action     extra writes, or different write tools
    communication    the database ended up right, but an NL assertion failed

Also reports two transcript heuristics: refusal language ("cannot", "unable",
"not permitted"...) in the agent's last three messages of under-action failures,
and conversations where the simulated user confirmed and ended the conversation
in the same message, before the agent could write (a user-simulator artifact).

These are automatic, pattern-based labels. Hand-code a sample before citing
category differences.

Usage:
    python3 scripts/failures.py results/mvt-2026-10-07/
"""

import argparse
import gzip
import json
import re
from collections import Counter, defaultdict
from pathlib import Path

WRITE_TOOLS = {
    "cancel_pending_order", "exchange_delivered_order_items", "modify_pending_order_address",
    "modify_pending_order_items", "modify_pending_order_payment", "modify_user_address",
    "return_delivered_order_items",
}
GROUPS = ["under-action", "wrong details", "wrong action", "communication"]
REFUSAL = re.compile(r"\b(cannot|can't|unable|not (?:able|permitted|allowed|possible)|not eligible)\b", re.I)
YES = re.compile(r"\b(yes|yep|sure|go ahead|please proceed|let'?s do it|confirm(?:ed)?|sounds good|perfect)\b", re.I)
CONDITION = re.compile(r"_cond(cv2|[abc])")


def load(path: Path) -> list[dict]:
    with (gzip.open(path, "rt") if path.suffix == ".gz" else open(path)) as f:
        return json.load(f)["simulations"]


def tool_calls(sim: dict):
    for m in sim["messages"]:
        if m["role"] == "assistant":
            yield from m.get("tool_calls") or []


def classify(sim: dict) -> str:
    """Return a fine-grained failure label for a failed simulation."""
    ri = sim["reward_info"]
    if (ri.get("reward_breakdown") or {}).get("DB", 1.0) == 1.0:
        return "communication: DB right, NL assertion failed"
    expected = [a["action"] for a in ri.get("action_checks") or [] if a["action"]["name"] in WRITE_TOOLS]
    got = [(c["name"], c.get("arguments") or {}) for c in tool_calls(sim) if c["name"] in WRITE_TOOLS]
    if expected and not got:
        transferred = any(c["name"] == "transfer_to_human_agents" for c in tool_calls(sim))
        return "under-action: no write, transferred" if transferred else "under-action: no write, stopped short"
    if not expected and got:
        return "wrong action: write when none expected"
    exp_n, got_n = Counter(a["name"] for a in expected), Counter(n for n, _ in got)
    if exp_n == got_n:
        diffs = {k for a in expected for n, args in got if n == a["name"]
                 for k, v in a["arguments"].items() if args.get(k) != v}
        return f"wrong details: {','.join(sorted(diffs))}" if diffs else "wrong details: DB differs"
    if sum(got_n.values()) < sum(exp_n.values()):
        return "under-action: fewer writes than expected"
    if sum(got_n.values()) > sum(exp_n.values()):
        return "wrong action: extra writes"
    return "wrong action: different write tools"


def hung_up_on_confirmation(sim: dict) -> bool:
    """User confirmed and ended in one message, right after an agent question."""
    msgs = [m for m in sim["messages"] if m["role"] in ("user", "assistant")]
    if len(msgs) < 2 or msgs[-1]["role"] != "user":
        return False
    last = msgs[-1].get("content") or ""
    prev = (msgs[-2].get("content") or "").strip()
    return "###STOP###" in last and bool(YES.search(last)) and prev.endswith("?")


def main():
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("results_dir", type=Path)
    args = parser.parse_args()

    runs = {}
    for path in sorted([*args.results_dir.glob("*.json"), *args.results_dir.glob("*.json.gz")]):
        m = CONDITION.search(path.name)
        if m:
            runs[m.group(1).upper()] = load(path)
    conds = list(runs)

    labels = {c: [classify(s) for s in sims if s["reward_info"]["reward"] != 1.0] for c, sims in runs.items()}
    header = f"{'':48}" + "".join(f"{c:>6}" for c in conds)

    print("Failures by group\n" + header)
    for g in GROUPS:
        print(f"{g:48}" + "".join(f"{sum(l.startswith(g) for l in labels[c]):>6}" for c in conds))
    print(f"{'total':48}" + "".join(f"{len(labels[c]):>6}" for c in conds))

    print("\nFailures by type\n" + header)
    fine = Counter(l for c in conds for l in labels[c])
    for label, _ in fine.most_common():
        print(f"{label[:48]:48}" + "".join(f"{labels[c].count(label):>6}" for c in conds))

    print("\nTranscript heuristics\n" + header)
    refusals, hangups = {}, {}
    for c, sims in runs.items():
        failed = [s for s in sims if s["reward_info"]["reward"] != 1.0]
        refusals[c] = sum(
            1 for s in failed if classify(s).startswith("under-action")
            and any(REFUSAL.search(m.get("content") or "")
                    for m in [m for m in s["messages"] if m["role"] == "assistant" and m.get("content")][-3:])
        )
        hangups[c] = sum(1 for s in failed if hung_up_on_confirmation(s))
    print(f"{'under-action with refusal language (last 3 msgs)':48}" + "".join(f"{refusals[c]:>6}" for c in conds))
    print(f"{'failed: user confirmed and hung up before write':48}" + "".join(f"{hangups[c]:>6}" for c in conds))

    print("\nTasks by number of passing trials (0..k)")
    for c, sims in runs.items():
        per_task = defaultdict(int)
        for s in sims:
            per_task[s["task_id"]] += s["reward_info"]["reward"] == 1.0
        k = max(Counter(s["task_id"] for s in sims).values())
        dist = Counter(per_task.values())
        print(f"  {c}: " + " ".join(f"{i}:{dist[i]}" for i in range(k + 1)))


if __name__ == "__main__":
    main()
