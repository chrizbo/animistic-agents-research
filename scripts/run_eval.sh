#!/usr/bin/env bash
# run_eval.sh — run one tau3-bench evaluation pass for the animistic agents study
#
# Usage:
#   ./scripts/run_eval.sh [options]
#
# Required options:
#   --condition   a | b | c           Prompt condition to evaluate
#   --domain      retail | airline    Domain to run
#   --model       gpt-4o | claude-sonnet-4-5   Agent model
#
# Optional:
#   --trials      Number of trials per task (default: 1)
#   --test        Run only 1 task (pipeline validation mode, no meaningful metrics)
#   --concurrency Max concurrent simulations (default: 5)
#
# Examples:
#   # Test mode — validate pipeline with one task
#   ./scripts/run_eval.sh --condition c --domain retail --model gpt-4o --test
#
#   # Full pilot run (k=1)
#   ./scripts/run_eval.sh --condition c --domain retail --model gpt-4o --trials 1
#
#   # Full final run (k=5)
#   ./scripts/run_eval.sh --condition c --domain retail --model gpt-4o --trials 5

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
RESEARCH_DIR="$(dirname "$SCRIPT_DIR")"

# Load .env if present
if [ -f "$RESEARCH_DIR/.env" ]; then
    set -a; source "$RESEARCH_DIR/.env"; set +a
fi
TAU2_DIR="$RESEARCH_DIR/tau2-bench"

# ── Defaults ──────────────────────────────────────────────────────────────────
CONDITION=""
DOMAIN=""
MODEL=""
TRIALS=1
TEST_MODE=false
CONCURRENCY=5
NUM_TASKS=""
USER_MODEL="gpt-4o"

# ── Parse arguments ───────────────────────────────────────────────────────────
while [[ $# -gt 0 ]]; do
    case "$1" in
        --condition)   CONDITION="$2";  shift 2 ;;
        --domain)      DOMAIN="$2";     shift 2 ;;
        --model)       MODEL="$2";      shift 2 ;;
        --user-model)  USER_MODEL="$2"; shift 2 ;;
        --trials)      TRIALS="$2";     shift 2 ;;
        --num-tasks)   NUM_TASKS="$2";  shift 2 ;;
        --test)        TEST_MODE=true;  shift ;;
        --concurrency) CONCURRENCY="$2"; shift 2 ;;
        *) echo "Unknown argument: $1"; exit 1 ;;
    esac
done

# ── Validate required args ────────────────────────────────────────────────────
if [[ -z "$CONDITION" || -z "$DOMAIN" || -z "$MODEL" ]]; then
    echo "Error: --condition, --domain, and --model are required."
    echo "Run with --help or see script header for usage."
    exit 1
fi

case "$CONDITION" in
    a)   PROMPT_FILE="$RESEARCH_DIR/prompts/$DOMAIN/condition-a-unstructured.md" ;;
    b)   PROMPT_FILE="$RESEARCH_DIR/prompts/$DOMAIN/condition-b-risen.md" ;;
    c)   PROMPT_FILE="$RESEARCH_DIR/prompts/$DOMAIN/condition-c-v1-animistic.md" ;;
    cv2) PROMPT_FILE="$RESEARCH_DIR/prompts/$DOMAIN/condition-c-animistic.md" ;;
    *) echo "Unknown condition: $CONDITION (must be a, b, c, or cv2)"; exit 1 ;;
esac

if [ ! -f "$PROMPT_FILE" ]; then
    echo "Prompt file not found: $PROMPT_FILE"
    exit 1
fi

# ── Build tau2 run arguments ──────────────────────────────────────────────────
NUM_TASKS_ARG=""
if [ "$TEST_MODE" = true ]; then
    NUM_TASKS_ARG="--num-tasks 1"
    echo "⚠  TEST MODE: running 1 task only. Results are not meaningful for analysis."
elif [ -n "$NUM_TASKS" ]; then
    NUM_TASKS_ARG="--num-tasks $NUM_TASKS"
fi

# Map model names to provider for user LLM
case "$MODEL" in
    gpt-4o*)       PROVIDER="openai" ;;
    claude-*)      PROVIDER="anthropic" ;;
    *)             PROVIDER="openai" ;;
esac

# Build a descriptive run name for result traceability
DATE=$(date +%Y-%m-%d_%H%M)
K_LABEL="k${TRIALS}"
if [ "$TEST_MODE" = true ]; then K_LABEL="k1"; fi
RUN_NAME="${DOMAIN}_cond${CONDITION}_${MODEL//-/_}_u_${USER_MODEL//-/_}_${K_LABEL}_${DATE}"

echo "=== Animistic agents: tau2-bench evaluation ==="
echo "  Condition:   $CONDITION"
echo "  Domain:      $DOMAIN"
echo "  Model:       $MODEL"
echo "  Trials:      $TRIALS"
echo "  Prompt file: $PROMPT_FILE"
echo "  Run name:    $RUN_NAME"
echo ""

# ── Run evaluation ────────────────────────────────────────────────────────────
cd "$TAU2_DIR"

ANIMISTIC_SYSTEM_PROMPT_FILE="$PROMPT_FILE" \
uv run tau2 run \
    --domain "$DOMAIN" \
    --agent animistic_agent \
    --agent-llm "$MODEL" \
    --user-llm "$USER_MODEL" \
    --num-trials "$TRIALS" \
    --max-concurrency "$CONCURRENCY" \
    --seed 300 \
    --save-to "$RUN_NAME" \
    $NUM_TASKS_ARG

# ── Copy results to research repo ─────────────────────────────────────────────
RESULT_SRC="$TAU2_DIR/data/simulations/$RUN_NAME/results.json"
RESULT_DEST="$RESEARCH_DIR/results/${RUN_NAME}.json"

if [ -f "$RESULT_SRC" ]; then
    cp "$RESULT_SRC" "$RESULT_DEST"
    echo ""
    echo "✓ Results copied to results/${RUN_NAME}.json"
else
    echo ""
    echo "⚠  results.json not found at expected path: $RESULT_SRC"
    echo "   Check $TAU2_DIR/data/simulations/$RUN_NAME/ manually."
fi
