"""Input manager for AgentClick system.

Manages multiple input strategies and selects appropriate one.
"""

from typing import Optional, List, Dict
from core.input_strategy import InputStrategy, InputType, InputContent
from core.input_strategies import (
    TextSelectionStrategy,
    FileUploadStrategy,
    ClipboardImageStrategy,
    ScreenshotStrategy,
    SelectedTextStrategy
)
from utils.logger import setup_logger

logger = setup_logger('InputManager')


class InputManager:
    """Manages input strategies for AgentClick.

    This manager coordinates multiple input strategies and automatically
    selects the best one based on availability and user preferences.

    Priority order for auto-detection:
    1. Text selection (fastest, most common)
    2. File upload (if file configured)
    3. Clipboard image (if image in clipboard)
    4. Screenshot (always available but requires action)
    """

    def __init__(self):
        """Initialize input manager with all strategies."""
        self.strategies: List[InputStrategy] = [
            TextSelectionStrategy(),
            SelectedTextStrategy(),  # NOVO: Mouse selection without clipboard
            FileUploadStrategy(),  # Will be configured when file is dropped
            ClipboardImageStrategy(),
            ScreenshotStrategy()
        ]
        self.active_strategy: Optional[InputStrategy] = None
        self.logger = logger

        self.logger.info(f"InputManager initialized with {len(self.strategies)} strategies")

    def capture_input(
        self,
        preferred_type: Optional[InputType] = None,
        fallback: bool = True,
        allowed_inputs: Optional[list[str]] = None  # NOVO: Filter by allowed inputs
    ) -> Optional[InputContent]:
        """Capture input using best available strategy.

        Args:
            preferred_type: Optional preferred input type to use first
            fallback: If True and preferred_type fails, try other strategies
            allowed_inputs: NOVO - Optional list of allowed input types to filter

        Returns:
            InputContent or None if no input available

        Behavior:
            - If preferred_type specified: tries that strategy first
            - If fallback is True and preferred fails: tries other strategies
            - If no preferred_type: auto-detects best available input
            - NOVO: If allowed_inputs specified, only consider those types
        """
        # If preferred type specified, try that first
        if preferred_type:
            # NOVO: Check if preferred type is allowed
            if allowed_inputs and preferred_type.value not in allowed_inputs:
                self.logger.warning(f"Preferred input type {preferred_type.value} not in allowed inputs")
                return None

            content = self._try_strategy_by_type(preferred_type)
            if content:
                self.active_strategy = self._get_strategy_by_type(preferred_type)
                self.logger.info(f"✅ Captured input using preferred: {preferred_type.value}")
                return content
            elif not fallback:
                self.logger.warning(f"Preferred input type {preferred_type.value} not available")
                return None

        # Auto-detect: try in priority order
        priority_order = [
            InputType.TEXT_SELECTION,
            InputType.SELECTED_TEXT,  # NOVO: Try mouse selection before clipboard image
            InputType.FILE_UPLOAD,
            InputType.CLIPBOARD_IMAGE,
        ]

        # NOVO: Filter by allowed inputs if specified
        if allowed_inputs:
            priority_order = [t for t in priority_order if t.value in allowed_inputs]
            self.logger.debug(f"Filtered priority order by allowed inputs: {[t.value for t in priority_order]}")

        for input_type in priority_order:
            content = self._try_strategy_by_type(input_type)
            if content:
                self.active_strategy = self._get_strategy_by_type(input_type)
                self.logger.info(f"✅ Auto-detected input: {input_type.value}")
                return content

        self.logger.warning("⚠️  No input available from any source")
        return None

    def _try_strategy_by_type(self, input_type: InputType) -> Optional[InputContent]:
        """Try to capture input using strategy of specified type.

        Args:
            input_type: Type of input to try

        Returns:
            InputContent or None
        """
        for strategy in self.strategies:
            if strategy.get_input_type() == input_type:
                if strategy.is_available():
                    return strategy.capture_input()
        return None

    def _get_strategy_by_type(self, input_type: InputType) -> Optional[InputStrategy]:
        """Get strategy instance by type.

        Args:
            input_type: Type of input

        Returns:
            Strategy instance or None
        """
        for strategy in self.strategies:
            if strategy.get_input_type() == input_type:
                return strategy
        return None

    def set_file_upload(self, file_path: str) -> None:
        """Configure file upload strategy.

        Args:
            file_path: Path to file to upload
        """
        for strategy in self.strategies:
            if isinstance(strategy, FileUploadStrategy):
                strategy.set_file(file_path)
                self.logger.info(f"📎 File upload configured: {file_path}")
                break

    def clear_file_upload(self) -> None:
        """Clear configured file upload."""
        for strategy in self.strategies:
            if isinstance(strategy, FileUploadStrategy):
                strategy.clear_file()
                self.logger.info("File upload cleared")
                break

    def take_screenshot(self, region: Optional[tuple] = None) -> Optional[InputContent]:
        """Take screenshot.

        Args:
            region: Optional (left, top, width, height) for partial screenshot

        Returns:
            InputContent with screenshot or None if failed

        Examples:
            # Full screen
            content = manager.take_screenshot()

            # Region
            content = manager.take_screenshot(region=(100, 100, 800, 600))
        """
        for strategy in self.strategies:
            if isinstance(strategy, ScreenshotStrategy):
                self.logger.info("📸 Taking screenshot...")
                content = strategy.capture_input(region=region)
                if content:
                    self.active_strategy = strategy
                return content
        return None

    def get_active_input_type(self) -> Optional[InputType]:
        """Get active input type.

        Returns:
            Active InputType or None
        """
        if self.active_strategy:
            return self.active_strategy.get_input_type()
        return None

    def check_available_inputs(self) -> Dict[InputType, bool]:
        """Check availability of all input types.

        Returns:
            Dictionary mapping InputType to availability boolean
        """
        availability = {}
        for strategy in self.strategies:
            availability[strategy.get_input_type()] = strategy.is_available()
        return availability

    def get_status_summary(self) -> str:
        """Get human-readable status summary.

        Returns:
            Status string
        """
        lines = ["Input Manager Status:", ""]

        availability = self.check_available_inputs()

        for input_type, available in availability.items():
            status = "✅" if available else "❌"
            lines.append(f"  {status} {input_type.value.replace('_', ' ').title()}")

        if self.active_strategy:
            lines.append("")
            lines.append(f"Active: {self.active_strategy.get_input_type().value}")

        return "\n".join(lines)

    def cleanup_temp_files(self, hours: int = 24) -> Dict[str, int]:
        """Clean up old temporary files from all strategies.

        Args:
            hours: Delete files older than this many hours

        Returns:
            Dictionary with cleanup counts per strategy
        """
        results = {}

        for strategy in self.strategies:
            strategy_name = strategy.get_input_type().value

            if hasattr(strategy, 'cleanup_old_images'):
                results[strategy_name] = strategy.cleanup_old_images(hours)

            if hasattr(strategy, 'cleanup_old_screenshots'):
                results[strategy_name] = strategy.cleanup_old_screenshots(hours)

        return results
