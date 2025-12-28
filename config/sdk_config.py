"""SDK configuration factory for AgentClick system."""

from claude_agent_sdk import ClaudeAgentOptions
from typing import Optional
from utils.logger import setup_logger

logger = setup_logger('SDKConfig')


def create_sdk_options(
    system_prompt: str,
    allowed_tools: Optional[list] = None,
    permission_mode: str = "default"
) -> ClaudeAgentOptions:
    """Create ClaudeAgentOptions with standard configuration.

    Args:
        system_prompt: System prompt for the agent
        allowed_tools: List of allowed tools (None for default set)
        permission_mode: Permission mode for SDK

    Returns:
        Configured ClaudeAgentOptions instance
    """
    if allowed_tools is None:
        allowed_tools = ["Read", "Write", "Edit", "Grep", "Glob"]

    options = ClaudeAgentOptions(
        system_prompt=system_prompt,
        allowed_tools=allowed_tools,
        permission_mode=permission_mode
    )

    logger.debug(f"Created SDK options with {len(allowed_tools)} tools")
    return options
