# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "claude-agent-sdk",
#     "pystray",
#     "keyboard",
#     "pyperclip",
#     "PyQt6",
# ]
# ///

"""AgentClick System - Multi-Agent Interface with Click Activation

A multi-agent system activated by keyboard shortcuts (Pause/Ctrl+Pause).
Provides popup interface showing real-time agent activity.

Features:
- 3 specialized agents (Prompt Assistant, Diagnostic, Implementation)
- Click-based activation without voice input
- Popup interface in bottom-right corner
- Real-time activity logging
- Clipboard integration
"""

import sys
from pathlib import Path
from PyQt6.QtWidgets import QApplication

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from core.system import AgentClickSystem
from utils.logger import setup_logger


def main():
    """Main entry point."""
    logger = setup_logger('Main')

    # Create QApplication FIRST (required before any QWidget)
    app = QApplication(sys.argv)

    # Initialize system variable to None to avoid UnboundLocalError
    system = None

    try:
        # Create system
        system = AgentClickSystem()

        # Run Qt event loop (this processes signals and GUI events)
        logger.info("Starting Qt event loop...")
        exit_code = app.exec()

        # Cleanup on exit
        if system:
            system.cleanup()
        logger.info(f"Exiting with code {exit_code}")
        sys.exit(exit_code)

    except KeyboardInterrupt:
        logger.info("Received interrupt signal")
        if system:
            system.cleanup()
        sys.exit(0)
    except Exception as e:
        logger.error(f"Fatal error: {e}", exc_info=True)
        if system:
            system.cleanup()
        sys.exit(1)


if __name__ == "__main__":
    main()
