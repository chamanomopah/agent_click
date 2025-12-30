"""VSCode active file input strategy.

Captures the file currently active/open in VSCode by detecting the VSCode window
and extracting the file path from the window title.
"""

import os
import re
from pathlib import Path
from typing import Optional
from core.input_strategy import InputStrategy, InputType, InputContent
from utils.logger import setup_logger

logger = setup_logger('VSCodeActiveFileStrategy')

# Try to import win32gui, provide helpful error if not available
try:
    import win32gui
    import win32con
    import win32process
    WINDOWS_AVAILABLE = True
except ImportError:
    WINDOWS_AVAILABLE = False
    logger.warning("pywin32 not available - VSCode Active File strategy will not work")


class VSCodeActiveFileStrategy(InputStrategy):
    """Strategy for reading the currently active file in VSCode.

    This strategy detects VSCode as the active window, extracts the file path
    from the window title, and reads the file content from disk.

    Window title formats:
    - "filename.ext - foldername - Visual Studio Code"
    - "filename.ext - Visual Studio Code"
    - "Untitled-*" (unsaved files - not supported)
    """

    def __init__(self):
        """Initialize VSCode active file strategy."""
        self.logger = logger

    def get_input_type(self) -> InputType:
        """Return input type."""
        return InputType.VSCODE_ACTIVE_FILE

    def _get_vscode_window(self) -> Optional[int]:
        """Get the handle of the active VSCode window.

        Returns:
            Window handle (HWND) if VSCode is active, None otherwise
        """
        if not WINDOWS_AVAILABLE:
            self.logger.error("pywin32 not available - cannot detect VSCode window")
            return None

        try:
            # Get the foreground window (active window)
            hwnd = win32gui.GetForegroundWindow()

            if not hwnd:
                self.logger.warning("No active window found")
                return None

            # Get the window title
            title = win32gui.GetWindowText(hwnd)

            if not title:
                self.logger.warning("Active window has no title")
                return None

            # Check if this is a VSCode window
            if "Visual Studio Code" not in title:
                self.logger.debug(f"Active window is not VSCode: {title}")
                return None

            self.logger.debug(f"VSCode window detected: {title}")
            return hwnd

        except Exception as e:
            self.logger.error(f"Error detecting VSCode window: {e}")
            return None

    def _extract_file_path_from_title(self, title: str) -> Optional[str]:
        """Extract file path from VSCode window title.

        Args:
            title: Window title string

        Returns:
            Absolute file path or None if cannot be determined
        """
        try:
            # Handle untitled files
            if title.startswith("Untitled-"):
                self.logger.info("Untitled file detected - file must be saved first")
                return None

            # Handle remote files (SSH, WSL, etc.)
            if any(prefix in title for prefix in ["[SSH]", "[WSL]", "[SSH:", "DEVCONTAINER"]):
                self.logger.info("Remote file detected - not supported")
                return None

            # Extract filename from title
            # Format: "filename.ext - foldername - Visual Studio Code"
            # or: "filename.ext - Visual Studio Code"

            # Remove " - Visual Studio Code" suffix
            title = title.replace(" - Visual Studio Code", "").strip()

            # The first part before " - " is the filename
            parts = title.split(" - ")
            if not parts:
                return None

            filename = parts[0].strip()

            # If filename contains path separators, it might already be a path
            if os.path.sep in filename or "/" in filename:
                # VSCode sometimes shows partial paths in title
                # Try to resolve it
                if os.path.exists(filename):
                    return os.path.abspath(filename)

            # Search for the file in common project directories
            # Start from current working directory and search up
            return self._search_file_in_project(filename)

        except Exception as e:
            self.logger.error(f"Error extracting file path from title: {e}")
            return None

    def _search_file_in_project(self, filename: str) -> Optional[str]:
        """Search for file in project directories.

        Args:
            filename: Name of file to search for

        Returns:
            Absolute file path if found, None otherwise
        """
        try:
            # Start from current directory
            current_dir = os.getcwd()

            # Search in current directory and subdirectories (limited depth)
            for root, dirs, files in os.walk(current_dir):
                # Limit search depth to avoid scanning entire filesystem
                depth = root[len(current_dir):].count(os.sep)
                if depth > 5:  # Limit to 5 levels deep
                    dirs[:] = []  # Don't go deeper
                    continue

                if filename in files:
                    filepath = os.path.join(root, filename)
                    self.logger.debug(f"Found file: {filepath}")
                    return os.path.abspath(filepath)

            self.logger.warning(f"File not found in project: {filename}")
            return None

        except Exception as e:
            self.logger.error(f"Error searching for file: {e}")
            return None

    def _read_file_content(self, file_path: str) -> Optional[tuple[str, dict]]:
        """Read file content with encoding handling.

        Args:
            file_path: Path to file

        Returns:
            Tuple of (content, metadata) or None if failed
        """
        try:
            if not os.path.exists(file_path):
                self.logger.error(f"File does not exist: {file_path}")
                return None

            # Check file size
            file_size = os.path.getsize(file_path)
            if file_size > 5 * 1024 * 1024:  # 5MB limit
                self.logger.warning(f"File is very large ({file_size / 1024 / 1024:.1f}MB)")

            # Try to read with different encodings
            content = None
            encoding = None

            for enc in ['utf-8', 'utf-16', 'latin-1']:
                try:
                    with open(file_path, 'r', encoding=enc) as f:
                        content = f.read()
                        encoding = enc
                        break
                except UnicodeDecodeError:
                    continue

            if content is None:
                self.logger.error(f"Could not decode file: {file_path}")
                return None

            # Check if it's a binary file (heuristic)
            if '\x00' in content:
                self.logger.error(f"Binary file detected: {file_path}")
                return None

            # Collect metadata
            filename = os.path.basename(file_path)
            extension = os.path.splitext(filename)[1]
            line_count = len(content.splitlines())

            metadata = {
                "filename": filename,
                "file_path": file_path,
                "file_size": file_size,
                "line_count": line_count,
                "extension": extension,
                "encoding": encoding
            }

            self.logger.info(f"Read file: {filename} ({file_size} bytes, {line_count} lines)")
            return content, metadata

        except Exception as e:
            self.logger.error(f"Error reading file: {e}")
            return None

    def capture_input(self) -> Optional[InputContent]:
        """Capture the active file from VSCode.

        Returns:
            InputContent with file content or None if not available
        """
        try:
            # Step 1: Detect VSCode window
            hwnd = self._get_vscode_window()
            if not hwnd:
                return None

            # Step 2: Get window title and extract file path
            title = win32gui.GetWindowText(hwnd)
            file_path = self._extract_file_path_from_title(title)

            if not file_path:
                return None

            # Step 3: Read file content
            result = self._read_file_content(file_path)
            if not result:
                return None

            content, metadata = result

            # Step 4: Return InputContent
            return InputContent(
                input_type=InputType.VSCODE_ACTIVE_FILE,
                text=content,
                file_path=file_path,
                metadata=metadata
            )

        except Exception as e:
            self.logger.error(f"Error capturing VSCode active file: {e}")
            return None

    def is_available(self) -> bool:
        """Check if VSCode active file input is available.

        This is a fast check - it only verifies VSCode is active and has
        a file in the title, without reading the file content.

        Returns:
            True if VSCode is active with a file, False otherwise
        """
        if not WINDOWS_AVAILABLE:
            return False

        try:
            hwnd = self._get_vscode_window()
            if not hwnd:
                return False

            title = win32gui.GetWindowText(hwnd)

            # Check if title has a file (not just "Visual Studio Code")
            if title == "Visual Studio Code" or title.startswith("Welcome"):
                return False

            # Check if it's not an untitled file
            if title.startswith("Untitled-"):
                return False

            # Check if it's not a remote file
            if any(prefix in title for prefix in ["[SSH]", "[WSL]", "[SSH:", "DEVCONTAINER"]):
                return False

            return True

        except Exception as e:
            self.logger.error(f"Error checking VSCode availability: {e}")
            return False
