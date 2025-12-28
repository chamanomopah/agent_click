"""Selection manager for AgentClick system.

Captures selected text and clipboard content.
"""

import pyperclip
from typing import Optional
from utils.logger import setup_logger

logger = setup_logger('SelectionManager')


class SelectionManager:
    """Manages text selection and clipboard operations."""

    @staticmethod
    def get_selected_text() -> Optional[str]:
        """Get currently selected text from clipboard.

        Returns:
            Selected text or None if clipboard is empty
        """
        try:
            text = pyperclip.paste()
            if text and text.strip():
                logger.debug(f"Captured selection: {text[:50]}...")
                return text.strip()
            return None
        except Exception as e:
            logger.error(f"Error getting selected text: {e}")
            return None

    @staticmethod
    def copy_to_clipboard(text: str) -> bool:
        """Copy text to clipboard.

        Args:
            text: Text to copy

        Returns:
            True if successful, False otherwise
        """
        try:
            pyperclip.copy(text)
            logger.debug("Text copied to clipboard")
            return True
        except Exception as e:
            logger.error(f"Error copying to clipboard: {e}")
            return False

    @staticmethod
    def paste_from_clipboard() -> bool:
        """Simulate paste from clipboard (Ctrl+V).

        Returns:
            True if successful, False otherwise
        """
        try:
            import keyboard
            keyboard.press_and_release('ctrl+v')
            logger.debug("Paste simulated")
            return True
        except Exception as e:
            logger.error(f"Error simulating paste: {e}")
            return False
