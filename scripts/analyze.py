#!/usr/bin/env python3
"""
analyze.py — parse tau3-bench results and generate comparison graphs.

Usage:
    python scripts/analyze.py --results-dir results/ --output-dir analysis/

    # Inspect raw structure of a single results file:
    python scripts/analyze.py --inspect results/retail_condA_gpt4o_k1_2026-07-01.json

Results files are named:
    {domain}_cond{A|B|C}_{model}_k{trials}_{date}.json

Metrics computed:
    pass@1   — mean reward across all tasks (primary tau-bench metric)
    pass^k   — fraction of tasks where ALL k trials succeeded (when k > 1)
    db_reward       — database state correctness (back of house: what was written)
    nl_assertion_reward — share of sims passing all NL assertions, over tasks that define them
    communicate_reward  — share of sims communicating all required info, over tasks that define it
                          (the last two are front of house: what the user was told)
    read_before_auth — share of sims where a data tool ran before identity lookup (scope violation)

Comparisons:
    analysis/comparisons.csv — each condition vs A and B on the same tasks, with paired
                               bootstrap 95% CIs over tasks for pass@1 and pass^k

Output:
    analysis/pass_at_1_{domain}.png/pdf    — bar chart, all conditions × models
    analysis/pass_k_{domain}.png/pdf       — pass^k chart (when k>1 data exists)
    analysis/db_reward_{domain}.png/pdf    — policy adherence bar chart
    analysis/summary.csv                   — full metrics table
"""

import argparse
import json
import re
import sys
from collections import defaultdict
from pathlib import Path

# ── Optional imports: only needed for graphing ─────────────────────────────────
try:
    import matplotlib
    matplotlib.use("Agg")  # headless backend
    import matplotlib.pyplot as plt
    import numpy as np
    HAS_MATPLOTLIB = True
except ImportError:
    HAS_MATPLOTLIB = False

try:
    import pandas as pd
    HAS_PANDAS = True
except ImportError:
    HAS_PANDAS = False


# ── Result file parsing ────────────────────────────────────────────────────────

FILENAME_RE = re.compile(
    r"(?P<domain>retail|airline)"
    r"_cond(?P<condition>cv2|[abc])"
    r"(?P<policy>_pol)?"  # framing experiment: verbatim policy appended
    r"_(?P<model>[^_]+(?:_[^_]+)*?)(?:_u_(?P<user_model>[^_]+(?:_[^_]+)*?))?(?=_k)"  # agent model + optional _u_ user model
    r"_k(?P<trials>\d+)"
    r"_(?P<date>\d{4}-\d{2}-\d{2})"
    r"(?:_(?P<suffix>.+))?"
    r"\.json$",
    re.IGNORECASE,
)


def parse_filename(path: Path) -> dict | None:
    """Extract condition/domain/model/trials from a results filename."""
    m = FILENAME_RE.match(path.name)
    if not m:
        return None
    d = m.groupdict()
    d["model"] = d["model"].replace("_", "-")  # restore hyphens
    # Keep the two experiments apart in every chart and table
    if d.pop("policy"):
        d["model"] += " +policy"
    d["trials"] = int(d["trials"])
    d["condition"] = d["condition"].upper() if d["condition"] != "cv2" else "CV2"
    return d


def load_results(path: Path) -> list[dict]:
    """
    Load tau3-bench results.json and return a flat list of simulation records.

    Expected structure (text/half-duplex runs):
    {
        "simulations": [
            {
                "task_id": "1",
                "trial": 0,
                "reward": 1.0,
                "reward_info": {
                    "db_reward": 1.0,
                    "communicate_reward": 1.0,
                    ...
                }
            },
            ...
        ]
    }

    NOTE: If the structure differs (tau3-bench is under active development),
    run with --inspect to see the raw format and adjust accordingly.
    """
    with open(path) as f:
        data = json.load(f)

    # Handle both top-level list and {"simulations": [...]} formats
    if isinstance(data, list):
        sims = data
    elif "simulations" in data:
        sims = data["simulations"]
    else:
        raise ValueError(
            f"Unexpected results format in {path}. "
            "Run with --inspect to see the raw structure."
        )

    # Rate limits and provider outages say nothing about the prompt; tau2 excludes
    # these from its own metrics, and `run_eval.sh --resume` reruns them.
    infra = [s for s in sims if s.get("termination_reason") == "infrastructure_error"]
    if infra:
        print(f"  ⚠ {path.name}: excluding {len(infra)} infrastructure-error sims "
              f"(rerun with run_eval.sh --resume)")
        sims = [s for s in sims if s.get("termination_reason") != "infrastructure_error"]
    return sims


