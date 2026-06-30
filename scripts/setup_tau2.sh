#!/usr/bin/env bash
# setup_tau2.sh — one-time setup after cloning tau2-bench
#
# Run this from the animistic-agents-research/ directory:
#   ./scripts/setup_tau2.sh
#
# What it does:
#   1. Verifies tau2-bench is cloned next to this repo
#   2. Copies our custom agent into tau2-bench's agent package
#   3. Injects a registration line into tau2-bench's registry.py
#      so `tau2 run --agent animistic_agent` works
#
# Safe to re-run: the registry patch is idempotent.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
RESEARCH_DIR="$(dirname "$SCRIPT_DIR")"
TAU2_DIR="$RESEARCH_DIR/tau2-bench"

echo "=== Animistic agents: tau2-bench setup ==="

# 1. Check tau2-bench exists
if [ ! -d "$TAU2_DIR" ]; then
    echo ""
    echo "tau2-bench not found at $TAU2_DIR"
    echo "Clone it first:"
    echo "  cd $RESEARCH_DIR"
    echo "  git clone https://github.com/sierra-research/tau2-bench"
    echo "  cd tau2-bench && uv sync"
    exit 1
fi
echo "✓ tau2-bench found at $TAU2_DIR"

# 2. Copy custom agent into tau2-bench
AGENT_DEST="$TAU2_DIR/src/tau2/agent/animistic_agent.py"
cp "$SCRIPT_DIR/agent.py" "$AGENT_DEST"
echo "✓ Copied agent.py → $AGENT_DEST"

# 3. Patch registry.py (idempotent)
REGISTRY="$TAU2_DIR/src/tau2/registry.py"
PATCH_MARKER="animistic_agent"

if grep -q "$PATCH_MARKER" "$REGISTRY"; then
    echo "✓ registry.py already patched (skipping)"
else
    # Append import and registration at end of file
    cat >> "$REGISTRY" << 'EOF'

# --- Animistic agents research: custom prompt agent ---
from tau2.agent.animistic_agent import create_animistic_agent
registry.register_agent_factory(create_animistic_agent, "animistic_agent")
# --- end animistic agents research ---
EOF
    echo "✓ Patched $REGISTRY to register animistic_agent"
fi

echo ""
echo "Setup complete. You can now run evaluations with:"
echo "  ANIMISTIC_SYSTEM_PROMPT_FILE=prompts/retail/condition-a-unstructured.md \\"
echo "  tau2 run --domain retail --agent animistic_agent --agent-llm gpt-4o --user-llm gpt-4o"
