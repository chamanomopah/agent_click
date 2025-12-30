# Implementação de Sistema de Múltiplos Outputs - AgentClick v1.1

## 📋 Índice
1. [Visão Geral](#visão-geral)
2. [Arquitetura da Solução](#arquitetura-da-solução)
3. [Passo 1: Configuração](#passo-1-configuração)
4. [Passo 2: Modificar AgentSettings](#passo-2-modificar-agentsettings)
5. [Passo 3: Criar Sistema de Output](#passo-3-criar-sistema-de-output)
6. [Passo 4: Modificar BaseAgent](#passo-4-modificar-baseagent)
7. [Passo 5: Atualizar Sistema Principal](#passo-5-atualizar-sistema-principal)
8. [Passo 6: Atualizar Interface](#passo-6-atualizar-interface)
9. [Passo 7: Testes e Validação](#passo-7-testes-e-validação)
10. [Exemplos de Uso](#exemplos-de-uso)

---

## 🎯 Visão Geral

### Objetivo
Adicionar um sistema flexível de **múltiplos tipos de output** para os agentes do AgentClick, permitindo que o usuário configure como o resultado será entregue.

### Modos de Output Disponíveis

| Modo | Código | Descrição |
|------|--------|-----------|
| **Automático** | `AUTO` | O agente decide o melhor output baseado na tarefa |
| **Clipboard Puro** | `CLIPBOARD_PURE` | Apenas o conteúdo essencial, sem formatação ou metadados |
| **Clipboard Rico** | `CLIPBOARD_RICH` | Conteúdo formatado com markdown, cores e estrutura |
| **Arquivo** | `FILE` | Salva diretamente em um arquivo no projeto |
| **Editor Interativo** | `INTERACTIVE_EDITOR` | Abre uma janela para preview e edição antes de salvar |

### Fluxo Atual vs Novo Fluxo

```
【FLUXO ATUAL】
Usuário → Pause → Agent.process() → result (str) → Clipboard

【NOVO FLUXO】
Usuário → Pause → Agent.process() → AgentResult → OutputHandler → Ação Configurada
                                                        ├─ AUTO (decide)
                                                        ├─ CLIPBOARD_PURE
                                                        ├─ CLIPBOARD_RICH
                                                        ├─ FILE
                                                        └─ INTERACTIVE_EDITOR
```

---

## 🏗️ Arquitetura da Solução

### Estrutura de Arquivos

```
C:\.agent_click\
├── config/
│   ├── agent_config.py              [MODIFICAR] ✏️
│   └── agent_config.json            [ATUALIZAR AUTOMATICamente]
│
├── agents/
│   ├── base_agent.py                [MODIFICAR] ✏️
│   └── output_modes.py              [NOVO] 🆕
│
├── core/
│   ├── system.py                    [MODIFICAR] ✏️
│   ├── output_handler.py            [NOVO] 🆕
│   └── interactive_editor.py        [NOVO] 🆕
│
└── ui/
    └── popup_window.py              [MODIFICAR] ✏️
```

### Componentes Novos

1. **`agents/output_modes.py`**: Enum de modos e lógica de decisão
2. **`core/output_handler.py`**: Handler para cada tipo de output
3. **`core/interactive_editor.py`**: Janela de preview/edição

---

## 📝 Passo 1: Configuração

### 1.1 Criar Enum de Modos de Output

**Arquivo**: `agents/output_modes.py` (NOVO)

```python
"""Output mode definitions for AgentClick agents."""

from enum import Enum
from typing import Optional
from utils.logger import setup_logger

logger = setup_logger('OutputModes')


class OutputMode(Enum):
    """Available output modes for agents."""

    AUTO = "AUTO"
    """Agent automatically decides the best output mode based on content."""

    CLIPBOARD_PURE = "CLIPBOARD_PURE"
    """Copy only essential content to clipboard, no formatting or metadata."""

    CLIPBOARD_RICH = "CLIPBOARD_RICH"
    """Copy formatted content (markdown, structure) to clipboard."""

    FILE = "FILE"
    """Save output directly to a file in the project."""

    INTERACTIVE_EDITOR = "INTERACTIVE_EDITOR"
    """Open preview window for editing before finalizing output."""


    @property
    def display_name(self) -> str:
        """Human-readable name for UI display."""
        display_map = {
            OutputMode.AUTO: "🤖 Auto (Agent Decide)",
            OutputMode.CLIPBOARD_PURE: "📋 Clipboard (Pure)",
            OutputMode.CLIPBOARD_RICH: "📋 Clipboard (Rich)",
            OutputMode.FILE: "💾 Save to File",
            OutputMode.INTERACTIVE_EDITOR: "✏️ Interactive Editor"
        }
        return display_map.get(self, self.value)


    @property
    def description(self) -> str:
        """Detailed description for tooltips."""
        desc_map = {
            OutputMode.AUTO: "Agent chooses best output based on task",
            OutputMode.CLIPBOARD_PURE: "Raw content without formatting or metadata",
            OutputMode.CLIPBOARD_RICH: "Formatted content with markdown structure",
            OutputMode.FILE: "Automatically save to file in project folder",
            OutputMode.INTERACTIVE_EDITOR: "Preview and edit before final output"
        }
        return desc_map.get(self, "")


    @classmethod
    def from_string(cls, value: str) -> 'OutputMode':
        """Convert string to OutputMode.

        Args:
            value: String value to convert

        Returns:
            OutputMode enum value

        Raises:
            ValueError: If value is not a valid mode
        """
        try:
            return cls(value.upper())
        except ValueError:
            logger.warning(f"Invalid output mode: {value}, defaulting to AUTO")
            return cls.AUTO


    def should_use_file(self) -> bool:
        """Check if this mode requires file output."""
        return self == OutputMode.FILE


    def should_use_clipboard(self) -> bool:
        """Check if this mode uses clipboard."""
        return self in {
            OutputMode.CLIPBOARD_PURE,
            OutputMode.CLIPBOARD_RICH
        }


    def requires_interaction(self) -> bool:
        """Check if this mode requires user interaction."""
        return self == OutputMode.INTERACTIVE_EDITOR
```

**Salve como**: `C:\.agent_click\agents\output_modes.py`

---

## 📝 Passo 2: Modificar AgentSettings

### 2.1 Adicionar Campo de Output Mode

**Arquivo**: `config/agent_config.py` (MODIFICAR)

**Localização**: Linha 12-28

**ANTES**:
```python
@dataclass
class AgentSettings:
    """Settings for a specific agent."""
    context_folder: Optional[str] = None
    focus_file: Optional[str] = None

    def to_dict(self) -> dict:
        """Convert to dictionary."""
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict) -> 'AgentSettings':
        """Create from dictionary."""
        return cls(
            context_folder=data.get('context_folder'),
            focus_file=data.get('focus_file')
        )
```

**DEPOIS**:
```python
@dataclass
class AgentSettings:
    """Settings for a specific agent."""
    context_folder: Optional[str] = None
    focus_file: Optional[str] = None
    output_mode: str = "AUTO"  # NOVO CAMPO

    def to_dict(self) -> dict:
        """Convert to dictionary."""
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict) -> 'AgentSettings':
        """Create from dictionary."""
        return cls(
            context_folder=data.get('context_folder'),
            focus_file=data.get('focus_file'),
            output_mode=data.get('output_mode', 'AUTO')  # NOVO
        )
```

### 2.2 Adicionar Métodos de Output Mode

**Adicione após a linha 160** (final do arquivo `config/agent_config.py`):

```python
    def set_output_mode(self, agent_name: str, mode: str) -> None:
        """Set output mode for an agent.

        Args:
            agent_name: Name of the agent
            mode: Output mode string (AUTO, CLIPBOARD_PURE, etc.)
        """
        from agents.output_modes import OutputMode

        # Validate mode
        try:
            OutputMode.from_string(mode)
        except ValueError as e:
            logger.error(f"Invalid output mode: {mode}")
            raise ValueError(f"Invalid output mode: {mode}. Must be one of: {[m.value for m in OutputMode]}")

        settings = self.get_settings(agent_name)
        settings.output_mode = mode
        self._save()
        logger.info(f"Set output mode for {agent_name}: {mode}")

    def get_output_mode(self, agent_name: str) -> str:
        """Get output mode for an agent.

        Args:
            agent_name: Name of the agent

        Returns:
            Output mode string
        """
        settings = self.get_settings(agent_name)
        return settings.output_mode
```

---

## 📝 Passo 3: Criar Sistema de Output

### 3.1 Criar Dataclass de Resultado

**Arquivo**: `agents/output_modes.py` (ADICIONAR AO FINAL)

```python
from dataclasses import dataclass
from typing import Optional, Dict, Any


@dataclass
class AgentResult:
    """Structured result from agent processing."""

    content: str
    """Main content/output from the agent."""

    output_mode: OutputMode
    """How the output should be delivered."""

    metadata: Optional[Dict[str, Any]] = None
    """Additional metadata (filename, language, etc)."""

    raw_thoughts: Optional[str] = None
    """Agent's internal reasoning/thoughts (separated from content)."""

    suggested_filename: Optional[str] = None
    """Suggested filename for FILE mode."""

    def __post_init__(self):
        """Initialize metadata if None."""
        if self.metadata is None:
            self.metadata = {}


    def get_pure_content(self) -> str:
        """Get content without metadata or formatting."""
        return self.content


    def get_rich_content(self) -> str:
        """Get content with formatting."""
        if self.raw_thoughts:
            return f"# Reasoning\n\n{self.raw_thoughts}\n\n---\n\n# Output\n\n{self.content}"
        return self.content
```

### 3.2 Criar Output Handler

**Arquivo**: `core/output_handler.py` (NOVO)

```python
"""Output handler for AgentClick system.

Handles different output modes for agent results.
"""

import os
from pathlib import Path
from typing import Optional
from PyQt6.QtWidgets import QApplication
from agents.output_modes import OutputMode, AgentResult
from core.selection_manager import SelectionManager
from core.interactive_editor import InteractiveEditorDialog
from utils.logger import setup_logger

logger = setup_logger('OutputHandler')


class OutputHandler:
    """Handles output based on configured mode."""

    def __init__(self, selection_manager: SelectionManager):
        """Initialize output handler.

        Args:
            selection_manager: Selection manager for clipboard operations
        """
        self.selection_manager = selection_manager
        self.logger = logger


    def handle(self, result: AgentResult, context_folder: Optional[str] = None) -> bool:
        """Handle agent result based on output mode.

        Args:
            result: Agent result to handle
            context_folder: Optional context folder for file operations

        Returns:
            True if successful, False otherwise
        """
        mode = result.output_mode

        self.logger.info(f"Handling output with mode: {mode.value}")

        try:
            # AUTO mode: decide based on content
            if mode == OutputMode.AUTO:
                return self._handle_auto(result, context_folder)

            # CLIPBOARD_PURE: content only
            elif mode == OutputMode.CLIPBOARD_PURE:
                return self._handle_clipboard_pure(result)

            # CLIPBOARD_RICH: formatted content
            elif mode == OutputMode.CLIPBOARD_RICH:
                return self._handle_clipboard_rich(result)

            # FILE: save to file
            elif mode == OutputMode.FILE:
                return self._handle_file(result, context_folder)

            # INTERACTIVE_EDITOR: preview and edit
            elif mode == OutputMode.INTERACTIVE_EDITOR:
                return self._handle_interactive(result, context_folder)

            else:
                self.logger.warning(f"Unknown mode: {mode}, defaulting to AUTO")
                return self._handle_auto(result, context_folder)

        except Exception as e:
            self.logger.error(f"Error handling output: {e}", exc_info=True)
            return False


    def _handle_auto(self, result: AgentResult, context_folder: Optional[str]) -> bool:
        """AUTO mode: decide best output based on content.

        Rules:
        - If has suggested_filename and context_folder → FILE
        - If content is code (>50 lines) → FILE
        - If content has raw_thoughts → CLIPBOARD_RICH
        - Otherwise → CLIPBOARD_PURE
        """
        content_lines = result.content.count('\n')

        # Has filename and folder? Save to file
        if result.suggested_filename and context_folder:
            self.logger.info("AUTO: Detected filename + context, using FILE mode")
            return self._handle_file(result, context_folder)

        # Large code content? Save to file
        if content_lines > 50 and context_folder:
            self.logger.info("AUTO: Large content (>50 lines), using FILE mode")
            result.suggested_filename = result.suggested_filename or "output.txt"
            return self._handle_file(result, context_folder)

        # Has thoughts? Use rich format
        if result.raw_thoughts:
            self.logger.info("AUTO: Has reasoning, using CLIPBOARD_RICH")
            return self._handle_clipboard_rich(result)

        # Default: pure clipboard
        self.logger.info("AUTO: Using CLIPBOARD_PURE")
        return self._handle_clipboard_pure(result)


    def _handle_clipboard_pure(self, result: AgentResult) -> bool:
        """Copy only pure content to clipboard."""
        content = result.get_pure_content()

        if self.selection_manager.copy_to_clipboard(content):
            self.logger.info(f"✅ Copied pure content to clipboard ({len(content)} chars)")
            return True
        else:
            self.logger.error("❌ Failed to copy to clipboard")
            return False


    def _handle_clipboard_rich(self, result: AgentResult) -> bool:
        """Copy formatted content to clipboard."""
        content = result.get_rich_content()

        if self.selection_manager.copy_to_clipboard(content):
            self.logger.info(f"✅ Copied rich content to clipboard ({len(content)} chars)")
            return True
        else:
            self.logger.error("❌ Failed to copy to clipboard")
            return False


    def _handle_file(self, result: AgentResult, context_folder: Optional[str]) -> bool:
        """Save content to file."""
        if not context_folder:
            self.logger.warning("No context folder for FILE mode, falling back to clipboard")
            return self._handle_clipboard_pure(result)

        # Determine filename
        filename = result.suggested_filename or "output.txt"
        if not filename.endswith('.txt') and not any(filename.endswith(ext) for ext in ['.py', '.js', '.md', '.json', '.yaml', '.yml']):
            filename += '.txt'

        # Create full path
        file_path = Path(context_folder) / filename

        try:
            # Ensure directory exists
            file_path.parent.mkdir(parents=True, exist_ok=True)

            # Write content
            content = result.get_pure_content()
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)

            self.logger.info(f"✅ Saved to file: {file_path}")

            # Also copy to clipboard for convenience
            self.selection_manager.copy_to_clipboard(content)
            self.logger.info("📋 Also copied to clipboard")

            return True

        except Exception as e:
            self.logger.error(f"❌ Failed to save file: {e}")
            return False


    def _handle_interactive(self, result: AgentResult, context_folder: Optional[str]) -> bool:
        """Open interactive editor for preview and editing."""
        try:
            # Create dialog (non-blocking)
            dialog = InteractiveEditorDialog(result, context_folder)

            # Show dialog
            dialog.exec()

            # Check if user confirmed
            if dialog.was_confirmed():
                final_result = dialog.get_final_result()
                self.logger.info(f"✅ Interactive editor confirmed")

                # Handle based on user's final choice
                if dialog.get_final_action() == "file":
                    return self._handle_file(final_result, context_folder)
                else:
                    return self._handle_clipboard_pure(final_result)
            else:
                self.logger.info("❌ Interactive editor cancelled")
                return False

        except Exception as e:
            self.logger.error(f"❌ Error in interactive editor: {e}", exc_info=True)
            return False
```

**Salve como**: `C:\.agent_click\core\output_handler.py`

### 3.3 Criar Editor Interativo

**Arquivo**: `core/interactive_editor.py` (NOVO)

```python
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
```

**Salve como**: `C:\.agent_click\core\interactive_editor.py`

---

## 📝 Passo 4: Modificar BaseAgent

### 4.1 Atualizar Método process()

**Arquivo**: `agents/base_agent.py` (MODIFICAR)

**Localização**: Linha 47-82

**ANTES**:
```python
def process(self, text: str, context_folder: Optional[str] = None, focus_file: Optional[str] = None) -> str:
    """Process text with this agent.

    Args:
        text: Text to process
        context_folder: Optional context folder path
        focus_file: Optional focus file path

    Returns:
        Processed result
    """
    self.logger.info(f"Processing with {self.metadata.name}")
    self.logger.debug(f"Input text: {text[:100]}...")

    if context_folder:
        self.logger.info(f"Context folder: {context_folder}")
    if focus_file:
        self.logger.info(f"Focus file: {focus_file}")

    try:
        # Create SDK options
        system_prompt = self.get_system_prompt(text, context_folder, focus_file)
        options = create_sdk_options(system_prompt)

        # Build prompt with context
        prompt = self._build_prompt(text, context_folder, focus_file)

        # Query Claude SDK
        result_text = self._query_sdk(prompt, options)

        self.logger.info(f"Processing complete: {len(result_text)} chars")
        return result_text

    except Exception as e:
        self.logger.error(f"Error processing: {e}", exc_info=True)
        raise
```

**DEPOIS**:
```python
def process(self, text: str, context_folder: Optional[str] = None, focus_file: Optional[str] = None, output_mode: str = "AUTO") -> AgentResult:
    """Process text with this agent.

    Args:
        text: Text to process
        context_folder: Optional context folder path
        focus_file: Optional focus file path
        output_mode: Output mode (AUTO, CLIPBOARD_PURE, etc.)

    Returns:
        AgentResult with content and metadata
    """
    from agents.output_modes import OutputMode, AgentResult

    self.logger.info(f"Processing with {self.metadata.name}")
    self.logger.debug(f"Input text: {text[:100]}...")
    self.logger.info(f"Output mode: {output_mode}")

    if context_folder:
        self.logger.info(f"Context folder: {context_folder}")
    if focus_file:
        self.logger.info(f"Focus file: {focus_file}")

    try:
        # Create SDK options
        system_prompt = self.get_system_prompt(text, context_folder, focus_file)
        options = create_sdk_options(system_prompt)

        # Build prompt with context
        prompt = self._build_prompt(text, context_folder, focus_file)

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
                "focus_file": focus_file
            },
            raw_thoughts=raw_thoughts,
            suggested_filename=suggested_filename
        )

        return result

    except Exception as e:
        self.logger.error(f"Error processing: {e}", exc_info=True)
        raise


def _parse_output(self, output: str) -> tuple[str, Optional[str]]:
    """Parse output to extract thoughts and main content.

    Args:
        output: Raw output from SDK

    Returns:
        Tuple of (content, thoughts) where thoughts may be None
    """
    # Check if output has thought markers (---, ###, etc)
    separators = ["\n---\n", "\n\n### Reasoning", "\n\n## Thoughts"]

    for sep in separators:
        if sep in output:
            parts = output.split(sep, 1)
            if len(parts) == 2:
                # First part is content, second is thoughts (or vice versa)
                # Usually: content first, then thoughts
                return parts[0].strip(), parts[1].strip()

    # No separation found
    return output.strip(), None


def _generate_filename(self, task: str, context_folder: Optional[str]) -> Optional[str]:
    """Generate suggested filename based on task.

    Args:
        task: Task description
        context_folder: Optional context folder

    Returns:
        Suggested filename or None
    """
    task_lower = task.lower()

    # Detect task type and generate appropriate filename
    if "json" in task_lower:
        return "output.json"
    elif "config" in task_lower or "yaml" in task_lower:
        return "config.yaml"
    elif "markdown" in task_lower or "md" in task_lower:
        return "output.md"
    elif "python" in task_lower or ".py" in task_lower:
        return "script.py"
    elif "javascript" in task_lower or ".js" in task_lower:
        return "script.js"
    elif "readme" in task_lower:
        return "README.md"
    elif "test" in task_lower:
        return "test_output.txt"

    return None
```

### 4.2 Atualizar Imports

**Localização**: Topo do arquivo `agents/base_agent.py`

**ANTES**:
```python
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Optional, Dict, Any
from claude_agent_sdk import query, ClaudeAgentOptions
from config.sdk_config import create_sdk_options
from utils.logger import setup_logger
```

**DEPOIS**:
```python
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Optional, Dict, Any, Tuple
from claude_agent_sdk import query, ClaudeAgentOptions
from config.sdk_config import create_sdk_options
from utils.logger import setup_logger
```

---

## 📝 Passo 5: Atualizar Sistema Principal

### 5.1 Modificar AgentClickSystem

**Arquivo**: `core/system.py` (MODIFICAR)

**Localização**: Linha 28-30

**Adicionar import**:
```python
from core.output_handler import OutputHandler
```

**Localização**: Linha 44-48 (no `__init__`)

**ANTES**:
```python
# Initialize components
self.selection_manager = SelectionManager()
self.click_processor = ClickProcessor()
self.agent_registry = AgentRegistry()
self.config_manager = AgentConfigManager()
```

**DEPOIS**:
```python
# Initialize components
self.selection_manager = SelectionManager()
self.click_processor = ClickProcessor()
self.agent_registry = AgentRegistry()
self.config_manager = AgentConfigManager()
self.output_handler = OutputHandler(self.selection_manager)  # NOVO
```

**Localização**: Linha 71-103 (método `_on_pause_pressed`)

**ANTES**:
```python
def _on_pause_pressed(self) -> None:
    """Handle Pause key - activate current agent (no popup)."""
    current_agent = self.agent_registry.get_current_agent()
    if not current_agent:
        logger.warning("No agents available")
        return

    logger.info(f"Activating agent: {current_agent.metadata.name}")

    # Get selected text
    selected_text = self.selection_manager.get_selected_text()
    if not selected_text:
        logger.warning("No text selected")
        # Optionally show a brief notification in mini popup
        return

    # Get agent configuration
    agent_name = current_agent.metadata.name
    context_folder = self.config_manager.get_context_folder(agent_name)
    focus_file = self.config_manager.get_focus_file(agent_name)

    logger.info(f"Processing with {current_agent.metadata.name}...")
    if context_folder or focus_file:
        logger.info(f"Using config - Folder: {context_folder}, File: {focus_file}")

    # Process with agent (this happens in keyboard thread)
    try:
        result = current_agent.process(selected_text, context_folder, focus_file)
        self._handle_result(result, current_agent)
    except Exception as e:
        error_msg = f"Error processing: {str(e)}"
        logger.error(error_msg)
```

**DEPOIS**:
```python
def _on_pause_pressed(self) -> None:
    """Handle Pause key - activate current agent (no popup)."""
    current_agent = self.agent_registry.get_current_agent()
    if not current_agent:
        logger.warning("No agents available")
        return

    logger.info(f"Activating agent: {current_agent.metadata.name}")

    # Get selected text
    selected_text = self.selection_manager.get_selected_text()
    if not selected_text:
        logger.warning("No text selected")
        # Optionally show a brief notification in mini popup
        return

    # Get agent configuration
    agent_name = current_agent.metadata.name
    context_folder = self.config_manager.get_context_folder(agent_name)
    focus_file = self.config_manager.get_focus_file(agent_name)
    output_mode = self.config_manager.get_output_mode(agent_name)  # NOVO

    logger.info(f"Processing with {current_agent.metadata.name}...")
    logger.info(f"Output mode: {output_mode}")  # NOVO
    if context_folder or focus_file:
        logger.info(f"Using config - Folder: {context_folder}, File: {focus_file}")

    # Process with agent (this happens in keyboard thread)
    try:
        result = current_agent.process(
            selected_text,
            context_folder,
            focus_file,
            output_mode  # NOVO
        )
        self._handle_result(result, current_agent)  # MODIFICADO
    except Exception as e:
        error_msg = f"Error processing: {str(e)}"
        logger.error(error_msg)


def _handle_result(self, result: AgentResult, agent: BaseAgent) -> None:  # ASSINATURA MUDOU
    """Handle agent processing result.

    Args:
        result: AgentResult from agent  # MUDOU
        agent: Agent that processed the request
    """
    from agents.output_modes import OutputMode  # NOVO

    if not result.content:  # MUDOU
        logger.warning("Agent returned empty result")
        if self.large_popup:
            self.signals.log_message_signal.emit("⚠️ No result generated", "warning")
        return

    logger.info("Processing complete...")

    # Handle based on output mode  # NOVO
    success = self.output_handler.handle(result, result.metadata.get('context_folder'))

    if success:
        mode = result.output_mode
        if mode == OutputMode.FILE:
            logger.info("✅ Output saved to file")
            if self.large_popup:
                self.signals.log_message_signal.emit("✅ Saved to file", "success")
        elif mode == OutputMode.INTERACTIVE_EDITOR:
            logger.info("✅ Interactive editor completed")
            if self.large_popup:
                self.signals.log_message_signal.emit("✅ Editor completed", "success")
        else:
            logger.info("✅ Copied to clipboard")
            if self.large_popup:
                self.signals.log_message_signal.emit("✅ Copied to clipboard", "success")
    else:
        logger.error("❌ Failed to handle output")
        if self.large_popup:
            self.signals.log_message_signal.emit("❌ Output failed", "error")
```

---

## 📝 Passo 6: Atualizar Interface

### 6.1 Adicionar Dropdown de Output Mode

**Arquivo**: `ui/popup_window.py` (MODIFICAR)

**Localização**: Linha 8

**Adicionar import**:
```python
from agents.output_modes import OutputMode
```

**Localização**: Linha 205-270 (método `_create_config_tab`)

**APÓS a linha do Focus File (linha 269)**, adicione:

```python
# Output Mode
from PyQt6.QtWidgets import QComboBox  # Adicionar ao import no topo

output_mode_label = QLabel("Output Mode:")
output_mode_label.setStyleSheet("""
    QLabel {
        font-size: 11px;
        font-weight: bold;
        color: #333333;
    }
""")

self.output_mode_combo = QComboBox()
self.output_mode_combo.setStyleSheet("""
    QComboBox {
        padding: 5px;
        border: 1px solid #cccccc;
        border-radius: 3px;
        background-color: white;
    }
    QComboBox::drop-down {
        border: none;
    }
    QComboBox::down-arrow {
        width: 12px;
        height: 12px;
    }
""")

# Add all output modes
for mode in OutputMode:
    self.output_mode_combo.addItem(mode.display_name, mode.value)

config_form.addRow(output_mode_label, self.output_mode_combo)
```

**Localização**: Linha 340-350 (método `_load_current_config`)

**ADICIONAR ao final**:
```python
def _load_current_config(self):
    """Load configuration for current agent."""
    settings = self.config_manager.get_settings(self.current_agent.metadata.name)

    if settings.context_folder:
        self.context_folder_edit.setText(settings.context_folder)

    if settings.focus_file:
        self.focus_file_edit.setText(settings.focus_file)

    # NOVO: Load output mode
    if settings.output_mode:
        mode_index = self.output_mode_combo.findData(settings.output_mode)
        if mode_index >= 0:
            self.output_mode_combo.setCurrentIndex(mode_index)

    self.logger.info(f"Loaded config for {self.current_agent.metadata.name}")
```

**Localização**: Linha 352-368 (método `_save_config`)

**MODIFICAR**:
```python
def _save_config(self):
    """Save configuration for current agent."""
    context_folder = self.context_folder_edit.text().strip() or None
    focus_file = self.focus_file_edit.text().strip() or None
    output_mode = self.output_mode_combo.currentData()  # NOVO

    settings = AgentSettings(
        context_folder=context_folder,
        focus_file=focus_file,
        output_mode=output_mode  # NOVO
    )

    self.config_manager.update_settings(
        self.current_agent.metadata.name,
        settings
    )

    self.log("✅ Configuration saved", "success")
    self.logger.info(f"Saved config for {self.current_agent.metadata.name}")
```

### 6.2 Adicionar Informação sobre Output Modes

**Localização**: Linha 274-290 (info label no config tab)

**MODIFICAR**:
```python
# Info text
info_label = QLabel(
    "💡 These settings configure how the agent processes:\n"
    "• Context Folder: Project folder the agent can work in\n"
    "• Focus File: Specific file that provides project context\n"
    "• Output Mode: How the agent delivers results\n\n"
    "📋 Output Modes:\n"
    "  🤖 Auto: Agent decides best output\n"
    "  📋 Pure: Raw content to clipboard\n"
    "  📋 Rich: Formatted content with reasoning\n"
    "  💾 File: Save to project folder\n"
    "  ✏️ Editor: Preview & edit before output"
)
```

---

## 📝 Passo 7: Testes e Validação

### 7.1 Teste 1 - Modo AUTO

1. Configure um agente com `AUTO`
2. Selecione um texto curto → deve copiar para clipboard
3. Selecione um prompt pedindo para criar um arquivo Python → deve sugerir salvar como arquivo

**Verificar**:
- ✅ Logs mostram "AUTO: Using CLIPBOARD_PURE" ou "AUTO: Using FILE"
- ✅ Clipboard contém o conteúdo
- ✅ Arquivo criado (quando aplicável)

### 7.2 Teste 2 - Modo CLIPBOARD_PURE

1. Configure agente com `CLIPBOARD_PURE`
2. Execute qualquer tarefa
3. Cole o conteúdo

**Verificar**:
- ✅ Conteúdo colado é "puro" (sem formatação extra)
- ✅ Sem reasoning/thoughts no output

### 7.3 Teste 3 - Modo CLIPBOARD_RICH

1. Configure agente com `CLIPBOARD_RICH`
2. Execute tarefa que gere reasoning
3. Cole o conteúdo

**Verificar**:
- ✅ Conteúdo inclui seções separadas
- ✅ Reasoning aparece formatado

### 7.4 Teste 4 - Modo FILE

1. Configure agente com `FILE` e context folder
2. Execute tarefa
3. Verifique pasta do projeto

**Verificar**:
- ✅ Arquivo criado na pasta correta
- ✅ Conteúdo também copiado para clipboard
- ✅ Log mostra caminho do arquivo

### 7.5 Teste 5 - Modo INTERACTIVE_EDITOR

1. Configure agente com `INTERACTIVE_EDITOR`
2. Execute tarefa
3. Edite o conteúdo na janela
4. Confirme

**Verificar**:
- ✅ Janela de editor abre
- ✅ Pode editar conteúdo
- ✅ Pode escolher ação final (clipboard/file)
- ✅ Output reflete edições

---

## 💡 Exemplos de Uso

### Exemplo 1: Diagnostic Agent com AUTO

**Configuração**:
```json
{
  "Diagnostic Agent": {
    "context_folder": "C:/my_project",
    "focus_file": "C:/my_project/app.py",
    "output_mode": "AUTO"
  }
}
```

**Resultado**: Agente decide o melhor output baseado no tamanho do diagnóstico.

### Exemplo 2: Implementation Agent com FILE

**Configuração**:
```json
{
  "Implementation Agent": {
    "context_folder": "C:/my_project",
    "focus_file": null,
    "output_mode": "FILE"
  }
}
```

**Resultado**: Código salvo automaticamente em arquivo.

### Exemplo 3: Prompt Assistant com CLIPBOARD_RICH

**Configuração**:
```json
{
  "Prompt Assistant": {
    "context_folder": null,
    "focus_file": null,
    "output_mode": "CLIPBOARD_RICH"
  }
}
```

**Resultado**: Prompt refinado com contexto e explicações.

---

## 🎉 Conclusão

Após implementar todos os passos, o sistema AgentClick terá:

✅ **5 modos de output configuráveis**
✅ **Decisão automática do agente (AUTO)**
✅ **Editor interativo para preview**
✅ **Suporte a arquivos**
✅ **Clipboard puro e rico**
✅ **Interface atualizada com dropdown**
✅ **Persistência de configuração**

### Próximos Melhorias (Opcional)

- 📊 Adicionar estatísticas de uso por modo
- 🎨 Customizar cores do editor interativo
- 🔍 Adicionar preview de sintaxe no editor
- 📁 Suportar múltiplos arquivos em uma execução
- ⚡ Adicionar templates de filename

---

**Documento criado em**: 2025-12-30
**Versão do AgentClick**: 1.0 → 1.1
**Autor**: Sistema AgentClick

