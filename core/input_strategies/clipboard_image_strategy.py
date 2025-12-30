"""Clipboard image input strategy.

Captures images copied to clipboard.
"""

from core.input_strategy import InputStrategy, InputType, InputContent
from pathlib import Path
from typing import Optional
import tempfile
from datetime import datetime
from utils.logger import setup_logger

logger = setup_logger('ClipboardImageStrategy')


class ClipboardImageStrategy(InputStrategy):
    """Strategy for clipboard image input.

    User copies image to clipboard (Ctrl+C on image in browser,
    file explorer, screenshot tool, etc.).
    """

    def __init__(self):
        """Initialize clipboard image strategy."""
        self.temp_dir = Path(tempfile.gettempdir()) / "agent_click_images"
        self.temp_dir.mkdir(exist_ok=True)
        self.captured_image_path: Optional[str] = None
        self.logger = logger

        self.logger.debug(f"Temp directory: {self.temp_dir}")

    def get_input_type(self) -> InputType:
        """Return input type."""
        return InputType.CLIPBOARD_IMAGE

    def capture_input(self) -> Optional[InputContent]:
        """Capture image from clipboard.

        Returns:
            InputContent with saved image path or None if no image in clipboard

        Note:
            Images are saved to temp directory for processing.
            Supports PNG, JPEG, and other image formats.
        """
        try:
            from PIL import ImageGrab

            # Check if clipboard has image
            clipboard_content = ImageGrab.grabclipboard()

            if clipboard_content is None:
                self.logger.debug("No content in clipboard")
                return None

            # Check if it's an image
            if not hasattr(clipboard_content, 'save'):
                self.logger.debug("Clipboard does not contain image")
                return None

            # Generate unique filename
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")[:-3]
            image_path = self.temp_dir / f"clipboard_{timestamp}.png"

            # Save image
            clipboard_content.save(image_path, "PNG")
            self.captured_image_path = str(image_path)

            file_size = image_path.stat().st_size

            self.logger.info(
                f"Image captured from clipboard: {image_path.name} ({file_size} bytes)"
            )

            return InputContent(
                input_type=InputType.CLIPBOARD_IMAGE,
                text="[Image captured from clipboard - ready for visual analysis]",
                image_path=str(image_path),
                metadata={
                    "image_format": "PNG",
                    "saved_path": str(image_path),
                    "file_size": file_size,
                    "width": clipboard_content.width if hasattr(clipboard_content, 'width') else None,
                    "height": clipboard_content.height if hasattr(clipboard_content, 'height') else None
                }
            )

        except ImportError:
            self.logger.error("PIL not installed - install with: pip install Pillow")
            return None

        except Exception as e:
            self.logger.error(f"Error capturing clipboard image: {e}")
            return None

    def is_available(self) -> bool:
        """Check if image is available in clipboard.

        Returns:
            True if clipboard contains image
        """
        try:
            from PIL import ImageGrab

            clipboard_content = ImageGrab.grabclipboard()
            return clipboard_content is not None and hasattr(clipboard_content, 'save')

        except ImportError:
            return False

        except Exception:
            return False

    def cleanup_old_images(self, hours: int = 24) -> int:
        """Clean up old images from temp directory.

        Args:
            hours: Delete images older than this many hours

        Returns:
            Number of files deleted
        """
        try:
            import time

            cutoff_time = time.time() - (hours * 3600)
            deleted_count = 0

            for file_path in self.temp_dir.glob("clipboard_*.png"):
                if file_path.stat().st_mtime < cutoff_time:
                    file_path.unlink()
                    deleted_count += 1

            if deleted_count > 0:
                self.logger.info(f"Cleaned up {deleted_count} old images")

            return deleted_count

        except Exception as e:
            self.logger.error(f"Error cleaning up images: {e}")
            return 0
