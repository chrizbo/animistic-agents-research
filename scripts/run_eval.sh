#!/usr/bin/env bash
# run_eval.sh — run one tau3-bench evaluation pass for the animistic agents study
#
# Usage:
#   ./scripts/run_eval.sh [options]
#
# Required options:
#   --condition   a | b | c           Prompt condition to evaluate
#   --domain      retail | airline    Domain to run
#   --model       Agent model, as a LiteLLM model string (gpt-4o, claude-sonnet-5-5,
#                 openrouter/deepseek/deepseek-v4-flash, openai/<name> for a local server)
#
# Optional:
#   --trials      Number of trials per task (default: 1)
#   --test        Run only 1 task (pipeline validation mode, no meaningful metrics)
#   --concurrency Max concurrent simulations (default: 5)
#   --agent-api-base  OpenAI-compatible endpoint for the agent only, e.g. a local
#                     llama-server at http://localhost:8080/v1
#   --user-api-base   Same, for the user simulator only
#   --agent-provider  Pin an openrouter/ agent model to one host (e.g. StreamLake), no fallbacks
#   --user-provider   Same, for the user simulator
#   --with-policy     Use prompts/<domain>/with-policy/ (framing only) and append the
#                     verbatim tau2 policy to every condition
#   --resume RUN_NAME Rerun only the infrastructure-error sims of an earlier run (pass
#                     the same condition/model/user flags as the original run)
#   --agent-thinking  on | off — fix the agent's thinking mode (default: model default)
#   --user-thinking   on | off — same, for the user simulator
#
#   # Local agent (llama-server) with a hosted user simulator
#   ./scripts/run_eval.sh --condition a --domain retail --model openai/qwen3.5-9b \
#       --agent-api-base http://localhost:8080/v1 --concurrency 1 --num-tasks 20
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
WITH_POLICY=false
RESUME=""
CONCURRENCY=5
NUM_TASKS=""
USER_MODEL="${USER_MODEL:-gpt-4o}"   # .env may set the study-wide user simulator
AGENT_API_BASE=""
USER_API_BASE=""
AGENT_PROVIDER=""
USER_PROVIDER="${USER_PROVIDER:-}"
AGENT_THINKING=""
USER_THINKING="${USER_THINKING:-}"

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
        --with-policy) WITH_POLICY=true; shift ;;
        --resume)      RESUME="$2"; shift 2 ;;
        --concurrency) CONCURRENCY="$2"; shift 2 ;;
        --agent-api-base) AGENT_API_BASE="$2"; shift 2 ;;
        --user-api-base)  USER_API_BASE="$2";  shift 2 ;;
        --agent-provider) AGENT_PROVIDER="$2"; shift 2 ;;
        --user-provider)  USER_PROVIDER="$2";  shift 2 ;;
        --agent-thinking) AGENT_THINKING="$2"; shift 2 ;;
        --user-thinking)  USER_THINKING="$2";  shift 2 ;;
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

# Framing experiment: framing-only prompts, with the verbatim policy appended by agent.py
if [ "$WITH_POLICY" = true ]; then
    PROMPT_FILE="$RESEARCH_DIR/prompts/$DOMAIN/with-policy/condition-$CONDITION.md"
fi

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

# LLM args per side. An api_base routes only that side to a custom endpoint, so a
# local agent never redirects the hosted user simulator (as OPENAI_API_BASE would).
# Temperature 0 matches tau2's default, which passing llm-args would otherwise replace.
# A provider pins an OpenRouter model to one host with fallbacks off: hosts serve the
# same open model at different quantizations, so silent rerouting would add noise.
# Thinking (on|off) is fixed per run so conditions never differ in it; empty keeps the
# model's default. OpenRouter takes a unified reasoning switch, llama-server the template's.
llm_args() {
    python3 - "$1" "$2" "$3" <<'PY'
import json, sys
api_base, provider, thinking = sys.argv[1:4]
args, extra = {"temperature": 0.0}, {}
if api_base:
    args.update(api_base=api_base, api_key="local")
if provider:
    extra["provider"] = {"order": [provider], "allow_fallbacks": False}
if thinking:
    on = thinking == "on"
    if api_base:
        extra["chat_template_kwargs"] = {"enable_thinking": on}
    else:
        extra["reasoning"] = {"enabled": on}
if extra:
    args["extra_body"] = extra
print(json.dumps(args))
PY
}
for t in "$AGENT_THINKING" "$USER_THINKING"; do
    case "$t" in ""|on|off) ;; *) echo "Thinking must be on or off, got: $t"; exit 1 ;; esac
done
AGENT_LLM_ARGS=$(llm_args "$AGENT_API_BASE" "$AGENT_PROVIDER" "$AGENT_THINKING")
USER_LLM_ARGS=$(llm_args "$USER_API_BASE" "$USER_PROVIDER" "$USER_THINKING")

# Build a descriptive run name for result traceability. Model strings may contain
# provider prefixes with slashes (openrouter/..., openai/...), so flatten them.
safe_name() { local s="${1//\//_}"; s="${s//-/_}"; echo "${s//./_}"; }
DATE=$(date +%Y-%m-%d_%H%M)
K_LABEL="k${TRIALS}"
if [ "$TEST_MODE" = true ]; then K_LABEL="k1"; fi
AGENT_TAG="$(safe_name "$MODEL")${AGENT_THINKING:+_think_$AGENT_THINKING}"
POLICY_TAG=""
if [ "$WITH_POLICY" = true ]; then POLICY_TAG="_pol"; fi
RUN_NAME="${DOMAIN}_cond${CONDITION}${POLICY_TAG}_${AGENT_TAG}_u_$(safe_name "$USER_MODEL")_${K_LABEL}_${DATE}"
# Resuming reuses the run's directory; tau2 then reruns only infrastructure-error sims
RESUME_ARG=""
if [ -n "$RESUME" ]; then
    RUN_NAME="$RESUME"
    RESUME_ARG="--auto-resume"
fi

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
ANIMISTIC_INCLUDE_POLICY=$([ "$WITH_POLICY" = true ] && echo 1 || echo 0) \
uv run tau2 run \
    --domain "$DOMAIN" \
    --agent animistic_agent \
    --agent-llm "$MODEL" \
    --agent-llm-args "$AGENT_LLM_ARGS" \
    --user-llm "$USER_MODEL" \
    --user-llm-args "$USER_LLM_ARGS" \
    --num-trials "$TRIALS" \
    --max-concurrency "$CONCURRENCY" \
    --seed 300 \
    --save-to "$RUN_NAME" \
    $RESUME_ARG \
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
