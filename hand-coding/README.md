# Hand-coding failures

A blinded sample of failed conversations from the [k=5 minimum viable test](../results-preliminary/mvt-retail-k5-qwen.md), for checking by hand whether the ledger framing shifts failures from doing the wrong thing toward not doing the right thing.

**Coding page:** https://claude.ai/artifact/UAZY2nYBoBKPzEvbSecd8Z (private to the owner). Labels save automatically to the page's database.

| File | What it is |
|---|---|
| `coding.html` | The coding page (published as the artifact above) |
| `items.json` | The 60 sampled failures as the page shows them: customer goal, expected and actual writes, conversation. No condition, task id, or automatic label |
| `key.csv` | **The unblinding key. Don't open it until coding is done.** Maps each item id to condition, task, trial, and the automatic label from `scripts/failures.py` |

## Sample

30 failures drawn at random from condition A (role) and 30 from condition C (ledger), shuffled together and given neutral ids F01–F60. Seed 20261013. Rebuild with:

```bash
PYTHONPATH=scripts python3 scripts/make_coding_sample.py results/mvt-2026-10-07/ --conditions A C --n 30
```

## Codebook

**What went wrong?** (one)

| Label | Meaning |
|---|---|
| Did the wrong thing | A write that shouldn't have happened, or one with wrong details (items, payment method, order, an extra or different action) |
| Didn't do the right thing | A needed write never happened: the agent refused, said it wasn't possible, transferred, stopped, or did only part of the request |
| Both | A wrong write and a missing one |
| Not the agent's fault | The customer confirmed and hung up in the same message, contradicted their own goal, or the expected writes look wrong given the conversation |
| Can't tell | |

**Refusal involved** (yes/no): the agent refused or said something wasn't allowed, whether or not that was correct.

**Which prompt was this?** (optional, after labeling): role, ledger, or can't tell. This is a rough manipulation check. If the framing can't be told apart from the transcripts, it barely shows in the agent's language.

## Blinding limits

Condition labels are hidden, but the ledger's wording ("entries", "write") can give it away. Label from the expected and actual writes first, then guess the prompt.

## Analysis plan (fixed before coding)

1. Share of "did the wrong thing" vs. "didn't do the right thing" in A vs. C, compared with the automatic labels.
2. Agreement between hand and automatic labels.
3. Share of "not the agent's fault" per condition, which estimates benchmark noise.
4. Accuracy of prompt guesses against chance (50%).