# ── Metrics ────────────────────────────────────────────────────────────────────

AUTH_TOOLS = {"find_user_id_by_email", "find_user_id_by_name_zip"}
NEUTRAL_TOOLS = {"think", "calculate", "transfer_to_human_agents"}


def read_before_auth(sim: dict) -> bool:
    """True if the agent called a data tool before any identity lookup.

    A scope violation the DB check cannot see: the policy requires verifying the
    user first, but reading an order early leaves the database unchanged.
    """
    for m in sim.get("messages") or []:
        for call in (m.get("tool_calls") or []) if m.get("role") == "assistant" else []:
            name = call.get("name")
            if name in AUTH_TOOLS:
                return False
            if name not in NEUTRAL_TOOLS:
                return True
    return False

def compute_metrics(sims: list[dict], trials: int) -> dict:
    """
    Compute pass@1, pass^k, db_reward, communicate_reward from simulation records.
    """
    # Group by task_id
    by_task = defaultdict(list)
    for s in sims:
        task_id = s.get("task_id") or s.get("id") or s.get("task", {}).get("id")
        ri = s.get("reward_info") or {}
        reward = ri.get("reward", s.get("reward", 0.0))
        by_task[task_id].append(reward)

    rewards = []
    pass_k_scores = []
    db_rewards = []
    nl_rewards = []
    comm_rewards = []

    for task_id, task_rewards in by_task.items():
        rewards.extend(task_rewards)
        pass_k_scores.append(1.0 if all(r == 1.0 for r in task_rewards) else 0.0)

    # Extract component rewards if present
    for s in sims:
        ri = s.get("reward_info") or {}
        db_check = ri.get("db_check") or {}
        if "db_reward" in db_check:
            db_rewards.append(db_check["db_reward"])
        elif "db_reward" in ri:
            db_rewards.append(ri["db_reward"])
        # Front-of-house checks (tau2 >= 1.0.1). Only sims whose task defines the
        # check count; tasks without assertions would otherwise score a free 1.0.
        if ri.get("nl_assertions"):
            nl_rewards.append(float(all(a.get("met") for a in ri["nl_assertions"])))
        if ri.get("communicate_checks"):
            comm_rewards.append(float(all(c.get("met") for c in ri["communicate_checks"])))

    n_tasks = len(by_task)
    mean = lambda xs: sum(xs) / len(xs) if xs else None
    rba = [float(read_before_auth(s)) for s in sims]

    return {
        "n_tasks": n_tasks,
        "n_simulations": len(sims),
        "trials": trials,
        "pass_at_1": mean(rewards),
        "pass_k": mean(pass_k_scores) if trials > 1 else None,
        "db_reward": mean(db_rewards),
        "nl_assertion_reward": mean(nl_rewards),
        "communicate_reward": mean(comm_rewards),
        "read_before_auth": mean(rba),
        "task_rewards": dict(by_task),  # for paired comparisons, not written to CSV
    }


# ── Loading all results ────────────────────────────────────────────────────────

def load_all(results_dir: Path) -> list[dict]:
    """Load and parse all results files in the directory."""
    records = []
    for path in sorted(results_dir.glob("*.json")):
        meta = parse_filename(path)
        if meta is None:
            print(f"  Skipping (unrecognised filename): {path.name}")
            continue
        try:
            sims = load_results(path)
            metrics = compute_metrics(sims, meta["trials"])
            records.append({**meta, **metrics, "file": path.name})
            print(f"  Loaded {path.name}: {metrics['n_tasks']} tasks, "
                  f"pass@1={metrics['pass_at_1']:.3f}")
        except Exception as e:
            print(f"  Error loading {path.name}: {e}")
    return records


# ── Graphing ───────────────────────────────────────────────────────────────────

CONDITION_LABELS = {"A": "Condition A\n(unstructured)", "B": "Condition B\n(RISEN)", "C": "Condition C\n(animistic)", "CV2": "Condition C-v2\n(animistic+mood)"}
CONDITION_COLORS = {"A": "#6baed6", "B": "#74c476", "C": "#fd8d3c", "CV2": "#e84393"}
MODEL_HATCHES   = {"gpt-4o": "", "claude-sonnet-4-5": "///"}


