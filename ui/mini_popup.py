"""Mini popup widget - Always visible, discreet indicator in bottom-right corner."""

from PyQt6.QtWidgets import QWidget, QLabel, QVBoxLayout
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QCursor, QFont
from agents.base_agent import BaseAgent
from utils.logger import setup_logger

logger = setup_logger('MiniPopup')


class MiniPopupWidget(QWidget):
    """Small, always-visible popup showing current agent icon."""

    clicked = pyqtSignal()  # Signal when clicked

    def __init__(self, initial_agent: BaseAgent):
        """Initialize mini popup.

        Args:
            initial_agent: Initial agent to display
        """
        super().__init__()
        self.current_agent = initial_agent
        self.logger = setup_logger('MiniPopup')

        self._setup_ui()
        self.logger.info("Mini popup initialized")

    def _setup_ui(self):
        """Setup mini popup UI."""
        # Window properties - very small and discreet
        self.setWindowTitle("")
        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint |
            Qt.WindowType.WindowStaysOnTopHint |
            Qt.WindowType.Tool
        )

        # Very small size
        self.setFixedSize(60, 60)

        # Position in bottom right
        self._position_window()

        # Layout
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # Icon label (centered)
        self.icon_label = QLabel(self.current_agent.metadata.icon)
        self.icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.icon_label.setStyleSheet("""
            QLabel {
                font-size: 32px;
                background-color: %s;
                color: #ffffff;
                border-radius: 30px;
            }
        """ % self.current_agent.metadata.color)
        layout.addWidget(self.icon_label)

        self.setLayout(layout)

        # Enable click detection
        self.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

    def _position_window(self):
        """Position window in bottom right corner."""
        from PyQt6.QtWidgets import QApplication
        screen = QApplication.primaryScreen()
        if screen:
            screen_geometry = screen.availableGeometry()
            x = screen_geometry.width() - self.width() - 10
            y = screen_geometry.height() - self.height() - 10
            self.move(x, y)

    def update_agent(self, agent: BaseAgent):
        """Update displayed agent.

        Args:
            agent: New agent to display
        """
        self.current_agent = agent
        self.icon_label.setText(agent.metadata.icon)
        self.icon_label.setStyleSheet("""
            QLabel {
                font-size: 32px;
                background-color: %s;
                color: #ffffff;
                border-radius: 30px;
            }
        """ % agent.metadata.color)
        self.logger.info(f"Mini popup updated: {agent.metadata.icon} {agent.metadata.name}")

    def mousePressEvent(self, event):
        """Handle mouse click - emit signal to open large popup."""
        if event.button() == Qt.MouseButton.LeftButton:
            self.logger.info("Mini popup clicked")
            self.clicked.emit()
        super().mousePressEvent(event)

    def enterEvent(self, event):
        """Mouse hover - slight enlargement."""
        self.setFixedSize(65, 65)
        self.icon_label.setStyleSheet("""
            QLabel {
                font-size: 36px;
                background-color: %s;
                color: #ffffff;
                border-radius: 32px;
                border: 2px solid #ffffff;
            }
        """ % self.current_agent.metadata.color)
        super().enterEvent(event)

    def leaveEvent(self, event):
        """Mouse leave - return to normal size."""
        self.setFixedSize(60, 60)
        self.icon_label.setStyleSheet("""
            QLabel {
                font-size: 32px;
                background-color: %s;
                color: #ffffff;
                border-radius: 30px;
            }
        """ % self.current_agent.metadata.color)
        super().leaveEvent(event)
