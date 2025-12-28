# Referência de Padrões PyQt6

## Padrões de Estilo (Stylesheet)

### Estrutura Base de Stylesheet

```python
def _get_base_stylesheet(self) -> str:
    """Retorna stylesheet base com suporte a dark/light mode."""
    return """
    /* Dark mode (default) */
    QWidget {
        background-color: #1e1e1e;
        color: #e0e0e0;
        font-family: 'Segoe UI', 'Roboto', 'Helvetica Neue', sans-serif;
        font-size: 11px;
    }

    QPushButton {
        background-color: #0078d4;
        color: #ffffff;
        border: none;
        padding: 8px 16px;
        border-radius: 4px;
        font-weight: 500;
        min-width: 80px;
    }

    QPushButton:hover {
        background-color: #106ebe;
        border: 1px solid #005a9e;
    }

    QPushButton:pressed {
        background-color: #005a9e;
    }

    QPushButton:focus {
        border: 2px solid #60cdff;
        outline: none;
    }

    QPushButton:disabled {
        background-color: #3a3a3a;
        color: #666666;
    }

    QLineEdit, QTextEdit {
        background-color: #2d2d2d;
        color: #e0e0e0;
        border: 1px solid #3a3a3a;
        border-radius: 3px;
        padding: 6px;
        selection-background-color: #0078d4;
    }

    QLineEdit:focus, QTextEdit:focus {
        border: 2px solid #0078d4;
        outline: none;
    }

    QLabel {
        color: #e0e0e0;
    }

    QTabWidget::pane {
        border: 1px solid #3a3a3a;
        background-color: #252525;
        border-radius: 4px;
    }

    QTabBar::tab {
        background-color: #2d2d2d;
        color: #b0b0b0;
        padding: 8px 16px;
        margin-right: 2px;
        border-top-left-radius: 4px;
        border-top-right-radius: 4px;
    }

    QTabBar::tab:selected {
        background-color: #252525;
        color: #ffffff;
        font-weight: 600;
    }

    QTabBar::tab:hover {
        background-color: #3a3a3a;
    }
    """
```

### Light Mode Stylesheet

```python
def _get_light_stylesheet(self) -> str:
    """Retorna stylesheet para light mode."""
    return """
    QWidget {
        background-color: #ffffff;
        color: #1a1a1a;
        font-family: 'Segoe UI', 'Roboto', sans-serif;
        font-size: 11px;
    }

    QPushButton {
        background-color: #0078d4;
        color: #ffffff;
        border: none;
        padding: 8px 16px;
        border-radius: 4px;
    }

    QLineEdit, QTextEdit {
        background-color: #f5f5f5;
        color: #1a1a1a;
        border: 1px solid #cccccc;
        padding: 6px;
    }

    QTabWidget::pane {
        border: 1px solid #e0e0e0;
        background-color: #fafafa;
    }

    QTabBar::tab {
        background-color: #f0f0f0;
        color: #333333;
    }

    QTabBar::tab:selected {
        background-color: #fafafa;
        color: #0078d4;
        font-weight: 600;
    }
    """
```

## Padrões de Acessibilidade

### Configuração Completa de Acessibilidade

