"""Popup window for AgentClick system.

Minimalist popup showing agent status and activity log.
"""

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QTextEdit, QPushButton,
    QLineEdit, QHBoxLayout, QFileDialog, QTabWidget, QGroupBox, QFormLayout, QComboBox, QCheckBox
)
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QFont, QTextCursor
from typing import Optional
from agents.base_agent import BaseAgent
from agents.output_modes import OutputMode
from config.agent_config import AgentConfigManager, AgentSettings
from utils.logger import setup_logger

logger = setup_logger('PopupWindow')


class PopupWindow(QWidget):
    """Minimalist popup window for agent activity."""

    def __init__(self, current_agent: BaseAgent):
        """Initialize popup window.

        Args:
            current_agent: Currently active agent
        """
        super().__init__()
        self.logger = setup_logger('PopupWindow')
        self.current_agent = current_agent
        self.config_manager = AgentConfigManager()

        self._setup_ui()
        self._load_current_config()
        self.logger.info("Popup window initialized")

    def _setup_ui(self):
        """Setup UI components."""
        # Window properties
        self.setWindowTitle("AgentClick")
        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint |
            Qt.WindowType.WindowStaysOnTopHint |
            Qt.WindowType.Tool
        )

        # Size and position (bottom right)
        self.setFixedSize(600, 550)
        self._position_window()

        # Main layout
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(15, 15, 15, 15)
        main_layout.setSpacing(10)

        # Header with agent info
        header_layout = QVBoxLayout()

        # Agent name and icon
        self.agent_label = QLabel(
            f"{self.current_agent.metadata.icon} "
            f"{self.current_agent.metadata.name}"
        )
        self.agent_label.setStyleSheet("""
            QLabel {
                font-size: 18px;
                font-weight: bold;
                color: #ffffff;
                background-color: %s;
                padding: 10px;
                border-radius: 5px;
            }
        """ % self.current_agent.metadata.color)
        self.agent_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        header_layout.addWidget(self.agent_label)

        # Description
        self.desc_label = QLabel(self.current_agent.metadata.description)
        self.desc_label.setStyleSheet("""
            QLabel {
                font-size: 11px;
                color: #666666;
                padding: 5px;
            }
        """)
        self.desc_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.desc_label.setWordWrap(True)
        header_layout.addWidget(self.desc_label)

        main_layout.addLayout(header_layout)

        # Tab widget
        self.tab_widget = QTabWidget()
        self.tab_widget.setMinimumHeight(350)
        self.tab_widget.setStyleSheet("""
            QTabWidget::pane {
                border: 1px solid #cccccc;
                border-radius: 5px;
                background-color: #ffffff;
                top: -1px;
            }
            QTabBar::tab {
                background-color: #e0e0e0;
                padding: 10px 18px;
                margin-right: 2px;
                margin-bottom: 2px;
                border-top-left-radius: 5px;
                border-top-right-radius: 5px;
                font-size: 11px;
                font-weight: 500;
            }
            QTabBar::tab:selected {
                background-color: #ffffff;
                font-weight: bold;
                border-bottom: 2px solid #0078d4;
            }
            QTabBar::tab:hover:!selected {
                background-color: #eeeeee;
            }
        """)

        # Activity Log Tab
        self._create_activity_log_tab()

        # Configuration Tab
        self._create_config_tab()

        main_layout.addWidget(self.tab_widget)

        # Close button
        close_btn = QPushButton("✕ Close")
        close_btn.setStyleSheet("""
            QPushButton {
                background-color: #cccccc;
                color: #333333;
                border: none;
                padding: 8px;
                border-radius: 5px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #bbbbbb;
            }
            QPushButton:pressed {
                background-color: #aaaaaa;
            }
        """)
        close_btn.clicked.connect(self.close)
        main_layout.addWidget(close_btn)

        self.setLayout(main_layout)

        # Initial log message
        self.log("✨ Agent ready", "info")

    def _create_activity_log_tab(self):
        """Create activity log tab."""
        log_tab = QWidget()
        log_layout = QVBoxLayout()
        log_layout.setContentsMargins(10, 10, 10, 10)
        log_layout.setSpacing(8)

        log_label = QLabel("Activity Log:")
        log_label.setStyleSheet("""
            QLabel {
                font-size: 12px;
                font-weight: bold;
                color: #333333;
            }
        """)
        log_layout.addWidget(log_label)

        self.log_text = QTextEdit()
        self.log_text.setReadOnly(True)
        self.log_text.setStyleSheet("""
            QTextEdit {
                background-color: #f5f5f5;
                border: 1px solid #cccccc;
                border-radius: 5px;
                padding: 8px;
                font-family: 'Consolas', 'Monaco', monospace;
                font-size: 11px;
            }
            QScrollBar:vertical {
                border: none;
                background-color: #f0f0f0;
                width: 12px;
                margin: 0px;
            }
            QScrollBar::handle:vertical {
                background-color: #cccccc;
                min-height: 20px;
                border-radius: 6px;
            }
            QScrollBar::handle:vertical:hover {
                background-color: #aaaaaa;
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                height: 0px;
            }
        """)
        log_layout.addWidget(self.log_text)

        # Clear Log button
        clear_log_btn = QPushButton("🗑️ Clear Log")
        clear_log_btn.setStyleSheet("""
            QPushButton {
                background-color: #6c757d;
                color: #ffffff;
                border: none;
                padding: 6px 12px;
                border-radius: 4px;
                font-size: 11px;
                font-weight: 500;
            }
            QPushButton:hover {
                background-color: #5a6268;
            }
            QPushButton:pressed {
                background-color: #4e5456;
            }
        """)
        clear_log_btn.clicked.connect(self._clear_log)
        log_layout.addWidget(clear_log_btn)

        # Add stretch to push log_text to top
        log_layout.addStretch()

        log_tab.setLayout(log_layout)
        self.tab_widget.addTab(log_tab, "📋 Activity")

    def _create_config_tab(self):
        """Create configuration tab."""
        config_tab = QWidget()
        config_layout = QVBoxLayout()
        config_layout.setContentsMargins(10, 5, 10, 10)
        config_layout.setSpacing(10)

        # Configuration group
        config_group = QGroupBox("Agent Configuration")
        config_group.setStyleSheet("""
            QGroupBox {
                font-size: 12px;
                font-weight: bold;
                color: #333333;
                border: 2px solid #cccccc;
                border-radius: 5px;
                margin-top: 10px;
                padding-top: 10px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px;
            }
        """)
        config_form = QFormLayout()
        config_form.setSpacing(8)
        config_form.setContentsMargins(5, 5, 5, 5)

        # Context Folder
        self.context_folder_edit = QLineEdit()
        self.context_folder_edit.setPlaceholderText(r"C:\path\to\project")
        self.context_folder_edit.setStyleSheet("""
            QLineEdit {
                padding: 5px;
                border: 1px solid #cccccc;
                border-radius: 3px;
            }
        """)

        context_browse_btn = QPushButton("📁 Browse")
        context_browse_btn.setStyleSheet("""
            QPushButton {
                background-color: #0078d4;
                color: #ffffff;
                border: none;
                padding: 5px 10px;
                border-radius: 3px;
            }
            QPushButton:hover {
                background-color: #005a9e;
            }
        """)
        context_browse_btn.clicked.connect(self._browse_context_folder)

        context_layout = QHBoxLayout()
        context_layout.addWidget(self.context_folder_edit)
        context_layout.addWidget(context_browse_btn)

        config_form.addRow("Context Folder:", context_layout)

        # Focus File
        self.focus_file_edit = QLineEdit()
        self.focus_file_edit.setPlaceholderText(r"C:\path\to\file.ext")
        self.focus_file_edit.setStyleSheet("""
            QLineEdit {
                padding: 5px;
                border: 1px solid #cccccc;
                border-radius: 3px;
            }
        """)

        focus_browse_btn = QPushButton("📄 Browse")
        focus_browse_btn.setStyleSheet("""
            QPushButton {
                background-color: #0078d4;
                color: #ffffff;
                border: none;
                padding: 5px 10px;
                border-radius: 3px;
            }
            QPushButton:hover {
                background-color: #005a9e;
            }
        """)
        focus_browse_btn.clicked.connect(self._browse_focus_file)

        focus_layout = QHBoxLayout()
        focus_layout.addWidget(self.focus_file_edit)
        focus_layout.addWidget(focus_browse_btn)

        config_form.addRow("Focus File:", focus_layout)

        # Output
        output_mode_label = QLabel("Output:")
        output_mode_label.setStyleSheet("""
            QLabel {
                font-size: 11px;
                font-weight: bold;
                color: #333333;
            }
        """)

        self.output_mode_combo = QComboBox()
        self.output_mode_combo.setStyleSheet("""
            QComboBox {
                padding: 5px;
                border: 1px solid #cccccc;
                border-radius: 3px;
                background-color: white;
            }
            QComboBox::drop-down {
                border: none;
            }
            QComboBox::down-arrow {
                width: 12px;
                height: 12px;
            }
        """)

        # Add all output modes
        for mode in OutputMode:
            self.output_mode_combo.addItem(mode.display_name, mode.value)

        config_form.addRow(output_mode_label, self.output_mode_combo)

        # Input selection (simplified dropdown)
        input_label = QLabel("Input:")
        input_label.setStyleSheet("""
            QLabel {
                font-size: 11px;
                font-weight: bold;
                color: #333333;
            }
        """)

        self.input_combo = QComboBox()
        self.input_combo.setStyleSheet("""
            QComboBox {
                padding: 5px;
                border: 1px solid #cccccc;
                border-radius: 3px;
                background-color: white;
            }
            QComboBox::drop-down {
                border: none;
            }
            QComboBox::down-arrow {
                width: 12px;
                height: 12px;
            }
        """)

        # Add input options with friendly names
        from core.input_strategy import InputType
        input_options = [
            ("Text Selection (clipboard)", InputType.TEXT_SELECTION.value),
            ("Selected Text (mouse)", InputType.SELECTED_TEXT.value),
            ("VSCode Active File", InputType.VSCODE_ACTIVE_FILE.value),
            ("File Upload (drag & drop)", InputType.FILE_UPLOAD.value),
            ("Clipboard Image", InputType.CLIPBOARD_IMAGE.value),
            ("Screenshot (Ctrl+Shift+Pause)", InputType.SCREENSHOT.value)
        ]

        for display_name, value in input_options:
            self.input_combo.addItem(display_name, value)

        config_form.addRow(input_label, self.input_combo)

        # Verbose Logging checkbox
        self.verbose_logging_checkbox = QCheckBox("Enable Verbose Logging")
        self.verbose_logging_checkbox.setStyleSheet("""
            QCheckBox {
                font-size: 11px;
                color: #333333;
                padding: 5px;
            }
            QCheckBox::indicator {
                width: 18px;
                height: 18px;
            }
            QCheckBox::indicator:checked {
                background-color: #0078d4;
                border: 2px solid #0078d4;
                border-radius: 3px;
            }
            QCheckBox::indicator:unchecked {
                background-color: #ffffff;
                border: 2px solid #cccccc;
                border-radius: 3px;
            }
        """)
        self.verbose_logging_checkbox.setToolTip(
            "Show real-time logs of Claude's tool usage during processing"
        )
        config_form.addRow("", self.verbose_logging_checkbox)

        config_group.setLayout(config_form)
        config_layout.addWidget(config_group)

        # Save button
        save_btn = QPushButton("💾 Save Configuration")
        save_btn.setStyleSheet("""
            QPushButton {
                background-color: #107c10;
                color: #ffffff;
                border: none;
                padding: 10px;
                border-radius: 5px;
                font-weight: bold;
                font-size: 12px;
            }
            QPushButton:hover {
                background-color: #0b5c0b;
            }
            QPushButton:pressed {
                background-color: #094d09;
            }
        """)
        save_btn.clicked.connect(self._save_config)
        config_layout.addWidget(save_btn)

        config_layout.addStretch()
        config_tab.setLayout(config_layout)
        self.tab_widget.addTab(config_tab, "⚙️ Config")

    def _browse_context_folder(self):
        """Browse for context folder."""
        folder = QFileDialog.getExistingDirectory(
            self,
            "Select Context Folder",
            "",
            QFileDialog.Option.ShowDirsOnly
        )
        if folder:
            self.context_folder_edit.setText(folder)

    def _browse_focus_file(self):
        """Browse for focus file."""
        file, _ = QFileDialog.getOpenFileName(
            self,
            "Select Focus File",
            "",
            "All Files (*.*)"
        )
        if file:
            self.focus_file_edit.setText(file)

    def _load_current_config(self):
        """Load configuration for current agent."""
        settings = self.config_manager.get_settings(self.current_agent.metadata.name)

        if settings.context_folder:
            self.context_folder_edit.setText(settings.context_folder)

        if settings.focus_file:
            self.focus_file_edit.setText(settings.focus_file)

        # Load output mode
        if settings.output_mode:
            mode_index = self.output_mode_combo.findData(settings.output_mode)
            if mode_index >= 0:
                self.output_mode_combo.setCurrentIndex(mode_index)

        # Load selected input (first allowed input or default to text_selection)
        allowed_inputs = settings.allowed_inputs
        if allowed_inputs and len(allowed_inputs) > 0:
            # Load the first allowed input as the selected one
            selected_input = allowed_inputs[0]
            input_index = self.input_combo.findData(selected_input)
            if input_index >= 0:
                self.input_combo.setCurrentIndex(input_index)
        else:
            # Default to text_selection
            default_index = self.input_combo.findData("text_selection")
            if default_index >= 0:
                self.input_combo.setCurrentIndex(default_index)

        # Load verbose_logging setting
        self.verbose_logging_checkbox.setChecked(settings.verbose_logging)

        self.logger.info(f"Loaded config for {self.current_agent.metadata.name}")

    def _save_config(self):
        """Save configuration for current agent."""
        context_folder = self.context_folder_edit.text().strip() or None
        focus_file = self.focus_file_edit.text().strip() or None
        output_mode = self.output_mode_combo.currentData()

        # Get selected input (single selection)
        selected_input = self.input_combo.currentData()
        allowed_inputs = [selected_input]  # Store as single-item list for backward compatibility

        # Get verbose_logging setting
        verbose_logging = self.verbose_logging_checkbox.isChecked()

        settings = AgentSettings(
            context_folder=context_folder,
            focus_file=focus_file,
            output_mode=output_mode,
            allowed_inputs=allowed_inputs,
            verbose_logging=verbose_logging
        )

        self.config_manager.update_settings(
            self.current_agent.metadata.name,
            settings
        )

        self.log("✅ Configuration saved", "success")
        self.logger.info(f"Saved config for {self.current_agent.metadata.name}")

    def _position_window(self):
        """Position window in bottom right corner."""
        from PyQt6.QtWidgets import QApplication
        screen = QApplication.primaryScreen()
        if screen:
            screen_geometry = screen.availableGeometry()
            x = screen_geometry.width() - self.width() - 20
            y = screen_geometry.height() - self.height() - 50
            self.move(x, y)

    def set_current_agent(self, agent: BaseAgent):
        """Update current agent display.

        Args:
            agent: New current agent
        """
        self.current_agent = agent
        self.agent_label.setText(
            f"{agent.metadata.icon} {agent.metadata.name}"
        )
        self.agent_label.setStyleSheet("""
            QLabel {
                font-size: 18px;
                font-weight: bold;
                color: #ffffff;
                background-color: %s;
                padding: 10px;
                border-radius: 5px;
            }
        """ % agent.metadata.color)
        self.desc_label.setText(agent.metadata.description)

        # Reload configuration for the new agent
        self._load_current_config()

        self.logger.info(f"Agent switched to: {agent.metadata.name}")

    def log(self, message: str, level: str = "info"):
        """Add message to activity log.

        Args:
            message: Message to log
            level: Log level (info, success, warning, error)
        """
        # Add color coding based on level
        colors = {
            "info": "#0078d4",
            "success": "#107c10",
            "warning": "#ff8c00",
            "error": "#d13438"
        }

        color = colors.get(level, "#333333")
        timestamp = self._get_timestamp()
        formatted_msg = f'<span style="color: {color};">[{timestamp}] {message}</span>'

        self.log_text.append(formatted_msg)

        # Auto-scroll to bottom
        cursor = self.log_text.textCursor()
        cursor.movePosition(QTextCursor.MoveOperation.End)
        self.log_text.setTextCursor(cursor)

        self.logger.debug(f"Log: {message}")

    def _get_timestamp(self) -> str:
        """Get current timestamp.

        Returns:
            Formatted timestamp string
        """
        from datetime import datetime
        return datetime.now().strftime("%H:%M:%S")

    def _clear_log(self) -> None:
        """Clear the activity log."""
        self.log_text.clear()
        self.log("✨ Log cleared", "info")
        self.logger.debug("Activity log cleared")

    def closeEvent(self, event):
        """Handle window close event."""
        self.logger.info("Popup window closed")
        event.accept()
