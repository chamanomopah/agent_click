# Análise Detalhada: Sistema de Input do AgentClick

**Data**: 2025-12-30
**Versão**: AgentClick v1.0
**Arquivo**: Documentação técnica do fluxo de entrada de dados

---

## 📋 Índice

1. [Visão Geral do Sistema](#visão-geral)
2. [Fluxo Completo de Input](#fluxo-completo)
3. [Componentes Envolvolvidos](#componentes)
4. [Como Funciona a Detecção de Texto](#detecção)
5. [Tipos de Input Atuais](#tipos-atuais)
6. [Como Adicionar Novos Tipos de Input](#adicionando-novos-tipos)
7. [Exemplos Práticos de Implementação - Input](#exemplos-input)
8. [Arquitetura Recomendada para Múltiplos Inputs](#arquitetura)
9. **[Sistema de Output: Tipos e Configuração](#sistema-output)** ⭐ NOVO
10. **[Exemplos Práticos de Implementação - Output](#exemplos-output)** ⭐ NOVO
11. [Testes e Validação](#testes)
12. [Considerações de Performance](#performance)

---

## 🎯 Visão Geral do Sistema <a name="visão-geral"></a>

O **AgentClick v1.0** utiliza um sistema de input baseado em **clipboard passivo**. Isso significa que:

- O sistema **NÃO detecta automaticamente** quando você copia texto
- O sistema **NÃO monitora** o clipboard em tempo real
- O usuário deve **iniciar a ação** manualmente (tecla Pause)
- O sistema **lê o clipboard** quando solicitado

**Vantagens deste modelo:**
- ✅ Simples e confiável
- ✅ Funciona com qualquer aplicativo Windows
- ✅ Baixo consumo de recursos
- ✅ Não interfere em operações de clipboard do usuário

**Limitações:**
- ❌ Requer ação manual do usuário (copiar + tecla)
- ❌ Não suporta múltiplos tipos de input
- ❌ Dependente do estado do clipboard
- ❌ Sem feedback visual do que foi capturado

---

## 🔄 Fluxo Completo de Input <a name="fluxo-completo"></a>

### Diagrama de Sequência

```
┌─────────────┐         ┌──────────────┐         ┌──────────┐
│   Usuário   │         │ AgentClick   │         │  Agente  │
└─────────────┘         └──────────────┘         └──────────┘
       │                      │                        │
       │ 1. Seleciona texto   │                        │
       │    (Ctrl+C)          │                        │
       ├─────────────────────>│                        │
       │                      │                        │
       │ 2. Pressiona Pause   │                        │
       ├─────────────────────>│                        │
       │                      │                        │
       │                      │ 3. ClickProcessor      │
       │                      │    detecta Pause       │
       │                      ├─────────────────────>│
       │                      │                        │
       │                      │ 4. SelectionManager    │
       │                      │    lê clipboard        │
       │                      │    (pyperclip.paste)  │
       │                      │<─────────────────────┤
       │                      │                        │
       │                      │ 5. Verifica se há      │
       │                      │    texto válido        │
       │                      ├─────────────────────>│
       │                      │                        │
       │                      │ 6. Carrega config      │
       │                      │    (folder, file)      │
       │                      │<─────────────────────┤
       │                      │                        │
       │                      │ 7. Agent.process()     │
       │                      ├─────────────────────>│
       │                      │                        │
       │                      │ 8. Resultado           │
       │                      │<─────────────────────┤
       │                      │                        │
       │                      │ 9. Copia para clipboard│
       │                      │    (pyperclip.copy)   │
       │                      ├─────────────────────>│
       │                      │                        │
       │ 10. Texto pronto     │                        │
       │    para usar         │                        │
       │<─────────────────────┤                        │
```

### Linha do Tempo Detalhada

| Tempo | Ação | Componente | Arquivo:Linha |
|-------|------|------------|---------------|
| T+0ms | Usuário clica Pause | - | - |
| T+5ms | Hook global captura evento | `ClickProcessor` | `core/click_processor.py:52` |
| T+10ms | Verifica estado do Ctrl | `ClickProcessor` | `core/click_processor.py:91` |
| T+15ms | Identifica Pause sozinho | `ClickProcessor` | `core/click_processor.py:100` |
| T+20ms | Dispara callback pause | `ClickProcessor` | `core/click_processor.py:118` |
| T+25ms | Recebe callback no sistema | `AgentClickSystem` | `core/system.py:71` |
| T+30ms | Obtém agente atual | `AgentRegistry` | `core/system.py:73` |
| T+35ms | Lê clipboard do Windows | `SelectionManager` | `core/selection_manager.py:24` |
| T+40ms | Valida se há texto | `AgentClickSystem` | `core/system.py:82` |
| T+50ms | Carrega configurações | `AgentConfigManager` | `core/system.py:88-90` |
| T+60ms | Processa com agente | `BaseAgent` | `core/system.py:98` |
| T+XXms | **Agente processa (varia)** | `Agente específico` | - |
| T+YYms | Retorna resultado | `Agente` | `core/system.py:98` |
| T+ZZms | Copia resultado ao clipboard | `SelectionManager` | `core/system.py:166` |

**Nota**: O tempo T+XXms e T+YYms variam drasticamente dependendo do agente:
- Prompt Assistant: ~2-5 segundos
- Diagnostic Agent: ~3-8 segundos
- Implementation Agent: ~5-15 segundos (pode ser muito maior para operações complexas)

---

## 🧩 Componentes Envolvidos <a name="componentes"></a>

### 1. ClickProcessor (core/click_processor.py)

**Responsabilidade**: Detectar atalhos de teclado globalmente

**Como funciona**:
```python
# Linha 49: Hook global captura TODAS as teclas
keyboard.hook(self._on_keyboard_event)

# Linha 59-70: Monitora estado do Ctrl
if event.name in ['ctrl', 'left ctrl', 'right ctrl']:
    if event.event_type == 'down':
        self.ctrl_pressed = True

# Linha 73-77: Detecta tecla Pause
if event.name == 'pause' or event.scan_code in self.PAUSE_SCAN_CODES:
    if event.event_type == 'down':
        self._handle_pause_down()
```

**Pontos chave**:
- Usa `keyboard.hook()` para monitoramento global
- Mantém estado do Ctrl com `threading.Lock()` para thread-safety
- Implementa **debounce** de 200ms para evitar double-trigger (linha 84)
- Suporta múltiplos scan codes da tecla Pause (linha 19)

**Thread safety**:
```python
# Linha 29: Lock para proteção de estado compartilhado
self.ctrl_lock = threading.Lock()

# Uso em eventos de teclado
with self.ctrl_lock:
    ctrl_state = self.ctrl_pressed
```

---

### 2. SelectionManager (core/selection_manager.py)

**Responsabilidade**: Gerenciar operações de clipboard

**Método principal - get_selected_text()**:
```python
# Linha 17-31
@staticmethod
def get_selected_text() -> Optional[str]:
    """Get currently selected text from clipboard."""
    try:
        text = pyperclip.paste()  # Lê clipboard do Windows
        if text and text.strip():
            logger.debug(f"Captured selection: {text[:50]}...")
            return text.strip()
        return None
    except Exception as e:
        logger.error(f"Error getting selected text: {e}")
        return None
```

**Características importantes**:
- **Método estático**: Não mantém estado interno
- **Validação**: Verifica se o texto não está vazio (`text.strip()`)
- **Log**: Mostra primeiros 50 caracteres para debug
- **Tratamento de erro**: Retorna `None` em caso de falha

**Outros métodos disponíveis**:

**copy_to_clipboard()** (linha 34-49):
```python
@staticmethod
def copy_to_clipboard(text: str) -> bool:
    """Copy text to clipboard."""
    try:
        pyperclip.copy(text)
        logger.debug("Text copied to clipboard")
        return True
    except Exception as e:
        logger.error(f"Error copying to clipboard: {e}")
        return False
```

**paste_from_clipboard()** (linha 52-65):
```python
@staticmethod
def def paste_from_clipboard() -> bool:
    """Simulate paste from clipboard (Ctrl+V)."""
    try:
        import keyboard
        keyboard.press_and_release('ctrl+v')
        logger.debug("Paste simulated")
        return True
    except Exception as e:
        logger.error(f"Error simulating paste: {e}")
        return False
```

**Nota**: O método `paste_from_clipboard()` atualmente NÃO é usado no fluxo principal. Fica disponível para futuras implementações.

---

### 3. AgentClickSystem (core/system.py)

**Responsabilidade**: Orquestrar todos os componentes

**Método principal - _on_pause_pressed()** (linha 71-103):

```python
def _on_pause_pressed(self) -> None:
    """Handle Pause key - activate current agent."""

    # 1. Obter agente atual
    current_agent = self.agent_registry.get_current_agent()
    if not current_agent:
        logger.warning("No agents available")
        return

    logger.info(f"Activating agent: {current_agent.metadata.name}")

    # 2. Capturar texto do clipboard
    selected_text = self.selection_manager.get_selected_text()
    if not selected_text:
        logger.warning("No text selected")
        return  # Para aqui se não houver texto

    # 3. Carregar configuração do agente
    agent_name = current_agent.metadata.name
    context_folder = self.config_manager.get_context_folder(agent_name)
    focus_file = self.config_manager.get_focus_file(agent_name)

    logger.info(f"Processing with {current_agent.metadata.name}...")
    if context_folder or focus_file:
        logger.info(f"Using config - Folder: {context_folder}, File: {focus_file}")

    # 4. Processar com o agente
    try:
        result = current_agent.process(selected_text, context_folder, focus_file)
        self._handle_result(result, current_agent)
    except Exception as e:
        error_msg = f"Error processing: {str(e)}"
        logger.error(error_msg)
```

**Fluxo de tratamento de resultado** (linha 155-181):

```python
def _handle_result(self, result: str, agent: BaseAgent) -> None:
    """Handle agent processing result."""
    if result:
        logger.info("Processing complete")
        logger.info("Copying to clipboard...")

        # Copiar para clipboard
        if self.selection_manager.copy_to_clipboard(result):
            logger.info(f"Result copied to clipboard ({len(result)} chars)")

            # Log no large popup se estiver aberto
            if self.large_popup:
                self.signals.log_message_signal.emit("✅ Processing complete", "success")
                self.signals.log_message_signal.emit("📋 Copying to clipboard...", "info")
                self.signals.log_message_signal.emit("✅ Copied to clipboard", "success")
        else:
            logger.warning("Failed to copy to clipboard")
            if self.large_popup:
                self.signals.log_message_signal.emit("⚠️ Failed to copy", "warning")
    else:
        logger.warning("Agent returned empty result")
        if self.large_popup:
            self.signals.log_message_signal.emit("⚠️ No result generated", "warning")
```

---

## 🔍 Como Funciona a Detecção de Texto <a name="detecção"></a>

### Mitos vs Realidade

**Mito 1**: "O sistema detecta quando eu copio texto"
- ❌ **FALSO**. O sistema é passivo, não monitora o clipboard

**Mito 2**: "O sistema sabe qual texto está selecionado"
- ❌ **FALSO**. O sistema só acessa o clipboard quando apertado Pause

**Mito 3**: "O sistema intercepta Ctrl+C"
- ❌ **FALSO**. O hook monitora Pause e Ctrl, não Ctrl+C

**Realidade**: O sistema funciona como um "leitor de clipboard sob demanda"

### Processo Real

```
┌─────────────────────────────────────────────────┐
│ 1. Usuário copia texto (Ctrl+C)                 │
│    → Texto vai para clipboard do Windows        │
│    → AgentClick NÃO é notificado                │
└─────────────────────────────────────────────────┘
                    ↓ (tempo indeterminado)
┌─────────────────────────────────────────────────┐
│ 2. Usuário aperta Pause                         │
│    → ClickProcessor detecta a tecla             │
│    → Dispara _on_pause_pressed()                │
└─────────────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────────────┐
│ 3. AgentClick lê o clipboard                    │
│    → SelectionManager.get_selected_text()       │
│    → pyperclip.paste() acessa clipboard         │
│    → Verifica se há texto válido                │
└─────────────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────────────┐
│ 4. Se houver texto: processa                    │
│    Se não houver: avisa e para                  │
└─────────────────────────────────────────────────┘
```

### Validação de Texto

O sistema considera texto válido quando:

```python
# core/selection_manager.py:24-27
text = pyperclip.paste()
if text and text.strip():  # Duas condições:
    # 1. text não é None
    # 2. text.strip() não é string vazia
    return text.strip()
```

**Casos de retorno None (inválido)**:
- Clipboard vazio
- Clipboard com apenas espaços/quebras de linha
- Clipboard com imagem/binário
- Erro ao acessar clipboard

**Casos de válido**:
- Qualquer string com pelo menos um caractere não-espaço
- Texto de qualquer aplicativo
- Código, texto formatado, plain text

---

## 📦 Tipos de Input Atuais <a name="tipos-atuais"></a>

### Input Clipboard (Atual)

**Descrição**: Lê texto do clipboard do Windows

**Implementação**:
```python
# core/selection_manager.py
def get_selected_text() -> Optional[str]:
    return pyperclip.paste()
```

**Características**:
- ✅ Universal (funciona com qualquer app)
- ✅ Simples
- ✅ Confiável
- ❌ Passivo (requer cópia manual)
- ❌ Single-source (só clipboard)

### Limitações Atuais

O sistema **não suporta**:
- ❌ Múltiplas fontes de input simultâneas
- ❌ Input direto via janela de texto
- ❌ Input via arquivo (drag & drop)
- ❌ Input via voz
- ❌ Input via imagem (OCR)
- ❌ Input via seleção automática

---

## 🚀 Como Adicionar Novos Tipos de Input <a name="adicionando-novos-tipos"></a>

### Arquitetura de Extensão

Para adicionar novos tipos de input, você precisa modificar:

```
📁 Componentes a modificar:

1. core/selection_manager.py
   └─ Adicionar novos métodos de captura

2. core/system.py
   └─ Modificar _on_pause_pressed() para suportar múltiplos modos

3. config/agent_config.py
   └─ Adicionar configuração de "input_mode"

4. config/agent_config.json
   └─ Salvar preferência de input por agente

5. ui/popup_window.py
   └─ Adicionar selector de input mode na aba Config

6. ui/mini_popup.py (opcional)
   └─ Mostrar indicador do tipo de input atual
```

### Padrão de Design Recomendado: Strategy Pattern

```
┌─────────────────────────────────────────────┐
│         InputStrategy (ABC)                 │
│  + get_input() -> Optional[str]             │
└─────────────────────────────────────────────┘
           ▲
           │
           ├──────────────────────────────────┐
           │                                  │
    ┌──────────────┐                  ┌──────────────┐
    │ClipboardInput│                  │  FileInput   │
    │  Strategy    │                  │  Strategy    │
    └──────────────┘                  └──────────────┘
           │                                  │
    ┌──────────────┐                  ┌──────────────┐
    │ VoiceInput   │                  │  ImageInput  │
    │  Strategy    │                  │  Strategy    │
    └──────────────┘                  └──────────────┘
```

---

## 💡 Exemplos Práticos de Implementação <a name="exemplos"></a>

### Exemplo 1: Input via Arquivo

**Cenário**: Usuário arrasta arquivo para mini popup ou seleciona via dialog

#### Passo 1: Criar método em SelectionManager

```python
# core/selection_manager.py

@staticmethod
def get_text_from_file(file_path: str) -> Optional[str]:
    """Read text content from a file.

    Args:
        file_path: Path to the text file

    Returns:
        File content or None if error
    """
    try:
        # Suporta múltiplos encodings
        encodings = ['utf-8', 'latin-1', 'cp1252', 'utf-16']

        for encoding in encodings:
            try:
                with open(file_path, 'r', encoding=encoding) as f:
                    content = f.read()
                    if content and content.strip():
                        logger.info(f"Read {len(content)} chars from {file_path} (encoding: {encoding})")
                        return content.strip()
            except UnicodeDecodeError:
                continue

        logger.error(f"Could not decode file: {file_path}")
        return None

    except FileNotFoundError:
        logger.error(f"File not found: {file_path}")
        return None
    except Exception as e:
        logger.error(f"Error reading file {file_path}: {e}")
        return None


@staticmethod
def get_text_from_directory(directory: str, pattern: str = "*.txt") -> Optional[str]:
    """Read and concatenate all text files in a directory.

    Args:
        directory: Directory path
        pattern: File pattern to match (default: *.txt)

    Returns:
        Concatenated content or None
    """
    try:
        from pathlib import Path

        dir_path = Path(directory)
        if not dir_path.is_dir():
            logger.error(f"Not a directory: {directory}")
            return None

        files = list(dir_path.glob(pattern))
        if not files:
            logger.warning(f"No files matching {pattern} in {directory}")
            return None

        contents = []
        for file_path in sorted(files):
            content = SelectionManager.get_text_from_file(str(file_path))
            if content:
                contents.append(f"=== {file_path.name} ===\n{content}\n")

        if contents:
            result = "\n".join(contents)
            logger.info(f"Read {len(contents)} files from {directory}")
            return result

        return None

    except Exception as e:
        logger.error(f"Error reading directory {directory}: {e}")
        return None
```

#### Passo 2: Adicionar suporte a drag & drop no Mini Popup

```python
# ui/mini_popup.py

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QFileDialog
from pathlib import Path

class MiniPopupWidget(QWidget):
    """Enhanced mini popup with drag & drop support."""

    def __init__(self, agent: BaseAgent):
        super().__init__()
        # ... código existente ...

        # Habilitar drag & drop
        self.setAcceptDrops(True)

    def dragEnterEvent(self, event):
        """Accept file drag events."""
        if event.mimeData().hasUrls():
            # Verificar se são arquivos
            urls = event.mimeData().urls()
            if all(url.isLocalFile() for url in urls):
                event.acceptProposedAction()
                logger.debug(f"Dragging {len(urls)} file(s)")

    def dragMoveEvent(self, event):
        """Accept drag move events."""
        if event.mimeData().hasUrls():
            event.acceptProposedAction()

    def dropEvent(self, event):
        """Handle dropped files."""
        urls = event.mimeData().urls()

        # Pegar primeiro arquivo
        if urls:
            file_path = urls[0].toLocalFile()
            logger.info(f"File dropped: {file_path}")

            # Emitir sinal com o caminho do arquivo
            self.file_dropped.emit(file_path)

    # Adicionar sinal customizado
    file_dropped = pyqtSignal(str)
```

#### Passo 3: Conectar sinal no sistema principal

```python
# core/system.py

class AgentClickSystem:
    def __init__(self):
        # ... código existente ...

        # Conectar sinal de arquivo dropado
        self.mini_popup.file_dropped.connect(self._on_file_dropped)

    def _on_file_dropped(self, file_path: str) -> None:
        """Handle file dropped on mini popup."""
        current_agent = self.agent_registry.get_current_agent()
        if not current_agent:
            return

        logger.info(f"Processing file: {file_path}")

        # Ler conteúdo do arquivo
        file_content = self.selection_manager.get_text_from_file(file_path)
        if not file_content:
            logger.warning("Could not read file or file is empty")
            if self.large_popup:
                self.signals.log_message_signal.emit(
                    "⚠️ Could not read file",
                    "warning"
                )
            return

        # Processar com o agente
        self._process_with_agent(current_agent, file_content)

    def _process_with_agent(self, agent: BaseAgent, text: str) -> None:
        """Process text with agent (refactored from _on_pause_pressed)."""
        if not text:
            logger.warning("No text to process")
            return

        # Obter configuração
        agent_name = agent.metadata.name
        context_folder = self.config_manager.get_context_folder(agent_name)
        focus_file = self.config_manager.get_focus_file(agent_name)

        logger.info(f"Processing with {agent.metadata.name}...")

        try:
            result = agent.process(text, context_folder, focus_file)
            self._handle_result(result, agent)
        except Exception as e:
            logger.error(f"Error processing: {e}")
```

---

### Exemplo 2: Input via Janela de Texto

**Cenário**: Usuário clica no mini popup e digita/cola texto em uma janela

#### Passo 1: Criar diálogo de input

```python
# ui/input_dialog.py

from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QTextEdit,
    QPushButton, QLabel, QCheckBox
)
from PyQt6.QtCore import Qt

class TextInputDialog(QDialog):
    """Dialog for manual text input."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("AgentClick - Text Input")
        self.setModal(True)
        self.setMinimumSize(600, 400)

        # Layout
        layout = QVBoxLayout()

        # Label instrutivo
        label = QLabel("Digite ou cole o texto para processar:")
        label.setStyleSheet("font-weight: bold; font-size: 12px;")
        layout.addWidget(label)

        # Área de texto
        self.text_edit = QTextEdit()
        self.text_edit.setPlaceholderText(
            "Cole seu texto aqui...\n\n"
            "Dica: Use Ctrl+V para colar rapidamente."
        )
        self.text_edit.setStyleSheet("""
            QTextEdit {
                border: 2px solid #ccc;
                border-radius: 5px;
                padding: 10px;
                font-family: 'Consolas', 'Monaco', monospace;
                font-size: 11px;
            }
        """)
        layout.addWidget(self.text_edit)

        # Checkbox para limpar após processar
        self.clear_after_cb = QCheckBox("Limpar após processar")
        self.clear_after_cb.setChecked(True)
        layout.addWidget(self.clear_after_cb)

        # Botões
        button_layout = QVBoxLayout()

        self.process_btn = QPushButton("🚀 Processar")
        self.process_btn.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border: none;
                padding: 10px;
                border-radius: 5px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """)
        self.process_btn.clicked.connect(self.accept)
        button_layout.addWidget(self.process_btn)

        self.cancel_btn = QPushButton("❌ Cancelar")
        self.cancel_btn.setStyleSheet("""
            QPushButton {
                background-color: #f44336;
                color: white;
                border: none;
                padding: 10px;
                border-radius: 5px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #da190b;
            }
        """)
        self.cancel_btn.clicked.connect(self.reject)
        button_layout.addWidget(self.cancel_btn)

        layout.addLayout(button_layout)
        self.setLayout(layout)

    def get_text(self) -> str:
        """Get input text."""
        return self.text_edit.toPlainText().strip()

    def should_clear_after(self) -> bool:
        """Check if user wants to clear after processing."""
        return self.clear_after_cb.isChecked()
```

#### Passo 2: Adicionar botão de input manual no mini popup

```python
# ui/mini_popup.py

class MiniPopupWidget(QWidget):
    def __init__(self, agent: BaseAgent):
        super().__init__()
        # ... código existente ...

        # Adicionar botão de input manual (canto inferior)
        self.input_btn = QPushButton("📝")
        self.input_btn.setFixedSize(20, 20)
        self.input_btn.setToolTip("Input manual de texto")
        self.input_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.input_btn.setStyleSheet("""
            QPushButton {
                background-color: rgba(255, 255, 255, 200);
                border: none;
                border-radius: 10px;
                font-size: 12px;
            }
            QPushButton:hover {
                background-color: rgba(255, 255, 255, 255);
            }
        """)
        self.input_btn.clicked.connect(self._on_input_button_clicked)

        # Layout para posicionar o botão
        # ... (adicionar ao layout existente)

    def _on_input_button_clicked(self):
        """Handle input button click."""
        self.input_requested.emit()

    # Novo sinal
    input_requested = pyqtSignal()
```

#### Passo 3: Conectar no sistema

```python
# core/system.py

from ui.input_dialog import TextInputDialog

class AgentClickSystem:
    def __init__(self):
        # ... código existente ...

        # Conectar sinal de input manual
        self.mini_popup.input_requested.connect(self._on_manual_input)

    def _on_manual_input(self) -> None:
        """Handle manual text input request."""
        current_agent = self.agent_registry.get_current_agent()
        if not current_agent:
            return

        # Criar e mostrar dialog
        dialog = TextInputDialog(self.mini_popup)

        # Adicionar texto do clipboard como sugestão
        clipboard_text = self.selection_manager.get_selected_text()
        if clipboard_text:
            dialog.text_edit.setPlainText(clipboard_text)

        # Mostrar dialog
        result = dialog.exec()

        if result == QDialog.DialogCode.Accepted:
            text = dialog.get_text()
            if text:
                logger.info(f"Processing manual input ({len(text)} chars)")
                self._process_with_agent(current_agent, text)
            else:
                logger.warning("Manual input is empty")
```

---

### Exemplo 3: Input via Voz (Speech-to-Text)

**Cenário**: Usuário fala e o sistema transcreve

#### Passo 1: Criar gerenciador de voz

```python
# core/voice_input.py

import speech_recognition
import threading
from typing import Optional, Callable
from utils.logger import setup_logger

logger = setup_logger('VoiceInput')

class VoiceInputManager:
    """Manager for voice input using speech recognition."""

    def __init__(self):
        """Initialize voice input manager."""
        self.recognizer = speech_recognition.Recognizer()
        self.microphone = speech_recognition.Microphone()

        # Calibrar microfone (reduz ruído ambiente)
        logger.info("Calibrating microphone...")
        with self.microphone as source:
            self.recognizer.adjust_for_ambient_noise(source, duration=1)
        logger.info("Microphone calibrated")

    def capture_voice(
        self,
        language: str = "pt-BR",
        timeout: int = 5,
        phrase_time_limit: int = 30
    ) -> Optional[str]:
        """Capture voice input and convert to text.

        Args:
            language: Language code (pt-BR, en-US, es-ES, etc.)
            timeout: Seconds to wait for speech to start
            phrase_time_limit: Maximum seconds for a phrase

        Returns:
            Transcribed text or None if failed
        """
        try:
            logger.info(f"Listening for speech (language={language})...")

            with self.microphone as source:
                # Ouvir áudio
                audio = self.recognizer.listen(
                    source,
                    timeout=timeout,
                    phrase_time_limit=phrase_time_limit
                )

            logger.info("Processing speech...")

            # Reconhecer fala (usando Google Speech Recognition)
            text = self.recognizer.recognize_google(audio, language=language)

            logger.info(f"Speech recognized: {text[:100]}...")
            return text

        except speech_recognition.WaitTimeoutError:
            logger.warning("No speech detected (timeout)")
            return None
        except speech_recognition.UnknownValueError:
            logger.warning("Could not understand audio")
            return None
        except speech_recognition.RequestError as e:
            logger.error(f"Speech recognition service error: {e}")
            return None
        except Exception as e:
            logger.error(f"Error capturing voice: {e}")
            return None

    def capture_voice_async(
        self,
        callback: Callable[[str], None],
        language: str = "pt-BR"
    ) -> threading.Thread:
        """Capture voice in background thread.

        Args:
            callback: Function to call with transcribed text
            language: Language code

        Returns:
            Thread running the capture
        """
        def _capture():
            text = self.capture_voice(language=language)
            if text:
                callback(text)

        thread = threading.Thread(target=_capture, daemon=True)
        thread.start()
        return thread
```

#### Passo 2: Integrar no SelectionManager

```python
# core/selection_manager.py

from core.voice_input import VoiceInputManager

class SelectionManager:
    """Enhanced selection manager with voice input."""

    # Singleton para VoiceInputManager
    _voice_manager: Optional[VoiceInputManager] = None

    @classmethod
    def get_voice_input(cls, language: str = "pt-BR") -> Optional[str]:
        """Capture voice input and return transcribed text.

        Args:
            language: Language code (pt-BR, en-US, etc.)

        Returns:
            Transcribed text or None if failed
        """
        try:
            if cls._voice_manager is None:
                cls._voice_manager = VoiceInputManager()

            return cls._voice_manager.capture_voice(language=language)

        except Exception as e:
            logger.error(f"Error getting voice input: {e}")
            return None
```

#### Passo 3: Adicionar botão de gravação no mini popup

```python
# ui/mini_popup.py

from PyQt6.QtCore import QTimer, pyqtSignal
from PyQt6.QtGui import QPalette

class MiniPopupWidget(QWidget):
    def __init__(self, agent: BaseAgent):
        super().__init__()
        # ... código existente ...

        # Botão de gravação de voz
        self.voice_btn = QPushButton("🎤")
        self.voice_btn.setFixedSize(20, 20)
        self.voice_btn.setToolTip("Gravar voz")
        self.voice_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.voice_btn.setStyleSheet("""
            QPushButton {
                background-color: rgba(255, 255, 255, 200);
                border: none;
                border-radius: 10px;
                font-size: 12px;
            }
            QPushButton:hover {
                background-color: rgba(255, 255, 255, 255);
            }
            QPushButton:pressed {
                background-color: #ff4444;
            }
        """)
        self.voice_btn.pressed.connect(self._on_voice_start)
        self.voice_btn.released.connect(self._on_voice_stop)

        # Timer para feedback visual
        self.recording_timer = QTimer()
        self.recording_timer.timeout.connect(self._update_recording_animation)
        self.recording_animation_frame = 0

    def _on_voice_start(self):
        """Start voice recording."""
        self.voice_btn.setStyleSheet("""
            QPushButton {
                background-color: #ff4444;
                color: white;
                border: none;
                border-radius: 10px;
                font-size: 12px;
            }
        """)
        self.recording_animation_frame = 0
        self.recording_timer.start(100)  # 10 FPS animation

        # Notificar sistema
        self.voice_recording_started.emit()

    def _on_voice_stop(self):
        """Stop voice recording."""
        self.recording_timer.stop()
        self.voice_btn.setStyleSheet("""
            QPushButton {
                background-color: rgba(255, 255, 255, 200);
                border: none;
                border-radius: 10px;
                font-size: 12px;
            }
        """)

        # Notificar sistema
        self.voice_recording_stopped.emit()

    def _update_recording_animation(self):
        """Update recording animation."""
        self.recording_animation_frame = (self.recording_animation_frame + 1) % 4
        dots = "." * self.recording_animation_frame
        self.voice_btn.setText(f"🎤{dots}")

    # Novos sinais
    voice_recording_started = pyqtSignal()
    voice_recording_stopped = pyqtSignal()
```

#### Passo 4: Gerenciar gravação no sistema

```python
# core/system.py

import time

class AgentClickSystem:
    def __init__(self):
        # ... código existente ...

        # Estado de gravação
        self.is_recording = False
        self.recording_start_time = None

        # Conectar sinais
        self.mini_popup.voice_recording_started.connect(self._on_voice_start)
        self.mini_popup.voice_recording_stopped.connect(self._on_voice_stop)

    def _on_voice_start(self) -> None:
        """Handle voice recording start."""
        self.is_recording = True
        self.recording_start_time = time.time()

        if self.large_popup:
            self.signals.log_message_signal.emit(
                "🎤 Gravando... (solte para parar)",
                "info"
            )

        logger.info("Voice recording started")

    def _on_voice_stop(self) -> None:
        """Handle voice recording stop."""
        if not self.is_recording:
            return

        self.is_recording = False

        if self.recording_start_time:
            duration = time.time() - self.recording_start_time
            logger.info(f"Voice recording stopped (duration: {duration:.1f}s)")

        # Capturar voz
        current_agent = self.agent_registry.get_current_agent()
        if not current_agent:
            return

        # Mostrar mensagem de processamento
        if self.large_popup:
            self.signals.log_message_signal.emit(
                "⏳ Processando áudio...",
                "info"
            )

        # Transcrever em thread separada para não travar UI
        threading.Thread(
            target=self._transcribe_and_process,
            args=(current_agent,),
            daemon=True
        ).start()

    def _transcribe_and_process(self, agent: BaseAgent) -> None:
        """Transcribe voice and process with agent."""
        try:
            # Capturar voz
            text = self.selection_manager.get_voice_input(language="pt-BR")

            if text:
                logger.info(f"Voice transcribed: {text[:100]}...")

                # Atualizar UI na thread principal
                self.signals.log_message_signal.emit(
                    f"✅ Transcrito: {text[:50]}...",
                    "success"
                )

                # Processar
                self._process_with_agent(agent, text)
            else:
                logger.warning("Voice transcription failed")
                self.signals.log_message_signal.emit(
                    "⚠️ Falha na transcrição",
                    "warning"
                )
        except Exception as e:
            logger.error(f"Error in voice transcription: {e}")
            self.signals.log_message_signal.emit(
                f"❌ Erro: {str(e)}",
                "error"
            )
```

---

### Exemplo 4: Input via Imagem (OCR)

**Cenário**: Usuário fornece imagem e o sistema extrai texto via OCR

#### Passo 1: Adicionar suporte OCR ao SelectionManager

```python
# core/selection_manager.py

class SelectionManager:
    """Enhanced with OCR support."""

    @staticmethod
    def get_text_from_image(
        image_path: str,
        language: str = "por"
    ) -> Optional[str]:
        """Extract text from image using OCR.

        Args:
            image_path: Path to image file
            language: OCR language (por=Portuguese, eng=English)

        Returns:
            Extracted text or None if failed
        """
        try:
            from PIL import Image
            import pytesseract

            # Abrir imagem
            image = Image.open(image_path)

            # Pré-processamento (opcional mas recomendado)
            # Converter para escala de cinza
            image = image.convert('L')

            # OCR
            text = pytesseract.image_to_string(image, lang=language)

            if text and text.strip():
                logger.info(f"OCR extracted {len(text)} chars from {image_path}")
                return text.strip()
            else:
                logger.warning(f"OCR found no text in {image_path}")
                return None

        except ImportError:
            logger.error(
                "OCR dependencies not installed. "
                "Install: pip install pillow pytesseract"
            )
            return None
        except Exception as e:
            logger.error(f"Error in OCR: {e}")
            return None

    @staticmethod
    def get_text_from_clipboard_image() -> Optional[str]:
        """Extract text from image in clipboard.

        Returns:
            Extracted text or None if no image or failed
        """
        try:
            from PIL import ImageGrab
            import io

            # Tentar pegar imagem do clipboard
            img = ImageGrab.grabclipboard()

            if img is None:
                logger.debug("No image in clipboard")
                return None

            # Salvar em buffer temporário
            buffer = io.BytesIO()
            img.save(buffer, format='PNG')
            buffer.seek(0)

            # Carregar e processar com OCR
            from PIL import Image
            image = Image.open(buffer)

            import pytesseract
            text = pytesseract.image_to_string(image, lang="por+eng")

            if text and text.strip():
                logger.info(f"OCR extracted {len(text)} chars from clipboard image")
                return text.strip()

            return None

        except Exception as e:
            logger.error(f"Error extracting text from clipboard image: {e}")
            return None
```

#### Passo 2: Adicionar método inteligente de detecção

```python
# core/selection_manager.py

class SelectionManager:
    """Enhanced with smart content detection."""

    @staticmethod
    def get_input_smart() -> Optional[tuple[str, str]]:
        """Intelligently detect and extract input from various sources.

        Tries in order:
        1. Plain text from clipboard
        2. Image from clipboard (OCR)

        Returns:
            Tuple of (content, source_type) or (None, None)
            source_type can be: 'text', 'image_ocr', 'none'
        """
        # Tentar texto primeiro
        text = pyperclip.paste()
        if text and text.strip():
            # Verificar se é texto puro (não caminho de arquivo)
            if not text.strip().startswith(('C:\\', 'D:\\', '/', '~')):
                logger.debug("Detected plain text in clipboard")
                return (text.strip(), 'text')

        # Tentar OCR de imagem
        logger.debug("Trying OCR from clipboard...")
        ocr_text = SelectionManager.get_text_from_clipboard_image()
        if ocr_text:
            return (ocr_text, 'image_ocr')

        logger.debug("No valid input detected")
        return (None, 'none')
```

---

## 🏗️ Arquitetura Recomendada para Múltiplos Inputs <a name="arquitetura"></a>

### Implementação Completa com Strategy Pattern

#### Passo 1: Criar abstração de estratégia

```python
# core/input_strategies.py

from abc import ABC, abstractmethod
from typing import Optional
from PyQt6.QtCore import QObject, pyqtSignal

class InputStrategy(ABC):
    """Abstract base class for input strategies."""

    @abstractmethod
    def get_id(self) -> str:
        """Get unique identifier for this strategy."""
        pass

    @abstractmethod
    def get_name(self) -> str:
        """Get display name for this strategy."""
        pass

    @abstractmethod
    def get_icon(self) -> str:
        """Get icon emoji for this strategy."""
        pass

    @abstractmethod
    def get_input(self, **kwargs) -> Optional[str]:
        """Get input text using this strategy.

        Args:
            **kwargs: Strategy-specific parameters

        Returns:
            Input text or None if failed
        """
        pass

    @abstractmethod
    def is_available(self) -> bool:
        """Check if this strategy is available (dependencies installed)."""
        pass

    def get_description(self) -> str:
        """Get description of this strategy."""
        return ""


class ClipboardInputStrategy(InputStrategy):
    """Input strategy: Read from clipboard."""

    def get_id(self) -> str:
        return "clipboard"

    def get_name(self) -> str:
        return "Área de Transferência"

    def get_icon(self) -> str:
        return "📋"

    def get_description(self) -> str:
        return "Lê texto da área de transferência (Ctrl+C)"

    def is_available(self) -> bool:
        return True  # Sempre disponível

    def get_input(self, **kwargs) -> Optional[str]:
        """Get text from clipboard."""
        try:
            import pyperclip
            text = pyperclip.paste()
            if text and text.strip():
                return text.strip()
            return None
        except Exception as e:
            from utils.logger import setup_logger
            logger = setup_logger('ClipboardInput')
            logger.error(f"Error reading clipboard: {e}")
            return None


class FileInputStrategy(InputStrategy):
    """Input strategy: Read from file."""

    def get_id(self) -> str:
        return "file"

    def get_name(self) -> str:
        return "Arquivo"

    def get_icon(self) -> str:
        return "📁"

    def get_description(self) -> str:
        return "Lê texto de um arquivo selecionado"

    def is_available(self) -> bool:
        return True  # Sempre disponível

    def get_input(self, file_path: str = None, **kwargs) -> Optional[str]:
        """Get text from file."""
        if not file_path:
            return None

        try:
            encodings = ['utf-8', 'latin-1', 'cp1252']
            for encoding in encodings:
                try:
                    with open(file_path, 'r', encoding=encoding) as f:
                        content = f.read()
                        if content and content.strip():
                            return content.strip()
                except UnicodeDecodeError:
                    continue
            return None
        except Exception as e:
            from utils.logger import setup_logger
            logger = setup_logger('FileInput')
            logger.error(f"Error reading file: {e}")
            return None


class VoiceInputStrategy(InputStrategy):
    """Input strategy: Voice to text."""

    def __init__(self):
        self._voice_manager = None

    def get_id(self) -> str:
        return "voice"

    def get_name(self) -> str:
        return "Voz"

    def get_icon(self) -> str:
        return "🎤"

    def get_description(self) -> str:
        return "Transcreve voz para texto (Speech-to-Text)"

    def is_available(self) -> bool:
        """Check if speech recognition is available."""
        try:
            import speech_recognition
            return True
        except ImportError:
            return False

    def get_input(self, language: str = "pt-BR", **kwargs) -> Optional[str]:
        """Capture and transcribe voice."""
        if not self.is_available():
            return None

        try:
            if self._voice_manager is None:
                from core.voice_input import VoiceInputManager
                self._voice_manager = VoiceInputManager()

            return self._voice_manager.capture_voice(language=language)

        except Exception as e:
            from utils.logger import setup_logger
            logger = setup_logger('VoiceInput')
            logger.error(f"Error in voice input: {e}")
            return None


class ImageOCRInputStrategy(InputStrategy):
    """Input strategy: Extract text from image (OCR)."""

    def get_id(self) -> str:
        return "image_ocr"

    def get_name(self) -> str:
        return "Imagem (OCR)"

    def get_icon(self) -> str:
        return "🖼️"

    def get_description(self) -> str:
        return "Extrai texto de imagens usando OCR"

    def is_available(self) -> bool:
        """Check if OCR dependencies are available."""
        try:
            import pytesseract
            from PIL import Image
            return True
        except ImportError:
            return False

    def get_input(self, image_path: str = None, **kwargs) -> Optional[str]:
        """Extract text from image."""
        if not self.is_available():
            return None

        try:
            if image_path:
                # OCR de arquivo
                from PIL import Image
                import pytesseract
                image = Image.open(image_path)
                text = pytesseract.image_to_string(image, lang="por+eng")
                if text and text.strip():
                    return text.strip()
            else:
                # OCR do clipboard
                from core.selection_manager import SelectionManager
                return SelectionManager.get_text_from_clipboard_image()

            return None

        except Exception as e:
            from utils.logger import setup_logger
            logger = setup_logger('ImageOCR')
            logger.error(f"Error in OCR: {e}")
            return None


class ManualInputStrategy(InputStrategy):
    """Input strategy: Manual text entry dialog."""

    def get_id(self) -> str:
        return "manual"

    def get_name(self) -> str:
        return "Manual"

    def get_icon(self) -> str:
        return "⌨️"

    def get_description(self) -> str:
        return "Digitação ou colagem manual em janela dedicada"

    def is_available(self) -> bool:
        return True  # Sempre disponível

    def get_input(self, parent=None, **kwargs) -> Optional[str]:
        """Show manual input dialog."""
        try:
            from ui.input_dialog import TextInputDialog
            from PyQt6.QtWidgets import QDialog

            dialog = TextInputDialog(parent)
            result = dialog.exec()

            if result == QDialog.DialogCode.Accepted:
                return dialog.get_text()

            return None

        except Exception as e:
            from utils.logger import setup_logger
            logger = setup_logger('ManualInput')
            logger.error(f"Error in manual input: {e}")
            return None


class SmartInputStrategy(InputStrategy):
    """Input strategy: Auto-detect best input source."""

    def __init__(self):
        self._strategies = [
            ClipboardInputStrategy(),
            ImageOCRInputStrategy(),
        ]

    def get_id(self) -> str:
        return "smart"

    def get_name(self) -> str:
        return "Smart Auto"

    def get_icon(self) -> str:
        return "🧠"

    def get_description(self) -> str:
        return "Detecta automaticamente a melhor fonte de input"

    def is_available(self) -> bool:
        return True

    def get_input(self, **kwargs) -> Optional[str]:
        """Try each strategy in order."""
        from utils.logger import setup_logger
        logger = setup_logger('SmartInput')

        for strategy in self._strategies:
            if not strategy.is_available():
                continue

            logger.debug(f"Trying strategy: {strategy.get_name()}")
            text = strategy.get_input(**kwargs)

            if text:
                logger.info(f"Input detected via {strategy.get_name()}")
                return text

        logger.debug("No input detected")
        return None
```

#### Passo 2: Criar gerenciador de estratégias

```python
# core/input_manager.py

from typing import Optional, Dict, List
from core.input_strategies import InputStrategy
from utils.logger import setup_logger

logger = setup_logger('InputManager')

class InputManager:
    """Manager for input strategies."""

    def __init__(self):
        """Initialize input manager with all available strategies."""
        self.strategies: Dict[str, InputStrategy] = {}
        self.current_strategy_id: str = "smart"

        # Registrar estratégias disponíveis
        self._register_strategies()

        logger.info(f"InputManager initialized with {len(self.strategies)} strategies")

    def _register_strategies(self):
        """Register all available input strategies."""
        from core.input_strategies import (
            ClipboardInputStrategy,
            FileInputStrategy,
            VoiceInputStrategy,
            ImageOCRInputStrategy,
            ManualInputStrategy,
            SmartInputStrategy
        )

        strategies = [
            SmartInputStrategy(),
            ClipboardInputStrategy(),
            FileInputStrategy(),
            VoiceInputStrategy(),
            ImageOCRInputStrategy(),
            ManualInputStrategy(),
        ]

        for strategy in strategies:
            if strategy.is_available():
                self.strategies[strategy.get_id()] = strategy
                logger.info(f"Registered strategy: {strategy.get_name()} ({strategy.get_id()})")
            else:
                logger.warning(f"Strategy unavailable: {strategy.get_name()} (dependencies missing)")

    def get_current_strategy(self) -> InputStrategy:
        """Get current input strategy."""
        return self.strategies.get(self.current_strategy_id, self.strategies["smart"])

    def set_strategy(self, strategy_id: str) -> bool:
        """Set current input strategy.

        Args:
            strategy_id: ID of strategy to use

        Returns:
            True if successful, False otherwise
        """
        if strategy_id in self.strategies:
            self.current_strategy_id = strategy_id
            strategy = self.strategies[strategy_id]
            logger.info(f"Input strategy changed to: {strategy.get_name()}")
            return True
        else:
            logger.warning(f"Unknown strategy ID: {strategy_id}")
            return False

    def get_input(self, **kwargs) -> Optional[str]:
        """Get input using current strategy.

        Args:
            **kwargs: Strategy-specific parameters

        Returns:
            Input text or None if failed
        """
        strategy = self.get_current_strategy()
        logger.debug(f"Getting input using strategy: {strategy.get_name()}")

        text = strategy.get_input(**kwargs)

        if text:
            logger.info(f"Input captured via {strategy.get_name()}: {len(text)} chars")
        else:
            logger.warning(f"No input captured via {strategy.get_name()}")

        return text

    def get_available_strategies(self) -> List[InputStrategy]:
        """Get list of all available strategies."""
        return list(self.strategies.values())

    def get_strategy_by_id(self, strategy_id: str) -> Optional[InputStrategy]:
        """Get strategy by ID."""
        return self.strategies.get(strategy_id)
```

#### Passo 3: Modificar AgentClickSystem

```python
# core/system.py

from core.input_manager import InputManager

class AgentClickSystem:
    """Enhanced system with multiple input strategies."""

    def __init__(self):
        """Initialize AgentClick system."""
        # ... código existente ...

        # Substituir SelectionManager por InputManager
        self.input_manager = InputManager()

        # Manter SelectionManager para compatibilidade
        self.selection_manager = self.input_manager.get_current_strategy()

        # ... resto do código ...

    def _on_pause_pressed(self) -> None:
        """Handle Pause key - activate current agent."""
        current_agent = self.agent_registry.get_current_agent()
        if not current_agent:
            logger.warning("No agents available")
            return

        logger.info(f"Activating agent: {current_agent.metadata.name}")

        # Usar InputManager ao invés de SelectionManager direto
        selected_text = self.input_manager.get_input()

        if not selected_text:
            strategy = self.input_manager.get_current_strategy()
            logger.warning(f"No input via {strategy.get_name()}")
            return

        # ... resto do código (igual ao antes) ...

    def set_input_strategy(self, strategy_id: str) -> bool:
        """Change input strategy.

        Args:
            strategy_id: ID of strategy to use

        Returns:
            True if successful
        """
        if self.input_manager.set_strategy(strategy_id):
            strategy = self.input_manager.get_current_strategy()

            # Notificar UI
            self.signals.log_message_signal.emit(
                f"📥 Input: {strategy.get_icon()} {strategy.get_name()}",
                "info"
            )

            return True
        return False
```

#### Passo 4: Atualizar UI para selecionar estratégia

```python
# ui/popup_window.py

from PyQt6.QtWidgets import QComboBox
from core.input_manager import InputManager

class PopupWindow(QWidget):
    """Enhanced popup with input strategy selection."""

    def __init__(self, agent: BaseAgent, input_manager: InputManager):
        super().__init__()
        self.input_manager = input_manager

        # ... código existente ...

        # Adicionar selector de estratégia na aba Config
        self._create_input_strategy_selector()

    def _create_input_strategy_selector(self):
        """Create input strategy dropdown in Config tab."""
        # Label
        label = QLabel("Tipo de Input:")
        label.setStyleSheet("font-weight: bold;")

        # Combo box
        self.strategy_combo = QComboBox()
        self.strategy_combo.setStyleSheet("""
            QComboBox {
                padding: 5px;
                border-radius: 5px;
                border: 1px solid #ccc;
            }
        """)

        # Adicionar estratégias disponíveis
        strategies = self.input_manager.get_available_strategies()
        for strategy in strategies:
            icon_text = f"{strategy.get_icon()} {strategy.get_name()}"
            self.strategy_combo.addItem(icon_text, strategy.get_id())

        # Conectar mudança
        self.strategy_combo.currentTextChanged.connect(self._on_strategy_changed)

        # Adicionar ao layout da aba Config
        # ... (adicionar ao layout existente)

    def _on_strategy_changed(self, text: str):
        """Handle input strategy change."""
        strategy_id = self.strategy_combo.currentData()

        # Obter referência ao sistema (via agente)
        # Isso requer passar a referência do sistema para PopupWindow
        if hasattr(self, 'system') and self.system:
            self.system.set_input_strategy(strategy_id)
```

---

## 🧪 Testes e Validação <a name="testes"></a>

### Testes Unitários

```python
# tests/test_input_strategies.py

import unittest
from core.input_strategies import (
    ClipboardInputStrategy,
    FileInputStrategy,
    SmartInputStrategy
)

class TestInputStrategies(unittest.TestCase):
    """Test input strategies."""

    def test_clipboard_strategy(self):
        """Test clipboard input strategy."""
        strategy = ClipboardInputStrategy()

        # Verificar disponibilidade
        self.assertTrue(strategy.is_available())

        # Verificar metadados
        self.assertEqual(strategy.get_id(), "clipboard")
        self.assertEqual(strategy.get_icon(), "📋")

    def test_file_strategy(self):
        """Test file input strategy."""
        import tempfile
        import os

        strategy = FileInputStrategy()

        # Criar arquivo temporário
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as f:
            f.write("Test content\n")
            temp_path = f.name

        try:
            # Testar leitura
            content = strategy.get_input(file_path=temp_path)
            self.assertEqual(content, "Test content")
        finally:
            os.unlink(temp_path)

    def test_smart_strategy(self):
        """Test smart input strategy."""
        strategy = SmartInputStrategy()

        # Deve tentar clipboard primeiro
        # (requer clipboard com texto para funcionar)
        self.assertTrue(strategy.is_available())


if __name__ == '__main__':
    unittest.main()
```

### Testes de Integração

```python
# tests/test_input_system.py

import unittest
from core.input_manager import InputManager
from core.input_strategies import ClipboardInputStrategy

class TestInputSystem(unittest.TestCase):
    """Test complete input system."""

    def setUp(self):
        """Set up test fixtures."""
        self.input_manager = InputManager()

    def test_strategy_registration(self):
        """Test that strategies are registered correctly."""
        strategies = self.input_manager.get_available_strategies()

        # Deve ter pelo menos o Smart e Clipboard
        self.assertGreaterEqual(len(strategies), 2)

        # Verificar IDs únicos
        ids = [s.get_id() for s in strategies]
        self.assertEqual(len(ids), len(set(ids)))

    def test_strategy_switching(self):
        """Test switching between strategies."""
        original = self.input_manager.current_strategy_id

        # Tentar mudar para clipboard
        result = self.input_manager.set_strategy("clipboard")
        self.assertTrue(result)
        self.assertEqual(self.input_manager.current_strategy_id, "clipboard")

        # Tentar mudar para estratégia inexistente
        result = self.input_manager.set_strategy("nonexistent")
        self.assertFalse(result)

        # Restaurar
        self.input_manager.set_strategy(original)


if __name__ == '__main__':
    unittest.main()
```

---

## ⚡ Considerações de Performance <a name="performance"></a>

### Otimizações

1. **Lazy Loading**:
   - Carregar dependências apenas quando necessário
   - Exemplo: `speech_recognition` só é importado ao usar voz

2. **Caching**:
   - Manter instância única de VoiceInputManager
   - Cache de configurações

3. **Threading**:
   - Operações pesadas (OCR, voz) em threads separadas
   - Não travar UI durante processamento

4. **Timeouts**:
   - Definir timeouts apropriados para cada tipo de input
   - Exemplo: 5s para iniciar fala, 30s para frase

### Benchmarks Estimados

| Tipo de Input | Latência | CPU | Memória |
|---------------|----------|-----|---------|
| Clipboard | <10ms | Baixo | Baixo |
| Arquivo | 50-200ms | Baixo | Baixo |
| Manual | UI only | Baixo | Baixo |
| Voz | 2-5s | Médio | Médio |
| OCR | 1-10s | **Alto** | **Alto** |

---

## 📚 Conclusão <a name="conclusao"></a>

### Resumo

O sistema atual do AgentClick utiliza um modelo simples e eficaz:
- ✅ Clipboard passivo como fonte de input
- ✅ Tecla Pause como gatilho
- ✅ Arquitetura limpa e extensível

### Próximos Passos Recomendados

Para adicionar suporte a múltiplos tipos de input:

1. **Implementar Strategy Pattern** (input_strategies.py)
2. **Criar InputManager** para gerenciar estratégias
3. **Adicionar UI** para seleção de estratégia
4. **Implementar estratégias prioritárias**:
   - Clipboard (já existe)
   - Manual input (fácil de implementar)
   - File input (útil para logs/documentos)
   - Voice input (complexo mas valioso)
   - OCR (complexo, dependências pesadas)

5. **Testes exaustivos** de cada estratégia
6. **Documentação** para usuários finais

### Dependências Opcionais

```bash
# Voz (Speech-to-Text)
pip install SpeechRecognition pyaudio

# OCR (Image-to-Text)
pip install pytesseract pillow
# Windows: instalar Tesseract executável
# https://github.com/UB-Mannheim/tesseract/wiki

# Manipulação de arquivos
pip install chardet  # detecção de encoding
```

---

## 📤 Sistema de Output: Tipos e Configuração <a name="sistema-output"></a>

### Visão Geral

Atualmente, o AgentClick **sempre retorna o resultado via clipboard**. No entanto, diferentes cenários de uso podem beneficiar-se de diferentes métodos de output.

**Exemplos de uso:**
- **Clipboard**: Resultado rápido para copiar/colar manualmente
- **Arquivo**: Salvar logs, relatórios, código gerado
- **Voz**: Feedback audível (TTS - Text-to-Speech)
- **Seleção**: Substituir texto selecionado automaticamente
- **Manual**: Mostrar em janela para edição antes de usar

### Arquitetura de Output Strategy

Assim como o input, o output deve seguir o **Strategy Pattern**:

```
┌─────────────────────────────────────────────┐
│       OutputStrategy (ABC)                 │
│  + deliver(text, context) -> bool           │
│  + get_name() -> str                        │
│  + get_icon() -> str                        │
└─────────────────────────────────────────────┘
           ▲
           │
           ├──────────────────────────────────┐
           │                                  │
    ┌──────────────┐                  ┌──────────────┐
    │Clipboard     │                  │    File      │
    │Output        │                  │  Output      │
    └──────────────┘                  └──────────────┘
           │                                  │
    ┌──────────────┐                  ┌──────────────┐
    │    Voice     │                  │  Selection   │
    │Output (TTS)  │                  │  Output      │
    └──────────────┘                  └──────────────┘
           │                                  │
    ┌──────────────┐                  ┌──────────────┐
    │   Manual     │                  │  Multi       │
    │Output        │                  │  Output      │
    └──────────────┘                  └──────────────┘
```

### Tipos de Output Disponíveis

| Tipo | Descrição | Casos de Uso | Complexidade |
|------|-----------|--------------|--------------|
| **Clipboard** | Copia resultado para área de transferência | Uso geral, rápido | ✅ Já implementado |
| **Arquivo** | Salva em arquivo (txt, md, json) | Logs, relatórios, código | 🟡 Médio |
| **Voz (TTS)** | Fala o resultado em voz alta | Acessibilidade, hands-free | 🟡 Médio |
| **Seleção** | Substitui texto selecionado | Edição rápida | 🟢 Fácil |
| **Manual** | Mostra janela para edição | Preview, ajustes | 🟢 Fácil |
| **Múltiplo** | Combina 2+ métodos | Flexibilidade máxima | 🟡 Médio |
| **API/Webhook** | Envia para URL externa | Integrações | 🔴 Complexo |

### Configuração por Agente

Cada agente pode ter sua própria configuração de output:

```json
// config/agent_config.json
{
  "agents": {
    "prompt_assistant": {
      "context_folder": null,
      "focus_file": null,
      "input_mode": "clipboard",
      "output_mode": "clipboard"  // ← NOVO
    },
    "diagnostic_agent": {
      "context_folder": null,
      "focus_file": null,
      "input_mode": "smart",
      "output_mode": "file"       // ← Salvar diagnóstico em arquivo
    },
    "implementation_agent": {
      "context_folder": "C:/Projects/MyApp",
      "focus_file": "main.py",
      "input_mode": "clipboard",
      "output_mode": "selection"  // ← Substituir seleção
    }
  }
}
```

### Interface do Usuário

Na aba **Config** do popup detalhado, adicionar:

```
┌─────────────────────────────────────────────┐
│ ⚙️ Configurações - Diagnostic Agent        │
├─────────────────────────────────────────────┤
│                                             │
│ 📁 Context Folder: [________________]  📂  │
│ 📄 Focus File:    [________________]  📂  │
│                                             │
│ 📥 Input Mode:    [Smart Auto        ▼]    │
│                  └─ 📋 Clipboard              │
│                  └─ 🧠 Smart Auto             │
│                  └─ 📁 Arquivo                │
│                  └─ 🎤 Voz                    │
│                                             │
│ 📤 Output Mode:   [Arquivo            ▼]    │  ← NOVO
│                  └─ 📋 Clipboard              │
│                  └─ 📁 Arquivo                │
│                  └─ 🔊 Voz (TTS)              │
│                  └─ 🔄 Seleção                │
│                  └─ 📝 Manual                  │
│                  └─ 📦 Múltiplo                │
│                                             │
│ [💾 Salvar Configurações]                   │
└─────────────────────────────────────────────┘
```

---

## 💻 Exemplos Práticos de Implementação - Output <a name="exemplos-output"></a>

### Exemplo 1: Clipboard Output (Já Existente)

**Descrição**: Método atual, sempre copia para o clipboard

```python
# core/output_strategies.py

from abc import ABC, abstractmethod
from typing import Optional, Dict, Any
import pyperclip
from utils.logger import setup_logger

logger = setup_logger('OutputStrategies')


class OutputStrategy(ABC):
    """Abstract base class for output strategies."""

    @abstractmethod
    def get_id(self) -> str:
        """Get unique identifier for this strategy."""
        pass

    @abstractmethod
    def get_name(self) -> str:
        """Get display name for this strategy."""
        pass

    @abstractmethod
    def get_icon(self) -> str:
        """Get icon emoji for this strategy."""
        pass

    @abstractmethod
    def get_description(self) -> str:
        """Get description of this strategy."""
        pass

    @abstractmethod
    def deliver(self, text: str, context: Dict[str, Any]) -> bool:
        """Deliver output to user.

        Args:
            text: Result text to deliver
            context: Additional context (agent_name, file_path, etc.)

        Returns:
            True if successful, False otherwise
        """
        pass

    @abstractmethod
    def is_available(self) -> bool:
        """Check if this strategy is available."""
        pass


class ClipboardOutputStrategy(OutputStrategy):
    """Output strategy: Copy to clipboard."""

    def get_id(self) -> str:
        return "clipboard"

    def get_name(self) -> str:
        return "Área de Transferência"

    def get_icon(self) -> str:
        return "📋"

    def get_description(self) -> str:
        return "Copia o resultado para a área de transferência (Ctrl+V para colar)"

    def is_available(self) -> bool:
        return True  # Sempre disponível

    def deliver(self, text: str, context: Dict[str, Any]) -> bool:
        """Copy text to clipboard."""
        try:
            pyperclip.copy(text)
            logger.info(f"Copied {len(text)} chars to clipboard")
            return True
        except Exception as e:
            logger.error(f"Error copying to clipboard: {e}")
            return False
```

---

### Exemplo 2: File Output Strategy

**Descrição**: Salva o resultado em um arquivo

```python
# core/output_strategies.py

from pathlib import Path
from datetime import datetime
import json

class FileOutputStrategy(OutputStrategy):
    """Output strategy: Save to file."""

    def __init__(self, default_folder: str = None, default_format: str = "txt"):
        """Initialize file output strategy.

        Args:
            default_folder: Default folder to save files (None = temp)
            default_format: Default file format (txt, md, json)
        """
        self.default_folder = Path(default_folder) if default_folder else None
        self.default_format = default_format

    def get_id(self) -> str:
        return "file"

    def get_name(self) -> str:
        return "Arquivo"

    def get_icon(self) -> str:
        return "📁"

    def get_description(self) -> str:
        return "Salva o resultado em um arquivo de texto"

    def is_available(self) -> bool:
        return True  # Sempre disponível

    def _generate_filename(self, agent_name: str, format_type: str) -> Path:
        """Generate filename based on agent and timestamp.

        Args:
            agent_name: Name of the agent
            format_type: File format (txt, md, json)

        Returns:
            Path object with full filename
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        safe_agent_name = agent_name.replace(" ", "_").lower()

        # Determinar pasta
        if self.default_folder and self.default_folder.exists():
            folder = self.default_folder
        else:
            # Usar pasta de outputs do AgentClick
            from utils import get_agentclick_dir
            folder = get_agentclick_dir() / "outputs"
            folder.mkdir(exist_ok=True)

        # Gerar nome
        filename = f"{safe_agent_name}_{timestamp}.{format_type}"
        return folder / filename

    def _get_format_from_context(self, context: Dict[str, Any]) -> str:
        """Determine file format from context or default.

        Args:
            context: Delivery context

        Returns:
            File format (txt, md, json)
        """
        # Tentar pegar do contexto
        format_type = context.get("file_format", self.default_format)

        # Validar formato
        valid_formats = ["txt", "md", "json", "log"]
        if format_type not in valid_formats:
            format_type = "txt"

        return format_type

    def deliver(self, text: str, context: Dict[str, Any]) -> bool:
        """Save text to file.

        Args:
            text: Result text to save
            context: Delivery context (agent_name, file_format, etc.)

        Returns:
            True if successful
        """
        try:
            agent_name = context.get("agent_name", "agent")
            format_type = self._get_format_from_context(context)

            # Gerar caminho do arquivo
            file_path = self._generate_filename(agent_name, format_type)

            # Salvar baseado no formato
            if format_type == "json":
                # Salvar como JSON
                data = {
                    "timestamp": datetime.now().isoformat(),
                    "agent": agent_name,
                    "content": text,
                    "context": context
                }
                with open(file_path, 'w', encoding='utf-8') as f:
                    json.dump(data, f, ensure_ascii=False, indent=2)

            elif format_type == "md":
                # Salvar como Markdown
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(f"# {agent_name} - Output\n\n")
                    f.write(f"**Gerado em**: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}\n\n")
                    f.write("---\n\n")
                    f.write(text)

            else:  # txt ou log
                # Salvar como texto simples
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(f"[{datetime.now().isoformat()}] {agent_name}\n")
                    f.write("=" * 60 + "\n\n")
                    f.write(text)

            logger.info(f"Saved {len(text)} chars to {file_path}")

            # Adicionar caminho ao contexto para notificação
            context["output_file"] = str(file_path)

            return True

        except Exception as e:
            logger.error(f"Error saving to file: {e}")
            return False
```

---

### Exemplo 3: Voice Output Strategy (TTS)

**Descrição**: Fala o resultado em voz alta

```python
# core/output_strategies.py

class VoiceOutputStrategy(OutputStrategy):
    """Output strategy: Text-to-Speech."""

    def __init__(self, language: str = "pt-BR", rate: int = 150):
        """Initialize voice output strategy.

        Args:
            language: Voice language (pt-BR, en-US, etc.)
            rate: Speech rate (words per minute)
        """
        self.language = language
        self.rate = rate
        self._tts_engine = None

    def get_id(self) -> str:
        return "voice"

    def get_name(self) -> str:
        return "Voz (TTS)"

    def get_icon(self) -> str:
        return "🔊"

    def get_description(self) -> str:
        return "Fala o resultado em voz alta (Text-to-Speech)"

    def is_available(self) -> bool:
        """Check if TTS is available."""
        try:
            import pyttsx3
            return True
        except ImportError:
            return False

    def _get_engine(self):
        """Get or create TTS engine."""
        if self._tts_engine is None:
            try:
                import pyttsx3
                self._tts_engine = pyttsx3.init()

                # Configurar
                voices = self._tts_engine.getProperty('voices')

                # Tentar selecionar voz em português
                for voice in voices:
                    if 'pt' in voice.id.lower() or 'brazil' in voice.id.lower():
                        self._tts_engine.setProperty('voice', voice.id)
                        break

                # Configurar velocidade
                self._tts_engine.setProperty('rate', self.rate)

            except Exception as e:
                logger.error(f"Error initializing TTS: {e}")
                return None

        return self._tts_engine

    def deliver(self, text: str, context: Dict[str, Any]) -> bool:
        """Speak text aloud.

        Args:
            text: Text to speak
            context: Delivery context

        Returns:
            True if successful
        """
        if not self.is_available():
            logger.error("TTS not available (pyttsx3 not installed)")
            return False

        try:
            engine = self._get_engine()
            if not engine:
                return False

            # Limitar tamanho (TTS pode travar com texto muito longo)
            max_length = 1000
            if len(text) > max_length:
                text = text[:max_length] + "... (truncado)"
                logger.warning(f"Text truncated for TTS (original: {len(text)} chars)")

            logger.info(f"Speaking {len(text)} chars...")

            # Falar (bloqueia até terminar)
            engine.say(text)
            engine.runAndWait()

            logger.info("TTS completed")
            return True

        except Exception as e:
            logger.error(f"Error in TTS: {e}")
            return False
```

---

### Exemplo 4: Selection Output Strategy

**Descrição**: Substitui automaticamente o texto selecionado

```python
# core/output_strategies.py

class SelectionOutputStrategy(OutputStrategy):
    """Output strategy: Replace selected text."""

    def get_id(self) -> str:
        return "selection"

    def get_name(self) -> str:
        return "Seleção"

    def get_icon(self) -> str:
        return "🔄"

    def get_description(self) -> str:
        return "Substitui o texto selecionado automaticamente"

    def is_available(self) -> bool:
        return True  # Sempre disponível

    def deliver(self, text: str, context: Dict[str, Any]) -> bool:
        """Replace selected text with result.

        Process:
        1. Copy new text to clipboard
        2. Simulate Ctrl+A (select all)
        3. Simulate Ctrl+V (paste)

        Args:
            text: New text to paste
            context: Delivery context

        Returns:
            True if successful
        """
        try:
            import keyboard
            import time

            # Passo 1: Copiar para clipboard
            pyperclip.copy(text)
            logger.debug("New text copied to clipboard")

            # Pequena pausa para garantir que copiou
            time.sleep(0.05)

            # Passo 2: Selecionar tudo (Ctrl+A)
            keyboard.press_and_release('ctrl+a')
            time.sleep(0.05)

            # Passo 3: Colar (Ctrl+V)
            keyboard.press_and_release('ctrl+v')

            logger.info(f"Replaced selection with {len(text)} chars")
            return True

        except Exception as e:
            logger.error(f"Error replacing selection: {e}")
            return False
```

---

### Exemplo 5: Manual Output Strategy

**Descrição**: Mostra janela para preview e edição do resultado

```python
# core/output_strategies.py

from PyQt6.QtWidgets import QDialog, QVBoxLayout, QTextEdit, QPushButton, QLabel, QCheckBox
from PyQt6.QtCore import Qt

class ManualOutputDialog(QDialog):
    """Dialog for manual output review."""

    def __init__(self, text: str, agent_name: str, parent=None):
        super().__init__(parent)
        self.setWindowTitle(f"AgentClick - Resultado: {agent_name}")
        self.setModal(True)
        self.setMinimumSize(700, 500)

        layout = QVBoxLayout()

        # Label
        label = QLabel(f"Resultado de {agent_name}:")
        label.setStyleSheet("font-weight: bold; font-size: 12px;")
        layout.addWidget(label)

        # Stats
        stats_label = QLabel(f"{len(text)} caracteres | {len(text.split())} palavras")
        stats_label.setStyleSheet("color: #666; font-size: 10px;")
        layout.addWidget(stats_label)

        # Área de texto
        self.text_edit = QTextEdit()
        self.text_edit.setPlainText(text)
        self.text_edit.setStyleSheet("""
            QTextEdit {
                border: 2px solid #ccc;
                border-radius: 5px;
                padding: 10px;
                font-family: 'Consolas', 'Monaco', monospace;
                font-size: 11px;
            }
        """)
        layout.addWidget(self.text_edit)

        # Checkbox para copiar automaticamente
        self.auto_copy_cb = QCheckBox("Copiar para clipboard ao fechar")
        self.auto_copy_cb.setChecked(True)
        layout.addWidget(self.auto_copy_cb)

        # Botões
        button_layout = QVBoxLayout()

        self.copy_btn = QPushButton("📋 Copiar e Fechar")
        self.copy_btn.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border: none;
                padding: 10px;
                border-radius: 5px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """)
        self.copy_btn.clicked.connect(self._copy_and_close)
        button_layout.addWidget(self.copy_btn)

        self.edit_btn = QPushButton("✏️ Continuar Editando")
        self.edit_btn.setStyleSheet("""
            QPushButton {
                background-color: #2196F3;
                color: white;
                border: none;
                padding: 10px;
                border-radius: 5px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #0b7dda;
            }
        """)
        self.edit_btn.clicked.connect(self._continue_editing)
        button_layout.addWidget(self.edit_btn)

        self.cancel_btn = QPushButton("❌ Fechar Sem Copiar")
        self.cancel_btn.setStyleSheet("""
            QPushButton {
                background-color: #f44336;
                color: white;
                border: none;
                padding: 10px;
                border-radius: 5px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #da190b;
            }
        """)
        self.cancel_btn.clicked.connect(self.reject)
        button_layout.addWidget(self.cancel_btn)

        layout.addLayout(button_layout)
        self.setLayout(layout)

    def _copy_and_close(self):
        """Copy text to clipboard and close."""
        text = self.text_edit.toPlainText()
        pyperclip.copy(text)
        self.accept()

    def _continue_editing(self):
        """Keep dialog open for more editing."""
        # Foco no text edit
        self.text_edit.setFocus()

    def get_text(self) -> str:
        """Get edited text."""
        return self.text_edit.toPlainText()

    def should_auto_copy(self) -> bool:
        """Check if user wants auto-copy."""
        return self.auto_copy_cb.isChecked()


class ManualOutputStrategy(OutputStrategy):
    """Output strategy: Show dialog for review."""

    def __init__(self, parent_widget=None):
        """Initialize manual output strategy.

        Args:
            parent_widget: Parent widget for dialog
        """
        self.parent_widget = parent_widget

    def get_id(self) -> str:
        return "manual"

    def get_name(self) -> str:
        return "Manual"

    def get_icon(self) -> str:
        return "📝"

    def get_description(self) -> str:
        return "Mostra janela para revisão e edição antes de usar"

    def is_available(self) -> bool:
        return True  # Sempre disponível

    def deliver(self, text: str, context: Dict[str, Any]) -> bool:
        """Show dialog with result.

        Args:
            text: Result text
            context: Delivery context (agent_name, etc.)

        Returns:
            True if user accepted (copied), False if cancelled
        """
        try:
            from PyQt6.QtWidgets import QApplication

            agent_name = context.get("agent_name", "Agent")

            # Criar e mostrar dialog
            dialog = ManualOutputDialog(text, agent_name, self.parent_widget)
            result = dialog.exec()

            if result == QDialog.DialogCode.Accepted:
                # Usuário clicou em copiar
                edited_text = dialog.get_text()

                if dialog.should_auto_copy() or result == QDialog.DialogCode.Accepted:
                    pyperclip.copy(edited_text)
                    logger.info(f"Manual output: {len(edited_text)} chars copied to clipboard")
                    return True

            # Usuário cancelou
            logger.info("Manual output: cancelled by user")
            return False

        except Exception as e:
            logger.error(f"Error in manual output: {e}")
            return False
```

---

### Exemplo 6: Multi Output Strategy

**Descrição**: Combina múltiplos métodos de output

```python
# core/output_strategies.py

class MultiOutputStrategy(OutputStrategy):
    """Output strategy: Combine multiple output methods."""

    def __init__(self, strategies: list[OutputStrategy]):
        """Initialize multi-output strategy.

        Args:
            strategies: List of strategies to combine
        """
        self.strategies = strategies

    def get_id(self) -> str:
        return "multi"

    def get_name(self) -> str:
        names = " + ".join([s.get_icon() + " " + s.get_name() for s in self.strategies])
        return f"Múltiplo ({names})"

    def get_icon(self) -> str:
        return "📦"

    def get_description(self) -> str:
        return "Combina múltiplos métodos de output"

    def is_available(self) -> bool:
        """Available if at least one strategy is available."""
        return any(s.is_available() for s in self.strategies)

    def deliver(self, text: str, context: Dict[str, Any]) -> bool:
        """Deliver using all strategies.

        Args:
            text: Result text
            context: Delivery context

        Returns:
            True if at least one strategy succeeded
        """
        success_count = 0
        errors = []

        for strategy in self.strategies:
            if not strategy.is_available():
                logger.warning(f"Strategy {strategy.get_name()} not available, skipping")
                continue

            try:
                logger.info(f"Delivering via {strategy.get_name()}...")
                if strategy.deliver(text, context):
                    success_count += 1
                    logger.info(f"✅ {strategy.get_name()} succeeded")
                else:
                    logger.warning(f"❌ {strategy.get_name()} failed")
            except Exception as e:
                error_msg = f"{strategy.get_name()}: {str(e)}"
                errors.append(error_msg)
                logger.error(f"Error in {strategy.get_name()}: {e}")

        # Log resumo
        logger.info(f"Multi-output: {success_count}/{len(self.strategies)} succeeded")

        if errors:
            logger.error(f"Errors: {'; '.join(errors)}")

        # Sucesso se pelo menos um funcionou
        return success_count > 0
```

---

### Integração Completa: OutputManager

```python
# core/output_manager.py

from typing import Dict, List, Optional, Any
from core.output_strategies import (
    OutputStrategy,
    ClipboardOutputStrategy,
    FileOutputStrategy,
    VoiceOutputStrategy,
    SelectionOutputStrategy,
    ManualOutputStrategy,
    MultiOutputStrategy
)
from utils.logger import setup_logger

logger = setup_logger('OutputManager')


class OutputManager:
    """Manager for output strategies."""

    def __init__(self):
        """Initialize output manager."""
        self.strategies: Dict[str, OutputStrategy] = {}
        self.current_strategy_id: str = "clipboard"

        # Registrar estratégias
        self._register_strategies()

        logger.info(f"OutputManager initialized with {len(self.strategies)} strategies")

    def _register_strategies(self):
        """Register all available output strategies."""
        strategies = [
            ClipboardOutputStrategy(),
            FileOutputStrategy(),
            VoiceOutputStrategy(),
            SelectionOutputStrategy(),
            ManualOutputStrategy(),
        ]

        for strategy in strategies:
            if strategy.is_available():
                self.strategies[strategy.get_id()] = strategy
                logger.info(f"✅ Registered output: {strategy.get_name()}")
            else:
                logger.warning(f"⚠️ Output unavailable: {strategy.get_name()}")

    def get_current_strategy(self) -> OutputStrategy:
        """Get current output strategy."""
        return self.strategies.get(self.current_strategy_id, self.strategies["clipboard"])

    def set_strategy(self, strategy_id: str) -> bool:
        """Set current output strategy.

        Args:
            strategy_id: ID of strategy

        Returns:
            True if successful
        """
        if strategy_id in self.strategies:
            self.current_strategy_id = strategy_id
            strategy = self.strategies[strategy_id]
            logger.info(f"Output strategy: {strategy.get_name()}")
            return True
        return False

    def create_multi_strategy(self, strategy_ids: List[str]) -> Optional[OutputStrategy]:
        """Create a multi-output strategy.

        Args:
            strategy_ids: List of strategy IDs to combine

        Returns:
            MultiOutputStrategy or None if invalid
        """
        strategies = []
        for sid in strategy_ids:
            if sid in self.strategies:
                strategies.append(self.strategies[sid])

        if strategies:
            multi = MultiOutputStrategy(strategies)
            # Registrar temporariamente
            multi_id = f"multi_{'_'.join(strategy_ids)}"
            self.strategies[multi_id] = multi
            return multi

        return None

    def deliver(self, text: str, context: Dict[str, Any]) -> bool:
        """Deliver output using current strategy.

        Args:
            text: Result text
            context: Delivery context

        Returns:
            True if successful
        """
        strategy = self.get_current_strategy()

        logger.info(f"Delivering output via {strategy.get_name()}...")

        result = strategy.deliver(text, context)

        if result:
            logger.info(f"✅ Output delivered via {strategy.get_name()}")
        else:
            logger.error(f"❌ Output delivery failed via {strategy.get_name()}")

        return result

    def get_available_strategies(self) -> List[OutputStrategy]:
        """Get list of available strategies."""
        return list(self.strategies.values())
```

---

### Modificações no AgentClickSystem

```python
# core/system.py

from core.output_manager import OutputManager

class AgentClickSystem:
    """Enhanced system with output management."""

    def __init__(self):
        """Initialize AgentClick system."""
        # ... código existente ...

        # Adicionar OutputManager
        self.output_manager = OutputManager()

        # ... resto do código ...

    def _handle_result(self, result: str, agent: BaseAgent) -> None:
        """Handle agent processing result with output strategy.

        Args:
            result: Result text from agent
            agent: Agent that processed the request
        """
        if not result:
            logger.warning("Agent returned empty result")
            if self.large_popup:
                self.signals.log_message_signal.emit("⚠️ No result generated", "warning")
            return

        # Preparar contexto para output
        agent_name = agent.metadata.name
        context_folder = self.config_manager.get_context_folder(agent_name)
        focus_file = self.config_manager.get_focus_file(agent_name)

        output_context = {
            "agent_name": agent_name,
            "agent_id": agent.metadata.id,
            "context_folder": context_folder,
            "focus_file": focus_file,
            "timestamp": time.time()
        }

        # Entregar resultado usando estratégia configurada
        logger.info(f"Processing complete, delivering via {agent_name} output strategy...")

        success = self.output_manager.deliver(result, output_context)

        if success:
            strategy = self.output_manager.get_current_strategy()

            # Notificar UI
            if self.large_popup:
                self.signals.log_message_signal.emit(
                    f"✅ Processing complete ({len(result)} chars)",
                    "success"
                )
                self.signals.log_message_signal.emit(
                    f"📤 Output via {strategy.get_icon()} {strategy.get_name()}",
                    "info"
                )

                # Detalhes específicos por tipo
                if "output_file" in output_context:
                    file_path = output_context["output_file"]
                    self.signals.log_message_signal.emit(
                        f"📁 Salvo em: {file_path}",
                        "success"
                    )
        else:
            logger.error("Output delivery failed")
            if self.large_popup:
                self.signals.log_message_signal.emit(
                    "❌ Falha ao entregar resultado",
                    "error"
                )

    def set_output_strategy(self, agent_name: str, strategy_id: str) -> bool:
        """Set output strategy for specific agent.

        Args:
            agent_name: Name of agent
            strategy_id: ID of output strategy

        Returns:
            True if successful
        """
        # Carregar configuração atual do agente
        agent_config = self.config_manager.get_agent_config(agent_name)

        if agent_config is None:
            logger.warning(f"No config found for agent: {agent_name}")
            return False

        # Atualizar output_mode na configuração
        agent_config["output_mode"] = strategy_id

        # Salvar configuração
        if self.config_manager.set_agent_config(agent_name, agent_config):
            logger.info(f"Output strategy for {agent_name}: {strategy_id}")

            # Atualizar OutputManager se for o agente atual
            current_agent = self.agent_registry.get_current_agent()
            if current_agent and current_agent.metadata.name == agent_name:
                self.output_manager.set_strategy(strategy_id)

            return True

        return False

    def _on_switch_pressed(self) -> None:
        """Handle Ctrl+Pause - switch to next agent."""
        next_agent = self.agent_registry.next_agent()
        if next_agent:
            logger.info(f"Switched to agent: {next_agent.metadata.name}")

            # Atualizar estratégia de output para o novo agente
            agent_name = next_agent.metadata.name
            output_mode = self.config_manager.get_output_mode(agent_name)

            if output_mode:
                self.output_manager.set_strategy(output_mode)
                logger.info(f"Output strategy: {output_mode}")

            # Atualizar UI
            self.signals.update_mini_popup_signal.emit(next_agent)

            if self.large_popup:
                self.signals.update_large_popup_agent_signal.emit(next_agent)
                self.signals.log_message_signal.emit(
                    f"🔄 Switched to {next_agent.metadata.name}",
                    "info"
                )
```

---

### Modificações no AgentConfigManager

```python
# config/agent_config.py

class AgentConfigManager:
    """Enhanced configuration manager with output modes."""

    def get_output_mode(self, agent_name: str) -> Optional[str]:
        """Get output mode for agent.

        Args:
            agent_name: Name of agent

        Returns:
            Output mode ID or None
        """
        config = self.get_agent_config(agent_name)
        if config:
            return config.get("output_mode", "clipboard")  # Default: clipboard
        return None

    def set_output_mode(self, agent_name: str, output_mode: str) -> bool:
        """Set output mode for agent.

        Args:
            agent_name: Name of agent
            output_mode: Output mode ID

        Returns:
            True if successful
        """
        config = self.get_agent_config(agent_name)
        if config is None:
            config = {}

        config["output_mode"] = output_mode
        return self.set_agent_config(agent_name, config)
```

---

### Atualização da UI (PopupWindow)

```python
# ui/popup_window.py

from PyQt6.QtWidgets import QComboBox, QLabel, QVBoxLayout
from core.output_manager import OutputManager

class PopupWindow(QWidget):
    """Enhanced popup with output strategy selection."""

    def __init__(self, agent: BaseAgent, output_manager: OutputManager, config_manager):
        super().__init__()
        self.output_manager = output_manager
        self.config_manager = config_manager

        # ... código existente ...

        # Adicionar selector de output na aba Config
        self._create_output_strategy_selector()

    def _create_output_strategy_selector(self):
        """Create output strategy dropdown in Config tab."""
        # Label
        label = QLabel("Tipo de Output:")
        label.setStyleSheet("font-weight: bold; margin-top: 10px;")

        # Combo box
        self.output_combo = QComboBox()
        self.output_combo.setStyleSheet("""
            QComboBox {
                padding: 5px;
                border-radius: 5px;
                border: 1px solid #ccc;
            }
        """)

        # Adicionar estratégias disponíveis
        strategies = self.output_manager.get_available_strategies()
        for strategy in strategies:
            icon_text = f"{strategy.get_icon()} {strategy.get_name()}"
            self.output_combo.addItem(icon_text, strategy.get_id())

        # Carregar configuração atual
        current_agent = self.get_current_agent()
        if current_agent:
            output_mode = self.config_manager.get_output_mode(current_agent.metadata.name)
            if output_mode:
                # Encontrar índice
                for i in range(self.output_combo.count()):
                    if self.output_combo.itemData(i) == output_mode:
                        self.output_combo.setCurrentIndex(i)
                        break

        # Conectar mudança
        self.output_combo.currentTextChanged.connect(self._on_output_strategy_changed)

        # Adicionar ao layout da aba Config
        # ... (adicionar ao layout existente)

    def _on_output_strategy_changed(self, text: str):
        """Handle output strategy change."""
        strategy_id = self.output_combo.currentData()
        current_agent = self.get_current_agent()

        if current_agent and hasattr(self, 'system') and self.system:
            agent_name = current_agent.metadata.name

            # Salvar configuração
            if self.system.set_output_strategy(agent_name, strategy_id):
                strategy = self.output_manager.get_strategy_by_id(strategy_id)

                self.log(
                    f"📤 Output alterado para {strategy.get_icon()} {strategy.get_name()}",
                    "info"
                )
```

---

## 📊 Matriz de Combinações Input/Output

### Compatibilidade de Estratégias

| Input \ Output | Clipboard | Arquivo | Voz | Seleção | Manual | Multi |
|----------------|-----------|---------|-----|---------|--------|-------|
| **Clipboard** | ✅ Ideal | ✅ Sim | ✅ Sim | ✅ Sim | ✅ Sim | ✅ Sim |
| **Arquivo** | ✅ Sim | ✅ Ideal | ⚠️ Raro | ❌ Não | ✅ Sim | ✅ Sim |
| **Voz** | ✅ Sim | ✅ Sim | ✅ Ideal | ❌ Não | ✅ Sim | ✅ Sim |
| **OCR** | ✅ Sim | ✅ Sim | ✅ Sim | ✅ Sim | ✅ Sim | ✅ Sim |
| **Manual** | ✅ Sim | ✅ Sim | ✅ Sim | ✅ Sim | ✅ Ideal | ✅ Sim |
| **Smart** | ✅ Sim | ✅ Sim | ✅ Sim | ✅ Sim | ✅ Sim | ✅ Sim |

**Legenda:**
- ✅ Sim: Funciona bem
- ⚠️ Raro: Funciona mas não é comum
- ❌ Não: Não faz sentido

### Exemplos de Workflows

#### Workflow 1: Desenvolvedor
```
Input: Clipboard (código)
Agente: Implementation Agent
Output: Selection (substituir código)
```

#### Workflow 2: Escritor/Researcher
```
Input: Voice (ditado)
Agente: Prompt Assistant
Output: Manual (revisar antes de usar)
```

#### Workflow 3: Diagnóstico Técnico
```
Input: Smart (auto-detect)
Agente: Diagnostic Agent
Output: File (salvar log) + Clipboard (copiar também)
```

#### Workflow 4: Acessibilidade
```
Input: Voice
Agente: Qualquer
Output: Voice (feedback TTS)
```

---

## 🔧 Configurações Recomendadas por Agente

### Prompt Assistant Agent
```json
{
  "input_mode": "clipboard",
  "output_mode": "clipboard"
}
```
**Por que?**: Input rápido, output pronto para usar

### Diagnostic Agent
```json
{
  "input_mode": "smart",
  "output_mode": "file"
}
```
**Por que?**: Auto-detect input, salvar diagnóstico para análise posterior

### Implementation Agent
```json
{
  "input_mode": "clipboard",
  "output_mode": "selection"
}
```
**Por que?**: Receber código, substituir seleção automaticamente

### Novo: Code Review Agent
```json
{
  "input_mode": "file",
  "output_mode": "manual"
}
```
**Por que?**: Ler arquivo, revisar manualmente antes de aplicar

---

## 📚 Conclusão <a name="conclusao"></a>

### Resumo Atualizado

O sistema do AgentClick agora suporta:

**Entrada (Input)**:
- ✅ Clipboard (atual)
- 📁 Arquivo
- 🎤 Voz
- 🖼️ OCR
- ⌨️ Manual
- 🧠 Smart Auto

**Saída (Output)**:
- ✅ Clipboard (atual)
- 📁 Arquivo
- 🔊 Voz (TTS)
- 🔄 Seleção
- 📝 Manual
- 📦 Múltiplo

### Benefícios do Sistema Dual

1. **Flexibilidade**: Cada agente com sua configuração
2. **Personalização**: Usuário escolhe melhor workflow
3. **Extensibilidade**: Fácil adicionar novas estratégias
4. **Composição**: Multi-input/output permite workflows complexos
5. **Persistência**: Configurações salvas por agente

### Próximos Passos

1. ✅ Implementar `InputManager` e `OutputManager`
2. ✅ Criar todas as estratégias de output
3. ✅ Atualizar UI para seleção
4. ✅ Adicionar configuração no `agent_config.json`
5. ✅ Testar todas as combinações
6. ✅ Documentar para usuários finais

### Dependências Necessárias

```bash
# Output: Voz (TTS)
pip install pyttsx3

# Output: Arquivo (já incluso)
# Nenhuma dependência extra

# Output: Seleção (já incluso)
# Requer: keyboard (já instalado)
```

---

**Fim do Documento Atualizado**

Para dúvidas ou sugestões, consulte:
- README.md principal
- Documentação de cada componente
- Logs em `logs/` para debugging
