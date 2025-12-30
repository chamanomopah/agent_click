# 🚀 Implementação Completa: Novos Tipos de Input no AgentClick

> **Guia passo a passo para implementar suporte a múltiplos tipos de input no sistema AgentClick**

---

## 📋 ÍNDICE

1. [Visão Geral](#1-visão-geral)
2. [Arquitetura Proposta](#2-arquitetura-proposta)
3. [Passo 1: Criar Estrutura Base](#3-passo-1-criar-estrutura-base)
4. [Passo 2: Implementar Estratégias de Input](#4-passo-2-implementar-estratégias-de-input)
5. [Passo 3: Modificar Sistema Core](#5-passo-3-modificar-sistema-core)
6. [Passo 4: Modificar Interface](#6-passo-4-modificar-interface)
7. [Passo 5: Modificar Agentes](#7-passo-5-modificar-agentes)
8. [Passo 6: Testes](#8-passo-6-testes)
9. [Troubleshooting](#9-troubleshooting)

---

## 1. VISÃO GERAL

### **Objetivo**
Adicionar suporte a múltiplos tipos de input além do texto selecionado atualmente:
- ✅ Texto selecionado (EXISTENTE)
- 📎 Arquivo anexado (NOVO)
- 🖼️ Imagem do clipboard (NOVO)
- 📸 Screenshot (NOVO)

### **Padrão de Design**
**Strategy Pattern** - Cada tipo de input é uma estratégia independente que implementa uma interface comum.

---

## 2. ARQUITETURA PROPOSTA

```
InputStrategy (ABC)
    │
    ├─▶ TextSelectionStrategy (EXISTENTE)
    │   └─▶ Captura texto do clipboard (pyperclip)
    │
    ├─▶ FileUploadStrategy (NOVO)
    │   └─▶ Lê arquivo do disco
    │
    ├─▶ ClipboardImageStrategy (NOVO)
    │   └─▶ Captura imagem do clipboard (Pillow)
    │
    └─▶ ScreenshotStrategy (NOVO)
        └─▶ Tira screenshot da tela (Pillow)

InputManager
    └─▶ Gerencia todas as estratégias
    └─▶ Auto-detecta melhor input disponível
```

---

## 3. PASSO 1: CRIAR ESTRUTURA BASE

### **3.1. Criar pasta para estratégias**

```bash
# No diretório C:\.agent_click
mkdir core\input_strategies
```

### **3.2. Criar arquivo de interface base**

**Arquivo:** `core/input_strategy.py` (NOVO)

```python
"""Input strategies for AgentClick system.

Defines different ways users can provide input to agents.
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Optional, Dict, Any
from enum import Enum
from utils.logger import setup_logger

logger = setup_logger('InputStrategy')


class InputType(Enum):
    """Types of input."""
    TEXT_SELECTION = "text_selection"
    FILE_UPLOAD = "file_upload"
    CLIPBOARD_IMAGE = "clipboard_image"
    SCREENSHOT = "screenshot"


@dataclass
class InputContent:
    """Content from user input.

    Attributes:
        input_type: Type of input
        text: Text content (if applicable)
        file_path: Path to file (if applicable)
        image_path: Path to image/screenshot (if applicable)
        metadata: Additional metadata
    """
    input_type: InputType
    text: Optional[str] = None
    file_path: Optional[str] = None
    image_path: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None

    def get_text_for_agent(self) -> str:
        """Get text representation for agent processing.

        Returns:
            Text string with context about input source
        """
        if self.input_type == InputType.TEXT_SELECTION:
            return self.text or ""

        elif self.input_type == InputType.FILE_UPLOAD:
            file_info = ""
            if self.metadata and "file_name" in self.metadata:
                file_info = f"File: {self.metadata['file_name']}"
            return f"[FILE UPLOAD: {file_info}]\n{self.text or ''}"

        elif self.input_type == InputType.CLIPBOARD_IMAGE:
            return f"[IMAGE from clipboard]\n{self.text or ''}"

        elif self.input_type == InputType.SCREENSHOT:
            return f"[SCREENSHOT captured]\n{self.text or ''}"

        return ""

    def has_image(self) -> bool:
        """Check if input contains an image.

        Returns:
            True if has image
        """
        return self.image_path is not None

    def has_file(self) -> bool:
        """Check if input contains a file.

        Returns:
            True if has file
        """
        return self.file_path is not None


class InputStrategy(ABC):
    """Abstract base class for input strategies.

    Each strategy represents a different way to capture user input.
    """

    @abstractmethod
    def get_input_type(self) -> InputType:
        """Return the input type.

        Returns:
            InputType enum value
        """
        pass

    @abstractmethod
    def capture_input(self) -> Optional[InputContent]:
        """Capture input from user.

        This is the main method that performs the actual input capture.

        Returns:
            InputContent object or None if no input available
        """
        pass

    @abstractmethod
    def is_available(self) -> bool:
        """Check if this input type is currently available.

        Returns:
            True if input is available and can be captured
        """
        pass

    def get_description(self) -> str:
        """Get human-readable description of this strategy.

        Returns:
            Description string
        """
        return self.get_input_type().value.replace("_", " ").title()
```

**✅ Ação:** Salvar arquivo em `C:\.agent_click\core\input_strategy.py`

---

## 4. PASSO 2: IMPLEMENTAR ESTRATÉGIAS DE INPUT

### **4.1. TextSelectionStrategy (Refatoração do código existente)**

**Arquivo:** `core/input_strategies/text_selection_strategy.py` (NOVO)

```python
"""Text selection input strategy.

Captures text selected by user (current behavior).
"""

from core.input_strategy import InputStrategy, InputType, InputContent
from core.selection_manager import SelectionManager
from typing import Optional
from utils.logger import setup_logger

logger = setup_logger('TextSelectionStrategy')


class TextSelectionStrategy(InputStrategy):
    """Strategy for text selection input (current behavior).

    This strategy captures text that user has selected and copied
    to clipboard using Ctrl+C.
    """

    def __init__(self):
        """Initialize text selection strategy."""
        self.selection_manager = SelectionManager()
        self.logger = logger

    def get_input_type(self) -> InputType:
        """Return input type."""
        return InputType.TEXT_SELECTION

    def capture_input(self) -> Optional[InputContent]:
        """Capture selected text from clipboard.

        Returns:
            InputContent with selected text or None if clipboard empty
        """
        try:
            text = self.selection_manager.get_selected_text()

            if text:
                self.logger.info(f"Captured text selection: {len(text)} chars")
                return InputContent(
                    input_type=InputType.TEXT_SELECTION,
                    text=text,
                    metadata={
                        "source": "clipboard",
                        "char_count": len(text),
                        "word_count": len(text.split())
                    }
                )

            return None

        except Exception as e:
            self.logger.error(f"Error capturing text selection: {e}")
            return None

    def is_available(self) -> bool:
        """Check if text is available in clipboard.

        Returns:
            True if clipboard has text content
        """
        try:
            text = self.selection_manager.get_selected_text()
            return text is not None and len(text.strip()) > 0
        except Exception as e:
            self.logger.error(f"Error checking availability: {e}")
            return False
```

**✅ Ação:** Salvar arquivo em `C:\.agent_click\core\input_strategies\text_selection_strategy.py`

---

### **4.2. FileUploadStrategy (NOVO)**

**Arquivo:** `core/input_strategies/file_upload_strategy.py` (NOVO)

```python
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
```

**✅ Ação:** Salvar arquivo em `C:\.agent_click\core\input_strategies\file_upload_strategy.py`

---

### **4.3. ClipboardImageStrategy (NOVO)**

**Arquivo:** `core/input_strategies/clipboard_image_strategy.py` (NOVO)

```python
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
```

**✅ Ação:** Salvar arquivo em `C:\.agent_click\core\input_strategies\clipboard_image_strategy.py`

---

### **4.4. ScreenshotStrategy (NOVO)**

**Arquivo:** `core/input_strategies/screenshot_strategy.py` (NOVO)

```python
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
```

**✅ Ação:** Salvar arquivo em `C:\.agent_click\core\input_strategies\screenshot_strategy.py`

---

### **4.5. Criar arquivo __init__.py para o pacote**

**Arquivo:** `core/input_strategies/__init__.py` (NOVO)

```python
"""Input strategies package.

Exports all available input strategies.
"""

from .text_selection_strategy import TextSelectionStrategy
from .file_upload_strategy import FileUploadStrategy
from .clipboard_image_strategy import ClipboardImageStrategy
from .screenshot_strategy import ScreenshotStrategy

__all__ = [
    'TextSelectionStrategy',
    'FileUploadStrategy',
    'ClipboardImageStrategy',
    'ScreenshotStrategy'
]
```

**✅ Ação:** Salvar arquivo em `C:\.agent_click\core\input_strategies\__init__.py`

---

## 5. PASSO 3: MODIFICAR SISTEMA CORE

### **5.1. Criar InputManager**

**Arquivo:** `core/input_manager.py` (NOVO)

```python
"""Input manager for AgentClick system.

Manages multiple input strategies and selects appropriate one.
"""

from typing import Optional, List
from core.input_strategy import InputStrategy, InputType, InputContent
from core.input_strategies import (
    TextSelectionStrategy,
    FileUploadStrategy,
    ClipboardImageStrategy,
    ScreenshotStrategy
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
        fallback: bool = True
    ) -> Optional[InputContent]:
        """Capture input using best available strategy.

        Args:
            preferred_type: Optional preferred input type to use first
            fallback: If True and preferred_type fails, try other strategies

        Returns:
            InputContent or None if no input available

        Behavior:
            - If preferred_type specified: tries that strategy first
            - If fallback is True and preferred fails: tries other strategies
            - If no preferred_type: auto-detects best available input
        """
        # If preferred type specified, try that first
        if preferred_type:
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
            InputType.FILE_UPLOAD,
            InputType.CLIPBOARD_IMAGE,
        ]

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

    def check_available_inputs(self) -> dict[InputType, bool]:
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

    def cleanup_temp_files(self, hours: int = 24) -> dict[str, int]:
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
```

**✅ Ação:** Salvar arquivo em `C:\.agent_click\core\input_manager.py`

---

### **5.2. Modificar core/system.py**

**Arquivo:** `core/system.py` (MODIFICAR)

Encontre a classe `AgentClickSystem` e faça as seguintes modificações:

#### **Modificação 1: Adicionar imports**

```python
# Adicione no topo com os outros imports:
from core.input_manager import InputManager
from core.input_strategy import InputType, InputContent
```

#### **Modificação 2: Modificar __init__**

```python
def __init__(self):
    """Initialize AgentClick system."""
    logger.info("=" * 60)
    logger.info("AgentClick System v1.0 - Initializing")
    logger.info("=" * 60)

    # Initialize signals for thread-safe GUI updates
    self.signals = SystemSignals()
    self.signals.show_large_popup_signal.connect(self._show_large_popup_in_main_thread)
    self.signals.update_mini_popup_signal.connect(self._update_mini_popup_in_main_thread)
    self.signals.update_large_popup_agent_signal.connect(self._update_large_popup_agent_in_main_thread)
    self.signals.log_message_signal.connect(self._log_in_main_thread)

    # MODIFICAÇÃO: Initialize components
    self.input_manager = InputManager()  # NOVO
    self.selection_manager = SelectionManager()  # Manter para compatibilidade
    self.click_processor = ClickProcessor()
    self.agent_registry = AgentRegistry()
    self.config_manager = AgentConfigManager()
    self.output_handler = OutputHandler(self.selection_manager)

    # Get initial agent
    initial_agent = self.agent_registry.get_current_agent()

    # Create mini popup (always visible)
    self.mini_popup: Optional[MiniPopupWidget] = MiniPopupWidget(initial_agent)
    self.mini_popup.clicked.connect(self._on_mini_popup_clicked)
    self.mini_popup.file_dropped.connect(self._on_file_dropped)  # NOVO
    self.mini_popup.show()

    # Large popup (shown only when clicked)
    self.large_popup: Optional[PopupWindow] = None

    # Register callbacks
    self.click_processor.register_pause_handler(self._on_pause_pressed)
    self.click_processor.register_switch_handler(self._on_switch_pressed)
    self.click_processor.register_screenshot_handler(self._on_screenshot_pressed)  # NOVO

    logger.info("AgentClick System initialized successfully")
    logger.info(f"Available agents: {list(self.agent_registry.agents.keys())}")
    logger.info("Press Pause to activate current agent")
    logger.info("Press Ctrl+Pause to switch to next agent")
    logger.info("Press Ctrl+Shift+Pause to take screenshot")  # NOVO
    logger.info("Click mini popup to open detailed view")
    logger.info(f"\n{self.input_manager.get_status_summary()}")  # NOVO
```

#### **Modificação 3: Adicionar novos handlers**

```python
# Adicione estes métodos novos à classe AgentClickSystem:

def _on_file_dropped(self, file_path: str) -> None:
    """Handle file dropped on mini popup.

    Args:
        file_path: Path to dropped file
    """
    from pathlib import Path

    logger.info(f"File dropped: {file_path}")

    # Configure file upload
    self.input_manager.set_file_upload(file_path)

    # Show notification in large popup if open
    if self.large_popup:
        self.signals.log_message_signal.emit(
            f"📎 File loaded: {Path(file_path).name}",
            "info"
        )

    # Auto-process after file drop
    logger.info("Auto-processing dropped file...")
    self._process_input_with_current_agent(InputType.FILE_UPLOAD)

def _on_screenshot_pressed(self) -> None:
    """Handle Ctrl+Shift+Pause - take screenshot."""
    logger.info("Screenshot hotkey pressed")

    # Take screenshot
    input_content = self.input_manager.take_screenshot()

    if input_content:
        if self.large_popup:
            self.signals.log_message_signal.emit(
                f"📸 Screenshot captured",
                "info"
            )

        # Auto-process screenshot
        self._process_input_with_current_agent(InputType.SCREENSHOT)
    else:
        logger.error("Failed to capture screenshot")
        if self.large_popup:
            self.signals.log_message_signal.emit(
                "❌ Failed to capture screenshot",
                "error"
            )

def _process_input_with_current_agent(self, input_type: InputType) -> None:
    """Process input with current agent.

    Args:
        input_type: Type of input to process
    """
    current_agent = self.agent_registry.get_current_agent()
    if not current_agent:
        logger.warning("No agents available")
        return

    logger.info(f"Activating agent: {current_agent.metadata.name}")

    # Capture input
    input_content = self.input_manager.capture_input(preferred_type=input_type)

    if not input_content:
        logger.warning(f"No input available for type: {input_type.value}")
        if self.large_popup:
            self.signals.log_message_signal.emit(
                f"⚠️  No input available",
                "warning"
            )
        return

    # Get text for agent
    selected_text = input_content.get_text_for_agent()

    # Get agent configuration
    agent_name = current_agent.metadata.name
    context_folder = self.config_manager.get_context_folder(agent_name)
    focus_file = self.config_manager.get_focus_file(agent_name)
    output_mode = self.config_manager.get_output_mode(agent_name)

    logger.info(f"Processing with {current_agent.metadata.name}...")
    logger.info(f"Input type: {input_type.value}")
    logger.info(f"Output mode: {output_mode}")

    # Pass image path if available
    image_path = input_content.image_path

    # Process with agent
    try:
        result = current_agent.process(
            selected_text,
            context_folder,
            focus_file,
            output_mode,
            image_path=image_path  # NOVO: Pass image path
        )
        self._handle_result(result, current_agent)
    except Exception as e:
        error_msg = f"Error processing: {str(e)}"
        logger.error(error_msg)
        if self.large_popup:
            self.signals.log_message_signal.emit(
                f"❌ {error_msg}",
                "error"
            )
```

#### **Modificação 4: Atualizar _on_pause_pressed**

```python
def _on_pause_pressed(self) -> None:
    """Handle Pause key - activate current agent (no popup)."""
    current_agent = self.agent_registry.get_current_agent()
    if not current_agent:
        logger.warning("No agents available")
        return

    logger.info(f"Activating agent: {current_agent.metadata.name}")

    # MODIFICAÇÃO: Usar InputManager para capturar input
    input_content = self.input_manager.capture_input()

    if not input_content:
        logger.warning("No input available")
        if self.large_popup:
            self.signals.log_message_signal.emit(
                "⚠️  No input available",
                "warning"
            )
        return

    # Log input type
    input_type = input_content.input_type
    logger.info(f"Input type: {input_type.value}")

    # Get text for agent
    selected_text = input_content.get_text_for_agent()

    # Get agent configuration
    agent_name = current_agent.metadata.name
    context_folder = self.config_manager.get_context_folder(agent_name)
    focus_file = self.config_manager.get_focus_file(agent_name)
    output_mode = self.config_manager.get_output_mode(agent_name)

    logger.info(f"Processing with {current_agent.metadata.name}...")
    logger.info(f"Output mode: {output_mode}")

    # Pass image path if available
    image_path = input_content.image_path

    # Process with agent
    try:
        result = current_agent.process(
            selected_text,
            context_folder,
            focus_file,
            output_mode,
            image_path=image_path  # NOVO
        )
        self._handle_result(result, current_agent)
    except Exception as e:
        error_msg = f"Error processing: {str(e)}"
        logger.error(error_msg)
        if self.large_popup:
            self.signals.log_message_signal.emit(
                f"❌ {error_msg}",
                "error"
            )
```

**✅ Ação:** Modificar `C:\.agent_click\core\system.py`

---

### **5.3. Modificar core/click_processor.py**

**Arquivo:** `core/click_processor.py` (MODIFICAR)

Adicione o novo método para screenshot:

```python
# Adicione este método à classe ClickProcessor:

def register_screenshot_handler(self, handler: callable) -> None:
    """Register handler for screenshot key (Ctrl+Shift+Pause).

    Args:
        handler: Callback function to execute when hotkey pressed
    """
    try:
        keyboard.add_hotkey('ctrl+shift+pause', handler)
        self.logger.info("Screenshot handler registered: Ctrl+Shift+Pause")
    except Exception as e:
        self.logger.error(f"Failed to register screenshot handler: {e}")
```

**✅ Ação:** Modificar `C:\.agent_click\core\click_processor.py`

---

## 6. PASSO 4: MODIFICAR INTERFACE

### **6.1. Modificar Mini Popup para Drag & Drop**

**Arquivo:** `ui/mini_popup.py` (MODIFICAR)

#### **Modificação 1: Adicionar imports**

```python
# Adicione aos imports existentes:
from PyQt6.QtCore import QMimeData
from PyQt6.QtGui import QDragEnterEvent, QDropEvent
```

#### **Modificação 2: Modificar classe MiniPopupWidget**

```python
class MiniPopupWidget(QWidget):
    """Small, always-visible popup showing current agent icon."""

    clicked = pyqtSignal()  # Signal when clicked
    file_dropped = pyqtSignal(str)  # NOVO: Signal when file dropped

    def __init__(self, initial_agent: BaseAgent):
        """Initialize mini popup.

        Args:
            initial_agent: Initial agent to display
        """
        super().__init__()
        self.current_agent = initial_agent
        self.logger = setup_logger('MiniPopup')

        self._setup_ui()

        # NOVO: Enable drag & drop
        self.setAcceptDrops(True)

        self.logger.info("Mini popup initialized with drag & drop support")

    # ... restante do código existente ...

    # NOVO: Adicione estes métodos após mousePressEvent:

    def dragEnterEvent(self, event: QDragEnterEvent):
        """Handle drag enter event.

        Called when user drags something over the mini popup.

        Args:
            event: Drag enter event
        """
        if event.mimeData().hasUrls():
            # Accept the drag event
            event.acceptProposedAction()
            self.logger.debug("File dragged over mini popup")

            # Visual feedback - slightly enlarge
            self.setFixedSize(70, 70)
            self.icon_label.setStyleSheet("""
                QLabel {
                    font-size: 38px;
                    background-color: %s;
                    color: #ffffff;
                    border-radius: 35px;
                    border: 3px solid #0078d4;
                }
            """ % self.current_agent.metadata.color)
        else:
            event.ignore()

    def dragLeaveEvent(self, event):
        """Handle drag leave event.

        Called when user drags something away from mini popup.

        Args:
            event: Drag leave event
        """
        # Reset to normal size
        self.setFixedSize(60, 60)
        self.icon_label.setStyleSheet("""
            QLabel {
                font-size: 32px;
                background-color: %s;
                color: #ffffff;
                border-radius: 30px;
            }
        """ % self.current_agent.metadata.color)

    def dropEvent(self, event: QDropEvent):
        """Handle drop event.

        Called when user drops file on mini popup.

        Args:
            event: Drop event
        """
        mime_data = event.mimeData()

        if mime_data.hasUrls():
            # Get first file from the list
            files = [u.toLocalFile() for u in mime_data.urls()]
            if files:
                file_path = files[0]
                self.logger.info(f"File dropped on mini popup: {file_path}")

                # Emit signal
                self.file_dropped.emit(file_path)

                # Reset appearance
                self.setFixedSize(60, 60)
                self.icon_label.setStyleSheet("""
                    QLabel {
                        font-size: 32px;
                        background-color: %s;
                        color: #ffffff;
                        border-radius: 30px;
                    }
                """ % self.current_agent.metadata.color)

        event.acceptProposedAction()
```

**✅ Ação:** Modificar `C:\.agent_click\ui\mini_popup.py`

---

### **6.2. (Opcional) Adicionar botões ao Popup Detalhado**

**Arquivo:** `ui/popup_window.py` (OPCIONAL)

Se quiser adicionar botões para capturar inputs manualmente, adicione à aba Activity:

```python
# Adicione na classe PopupWindow, no método _create_activity_log_tab():

# Adicione após criar o log_text:

# NOVO: Input buttons
input_buttons_layout = QHBoxLayout()

# Screenshot button
screenshot_btn = QPushButton("📸 Screenshot")
screenshot_btn.setStyleSheet("""
    QPushButton {
        background-color: #8b5cf6;
        color: #ffffff;
        border: none;
        padding: 6px 12px;
        border-radius: 4px;
        font-size: 11px;
    }
    QPushButton:hover {
        background-color: #7c3aed;
    }
""")

# Clipboard image button
clipboard_btn = QPushButton("🖼️  Clipboard Image")
clipboard_btn.setStyleSheet("""
    QPushButton {
        background-color: #ec4899;
        color: #ffffff;
        border: none;
        padding: 6px 12px;
        border-radius: 4px;
        font-size: 11px;
    }
    QPushButton:hover {
        background-color: #db2777;
    }
""")

input_buttons_layout.addWidget(screenshot_btn)
input_buttons_layout.addWidget(clipboard_btn)
input_buttons_layout.addStretch()

log_layout.addLayout(input_buttons_layout)

# Conectar sinais (será feito depois de ter acesso ao system)
# Por enquanto, apenas adicione os botões visualmente
```

**✅ Ação (Opcional):** Modificar `C:\.agent_click\ui\popup_window.py`

---

## 7. PASSO 5: MODIFICAR AGENTES

### **7.1. Modificar BaseAgent para Suportar Imagens**

**Arquivo:** `agents/base_agent.py` (MODIFICAR)

#### **Modificação 1: Atualizar método process**

```python
def process(
    self,
    text: str,
    context_folder: Optional[str] = None,
    focus_file: Optional[str] = None,
    output_mode: str = "AUTO",
    image_path: Optional[str] = None  # NOVO parâmetro
):
    """Process text with this agent.

    Args:
        text: Text to process
        context_folder: Optional context folder path
        focus_file: Optional focus file path
        output_mode: Output mode (AUTO, CLIPBOARD_PURE, etc.)
        image_path: NOVO - Optional image path for visual analysis

    Returns:
        AgentResult with content and metadata
    """
    from agents.output_modes import OutputMode, AgentResult

    self.logger.info(f"Processing with {self.metadata.name}")
    self.logger.debug(f"Input text: {text[:100]}...")
    self.logger.info(f"Output mode: {output_mode}")

    # NOVO: Log se tiver imagem
    if image_path:
        self.logger.info(f"Image provided: {image_path}")

    if context_folder:
        self.logger.info(f"Context folder: {context_folder}")
    if focus_file:
        self.logger.info(f"Focus file: {focus_file}")

    try:
        # Create SDK options
        system_prompt = self.get_system_prompt(text, context_folder, focus_file)
        options = create_sdk_options(system_prompt)

        # Build prompt with context
        prompt = self._build_prompt(text, context_folder, focus_file, image_path)  # NOVO: Pass image_path

        # Query Claude SDK
        result_text = self._query_sdk(prompt, options)

        # Parse output to extract thoughts and content (if formatted)
        content, raw_thoughts = self._parse_output(result_text)

        # Generate suggested filename based on task
        suggested_filename = self._generate_filename(text, context_folder)

        self.logger.info(f"Processing complete: {len(result_text)} chars")

        # Create structured result
        result = AgentResult(
            content=content,
            output_mode=OutputMode.from_string(output_mode),
            metadata={
                "agent": self.metadata.name,
                "context_folder": context_folder,
                "focus_file": focus_file,
                "image_path": image_path  # NOVO: Include in metadata
            },
            raw_thoughts=raw_thoughts,
            suggested_filename=suggested_filename
        )

        return result

    except Exception as e:
        self.logger.error(f"Error processing: {e}", exc_info=True)
        raise
```

#### **Modificação 2: Atualizar _build_prompt**

```python
def _build_prompt(
    self,
    text: str,
    context_folder: Optional[str] = None,
    focus_file: Optional[str] = None,
    image_path: Optional[str] = None  # NOVO parâmetro
) -> str:
    """Build prompt for Claude SDK.

    Args:
        text: Input text
        context_folder: Optional context folder
        focus_file: Optional focus file
        image_path: NOVO - Optional image path

    Returns:
        Formatted prompt
    """
    prompt_parts = []

    # Add context information if available
    if context_folder or focus_file:
        prompt_parts.append("CONTEXT INFORMATION:")

        if context_folder:
            prompt_parts.append(f"• Context Folder: {context_folder}")

        if focus_file:
            prompt_parts.append(f"• Focus File: {focus_file}")

        prompt_parts.append("")  # Empty line

    # NOVO: Add image information if available
    if image_path:
        prompt_parts.append("VISUAL CONTEXT:")
        prompt_parts.append(f"• Image attached: {image_path}")
        prompt_parts.append(f"• Use this image for visual analysis if needed")
        prompt_parts.append("")  # Empty line

    # Add the main task
    prompt_parts.append("TASK:")
    prompt_parts.append(f"Process the following:\n{text}")
    prompt_parts.append("\nProvide only the result, no explanations.")

    return "\n".join(prompt_parts)
```

**✅ Ação:** Modificar `C:\.agent_click\agents\base_agent.py`

---

## 8. PASSO 6: TESTES

### **8.1. Instalar Dependências**

```bash
# No diretório C:\.agent_click
pip install Pillow
```

### **8.2. Criar Script de Teste**

**Arquivo:** `test_inputs.py` (NOVO - temporário, na raiz)

```python
"""Test script for new input types."""

from core.input_manager import InputManager
from core.input_strategy import InputType
from pathlib import Path

def test_text_selection():
    """Test text selection input."""
    print("\n" + "="*60)
    print("TEST 1: Text Selection")
    print("="*60)

    manager = InputManager()

    # Copy some text to clipboard first
    import pyperclip
    test_text = "This is a test text for AgentClick input system."
    pyperclip.copy(test_text)
    print(f"✅ Text copied to clipboard: {test_text[:50]}...")

    # Capture
    content = manager.capture_input(preferred_type=InputType.TEXT_SELECTION)

    if content:
        print(f"✅ Input captured!")
        print(f"   Type: {content.input_type.value}")
        print(f"   Text: {content.text[:50]}...")
        print(f"   Metadata: {content.metadata}")
    else:
        print("❌ Failed to capture text selection")


def test_file_upload():
    """Test file upload input."""
    print("\n" + "="*60)
    print("TEST 2: File Upload")
    print("="*60)

    manager = InputManager()

    # Create test file
    test_file = Path("test_input.txt")
    test_content = "This is test content from a file.\nLine 2\nLine 3"

    test_file.write_text(test_content, encoding='utf-8')
    print(f"✅ Test file created: {test_file}")

    # Configure file upload
    manager.set_file_upload(str(test_file))

    # Capture
    content = manager.capture_input(preferred_type=InputType.FILE_UPLOAD)

    if content:
        print(f"✅ Input captured!")
        print(f"   Type: {content.input_type.value}")
        print(f"   File: {content.file_path}")
        print(f"   Text: {content.text[:50]}...")
        print(f"   Metadata: {content.metadata}")
    else:
        print("❌ Failed to capture file upload")

    # Cleanup
    test_file.unlink()
    print("🧹 Test file cleaned up")


def test_clipboard_image():
    """Test clipboard image input."""
    print("\n" + "="*60)
    print("TEST 3: Clipboard Image")
    print("="*60)

    manager = InputManager()

    # Check availability first
    available = manager.check_available_inputs()
    print(f"Clipboard image available: {available[InputType.CLIPBOARD_IMAGE]}")

    if available[InputType.CLIPBOARD_IMAGE]:
        # Capture
        content = manager.capture_input(preferred_type=InputType.CLIPBOARD_IMAGE)

        if content:
            print(f"✅ Input captured!")
            print(f"   Type: {content.input_type.value}")
            print(f"   Image: {content.image_path}")
            print(f"   Metadata: {content.metadata}")
        else:
            print("❌ Failed to capture clipboard image")
    else:
        print("⚠️  No image in clipboard - copy an image first (Ctrl+C on any image)")
        print("   Then run this test again.")


def test_screenshot():
    """Test screenshot input."""
    print("\n" + "="*60)
    print("TEST 4: Screenshot")
    print("="*60)

    manager = InputManager()

    print("Taking screenshot in 3 seconds...")
    print("Switch to the window you want to capture!")

    import time
    time.sleep(3)

    # Capture
    content = manager.take_screenshot()

    if content:
        print(f"✅ Input captured!")
        print(f"   Type: {content.input_type.value}")
        print(f"   Image: {content.image_path}")
        print(f"   Metadata: {content.metadata}")
    else:
        print("❌ Failed to capture screenshot")


def test_auto_detect():
    """Test auto-detection of best input."""
    print("\n" + "="*60)
    print("TEST 5: Auto-Detect Best Input")
    print("="*60)

    manager = InputManager()

    # Show status
    print("\nAvailable inputs:")
    print(manager.get_status_summary())

    # Auto-detect
    content = manager.capture_input()

    if content:
        print(f"\n✅ Auto-detected and captured!")
        print(f"   Type: {content.input_type.value}")
        print(f"   Text: {content.text[:50]}...")
    else:
        print("❌ No input available")


def main():
    """Run all tests."""
    print("\n" + "="*60)
    print("AgentClick Input System Tests")
    print("="*60)

    test_text_selection()
    test_file_upload()
    test_clipboard_image()
    # test_screenshot()  # Uncomment to test screenshot
    test_auto_detect()

    print("\n" + "="*60)
    print("Tests completed!")
    print("="*60)


if __name__ == "__main__":
    main()
```

**✅ Ação:** Criar `C:\.agent_click\test_inputs.py`

### **8.3. Executar Testes**

```bash
# No diretório C:\.agent_click
python test_inputs.py
```

---

## 9. TROUBLESHOOTING

### **Problema 1: "PIL not installed"**

**Solução:**
```bash
pip install Pillow
```

### **Problema 2: Drag & drop não funciona**

**Verificar:**
1. Confirme que `setAcceptDrops(True)` foi chamado no `__init__` do MiniPopupWidget
2. Verifique se os eventos `dragEnterEvent` e `dropEvent` foram implementados
3. Verifique se o sinal `file_dropped` está conectado no system.py

### **Problema 3: Clipboard image sempre retorna None**

**Possíveis causas:**
1. Nenhuma imagem no clipboard - copie uma imagem primeiro (Ctrl+C)
2. PIL/Pillow não instalado - instale com `pip install Pillow`
3. Formato de imagem não suportado - tente PNG ou JPEG

### **Problema 4: File upload lê arquivo vazio**

**Verificar:**
1. Caminho do arquivo está correto
2. Arquivo é texto (não binário)
3. Permissões de leitura no arquivo

### **Problema 5: Hotkey Ctrl+Shift+Pause não funciona**

**Verificar:**
1. Método `register_screenshot_handler` foi chamado no `__init__` do System
2. Handler `_on_screenshot_pressed` foi implementado
3. Nenhuma outra aplicação está usando o mesmo atalho

---

## 📊 CHECKLIST FINAL

Use este checklist para verificar se tudo foi implementado:

### **Arquivos Criados:**
- [ ] `core/input_strategy.py`
- [ ] `core/input_manager.py`
- [ ] `core/input_strategies/__init__.py`
- [ ] `core/input_strategies/text_selection_strategy.py`
- [ ] `core/input_strategies/file_upload_strategy.py`
- [ ] `core/input_strategies/clipboard_image_strategy.py`
- [ ] `core/input_strategies/screenshot_strategy.py`

### **Arquivos Modificados:**
- [ ] `core/system.py`
- [ ] `core/click_processor.py`
- [ ] `ui/mini_popup.py`
- [ ] `agents/base_agent.py`

### **Dependências:**
- [ ] Pillow instalado (`pip install Pillow`)

### **Testes:**
- [ ] Text selection funciona
- [ ] File upload via drag & drop funciona
- [ ] Clipboard image funciona
- [ ] Screenshot funciona
- [ ] Auto-detect funciona

---

## 🎯 PRÓXIMOS PASSOS (OPCIONAIS)

Após implementação básica funcionando, você pode adicionar:

1. **Integração com VSCode API**
   - Detectar arquivo selecionado no VSCode explorer
   - Atalho customizado no VSCode

2. **Suporte a Visão com Claude SDK**
   - Usar capacidades visuais do Claude para analisar imagens
   - Passar imagem diretamente para o SDK

3. **Interface Aprimorada**
   - Adicionar botões na UI para cada tipo de input
   - Preview de imagens antes de processar

4. **Configurações por Input Type**
   - Configurar quais agentes aceitam quais tipos de input
   - Priorizar estratégias por agente

5. **Histórico de Inputs**
   - Guardar últimos inputs capturados
   - Reutilizar inputs anteriores

---

## 📚 REFERÊNCIAS

- **Pillow Documentation:** https://pillow.readthedocs.io/
- **PyQt6 Drag & Drop:** https://www.riverbankcomputing.com/static/Docs/PyQt6/
- **Strategy Pattern:** https://refactoring.guru/design-patterns/strategy

---

**Fim do Guia de Implementação! 🎉**

Para dúvidas ou problemas, consulte a seção de Troubleshooting ou revise os passos anteriores.
