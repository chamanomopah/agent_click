"""Interactive editor dialog for AgentClick."""

from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel,
    QTextEdit, QPushButton, QComboBox, QGroupBox,
    QMessageBox
)
from PyQt6.QtCore import Qt
from agents.output_modes import OutputMode, AgentResult
from utils.logger import setup_logger

logger = setup_logger('InteractiveEditor')


class InteractiveEditorDialog(QDialog):
    """Dialog for previewing and editing agent output."""

    def __init__(self, result: AgentResult, context_folder: str = None):
        """Initialize dialog.

        Args:
            result: Agent result to edit
            context_folder: Optional context folder
        """
        super().__init__()
        self.result = result
        self.context_folder = context_folder
        self.confirmed = False
        self.final_action = "clipboard"

        self._setup_ui()
        self._load_content()

        logger.info("Interactive editor opened")


    def _setup_ui(self):
        """Setup UI components."""
        self.setWindowTitle("✏️ AgentClick - Output Editor")
        self.setModal(True)
        self.setFixedSize(700, 600)

        layout = QVBoxLayout()
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setSpacing(10)

        # Header
        header = QLabel("📝 Preview & Edit Output")
        header.setStyleSheet("""
            QLabel {
                font-size: 16px;
                font-weight: bold;
                color: #333333;
                padding: 5px;
            }
        """)
        layout.addWidget(header)

        # Mode selection
        mode_group = QGroupBox("Final Action")
        mode_group.setStyleSheet("""
            QGroupBox {
                font-size: 11px;
                font-weight: bold;
                border: 1px solid #cccccc;
                border-radius: 5px;
                margin-top: 10px;
                padding-top: 10px;
            }
        """)
        mode_layout = QHBoxLayout()

        mode_label = QLabel("Choose output:")
        mode_layout.addWidget(mode_label)

        self.action_combo = QComboBox()
        self.action_combo.addItem("📋 Copy to Clipboard", "clipboard")
        if self.context_folder:
            self.action_combo.addItem("💾 Save to File", "file")
        self.action_combo.currentIndexChanged.connect(self._on_action_changed)
        mode_layout.addWidget(self.action_combo)

        mode_layout.addStretch()
        mode_group.setLayout(mode_layout)
        layout.addWidget(mode_group)

        # Filename (initially hidden)
        self.filename_group = QGroupBox("Filename")
        self.filename_group.setStyleSheet(mode_group.styleSheet())
        filename_layout = QHBoxLayout()

        self.filename_edit = QPushButton()
        self.filename_edit.setStyleSheet("""
            QPushButton {
                text-align: left;
                padding: 5px;
                border: 1px solid #cccccc;
                border-radius: 3px;
                background-color: white;
            }
        """)
        self.filename_edit.clicked.connect(self._edit_filename)
        if self.result.suggested_filename:
            self.filename_edit.setText(f"📄 {self.result.suggested_filename}")
        else:
            self.filename_edit.setText("📄 Click to set filename...")

        filename_layout.addWidget(self.filename_edit)
        filename_layout.addStretch()
        self.filename_group.setLayout(filename_layout)
        self.filename_group.setVisible(False)
        layout.addWidget(self.filename_group)

        # Content editor
        content_label = QLabel("Content:")
        content_label.setStyleSheet("font-weight: bold; color: #333;")
        layout.addWidget(content_label)

        self.content_edit = QTextEdit()
        self.content_edit.setStyleSheet("""
            QTextEdit {
                font-family: 'Consolas', 'Monaco', monospace;
                font-size: 11px;
                border: 1px solid #cccccc;
                border-radius: 5px;
                padding: 8px;
                background-color: #f9f9f9;
            }
        """)
        layout.addWidget(self.content_edit)

        # Thoughts (if available)
        if self.result.raw_thoughts:
            thoughts_label = QLabel("🤔 Agent's Reasoning:")
            thoughts_label.setStyleSheet("font-weight: bold; color: #666;")
            layout.addWidget(thoughts_label)

            self.thoughts_edit = QTextEdit()
            self.thoughts_edit.setReadOnly(True)
            self.thoughts_edit.setStyleSheet("""
                QTextEdit {
                    font-family: 'Consolas', 'Monaco', monospace;
                    font-size: 10px;
                    border: 1px solid #cccccc;
                    border-radius: 5px;
                    padding: 8px;
                    background-color: #fffacd;
                    color: #666666;
                }
            """)
            self.thoughts_edit.setMaximumHeight(100)
            layout.addWidget(self.thoughts_edit)

        # Buttons
        button_layout = QHBoxLayout()

        cancel_btn = QPushButton("❌ Cancel")
        cancel_btn.setStyleSheet("""
            QPushButton {
                background-color: #d13438;
                color: white;
                border: none;
                padding: 10px 20px;
                border-radius: 5px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #a80000;
            }
        """)
        cancel_btn.clicked.connect(self._on_cancel)
        button_layout.addWidget(cancel_btn)

        button_layout.addStretch()

        confirm_btn = QPushButton("✅ Confirm & Output")
        confirm_btn.setStyleSheet("""
            QPushButton {
                background-color: #107c10;
                color: white;
                border: none;
                padding: 10px 20px;
                border-radius: 5px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #0b5c0b;
            }
        """)
        confirm_btn.clicked.connect(self._on_confirm)
        button_layout.addWidget(confirm_btn)

        layout.addLayout(button_layout)
        self.setLayout(layout)


    def _load_content(self):
        """Load result content into editor."""
        self.content_edit.setPlainText(self.result.content)

        if self.result.raw_thoughts and hasattr(self, 'thoughts_edit'):
            self.thoughts_edit.setPlainText(self.result.raw_thoughts)


    def _on_action_changed(self):
        """Handle action combo box change."""
        action = self.action_combo.currentData()

        if action == "file":
            self.filename_group.setVisible(True)
            self.final_action = "file"
        else:
            self.filename_group.setVisible(False)
            self.final_action = "clipboard"


    def _edit_filename(self):
        """Edit filename."""
        from PyQt6.QtWidgets import QInputDialog

        current = self.result.suggested_filename or "output.txt"
        filename, ok = QInputDialog.getText(
            self,
            "Set Filename",
            "Enter filename:",
            text=current
        )

        if ok and filename:
            self.result.suggested_filename = filename
            self.filename_edit.setText(f"📄 {filename}")


    def _on_confirm(self):
        """Confirm and output."""
        # Update result with edited content
        self.result.content = self.content_edit.toPlainText()
        self.confirmed = True
        self.accept()


    def _on_cancel(self):
        """Cancel editing."""
        self.confirmed = False
        self.reject()


    def was_confirmed(self) -> bool:
        """Check if user confirmed.

        Returns:
            True if confirmed, False if cancelled
        """
        return self.confirmed


    def get_final_result(self) -> AgentResult:
        """Get final edited result.

        Returns:
            Edited AgentResult
        """
        return self.result


    def get_final_action(self) -> str:
        """Get final action choice.

        Returns:
            "clipboard" or "file"
        """
        return self.final_action
