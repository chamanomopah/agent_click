"""Selected text input strategy.

Captures text currently selected by mouse (without requiring Ctrl+C).
"""

import time
from core.input_strategy import InputStrategy, InputType, InputContent
from core.selection_manager import SelectionManager
from typing import Optional
from utils.logger import setup_logger

logger = setup_logger('SelectedTextStrategy')


class SelectedTextStrategy(InputStrategy):
    """Strategy for mouse-selected text.

    This strategy captures text that user has currently selected with mouse
    by temporarily using Ctrl+C to copy it, then restoring the clipboard.
    """

    def __init__(self):
        """Initialize selected text strategy."""
        self.selection_manager = SelectionManager()
        self.logger = logger

    def get_input_type(self) -> InputType:
        """Return input type."""
        return InputType.SELECTED_TEXT

    def capture_input(self) -> Optional[InputContent]:
        """Capture selected text by temporarily copying it.

        This method:
        1. Saves current clipboard content
        2. Simulates Ctrl+C to copy selected text
        3. Retrieves the copied text
        4. Restores original clipboard content

        Returns:
            InputContent with selected text or None if no text selected
        """
        try:
            # Save current clipboard
            old_clipboard = self.selection_manager.get_selected_text()

            # Simulate Ctrl+C to copy selected text
            from pywinauto import keyboard
            keyboard.send_keys('^c')  # ^ represents Ctrl key

            # Small delay to let clipboard update
            time.sleep(0.1)

            # Get the copied text
            text = self.selection_manager.get_selected_text()

            # Restore original clipboard
            if old_clipboard:
                self.selection_manager.copy_to_clipboard(old_clipboard)

            if text and len(text.strip()) > 0:
                self.logger.info(f"Captured selected text: {len(text)} chars")
                return InputContent(
                    input_type=InputType.SELECTED_TEXT,
                    text=text,
                    metadata={
                        "source": "mouse_selection",
                        "char_count": len(text),
                        "word_count": len(text.split())
                    }
                )

            return None

        except Exception as e:
            self.logger.error(f"Error capturing selected text: {e}")
            return None

    def is_available(self) -> bool:
        """Check if text is currently selected.

        This is a best-effort check - we try to detect if something is selected
        by attempting to capture it.

        Returns:
            True if text appears to be selected
        """
        try:
            # Try to capture - if we get text, something was selected
            text = self.capture_input()
            return text is not None and len(text.text.strip()) > 0 if text else False
        except Exception as e:
            self.logger.error(f"Error checking availability: {e}")
            return False
