"""Output handler for AgentClick system.

Handles different output modes for agent results.
"""

import os
from pathlib import Path
from typing import Optional
from PyQt6.QtWidgets import QApplication
from agents.output_modes import OutputMode, AgentResult
from core.selection_manager import SelectionManager
from core.interactive_editor import InteractiveEditorDialog
from utils.logger import setup_logger

logger = setup_logger('OutputHandler')


class OutputHandler:
    """Handles output based on configured mode."""

    def __init__(self, selection_manager: SelectionManager):
        """Initialize output handler.

        Args:
            selection_manager: Selection manager for clipboard operations
        """
        self.selection_manager = selection_manager
        self.logger = logger


    def handle(self, result: AgentResult, context_folder: Optional[str] = None) -> bool:
        """Handle agent result based on output mode.

        Args:
            result: Agent result to handle
            context_folder: Optional context folder for file operations

        Returns:
            True if successful, False otherwise
        """
        mode = result.output_mode

        self.logger.info(f"Handling output with mode: {mode.value}")

        try:
            # AUTO mode: decide based on content
            if mode == OutputMode.AUTO:
                return self._handle_auto(result, context_folder)

            # CLIPBOARD_PURE: content only
            elif mode == OutputMode.CLIPBOARD_PURE:
                return self._handle_clipboard_pure(result)

            # CLIPBOARD_RICH: formatted content
            elif mode == OutputMode.CLIPBOARD_RICH:
                return self._handle_clipboard_rich(result)

            # FILE: save to file
            elif mode == OutputMode.FILE:
                return self._handle_file(result, context_folder)

            # INTERACTIVE_EDITOR: preview and edit
            elif mode == OutputMode.INTERACTIVE_EDITOR:
                return self._handle_interactive(result, context_folder)

            else:
                self.logger.warning(f"Unknown mode: {mode}, defaulting to AUTO")
                return self._handle_auto(result, context_folder)

        except Exception as e:
            self.logger.error(f"Error handling output: {e}", exc_info=True)
            return False


    def _handle_auto(self, result: AgentResult, context_folder: Optional[str]) -> bool:
        """AUTO mode: decide best output based on content.

        Rules:
        - If has suggested_filename and context_folder → FILE
        - If content is code (>50 lines) → FILE
        - If content has raw_thoughts → CLIPBOARD_RICH
        - Otherwise → CLIPBOARD_PURE
        """
        content_lines = result.content.count('\n')

        # Has filename and folder? Save to file
        if result.suggested_filename and context_folder:
            self.logger.info("AUTO: Detected filename + context, using FILE mode")
            return self._handle_file(result, context_folder)

        # Large code content? Save to file
        if content_lines > 50 and context_folder:
            self.logger.info("AUTO: Large content (>50 lines), using FILE mode")
            result.suggested_filename = result.suggested_filename or "output.txt"
            return self._handle_file(result, context_folder)

        # Has thoughts? Use rich format
        if result.raw_thoughts:
            self.logger.info("AUTO: Has reasoning, using CLIPBOARD_RICH")
            return self._handle_clipboard_rich(result)

        # Default: pure clipboard
        self.logger.info("AUTO: Using CLIPBOARD_PURE")
        return self._handle_clipboard_pure(result)


    def _handle_clipboard_pure(self, result: AgentResult) -> bool:
        """Copy only pure content to clipboard."""
        content = result.get_pure_content()

        if self.selection_manager.copy_to_clipboard(content):
            self.logger.info(f"✅ Copied pure content to clipboard ({len(content)} chars)")
            return True
        else:
            self.logger.error("❌ Failed to copy to clipboard")
            return False


    def _handle_clipboard_rich(self, result: AgentResult) -> bool:
        """Copy formatted content to clipboard."""
        content = result.get_rich_content()

        if self.selection_manager.copy_to_clipboard(content):
            self.logger.info(f"✅ Copied rich content to clipboard ({len(content)} chars)")
            return True
        else:
            self.logger.error("❌ Failed to copy to clipboard")
            return False


    def _handle_file(self, result: AgentResult, context_folder: Optional[str]) -> bool:
        """Save content to file."""
        if not context_folder:
            self.logger.warning("No context folder for FILE mode, falling back to clipboard")
            return self._handle_clipboard_pure(result)

        # Determine filename
        filename = result.suggested_filename or "output.txt"
        if not filename.endswith('.txt') and not any(filename.endswith(ext) for ext in ['.py', '.js', '.md', '.json', '.yaml', '.yml']):
            filename += '.txt'

        # Create full path
        file_path = Path(context_folder) / filename

        try:
            # Ensure directory exists
            file_path.parent.mkdir(parents=True, exist_ok=True)

            # Write content
            content = result.get_pure_content()
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)

            self.logger.info(f"✅ Saved to file: {file_path}")

            # Also copy to clipboard for convenience
            self.selection_manager.copy_to_clipboard(content)
            self.logger.info("📋 Also copied to clipboard")

            return True

        except Exception as e:
            self.logger.error(f"❌ Failed to save file: {e}")
            return False


    def _handle_interactive(self, result: AgentResult, context_folder: Optional[str]) -> bool:
        """Open interactive editor for preview and editing."""
        try:
            # Create dialog (non-blocking)
            dialog = InteractiveEditorDialog(result, context_folder)

            # Show dialog
            dialog.exec()

            # Check if user confirmed
            if dialog.was_confirmed():
                final_result = dialog.get_final_result()
                self.logger.info(f"✅ Interactive editor confirmed")

                # Handle based on user's final choice
                if dialog.get_final_action() == "file":
                    return self._handle_file(final_result, context_folder)
                else:
                    return self._handle_clipboard_pure(final_result)
            else:
                self.logger.info("❌ Interactive editor cancelled")
                return False

        except Exception as e:
            self.logger.error(f"❌ Error in interactive editor: {e}", exc_info=True)
            return False