```python
def _setup_accessibility(self):
    """Configura acessibilidade completa para widgets principais."""

    # 1. Labels e widgets de input
    self.context_folder_edit.setAccessibleName("Pasta de Contexto")
    self.context_folder_edit.setAccessibleDescription(
        "Selecione a pasta do projeto que o agente usará como contexto. "
        "Isso permite que o agente entenda a estrutura do seu projeto."
    )

    self.focus_file_edit.setAccessibleName("Arquivo Focal")
    self.focus_file_edit.setAccessibleDescription(
        "Selecione um arquivo específico que fornecerá contexto adicional. "
        "Útil para arquivos como README.md, package.json ou config files."
    )

    # 2. Botões com mnemônicos
    self.save_btn.setText("&Salvar")  # ALT+S
    self.save_btn.setAccessibleName("Salvar Configuração")
    self.save_btn.setAccessibleDescription(
        "Salva as configurações do agente atual. "
        "Pressione Ctrl+S para salvar rapidamente."
    )

    self.close_btn.setText("&Fechar")  # ALT+F
    self.close_btn.setAccessibleName("Fechar Janela")
    self.close_btn.setAccessibleDescription(
        "Fecha a janela de configurações. Pressione Esc para fechar."
    )

    # 3. Tabs com atalhos
    self.tab_widget.setTabText(0, "&Atividade")  # ALT+A
    self.tab_widget.setTabText(1, "&Configurações")  # ALT+C

    # 4. Tooltips descritivos
    self.context_browse_btn.setToolTip(
        "Procurar pasta (Ctrl+O)\n"
        "Selecione a pasta do projeto"
    )

    # 5. Focus policy
    for widget in [self.context_folder_edit, self.focus_file_edit,
                   self.save_btn, self.close_btn]:
        widget.setFocusPolicy(Qt.FocusPolicy.StrongFocus)

    # 6. Tab order (ordem lógica de navegação)
    self.setTabOrder(
        self.context_folder_edit,
        self.context_browse_btn
    )
    self.setTabOrder(
        self.context_browse_btn,
        self.focus_file_edit
    )
    self.setTabOrder(
        self.focus_file_edit,
        self.focus_browse_btn
    )
    self.setTabOrder(
        self.focus_browse_btn,
        self.save_btn
    )
    self.setTabOrder(
        self.save_btn,
        self.close_btn
    )
```

### High Contrast Mode

```python
def _apply_high_contrast(self):
    """Aplica tema high contrast para acessibilidade."""
    self.setStyleSheet("""
        QWidget {
            background-color: #000000;
            color: #ffffff;
        }

        QPushButton {
            background-color: #ffffff;
            color: #000000;
            border: 2px solid #ffffff;
            font-weight: bold;
        }

        QPushButton:hover {
            background-color: #ffff00;
            color: #000000;
        }

        QPushButton:focus {
            border: 3px solid #ffff00;
        }

        QLineEdit {
            background-color: #000000;
            color: #ffffff;
            border: 2px solid #ffffff;
        }

        QLineEdit:focus {
            border: 3px solid #ffff00;
    """)
```

## Padrões de Responsividade

### Size Policies

```python
def _setup_size_policies(self):
    """Configura size policies para layouts responsivos."""

    from PyQt6.QtWidgets import QSizePolicy

    # Expanding widgets (ocupam espaço disponível)
    for widget in [self.log_text, self.tab_widget]:
        widget.setSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Expanding
        )

    # Fixed widgets (tamanho fixo)
    for widget in [self.agent_label]:
        widget.setSizePolicy(
            QSizePolicy.Policy.Fixed,
            QSizePolicy.Policy.Fixed
        )

    # Minimum widgets (tamanho mínimo, podem crescer)
    for widget in [self.desc_label]:
        widget.setSizePolicy(
            QSizePolicy.Policy.Minimum,
            QSizePolicy.Policy.Minimum
        )
```

### Layout Responsivo com Breakpoints

```python
def _setup_responsive_layout(self):
    """Configura layout responsivo baseado em screen size."""

    screen = QApplication.primaryScreen()
    if not screen:
        return

    screen_geometry = screen.availableGeometry()
    screen_width = screen_geometry.width()

    # Breakpoints
    if screen_width < 768:  # Mobile
        self._apply_mobile_layout()
    elif screen_width < 1024:  # Tablet
        self._apply_tablet_layout()
    else:  # Desktop
        self._apply_desktop_layout()

def _apply_mobile_layout(self):
    """Layout compacto para mobile."""
    self.setFixedSize(350, 500)  # Portrait
    self._apply_compact_spacing()

def _apply_tablet_layout(self):
    """Layout para tablet."""
    self.setFixedSize(450, 400)
    self._apply_standard_spacing()

def _apply_desktop_layout(self):
    """Layout padrão desktop."""
    self.setFixedSize(550, 450)
    self._apply_standard_spacing()
```

### DPI Scaling

```python
def _setup_dpi_scaling(self):
    """Configura scaling para diferentes DPIs."""

    # Detectar DPI
    screen = QApplication.primaryScreen()
    dpi = screen.logicalDotsPerInch()

    # Ajustar font sizes baseado em DPI
    base_font_size = 11
    if dpi > 120:  # High DPI (125%, 150%)
        base_font_size = 13
    elif dpi > 144:  # Very high DPI (200%)
        base_font_size = 15

    # Aplicar a toda app
    font = QApplication.font()
    font.setPointSize(base_font_size)
    QApplication.setFont(font)

    # Ou usar stylesheet relativo
    self.setStyleSheet(f"""
        QLabel {{
            font-size: {base_font_size}px;
        }}
        QPushButton {{
            font-size: {base_font_size}px;
            padding: {int(base_font_size * 0.8)}px {int(base_font_size * 1.5)}px;
        }}
    """)
```

