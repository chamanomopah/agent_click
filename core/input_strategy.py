"""Input strategies for AgentClick system.

Defines different ways users can provide input to agents.
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Optional, Dict, Any
from enum import Enum
from utils.logger import setup_logger

logger = setup_logger('InputStrategy')


class InputType(Enum):
    """Types of input."""
    TEXT_SELECTION = "text_selection"
    FILE_UPLOAD = "file_upload"
    CLIPBOARD_IMAGE = "clipboard_image"
    SCREENSHOT = "screenshot"


@dataclass
class InputContent:
    """Content from user input.

    Attributes:
        input_type: Type of input
        text: Text content (if applicable)
        file_path: Path to file (if applicable)
        image_path: Path to image/screenshot (if applicable)
        metadata: Additional metadata
    """
    input_type: InputType
    text: Optional[str] = None
    file_path: Optional[str] = None
    image_path: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None

    def get_text_for_agent(self) -> str:
        """Get text representation for agent processing.

        Returns:
            Text string with context about input source
        """
        if self.input_type == InputType.TEXT_SELECTION:
            return self.text or ""

        elif self.input_type == InputType.FILE_UPLOAD:
            file_info = ""
            if self.metadata and "file_name" in self.metadata:
                file_info = f"File: {self.metadata['file_name']}"
            return f"[FILE UPLOAD: {file_info}]\n{self.text or ''}"

        elif self.input_type == InputType.CLIPBOARD_IMAGE:
            return f"[IMAGE from clipboard]\n{self.text or ''}"

        elif self.input_type == InputType.SCREENSHOT:
            return f"[SCREENSHOT captured]\n{self.text or ''}"

        return ""

    def has_image(self) -> bool:
        """Check if input contains an image.

        Returns:
            True if has image
        """
        return self.image_path is not None

    def has_file(self) -> bool:
        """Check if input contains a file.

        Returns:
            True if has file
        """
        return self.file_path is not None


class InputStrategy(ABC):
    """Abstract base class for input strategies.

    Each strategy represents a different way to capture user input.
    """

    @abstractmethod
    def get_input_type(self) -> InputType:
        """Return the input type.

        Returns:
            InputType enum value
        """
        pass

    @abstractmethod
    def capture_input(self) -> Optional[InputContent]:
        """Capture input from user.

        This is the main method that performs the actual input capture.

        Returns:
            InputContent object or None if no input available
        """
        pass

    @abstractmethod
    def is_available(self) -> bool:
        """Check if this input type is currently available.

        Returns:
            True if input is available and can be captured
        """
        pass

    def get_description(self) -> str:
        """Get human-readable description of this strategy.

        Returns:
            Description string
        """
        return self.get_input_type().value.replace("_", " ").title()