def bar_chart(records: list[dict], domain: str, metric: str, ylabel: str,
              title: str, output_dir: Path, filename: str):
    """Generate a grouped bar chart comparing conditions across models."""
    if not HAS_MATPLOTLIB:
        print(f"  Skipping chart {filename} (matplotlib not installed)")
        return

    domain_records = [r for r in records if r["domain"] == domain and r[metric] is not None]
    if not domain_records:
        print(f"  No data for {domain} / {metric}")
        return

    models = sorted({r["model"] for r in domain_records})
    conditions = [c for c in ["A", "B", "C", "CV2"] if any(r["condition"] == c for r in domain_records)]
    n_cond = len(conditions)
    n_models = len(models)

    x = np.arange(n_cond)
    width = 0.35
    offsets = np.linspace(-width * (n_models - 1) / 2, width * (n_models - 1) / 2, n_models)

    fig, ax = plt.subplots(figsize=(8, 5))

    for i, model in enumerate(models):
        values = []
        for cond in conditions:
            match = [r for r in domain_records if r["condition"] == cond and r["model"] == model]
            values.append(match[0][metric] if match else 0.0)

        bars = ax.bar(
            x + offsets[i], values, width * 0.9,
            label=model,
            color=[CONDITION_COLORS[c] for c in conditions],
            hatch=MODEL_HATCHES.get(model, ""),
            edgecolor="white",
            alpha=0.9,
        )
        # Value labels on bars
        for bar, val in zip(bars, values):
            ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.01,
                    f"{val:.2f}", ha="center", va="bottom", fontsize=8)

    ax.set_xticks(x)
    ax.set_xticklabels([CONDITION_LABELS[c] for c in conditions])
    ax.set_ylim(0, 1.1)
    ax.set_ylabel(ylabel)
    ax.set_title(title)
    ax.legend(title="Model", loc="upper left")
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    fig.tight_layout()

    for ext in ("png", "pdf"):
        out = output_dir / f"{filename}.{ext}"
        fig.savefig(out, dpi=150)
        print(f"  Saved {out}")
    plt.close(fig)


def pass_k_chart(records: list[dict], domain: str, output_dir: Path):
    """Chart pass^k where k>1 data is available."""
    bar_chart(
        records, domain, "pass_k",
        ylabel="pass^k (all trials must succeed)",
        title=f"Behavioral consistency (pass^k) — {domain}",
        output_dir=output_dir,
        filename=f"pass_k_{domain}",
    )


# ── CSV summary ────────────────────────────────────────────────────────────────

def write_csv(records: list[dict], output_dir: Path):
    cols = ["domain", "condition", "model", "trials", "n_tasks", "n_simulations",
            "pass_at_1", "pass_k", "db_reward", "nl_assertion_reward", "communicate_reward", "read_before_auth", "file"]
    lines = [",".join(cols)]
    for r in sorted(records, key=lambda x: (x["domain"], x["condition"], x["model"])):
        lines.append(",".join(str(r.get(c, "")) for c in cols))
    out = output_dir / "summary.csv"
    out.write_text("\n".join(lines))
    print(f"  Saved {out}")


# ── Paired comparisons ─────────────────────────────────────────────────────────

def paired_diff(a: dict, b: dict, k_metric: bool, n_boot: int = 10000, seed: int = 0):
    """Mean difference b - a over shared tasks, with a bootstrap 95% CI over tasks.

    Resampling tasks (not simulations) respects that trials of one task are correlated.
    """
    import random
    tasks = sorted(set(a) & set(b))
    if not tasks:
        return None
    score = (lambda rs: float(all(r == 1.0 for r in rs))) if k_metric else \
            (lambda rs: sum(rs) / len(rs))
    diffs = [score(b[t]) - score(a[t]) for t in tasks]
    rng = random.Random(seed)
    boots = sorted(
        sum(rng.choice(diffs) for _ in diffs) / len(diffs) for _ in range(n_boot)
    )
    return (sum(diffs) / len(diffs), boots[int(0.025 * n_boot)], boots[int(0.975 * n_boot)], len(tasks))


