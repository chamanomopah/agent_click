"""SDK Logger Module for verbose Claude Code SDK logging.

This module provides functionality to intercept and parse Claude SDK messages,
extracting tool usage, file operations, and progress information for real-time logging.
"""

from typing import Optional, Callable, Any, List
from dataclasses import dataclass
from utils.logger import setup_logger

logger = setup_logger('SDKLogger')


@dataclass
class ToolUseEvent:
    """Represents a tool use event extracted from SDK message."""
    tool_name: str
    file_path: Optional[str] = None
    description: str = ""

    def format_message(self) -> str:
        """Format tool use as a concise log message.

        Returns:
            Formatted message string
        """
        # Icon mapping for different tool types
        icons = {
            "Read": "📖",
            "Write": "✏️",
            "Edit": "📝",
            "Grep": "🔍",
            "Glob": "📁",
            "Bash": "💻",
            "Task": "🤖",
            "WebSearch": "🌐",
        }

        icon = icons.get(self.tool_name, "🔧")

        if self.file_path:
            # Truncate long file paths
            display_path = self.file_path
            if len(display_path) > 50:
                display_path = "..." + display_path[-47:]
            return f"{icon} Using {self.tool_name}: {display_path}"
        else:
            return f"{icon} Using {self.tool_name}"


class SDKMessageParser:
    """Parser for Claude SDK messages to extract tool usage and file operations."""

    # Tool names that we want to log
    LOGGED_TOOLS = {
        "Read", "Write", "Edit", "Grep", "Glob",
        "Bash", "Task", "WebSearch", "AskUserQuestion",
        "SlashCommand", "NotebookEdit", "Skill"
    }

    @staticmethod
    def extract_tool_use(message: Any) -> Optional[ToolUseEvent]:
        """Extract tool use information from SDK message.

        Args:
            message: SDK message object

        Returns:
            ToolUseEvent if message contains tool use, None otherwise
        """
        try:
            # Check if message has content blocks
            if not hasattr(message, 'content'):
                return None

            # Iterate through content blocks
            for block in message.content:
                # Look for tool use blocks
                if hasattr(block, 'type') and block.type == 'tool_use':
                    tool_name = getattr(block, 'name', None)
                    if not tool_name:
                        continue

                    # Only log specific tools
                    if tool_name not in SDKMessageParser.LOGGED_TOOLS:
                        continue

                    # Extract file path from tool input
                    file_path = None
                    if hasattr(block, 'input'):
                        input_data = block.input

                        # Common parameter names for file paths
                        for param in ['file_path', 'path', 'filepath', 'filename', 'url']:
                            if param in input_data:
                                file_path = input_data[param]
                                break

                    return ToolUseEvent(
                        tool_name=tool_name,
                        file_path=file_path,
                        description=""
                    )

        except Exception as e:
            logger.debug(f"Error extracting tool use: {e}")

        return None

    @staticmethod
    def is_tool_result(message: Any) -> bool:
        """Check if message is a tool result.

        Args:
            message: SDK message object

        Returns:
            True if message is a tool result
        """
        try:
            if hasattr(message, 'type'):
                return message.type == 'tool_result'
        except Exception:
            pass
        return False

    @staticmethod
    def get_message_type(message: Any) -> str:
        """Get the type of a message.

        Args:
            message: SDK message object

        Returns:
            Message type string
        """
        if hasattr(message, 'type'):
            return message.type
        return "unknown"


class VerboseSDKWrapper:
    """Wrapper around Claude SDK query that provides verbose logging callbacks.

    This wraps the async generator from query() and yields messages while
    emitting formatted log messages through a callback function.
    """

    def __init__(
        self,
        query_generator,
        log_callback: Optional[Callable[[str], None]] = None,
        enabled: bool = True
    ):
        """Initialize the verbose SDK wrapper.

        Args:
            query_generator: The async generator from query()
            log_callback: Function to call with formatted log messages
            enabled: Whether verbose logging is enabled
        """
        self.query_generator = query_generator
        self.log_callback = log_callback
        self.enabled = enabled
        self.parser = SDKMessageParser()
        self._message_count = 0

    def _log(self, message: str) -> None:
        """Internal logging method.

        Args:
            message: Message to log
        """
        if self.log_callback and self.enabled:
            self.log_callback(message)

    async def wrapped_query(self):
        """Async generator that wraps the original query with logging.

        Yields:
            Original messages from query() while logging tool usage
        """
        try:
            async for message in self.query_generator:
                self._message_count += 1

                # Extract and log tool usage
                if self.enabled:
                    tool_event = self.parser.extract_tool_use(message)
                    if tool_event:
                        self._log(tool_event.format_message())

                # Yield the original message
                yield message

        except Exception as e:
            logger.error(f"Error in verbose wrapper: {e}")
            raise

    def get_message_count(self) -> int:
        """Get the number of messages processed.

        Returns:
            Message count
        """
        return self._message_count


def create_verbose_wrapper(
    query_generator,
    log_callback: Optional[Callable[[str], None]] = None,
    enabled: bool = True
) -> VerboseSDKWrapper:
    """Factory function to create a VerboseSDKWrapper.

    Args:
        query_generator: The async generator from query()
        log_callback: Function to call with formatted log messages
        enabled: Whether verbose logging is enabled

    Returns:
        VerboseSDKWrapper instance
    """
    return VerboseSDKWrapper(
        query_generator=query_generator,
        log_callback=log_callback,
        enabled=enabled
    )
