"""Screenshot input strategy.

Captures screenshots of entire screen or regions.
"""

from core.input_strategy import InputStrategy, InputType, InputContent
from pathlib import Path
from typing import Optional
import tempfile
from datetime import datetime
from utils.logger import setup_logger

logger = setup_logger('ScreenshotStrategy')


class ScreenshotStrategy(InputStrategy):
    """Strategy for screenshot input.

    Captures full screen or selected region.
    Useful for visual debugging, UI analysis, etc.
    """

    def __init__(self):
        """Initialize screenshot strategy."""
        self.temp_dir = Path(tempfile.gettempdir()) / "agent_click_screenshots"
        self.temp_dir.mkdir(exist_ok=True)
        self.captured_screenshot_path: Optional[str] = None
        self.logger = logger

        self.logger.debug(f"Temp directory: {self.temp_dir}")

    def get_input_type(self) -> InputType:
        """Return input type."""
        return InputType.SCREENSHOT

    def capture_input(self, region: Optional[tuple] = None) -> Optional[InputContent]:
        """Capture screenshot.

        Args:
            region: Optional tuple (left, top, width, height) for partial screenshot.
                   If None, captures entire screen.

        Returns:
            InputContent with screenshot path or None if capture failed

        Examples:
            # Full screen
            content = strategy.capture_input()

            # Region (100, 100, 800, 600)
            content = strategy.capture_input(region=(100, 100, 800, 600))
        """
        try:
            from PIL import ImageGrab

            # Capture screenshot
            if region:
                self.logger.debug(f"Capturing region: {region}")
                screenshot = ImageGrab.grab(bbox=region)
                region_info = {
                    "left": region[0],
                    "top": region[1],
                    "width": region[2],
                    "height": region[3]
                }
            else:
                self.logger.debug("Capturing full screen")
                screenshot = ImageGrab.grab()
                region_info = None

            # Generate unique filename
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")[:-3]
            screenshot_path = self.temp_dir / f"screenshot_{timestamp}.png"

            # Save screenshot
            screenshot.save(screenshot_path, "PNG")
            self.captured_screenshot_path = str(screenshot_path)

            file_size = screenshot_path.stat().st_size

            self.logger.info(
                f"Screenshot saved: {screenshot_path.name} ({file_size} bytes)"
            )

            # Build context text
            if region:
                context_text = f"[Screenshot of region: {region[0]}x{region[1]} size {region[2]}x{region[3]}]"
            else:
                context_text = "[Screenshot of entire screen]"

            return InputContent(
                input_type=InputType.SCREENSHOT,
                text=f"{context_text}\nReady for visual analysis.",
                image_path=str(screenshot_path),
                metadata={
                    "image_format": "PNG",
                    "saved_path": str(screenshot_path),
                    "file_size": file_size,
                    "width": screenshot.width,
                    "height": screenshot.height,
                    "region": region_info
                }
            )

        except ImportError:
            self.logger.error("PIL not installed - install with: pip install Pillow")
            return None

        except Exception as e:
            self.logger.error(f"Error capturing screenshot: {e}")
            return None

    def is_available(self) -> bool:
        """Screenshot is always available.

        Returns:
            Always True (can always take screenshot)
        """
        return True

    def get_last_screenshot(self) -> Optional[str]:
        """Get path to last captured screenshot.

        Returns:
            Path to last screenshot or None
        """
        return self.captured_screenshot_path

    def cleanup_old_screenshots(self, hours: int = 24) -> int:
        """Clean up old screenshots from temp directory.

        Args:
            hours: Delete screenshots older than this many hours

        Returns:
            Number of files deleted
        """
        try:
            import time

            cutoff_time = time.time() - (hours * 3600)
            deleted_count = 0

            for file_path in self.temp_dir.glob("screenshot_*.png"):
                if file_path.stat().st_mtime < cutoff_time:
                    file_path.unlink()
                    deleted_count += 1

            if deleted_count > 0:
                self.logger.info(f"Cleaned up {deleted_count} old screenshots")

            return deleted_count

        except Exception as e:
            self.logger.error(f"Error cleaning up screenshots: {e}")
            return 0
