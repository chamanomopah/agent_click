"""Main system coordinator for AgentClick.

Orchestrates all components: click processing, agents, UI, and configuration.
"""

from typing import Optional, Dict, Any
from PyQt6.QtCore import QObject, pyqtSignal, QThread
from agents.base_agent import BaseAgent
from agents.agent_registry import AgentRegistry
from agents.output_modes import AgentResult
from core.click_processor import ClickProcessor
from core.selection_manager import SelectionManager
from core.output_handler import OutputHandler
from core.input_manager import InputManager
from core.input_strategy import InputType, InputContent
from ui.popup_window import PopupWindow
from ui.mini_popup import MiniPopupWidget
from config.agent_config import AgentConfigManager
from utils.logger import setup_logger

logger = setup_logger('AgentClickSystem')


class SystemSignals(QObject):
    """Signals for thread-safe GUI updates."""
    show_large_popup_signal = pyqtSignal()  # Open large popup
    update_mini_popup_signal = pyqtSignal(object)  # Update mini popup icon
    update_large_popup_agent_signal = pyqtSignal(object)  # Update large popup agent
    log_message_signal = pyqtSignal(str, str)  # message, level
    show_interactive_editor_signal = pyqtSignal(object, object)  # result, context_folder - Open interactive editor in main thread