def write_comparisons(records: list[dict], output_dir: Path):
    """Compare each condition against A and B within the same domain, model, and k."""
    lines = ["domain,model,trials,comparison,metric,diff,ci_low,ci_high,n_tasks,ci_excludes_zero"]
    print("\nPaired comparisons (diff, 95% CI over tasks):")
    groups = defaultdict(dict)
    for r in records:
        group = groups[(r["domain"], r["model"], r["trials"])]
        prev = group.get(r["condition"])
        if prev:
            # Pilots and finals for one cell must not be mixed; keep the larger run
            print(f"  ⚠ two runs for {r['condition']} {r['model']} k={r['trials']}: "
                  f"{prev['file']} and {r['file']}; comparing the larger. "
                  f"Move pilots to results/pilot/.")
            if r["n_simulations"] <= prev["n_simulations"]:
                continue
        group[r["condition"]] = r
    for (domain, model, trials), by_cond in sorted(groups.items()):
        for base in ["A", "B"]:
            for cond in ["B", "C", "CV2"]:
                if cond == base or base not in by_cond or cond not in by_cond:
                    continue
                for metric, k_metric in [("pass_at_1", False)] + ([("pass_k", True)] if trials > 1 else []):
                    res = paired_diff(by_cond[base]["task_rewards"], by_cond[cond]["task_rewards"], k_metric)
                    if res is None:
                        continue
                    d, lo, hi, n = res
                    sig = lo > 0 or hi < 0
                    lines.append(f"{domain},{model},{trials},{cond}-{base},{metric},{d:.3f},{lo:.3f},{hi:.3f},{n},{sig}")
                    print(f"  {domain} {model} k={trials}  {cond}-{base} {metric}: "
                          f"{d:+.3f} [{lo:+.3f}, {hi:+.3f}] n={n}{'  *' if sig else ''}")
    out = output_dir / "comparisons.csv"
    out.write_text("\n".join(lines))
    print(f"  Saved {out}")


# ── Inspect mode ───────────────────────────────────────────────────────────────

def inspect(path: Path):
    """Pretty-print the structure of a results.json for format debugging."""
    with open(path) as f:
        data = json.load(f)

    print(f"\n=== Structure of {path.name} ===")
    if isinstance(data, dict):
        print(f"Top-level keys: {list(data.keys())}")
        for key, val in data.items():
            if isinstance(val, list) and val:
                print(f"\n  {key}[0] sample:")
                sample = val[0]
                for k, v in (sample.items() if isinstance(sample, dict) else []):
                    print(f"    {k}: {repr(v)[:120]}")
            else:
                print(f"  {key}: {repr(val)[:120]}")
    elif isinstance(data, list) and data:
        print(f"Top-level: list of {len(data)} items. First item:")
        for k, v in (data[0].items() if isinstance(data[0], dict) else []):
            print(f"  {k}: {repr(v)[:120]}")


# ── Main ───────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="Analyze tau3-bench results for animistic agents study")
    parser.add_argument("--results-dir", type=Path, default=Path("results/"), help="Directory containing results JSON files")
    parser.add_argument("--output-dir",  type=Path, default=Path("analysis/"), help="Directory for output charts and CSV")
    parser.add_argument("--inspect",     type=Path, default=None, help="Inspect the raw structure of a single results file and exit")
    args = parser.parse_args()

    if args.inspect:
        inspect(args.inspect)
        return

    if not args.results_dir.exists():
        print(f"Results directory not found: {args.results_dir}")
        sys.exit(1)

    args.output_dir.mkdir(parents=True, exist_ok=True)

    if not HAS_MATPLOTLIB:
        print("Warning: matplotlib not installed. Charts will be skipped.")
        print("Install with: pip install matplotlib numpy --break-system-packages")
    if not HAS_PANDAS:
        print("Warning: pandas not installed. CSV will still be written.")

    print(f"\nLoading results from {args.results_dir}...")
    records = load_all(args.results_dir)

    if not records:
        print("No results files found or parsed.")
        sys.exit(0)

    print(f"\nGenerating charts in {args.output_dir}...")

    domains = sorted({r["domain"] for r in records})
    for domain in domains:
        bar_chart(records, domain, "pass_at_1",
                  ylabel="pass@1 (task completion rate)",
                  title=f"Task completion rate (pass@1) — {domain}",
                  output_dir=args.output_dir,
                  filename=f"pass_at_1_{domain}")

        bar_chart(records, domain, "db_reward",
                  ylabel="DB reward (policy / state correctness)",
                  title=f"Policy adherence (DB reward) — {domain}",
                  output_dir=args.output_dir,
                  filename=f"db_reward_{domain}")

        if any(r["trials"] > 1 for r in records if r["domain"] == domain):
            pass_k_chart(records, domain, args.output_dir)

    print("\nWriting summary CSV...")
    write_csv(records, args.output_dir)
    write_comparisons(records, args.output_dir)

    print("\nDone.")


if __name__ == "__main__":
    main()
