"""Click processor for AgentClick system.

Handles keyboard hotkeys for agent activation and switching.
"""

import keyboard
import threading
import time
from typing import Callable, Optional
from utils.logger import setup_logger

logger = setup_logger('ClickProcessor')


class ClickProcessor:
    """Processes keyboard shortcuts for agent control."""

    # Pause key scan codes (different scan codes for Pause/Break)
    PAUSE_SCAN_CODES = [29, 70, 110, 119]  # Common Pause scan codes

    def __init__(self):
        """Initialize click processor."""
        self.pause_callback: Optional[Callable] = None
        self.switch_callback: Optional[Callable] = None
        self.screenshot_callback: Optional[Callable] = None  # NOVO
        self.ctrl_pressed = False
        self.shift_pressed = False  # NOVO
        self.pause_pressed = False
        self.ctrl_pause_detected = False
        self.ctrl_shift_pause_detected = False  # NOVO
        self.last_pause_time = 0
        self.ctrl_lock = threading.Lock()
        logger.info("ClickProcessor initialized")

    def register_pause_handler(self, callback: Callable) -> None:
        """Register callback for Pause key (activate current agent).

        Args:
            callback: Function to call when Pause is pressed
        """
        self.pause_callback = callback

    def register_switch_handler(self, callback: Callable) -> None:
        """Register callback for Ctrl+Pause (switch agent).

        Args:
            callback: Function to call when Ctrl+Pause is pressed
        """
        self.switch_callback = callback

        # Use global hook to capture ALL keyboard events
        keyboard.hook(self._on_keyboard_event)
        logger.info("Global keyboard hook registered (Ctrl+Pause detection)")

    def register_screenshot_handler(self, callback: Callable) -> None:
        """Register callback for Ctrl+Shift+Pause (take screenshot).

        Args:
            callback: Function to call when Ctrl+Shift+Pause is pressed
        """
        self.screenshot_callback = callback
        logger.info("Screenshot handler registered: Ctrl+Shift+Pause")

    def _on_keyboard_event(self, event) -> None:
        """Handle all keyboard events globally.

        Args:
            event: KeyboardEvent from keyboard.hook
        """
        # Track Ctrl state
        if event.name in ['ctrl', 'left ctrl', 'right ctrl']:
            if event.event_type == 'down':
                with self.ctrl_lock:
                    if not self.ctrl_pressed:
                        self.ctrl_pressed = True
                        logger.info(f"Ctrl PRESSED (scan_code={event.scan_code})")
            elif event.event_type == 'up':
                with self.ctrl_lock:
                    if self.ctrl_pressed:
                        self.ctrl_pressed = False
                        logger.info(f"Ctrl RELEASED (scan_code={event.scan_code})")
            return

        # Track Shift state (NOVO)
        if event.name in ['shift', 'left shift', 'right shift']:
            if event.event_type == 'down':
                with self.ctrl_lock:
                    if not self.shift_pressed:
                        self.shift_pressed = True
                        logger.debug(f"Shift PRESSED (scan_code={event.scan_code})")
            elif event.event_type == 'up':
                with self.ctrl_lock:
                    if self.shift_pressed:
                        self.shift_pressed = False
                        logger.debug(f"Shift RELEASED (scan_code={event.scan_code})")
            return

        # Track Pause key
        if event.name == 'pause' or event.scan_code in self.PAUSE_SCAN_CODES:
            if event.event_type == 'down':
                self._handle_pause_down()
            elif event.event_type == 'up':
                self._handle_pause_up()

    def _handle_pause_down(self) -> None:
        """Handle Pause key press down."""
        current_time = time.time()

        # Debounce: prevent double-trigger within 200ms
        if current_time - self.last_pause_time < 0.2:
            return

        self.last_pause_time = current_time
        self.pause_pressed = True

        # Check Ctrl and Shift state (NOVO: Shift)
        with self.ctrl_lock:
            ctrl_state = self.ctrl_pressed
            shift_state = self.shift_pressed

        logger.info(f"PAUSE DOWN (Ctrl held={ctrl_state}, Shift held={shift_state})")

        if ctrl_state and shift_state:
            self.ctrl_shift_pause_detected = True
            logger.info(">>> Ctrl+Shift+Pause DETECTED! <<<")
        elif ctrl_state:
            self.ctrl_pause_detected = True
            self.ctrl_shift_pause_detected = False
            logger.info(">>> Ctrl+Pause DETECTED! <<<")
        else:
            self.ctrl_pause_detected = False
            self.ctrl_shift_pause_detected = False

    def _handle_pause_up(self) -> None:
        """Handle Pause key release."""
        if not self.pause_pressed:
            return

        self.pause_pressed = False

        if self.ctrl_shift_pause_detected:
            # Ctrl+Shift+Pause combination (NOVO: Screenshot)
            logger.info(">>> TRIGGERING SCREENSHOT (Ctrl+Shift+Pause released) <<<")
            if self.screenshot_callback:
                self.screenshot_callback()
            self.ctrl_shift_pause_detected = False
        elif self.ctrl_pause_detected:
            # Ctrl+Pause combination
            logger.info(">>> TRIGGERING AGENT SWITCH (Ctrl+Pause released) <<<")
            if self.switch_callback:
                self.switch_callback()
            self.ctrl_pause_detected = False
        else:
            # Just Pause
            logger.info(">>> TRIGGERING AGENT ACTIVATION (Pause only) <<<")
            if self.pause_callback:
                self.pause_callback()

    def cleanup(self) -> None:
        """Cleanup keyboard hooks."""
        try:
            keyboard.unhook_all()
            logger.info("Keyboard hooks cleaned up")
        except Exception as e:
            logger.error(f"Error cleaning up keyboard hooks: {e}")