class AgentClickSystem:
    """Main system coordinator."""

    def __init__(self):
        """Initialize AgentClick system."""
        logger.info("=" * 60)
        logger.info("AgentClick System v1.0 - Initializing")
        logger.info("=" * 60)

        # Initialize signals for thread-safe GUI updates
        self.signals = SystemSignals()
        self.signals.show_large_popup_signal.connect(self._show_large_popup_in_main_thread)
        self.signals.update_mini_popup_signal.connect(self._update_mini_popup_in_main_thread)
        self.signals.update_large_popup_agent_signal.connect(self._update_large_popup_agent_in_main_thread)
        self.signals.log_message_signal.connect(self._log_in_main_thread)
        self.signals.show_interactive_editor_signal.connect(self._show_interactive_editor_in_main_thread)  # NOVO: Interactive editor thread-safe

        # Initialize components
        self.input_manager = InputManager()  # NOVO: Gerenciador de múltiplos inputs
        self.selection_manager = SelectionManager()  # Mantido para compatibilidade
        self.click_processor = ClickProcessor()
        self.agent_registry = AgentRegistry()
        self.config_manager = AgentConfigManager()
        self.output_handler = OutputHandler(self.selection_manager, self.signals)  # NOVO: Pass signals for thread-safe GUI

        # Get initial agent
        initial_agent = self.agent_registry.get_current_agent()

        # Create mini popup (always visible)
        self.mini_popup: Optional[MiniPopupWidget] = MiniPopupWidget(initial_agent)
        self.mini_popup.clicked.connect(self._on_mini_popup_clicked)
        self.mini_popup.file_dropped.connect(self._on_file_dropped)  # NOVO: Drag & drop
        self.mini_popup.show()

        # Large popup (shown only when clicked)
        self.large_popup: Optional[PopupWindow] = None

        # Register callbacks
        self.click_processor.register_pause_handler(self._on_pause_pressed)
        self.click_processor.register_switch_handler(self._on_switch_pressed)
        self.click_processor.register_screenshot_handler(self._on_screenshot_pressed)  # NOVO: Screenshot

        logger.info("AgentClick System initialized successfully")
        logger.info(f"Available agents: {list(self.agent_registry.agents.keys())}")
        logger.info("Press Pause to activate current agent")
        logger.info("Press Ctrl+Pause to switch to next agent")
        logger.info("Press Ctrl+Shift+Pause to take screenshot")  # NOVO
        logger.info("Click mini popup to open detailed view")
        logger.info(f"\n{self.input_manager.get_status_summary()}")  # NOVO

    def _on_pause_pressed(self) -> None:
        """Handle Pause key - activate current agent (no popup)."""
        current_agent = self.agent_registry.get_current_agent()
        if not current_agent:
            logger.warning("No agents available")
            return

        logger.info(f"Activating agent: {current_agent.metadata.name}")

        # Get agent configuration
        agent_name = current_agent.metadata.name
        allowed_inputs = self.config_manager.get_allowed_inputs(agent_name)  # NOVO

        # NOVO: Usar InputManager para capturar input (auto-detect com filtro)
        input_content = self.input_manager.capture_input(allowed_inputs=allowed_inputs)

        if not input_content:
            logger.warning("No input available")
            if self.large_popup:
                self.signals.log_message_signal.emit(
                    "⚠️  No input available",
                    "warning"
                )
            return

        # Log input type
        input_type = input_content.input_type
        logger.info(f"Input type: {input_type.value}")

        # Get text for agent
        selected_text = input_content.get_text_for_agent()

        # Get agent configuration
        context_folder = self.config_manager.get_context_folder(agent_name)
        focus_file = self.config_manager.get_focus_file(agent_name)
        output_mode = self.config_manager.get_output_mode(agent_name)

        logger.info(f"Processing with {current_agent.metadata.name}...")
        logger.info(f"Output mode: {output_mode}")

        # Pass image path if available
        image_path = input_content.image_path

        # Get verbose logging setting
        verbose_logging = self.config_manager.get_verbose_logging(agent_name)

        # Create log callback for verbose logging
        def verbose_log_callback(message: str):
            """Callback to emit verbose log messages to GUI."""
            if self.large_popup:
                self.signals.log_message_signal.emit(message, "info")

        # Process with agent (this happens in keyboard thread)
        try:
            result = current_agent.process(
                selected_text,
                context_folder,
                focus_file,
                output_mode,
                image_path=image_path,  # NOVO: Pass image path
                verbose_logging=verbose_logging,
                log_callback=verbose_log_callback
            )
            self._handle_result(result, current_agent)
        except Exception as e:
            error_msg = f"Error processing: {str(e)}"
            logger.error(error_msg)
            if self.large_popup:
                self.signals.log_message_signal.emit(
                    f"❌ {error_msg}",
                    "error"
                )

    def _on_switch_pressed(self) -> None:
        """Handle Ctrl+Pause - switch to next agent."""
        next_agent = self.agent_registry.next_agent()
        if next_agent:
            logger.info(f"Switched to agent: {next_agent.metadata.name}")
            # Emit signal to update mini popup in main thread
            self.signals.update_mini_popup_signal.emit(next_agent)

            # Also update large popup if it's open
            if self.large_popup:
                self.signals.update_large_popup_agent_signal.emit(next_agent)
                self.signals.log_message_signal.emit(
                    f"🔄 Switched to {next_agent.metadata.name}",
                    "info"
                )

    def _on_file_dropped(self, file_path: str) -> None:
        """Handle file dropped on mini popup.

        Args:
            file_path: Path to dropped file
        """
        from pathlib import Path

        logger.info(f"File dropped: {file_path}")

        # Configure file upload
        self.input_manager.set_file_upload(file_path)

        # Show notification in large popup if open
        if self.large_popup:
            self.signals.log_message_signal.emit(
                f"📎 File loaded: {Path(file_path).name}",
                "info"
            )

        # Auto-process after file drop
        logger.info("Auto-processing dropped file...")
        self._process_input_with_current_agent(InputType.FILE_UPLOAD)

    def _on_screenshot_pressed(self) -> None:
        """Handle Ctrl+Shift+Pause - take screenshot."""
        logger.info("Screenshot hotkey pressed")

        # Take screenshot
        input_content = self.input_manager.take_screenshot()

        if input_content:
            if self.large_popup:
                self.signals.log_message_signal.emit(
                    f"📸 Screenshot captured",
                    "info"
                )

            # Auto-process screenshot
            self._process_input_with_current_agent(InputType.SCREENSHOT)
        else:
            logger.error("Failed to capture screenshot")
            if self.large_popup:
                self.signals.log_message_signal.emit(
                    "❌ Failed to capture screenshot",
                    "error"
                )

    def _process_input_with_current_agent(self, input_type: InputType) -> None:
        """Process input with current agent.

        Args:
            input_type: Type of input to process
        """
        current_agent = self.agent_registry.get_current_agent()
        if not current_agent:
            logger.warning("No agents available")
            return

        logger.info(f"Activating agent: {current_agent.metadata.name}")

        # Get agent configuration
        agent_name = current_agent.metadata.name
        allowed_inputs = self.config_manager.get_allowed_inputs(agent_name)

        # Check if input type is allowed
        if input_type.value not in allowed_inputs:
            # Get friendly name for the input type
            from core.input_strategy import InputType
            input_friendly_name = input_type.value.replace("_", " ").title()

            # Build clear error message
            error_msg = (
                f"⚠️  Input type '{input_friendly_name}' is not selected for agent '{agent_name}'.\n"
                f"   Please select '{input_friendly_name}' as the Input option in the agent configuration."
            )

            logger.warning(error_msg.replace("⚠️  ", "").strip())

            if self.large_popup:
                self.signals.log_message_signal.emit(
                    error_msg,
                    "warning"
                )
            return

        # Capture input
        input_content = self.input_manager.capture_input(
            preferred_type=input_type,
            allowed_inputs=allowed_inputs  # NOVO: Pass allowed inputs
        )

        if not input_content:
            logger.warning(f"No input available for type: {input_type.value}")
            if self.large_popup:
                self.signals.log_message_signal.emit(
                    f"⚠️  No input available",
                    "warning"
                )
            return

        # Get text for agent
        selected_text = input_content.get_text_for_agent()

        # Get agent configuration
        context_folder = self.config_manager.get_context_folder(agent_name)
        focus_file = self.config_manager.get_focus_file(agent_name)
        output_mode = self.config_manager.get_output_mode(agent_name)

        logger.info(f"Processing with {current_agent.metadata.name}...")
        logger.info(f"Input type: {input_type.value}")
        logger.info(f"Output mode: {output_mode}")

        # Pass image path if available
        image_path = input_content.image_path

        # Get verbose logging setting
        verbose_logging = self.config_manager.get_verbose_logging(agent_name)

        # Create log callback for verbose logging
        def verbose_log_callback(message: str):
            """Callback to emit verbose log messages to GUI."""
            if self.large_popup:
                self.signals.log_message_signal.emit(message, "info")

        # Process with agent
        try:
            result = current_agent.process(
                selected_text,
                context_folder,
                focus_file,
                output_mode,
                image_path=image_path,  # NOVO: Pass image path
                verbose_logging=verbose_logging,
                log_callback=verbose_log_callback
            )
            self._handle_result(result, current_agent)
        except Exception as e:
            error_msg = f"Error processing: {str(e)}"
            logger.error(error_msg)
            if self.large_popup:
                self.signals.log_message_signal.emit(
                    f"❌ {error_msg}",
                    "error"
                )

    def _on_mini_popup_clicked(self) -> None:
        """Handle mini popup click - show large popup."""
        logger.info("Mini popup clicked - opening large popup")
        self.signals.show_large_popup_signal.emit()

    def _show_large_popup_in_main_thread(self) -> None:
        """Show large popup window (called in main thread via signal)."""
        if not self.large_popup:
            current_agent = self.agent_registry.get_current_agent()
            self.large_popup = PopupWindow(current_agent)

        # Show popup and process Qt events immediately
        self.large_popup.show()
        self.large_popup.raise_()  # Bring to front
        self.large_popup.activateWindow()  # Ensure it's the active window

        # Process all pending Qt events to ensure popup is visible
        from PyQt6.QtWidgets import QApplication
        QApplication.processEvents()

    def _update_mini_popup_in_main_thread(self, agent: BaseAgent) -> None:
        """Update mini popup (called in main thread via signal)."""
        if self.mini_popup:
            self.mini_popup.update_agent(agent)

    def _update_large_popup_agent_in_main_thread(self, agent: BaseAgent) -> None:
        """Update current agent in large popup GUI (called in main thread via signal)."""
        if self.large_popup:
            self.large_popup.set_current_agent(agent)

    def _log_in_main_thread(self, message: str, level: str) -> None:
        """Log message in large popup GUI (called in main thread via signal)."""
        if self.large_popup:
            self.large_popup.log(message, level)

    def _show_interactive_editor_in_main_thread(self, result: AgentResult, context_folder: Optional[str]) -> None:
        """Show interactive editor dialog in main thread (called via signal for thread safety)."""
        from core.interactive_editor import InteractiveEditorDialog

        try:
            # Create dialog (now in Qt main thread - safe!)
            dialog = InteractiveEditorDialog(result, context_folder)

            # Show dialog (blocking in main thread)
            dialog.exec()

            # Check if user confirmed
            if dialog.was_confirmed():
                final_result = dialog.get_final_result()
                self.logger.info("✅ Interactive editor confirmed")

                # Handle based on user's final choice
                if dialog.get_final_action() == "file":
                    self.output_handler._handle_file(final_result, context_folder)
                else:
                    self.output_handler._handle_clipboard_pure(final_result)

                # Show success message
                if self.large_popup:
                    self.signals.log_message_signal.emit("✅ Interactive editor completed", "success")
            else:
                self.logger.info("❌ Interactive editor cancelled")
                if self.large_popup:
                    self.signals.log_message_signal.emit("❌ Editor cancelled", "warning")

        except Exception as e:
            self.logger.error(f"❌ Error in interactive editor: {e}", exc_info=True)
            if self.large_popup:
                self.signals.log_message_signal.emit(f"❌ Error: {str(e)}", "error")

    def _handle_result(self, result: AgentResult, agent: BaseAgent) -> None:
        """Handle agent processing result.

        Args:
            result: AgentResult from agent
            agent: Agent that processed the request
        """
        from agents.output_modes import OutputMode

        if not result.content:
            logger.warning("Agent returned empty result")
            if self.large_popup:
                self.signals.log_message_signal.emit("⚠️ No result generated", "warning")
            return

        logger.info("Processing complete...")

        # Handle based on output mode
        success = self.output_handler.handle(result, result.metadata.get('context_folder'))

        if success:
            mode = result.output_mode
            if mode == OutputMode.FILE:
                logger.info("✅ Output saved to file")
                if self.large_popup:
                    self.signals.log_message_signal.emit("✅ Saved to file", "success")
            elif mode == OutputMode.INTERACTIVE_EDITOR:
                logger.info("✅ Interactive editor completed")
                if self.large_popup:
                    self.signals.log_message_signal.emit("✅ Editor completed", "success")
            else:
                logger.info("✅ Copied to clipboard")
                if self.large_popup:
                    self.signals.log_message_signal.emit("✅ Copied to clipboard", "success")
        else:
            logger.error("❌ Failed to handle output")
            if self.large_popup:
                self.signals.log_message_signal.emit("❌ Output failed", "error")

    def run(self) -> None:
        """Run the system (Qt event loop handles main loop)."""
        logger.info("System ready. Press Ctrl+C to exit.")
        # No need for a loop here - Qt's app.exec() handles the event loop


    def cleanup(self) -> None:
        """Cleanup system resources."""
        logger.info("Cleaning up...")
        self.click_processor.cleanup()
        if self.mini_popup:
            self.mini_popup.close()
        if self.large_popup:
            self.large_popup.close()
        logger.info("Shutdown complete")
