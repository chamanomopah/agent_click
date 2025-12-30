"""Text selection input strategy.

Captures text selected by user (current behavior).
"""

from core.input_strategy import InputStrategy, InputType, InputContent
from core.selection_manager import SelectionManager
from typing import Optional
from utils.logger import setup_logger

logger = setup_logger('TextSelectionStrategy')


class TextSelectionStrategy(InputStrategy):
    """Strategy for text selection input (current behavior).

    This strategy captures text that user has selected and copied
    to clipboard using Ctrl+C.
    """

    def __init__(self):
        """Initialize text selection strategy."""
        self.selection_manager = SelectionManager()
        self.logger = logger

    def get_input_type(self) -> InputType:
        """Return input type."""
        return InputType.TEXT_SELECTION

    def capture_input(self) -> Optional[InputContent]:
        """Capture selected text from clipboard.

        Returns:
            InputContent with selected text or None if clipboard empty
        """
        try:
            text = self.selection_manager.get_selected_text()

            if text:
                self.logger.info(f"Captured text selection: {len(text)} chars")
                return InputContent(
                    input_type=InputType.TEXT_SELECTION,
                    text=text,
                    metadata={
                        "source": "clipboard",
                        "char_count": len(text),
                        "word_count": len(text.split())
                    }
                )

            return None

        except Exception as e:
            self.logger.error(f"Error capturing text selection: {e}")
            return None

    def is_available(self) -> bool:
        """Check if text is available in clipboard.

        Returns:
            True if clipboard has text content
        """
        try:
            text = self.selection_manager.get_selected_text()
            return text is not None and len(text.strip()) > 0
        except Exception as e:
            self.logger.error(f"Error checking availability: {e}")
            return False
