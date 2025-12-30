"""File upload input strategy.

Allows user to upload files for processing.
"""

from core.input_strategy import InputStrategy, InputType, InputContent
from pathlib import Path
from typing import Optional
import os
from utils.logger import setup_logger

logger = setup_logger('FileUploadStrategy')


class FileUploadStrategy(InputStrategy):
    """Strategy for file upload input.

    User can drag file to mini popup or select from VSCode.
    Supports text files, code files, JSON, YAML, etc.
    """

    def __init__(self, file_path: Optional[str] = None):
        """Initialize file upload strategy.

        Args:
            file_path: Optional pre-configured file path
        """
        self.file_path = file_path
        self.logger = logger

    def get_input_type(self) -> InputType:
        """Return input type."""
        return InputType.FILE_UPLOAD

    def set_file(self, file_path: str) -> None:
        """Set file to upload.

        Args:
            file_path: Path to file
        """
        self.file_path = file_path
        self.logger.info(f"File configured: {file_path}")

    def capture_input(self) -> Optional[InputContent]:
        """Capture file content.

        Returns:
            InputContent with file content or None if file not available

        Note:
            Only reads text files. Binary files will be skipped.
        """
        if not self.file_path:
            self.logger.warning("No file path configured")
            return None

        file_path_obj = Path(self.file_path)

        if not file_path_obj.exists():
            self.logger.error(f"File not found: {self.file_path}")
            return None

        if not file_path_obj.is_file():
            self.logger.error(f"Not a file: {self.file_path}")
            return None

        try:
            # Try to read as text file
            with open(self.file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            file_size = os.path.getsize(self.file_path)
            file_ext = file_path_obj.suffix
            file_name = file_path_obj.name

            self.logger.info(
                f"File loaded: {file_name} ({file_size} bytes, {len(content)} chars)"
            )

            return InputContent(
                input_type=InputType.FILE_UPLOAD,
                text=content,
                file_path=self.file_path,
                metadata={
                    "file_name": file_name,
                    "file_size": file_size,
                    "extension": file_ext,
                    "char_count": len(content),
                    "line_count": len(content.split('\n'))
                }
            )

        except UnicodeDecodeError:
            # Binary file - cannot process as text
            self.logger.error(
                f"Binary file detected (not supported): {self.file_path}"
            )
            return None

        except Exception as e:
            self.logger.error(f"Error reading file: {e}")
            return None

    def is_available(self) -> bool:
        """Check if file is available.

        Returns:
            True if file exists and is readable
        """
        if not self.file_path:
            return False

        try:
            return (
                Path(self.file_path).exists() and
                Path(self.file_path).is_file()
            )
        except Exception:
            return False

    def clear_file(self) -> None:
        """Clear configured file."""
        self.file_path = None
        self.logger.debug("File path cleared")