## Padrões de Feedback Visual

### Animações Suaves

```python
from PyQt6.QtCore import QPropertyAnimation, QEasingCurve, QParallelAnimationGroup
from PyQt6.QtGui import QCursor

def _animate_hover(self, widget, target_size: int):
    """Animação suave de hover."""
    animation = QPropertyAnimation(widget, b"size")
    animation.setDuration(150)  # ms
    animation.setStartValue(widget.size())
    animation.setEndValue(QtCore.QSize(target_size, target_size))
    animation.setEasingCurve(QEasingCurve.Type.OutCubic)
    animation.start()

def _animate_fade_in(self, widget):
    """Fade in animation."""
    from PyQt6.QtCore import Qt
    from PyQt6.QtWidgets import QGraphicsOpacityEffect

    effect = QGraphicsOpacityEffect(widget)
    widget.setGraphicsEffect(effect)

    animation = QPropertyAnimation(effect, b"opacity")
    animation.setDuration(300)
    animation.setStartValue(0.0)
    animation.setEndValue(1.0)
    animation.setEasingCurve(QEasingCurve.Type.InOutQuad)
    animation.start()
```

### Transições de Estado

```python
def _setup_state_transitions(self):
    """Configura transições suaves entre estados."""

    # Botão com transições
    self.save_btn.setStyleSheet("""
        QPushButton {
            background-color: #0078d4;
            color: #ffffff;
            border: none;
            padding: 8px 16px;
            border-radius: 4px;
        }

        QPushButton:hover {
            background-color: #106ebe;
        }

        QPushButton:hover {
            border: 1px solid #005a9e;
        }
    """)

    # Usar QStateMachine para transições complexas
    from PyQt6.QtStateMachine import QStateMachine, QState

    machine = QStateMachine(self)

    # Estado normal
    normal_state = QState(machine)
    normal_state.assignProperty(self.save_btn, "enabled", True)

    # Estado salvando (loading)
    saving_state = QState(machine)
    saving_state.assignProperty(self.save_btn, "enabled", False)
    saving_state.assignProperty(self.save_btn, "text", "Salvando...")

    # Transições
    normal_state.addTransition(
        self.save_btn.clicked,
        saving_state
    )

    saving_state.addTransition(
        self._save_finished,
        normal_state
    )

    machine.setInitialState(normal_state)
    machine.start()
```

### Indicadores de Progresso

```python
def _show_progress_indicator(self, message: str):
    """Mostra indicador de progresso durante operações."""

    from PyQt6.QtWidgets import QProgressBar

    # Criar ou atualizar progress bar
    if not hasattr(self, 'progress_bar'):
        self.progress_bar = QProgressBar()
        self.layout().addWidget(self.progress_bar)

    self.progress_bar.setRange(0, 0)  # Indeterminate progress
    self.progress_bar.setToolTip(message)
    self.progress_bar.setVisible(True)

    # Feedback visual
    self.log(f"⏳ {message}", "info")

def _hide_progress_indicator(self):
    """Esconde indicador de progresso."""
    if hasattr(self, 'progress_bar'):
        self.progress_bar.setVisible(False)
```

## Padrões de Atalhos de Teclado

### Atalhos Globais

