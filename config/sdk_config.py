"""SDK configuration factory for AgentClick system."""

from claude_agent_sdk import ClaudeAgentOptions
from typing import Optional
from utils.logger import setup_logger

logger = setup_logger('SDKConfig')


def create_sdk_options(
    system_prompt: str,
    allowed_tools: Optional[list] = None,
    permission_mode: str = "bypassPermissions",
    cwd: Optional[str] = None
) -> ClaudeAgentOptions:
    """Create ClaudeAgentOptions with standard configuration.

    Args:
        system_prompt: System prompt for the agent
        allowed_tools: List of allowed tools (None for default set)
        permission_mode: Permission mode for SDK (default: "bypassPermissions" for automated agents)
        cwd: Working directory for tool execution (where files should be edited)

    Returns:
        Configured ClaudeAgentOptions instance
    """
    if allowed_tools is None:
        allowed_tools = ["Read", "Write", "Edit", "Grep", "Glob"]

    options = ClaudeAgentOptions(
        system_prompt=system_prompt,
        allowed_tools=allowed_tools,
        permission_mode=permission_mode,
        cwd=cwd
    )

    logger.debug(f"Created SDK options with {len(allowed_tools)} tools, cwd={cwd}")
    return options
