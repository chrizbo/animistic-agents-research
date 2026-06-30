"""
CustomPromptLLMAgent — drops the tau2 system prompt wrapper entirely
and uses the contents of ANIMISTIC_SYSTEM_PROMPT_FILE as the sole system prompt.

Why override the wrapper?
    The default LLMAgent wraps domain_policy in:
        <instructions>You are a customer service agent...</instructions>
        <policy>{domain_policy}</policy>
    That outer instruction is role-based framing ("customer service agent"),
    which would confound the comparison between conditions. By overriding
    system_prompt we ensure all three conditions (A / B / C) are evaluated
    with exactly the text in their respective prompt files — nothing added,
    nothing removed.

Usage (after setup_tau2.sh has been run):
    ANIMISTIC_SYSTEM_PROMPT_FILE=../prompts/retail/condition-c-animistic.md \
    tau2 run --domain retail --agent animistic_agent --agent-llm gpt-4o ...
"""

import os
from pathlib import Path
from typing import List, Optional

from tau2.agent.llm_agent import LLMAgent
from tau2.environment.tool import Tool


class CustomPromptLLMAgent(LLMAgent):
    """
    Subclass of LLMAgent that replaces the system prompt entirely with the
    contents of a file specified by the ANIMISTIC_SYSTEM_PROMPT_FILE env var.
    All other behaviour (tool calling, message loop, state management) is
    inherited unchanged from LLMAgent.
    """

    def __init__(
        self,
        tools: List[Tool],
        domain_policy: str,
        llm: str,
        llm_args: Optional[dict] = None,
    ):
        super().__init__(
            tools=tools,
            domain_policy=domain_policy,
            llm=llm,
            llm_args=llm_args,
        )
        prompt_file = os.environ.get("ANIMISTIC_SYSTEM_PROMPT_FILE")
        if not prompt_file:
            raise EnvironmentError(
                "ANIMISTIC_SYSTEM_PROMPT_FILE env var must be set to the path "
                "of the system prompt file to use."
            )
        path = Path(prompt_file)
        if not path.exists():
            raise FileNotFoundError(f"System prompt file not found: {path}")
        self._custom_system_prompt = path.read_text().strip()

    @property
    def system_prompt(self) -> str:
        """Return the raw file contents as the sole system prompt."""
        return self._custom_system_prompt


def create_animistic_agent(tools, domain_policy, **kwargs):
    """
    Factory function registered with tau2's agent registry.
    Called by the eval framework when --agent animistic_agent is passed to tau2 run.
    """
    return CustomPromptLLMAgent(
        tools=tools,
        domain_policy=domain_policy,
        llm=kwargs.get("llm"),
        llm_args=kwargs.get("llm_args"),
    )