```python
def _setup_global_shortcuts(self):
    """Configura atalhos de teclado globais."""

    from PyQt6.QtGui import QShortcut, QKeySequence

    # Ctrl+S: Salvar
    save_shortcut = QShortcut(QKeySequence("Ctrl+S"), self)
    save_shortcut.activated.connect(self._save_config)

    # Ctrl+W ou Esc: Fechar
    close_shortcut = QShortcut(QKeySequence("Ctrl+W"), self)
    close_shortcut.activated.connect(self.close)

    escape_shortcut = QShortcut(QKeySequence(Qt.Key.Key_Escape), self)
    escape_shortcut.activated.connect(self.close)

    # Ctrl+Tab: Próxima tab
    next_tab_shortcut = QShortcut(QKeySequence("Ctrl+Tab"), self)
    next_tab_shortcut.activated.connect(
        lambda: self.tab_widget.setCurrentIndex(
            (self.tab_widget.currentIndex() + 1) % self.tab_widget.count()
        )
    )

    # Ctrl+Shift+Tab: Tab anterior
    prev_tab_shortcut = QShortcut(QKeySequence("Ctrl+Shift+Tab"), self)
    prev_tab_shortcut.activated.connect(
        lambda: self.tab_widget.setCurrentIndex(
            (self.tab_widget.currentIndex() - 1) % self.tab_widget.count()
        )
    )

    # F1: Ajuda
    help_shortcut = QShortcut(QKeySequence("F1"), self)
    help_shortcut.activated.connect(self._show_help)
```

### Mnemônicos por Widget

```python
def _setup_mnemonics(self):
    """Configura mnemônicos (ALT+letra) para widgets."""

    # Labels com buddy widgets
    context_label = QLabel("Conte&xto Folder:")
    context_label.setBuddy(self.context_folder_edit)

    focus_label = QLabel("Ar&quivo Focal:")
    focus_label.setBuddy(self.focus_file_edit)

    # Botões
    self.save_btn.setText("&Salvar")  # ALT+S
    self.close_btn.setText("&Fechar")  # ALT+F (ou ALT+C de Close)

    # Tabs
    self.tab_widget.setTabText(0, "&Atividade")  # ALT+A
    self.tab_widget.setTabText(1, "Con&figuração")  # ALT+F

    # Mostrar dica de mnemônicos na UI
    self._show_mnemonic_hint()
```

## Padrões de Tema

### Toggle Dark/Light Mode

```python
def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self.dark_mode = True  # Default
    self._load_theme_preference()
    self._apply_theme()

def _load_theme_preference(self):
    """Carrega preferência de tema do arquivo config."""
    import json
    try:
        with open('config/theme.json', 'r') as f:
            config = json.load(f)
            self.dark_mode = config.get('dark_mode', True)
    except:
        self.dark_mode = True  # Default

def _apply_theme(self):
    """Aplica tema baseado na preferência."""
    if self.dark_mode:
        self.setStyleSheet(self._get_dark_stylesheet())
    else:
        self.setStyleSheet(self._get_light_stylesheet())

def toggle_theme(self):
    """Alterna entre dark e light mode."""
    self.dark_mode = not self.dark_mode
    self._apply_theme()
    self._save_theme_preference()

def _save_theme_preference(self):
    """Salva preferência de tema."""
    import json
    config = {'dark_mode': self.dark_mode}
    with open('config/theme.json', 'w') as f:
        json.dump(config, f)
```

## Boas Práticas Gerais

### 1. Sempre fornecer feedback visual
```python
# Ruim
button.clicked.connect(do_something)

# Bom
button.clicked.connect(lambda: self._with_feedback(do_something))

def _with_feedback(self, func):
    """Executa função com feedback visual."""
    self._show_loading()
    result = func()
    self._hide_loading()
    self._show_success("Operação concluída!")
    return result
```

### 2. Manter contraste adequado
```python
# Ruim - contraste baixo
label.setStyleSheet("color: #888888; background: #aaaaaa;")

# Bom - contraste alto
label.setStyleSheet("color: #1a1a1a; background: #f5f5f5;")
```

### 3. Usar unidades relativas quando possível
```python
# Ruim - hardcoded pixels
widget.setFixedHeight(100)

# Bom - baseado em font size
widget.setFixedHeight(font_metrics.height() * 3)
```

### 4. Testar em diferentes DPIs
```python
# Detectar DPI e ajustar
dpi = screen.logicalDotsPerInch()
scale_factor = dpi / 96.0  # 96 DPI = 100%
```

### 5. Documentar atalhos de teclado
```python
# Criar widget de help
def _show_shortcuts_help(self):
    shortcuts = """
    Atalhos de Teclado:
    -------------------
    Ctrl+S - Salvar configurações
    Ctrl+W - Fechar janela
    Esc - Cancelar/Fechar
    Tab - Próximo campo
    Shift+Tab - Campo anterior
    Ctrl+Tab - Próxima aba
    F1 - Mostrar ajuda
    """
    QMessageBox.information(self, "Atalhos", shortcuts)
```
