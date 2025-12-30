"""Output mode definitions for AgentClick agents."""

from enum import Enum
from dataclasses import dataclass
from typing import Optional, Dict, Any
from utils.logger import setup_logger

logger = setup_logger('OutputModes')


class OutputMode(Enum):
    """Available output modes for agents."""

    AUTO = "AUTO"
    """Agent automatically decides the best output mode based on content."""

    CLIPBOARD_PURE = "CLIPBOARD_PURE"
    """Copy only essential content to clipboard, no formatting or metadata."""

    CLIPBOARD_RICH = "CLIPBOARD_RICH"
    """Copy formatted content (markdown, structure) to clipboard."""

    FILE = "FILE"
    """Save output directly to a file in the project."""

    INTERACTIVE_EDITOR = "INTERACTIVE_EDITOR"
    """Open preview window for editing before finalizing output."""


    @property
    def display_name(self) -> str:
        """Human-readable name for UI display."""
        display_map = {
            OutputMode.AUTO: "🤖 Auto (Agent Decide)",
            OutputMode.CLIPBOARD_PURE: "📋 Clipboard (Pure)",
            OutputMode.CLIPBOARD_RICH: "📋 Clipboard (Rich)",
            OutputMode.FILE: "💾 Save to File",
            OutputMode.INTERACTIVE_EDITOR: "✏️ Interactive Editor"
        }
        return display_map.get(self, self.value)


    @property
    def description(self) -> str:
        """Detailed description for tooltips."""
        desc_map = {
            OutputMode.AUTO: "Agent chooses best output based on task",
            OutputMode.CLIPBOARD_PURE: "Raw content without formatting or metadata",
            OutputMode.CLIPBOARD_RICH: "Formatted content with markdown structure",
            OutputMode.FILE: "Automatically save to file in project folder",
            OutputMode.INTERACTIVE_EDITOR: "Preview and edit before final output"
        }
        return desc_map.get(self, "")


    @classmethod
    def from_string(cls, value: str) -> 'OutputMode':
        """Convert string to OutputMode.

        Args:
            value: String value to convert

        Returns:
            OutputMode enum value

        Raises:
            ValueError: If value is not a valid mode
        """
        try:
            return cls(value.upper())
        except ValueError:
            logger.warning(f"Invalid output mode: {value}, defaulting to AUTO")
            return cls.AUTO


    def should_use_file(self) -> bool:
        """Check if this mode requires file output."""
        return self == OutputMode.FILE


    def should_use_clipboard(self) -> bool:
        """Check if this mode uses clipboard."""
        return self in {
            OutputMode.CLIPBOARD_PURE,
            OutputMode.CLIPBOARD_RICH
        }


    def requires_interaction(self) -> bool:
        """Check if this mode requires user interaction."""
        return self == OutputMode.INTERACTIVE_EDITOR


@dataclass
class AgentResult:
    """Structured result from agent processing."""

    content: str
    """Main content/output from the agent."""

    output_mode: OutputMode
    """How the output should be delivered."""

    metadata: Optional[Dict[str, Any]] = None
    """Additional metadata (filename, language, etc)."""

    raw_thoughts: Optional[str] = None
    """Agent's internal reasoning/thoughts (separated from content)."""

    suggested_filename: Optional[str] = None
    """Suggested filename for FILE mode."""

    def __post_init__(self):
        """Initialize metadata if None."""
        if self.metadata is None:
            self.metadata = {}


    def get_pure_content(self) -> str:
        """Get content without metadata or formatting."""
        return self.content


    def get_rich_content(self) -> str:
        """Get content with formatting."""
        if self.raw_thoughts:
            return f"# Reasoning\n\n{self.raw_thoughts}\n\n---\n\n# Output\n\n{self.content}"
        return self.content
