# Exemplos Práticos de UX/UI para PyQt6

## Exemplo 1: Transformar Mini Popup com Acessibilidade

### Antes
```python
def _setup_ui(self):
    """Setup mini popup UI."""
    self.setWindowTitle("")
    self.setWindowFlags(
        Qt.WindowType.FramelessWindowHint |
        Qt.WindowType.WindowStaysOnTopHint |
        Qt.WindowType.Tool
    )
    self.setFixedSize(60, 60)
    self._position_window()

    layout = QVBoxLayout()
    layout.setContentsMargins(0, 0, 0, 0)

    self.icon_label = QLabel(self.current_agent.metadata.icon)
    self.icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
    self.icon_label.setStyleSheet("""
        QLabel {
            font-size: 32px;
            background-color: %s;
            border-radius: 30px;
        }
    """ % self.current_agent.metadata.color)
    layout.addWidget(self.icon_label)

    self.setLayout(layout)
    self.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
```

### Depois (Completamente Acessível)
```python
def _setup_ui(self):
    """Setup mini popup UI com acessibilidade completa."""
    # Window properties (mesmo)
    self.setWindowTitle("AgentClick - Mini Popup")
    self.setWindowFlags(
        Qt.WindowType.FramelessWindowHint |
        Qt.WindowType.WindowStaysOnTopHint |
        Qt.WindowType.Tool
    )

    # Responsividade: tamanho baseado em DPI
    screen = QApplication.primaryScreen()
    dpi = screen.logicalDotsPerInch()
    base_size = int(60 * (dpi / 96.0))  # Escala com DPI
    self.setFixedSize(base_size, base_size)

    self._position_window()

    # Layout
    layout = QVBoxLayout()
    layout.setContentsMargins(2, 2, 2, 2)

    # Icon label com acessibilidade
    self.icon_label = QLabel(self.current_agent.metadata.icon)
    self.icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

    # Acessibilidade: nome e descrição
    self.icon_label.setAccessibleName(f"Agente Atual: {self.current_agent.metadata.name}")
    self.icon_label.setAccessibleDescription(
        f"{self.current_agent.metadata.name} - {self.current_agent.metadata.description}. "
        f"Clique para abrir configurações detalhadas. "
        f"Pressione Ctrl+Pause para alternar para o próximo agente."
    )

    # Tooltip informativo
    self.icon_label.setToolTip(
        f"{self.current_agent.metadata.name}\n"
        f"{self.current_agent.metadata.description}\n\n"
        f"Clique para configurações\n"
        f"Ctrl+Pause para alternar"
    )

    # Estilos melhorados com contraste e estados
    self.icon_label.setStyleSheet("""
        QLabel {
            font-size: 32px;
            background-color: %s;
            color: #ffffff;
            border-radius: 30px;
        }
        QLabel:hover {
            border: 2px solid #ffffff;
            background-color: %s;
        }
    """ % (
        self.current_agent.metadata.color,
        self._lighten_color(self.current_agent.metadata.color, 20)
    ))

    layout.addWidget(self.icon_label)
    self.setLayout(layout)

    # Cursor
    self.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

    # Focus policy (para acessibilidade)
    self.setFocusPolicy(Qt.FocusPolicy.TabFocus)

    # Tecla de atalho para abrir (Espaço ou Enter)
    self.icon_label.setFocusPolicy(Qt.FocusPolicy.StrongFocus)

def _lighten_color(self, hex_color: str, percent: int) -> str:
    """Clareia cor em X% para hover state."""
    hex_color = hex_color.lstrip('#')
    r, g, b = int(hex_color[0:2], 16), int(hex_color[2:4], 16), int(hex_color[4:6], 16)

    r = min(255, int(r + (255 - r) * percent / 100))
    g = min(255, int(g + (255 - g) * percent / 100))
    b = min(255, int(b + (255 - b) * percent / 100))

    return f"#{r:02x}{g:02x}{b:02x}"

def keyPressEvent(self, event):
    """Permite abrir com Espaço ou Enter."""
    if event.key() in [Qt.Key.Key_Space, Qt.Key.Key_Return]:
        self.clicked.emit()
    super().keyPressEvent(event)
```

## Exemplo 2: Popup Window com Navegação por Teclado

### Antes
```python
def _create_config_tab(self):
    """Create configuration tab."""
    config_tab = QWidget()
    config_layout = QVBoxLayout()

    config_group = QGroupBox("Agent Configuration")
    config_form = QFormLayout()

    self.context_folder_edit = QLineEdit()
    context_browse_btn = QPushButton("Browse")
    context_browse_btn.clicked.connect(self._browse_context_folder)

    config_form.addRow("Context Folder:", self.context_folder_edit)
    config_form.addRow("", context_browse_btn)

    self.focus_file_edit = QLineEdit()
    focus_browse_btn = QPushButton("Browse")
    focus_browse_btn.clicked.connect(self._browse_focus_file)

    config_form.addRow("Focus File:", self.focus_file_edit)
    config_form.addRow("", focus_browse_btn)

    config_group.setLayout(config_form)
    config_layout.addWidget(config_group)

    save_btn = QPushButton("Save Configuration")
    save_btn.clicked.connect(self._save_config)
    config_layout.addWidget(save_btn)

    config_tab.setLayout(config_layout)
    self.tab_widget.addTab(config_tab, "Config")
```

### Depois (Navegação Completa)
```python
def _create_config_tab(self):
    """Create configuration tab com navegação completa."""
    config_tab = QWidget()
    config_layout = QVBoxLayout()

    # GroupBox com accessible name
    config_group = QGroupBox("Configuração do Agente")
    config_group.setAccessibleDescription(
        "Configure as preferências do agente atual"
    )
    config_form = QFormLayout()

    # Context Folder com label e buddy
    context_label = QLabel("Conte&xto:")
    context_label.setBuddy(self.context_folder_edit)
    context_label.setToolTip(
        "Pasta do projeto que fornece contexto ao agente\n"
        "Use CTRL+O para buscar rapidamente"
    )

    self.context_folder_edit = QLineEdit()
    self.context_folder_edit.setPlaceholderText("C:\\path\\to\\project")
    self.context_folder_edit.setAccessibleName("Pasta de Contexto")
    self.context_folder_edit.setAccessibleDescription(
        "Digite o caminho da pasta ou clique em Procurar"
    )
    self.context_folder_edit.setFocusPolicy(Qt.FocusPolicy.StrongFocus)

    context_browse_btn = QPushButton("&Procurar...")
    context_browse_btn.setShortcut("Ctrl+O")
    context_browse_btn.setToolTip("Procurar pasta (Ctrl+O)")
    context_browse_btn.clicked.connect(self._browse_context_folder)

    # Layout horizontal para input + botão
    context_layout = QHBoxLayout()
    context_layout.addWidget(self.context_folder_edit, stretch=1)
    context_layout.addWidget(context_browse_btn)

    config_form.addRow(context_label, context_layout)

    # Focus File com label e buddy
    focus_label = QLabel("A&rquivo Focal:")
    focus_label.setBuddy(self.focus_file_edit)
    focus_label.setToolTip(
        "Arquivo específico para contexto adicional\n"
        "Ex: README.md, package.json"
    )

    self.focus_file_edit = QLineEdit()
    self.focus_file_edit.setPlaceholderText("C:\\path\\to\\file.ext")
    self.focus_file_edit.setAccessibleName("Arquivo Focal")
    self.focus_file_edit.setAccessibleDescription(
        "Digite o caminho do arquivo ou clique em Procurar"
    )
    self.focus_file_edit.setFocusPolicy(Qt.FocusPolicy.StrongFocus)

    focus_browse_btn = QPushButton("P&rocurar...")
    focus_browse_btn.setToolTip("Procurar arquivo (Ctrl+Shift+O)")
    focus_browse_btn.clicked.connect(self._browse_focus_file)

    # Layout horizontal
    focus_layout = QHBoxLayout()
    focus_layout.addWidget(self.focus_file_edit, stretch=1)
    focus_layout.addWidget(focus_browse_btn)

    config_form.addRow(focus_label, focus_layout)

    config_group.setLayout(config_form)
    config_layout.addWidget(config_group)

    # Info box com dicas
    info_label = QLabel(
        "💡 <b>Dicas de Navegação:</b><br>"
        "• Use <b>Tab</b> para avançar entre campos<br>"
        "• Use <b>Shift+Tab</b> para voltar<br>"
        "• Pressione <b>Ctrl+S</b> para salvar<br>"
        "• Pressione <b>Esc</b> para fechar<br>"
        "• Use <b>Alt+letra</b> para acessar campos (ex: Alt+C para Contexto)"
    )
    info_label.setWordWrap(True)
    info_label.setStyleSheet("""
        QLabel {
            background-color: #fffacd;
            border: 1px solid #ffd700;
            border-radius: 5px;
            padding: 10px;
            color: #333333;
        }
    """)
    config_layout.addWidget(info_label)

    # Save button com shortcut
    save_btn = QPushButton("&Salvar Configuração")
    save_btn.setShortcut("Ctrl+S")
    save_btn.setToolTip("Salvar configurações (Ctrl+S)")
    save_btn.setDefault(True)  # Enter dispara este botão
    save_btn.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
    save_btn.clicked.connect(self._save_config)

    # Close button
    close_btn = QPushButton("&Fechar")
    close_btn.setShortcut("Esc")
    close_btn.setToolTip("Fechar janela (Esc)")
    close_btn.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
    close_btn.clicked.connect(self.close)

    # Botões em linha
    button_layout = QHBoxLayout()
    button_layout.addStretch()
    button_layout.addWidget(save_btn)
    button_layout.addWidget(close_btn)

    config_layout.addLayout(button_layout)
    config_layout.addStretch()

    config_tab.setLayout(config_layout)

    # Tab com mnemônico
    self.tab_widget.addTab(config_tab, "&Configurações")

    # Configurar ordem de Tab
    self._setup_tab_order()

def _setup_tab_order(self):
    """Configura ordem lógica de navegação por Tab."""
    self.setTabOrder(self.context_folder_edit, self.context_browse_btn)
    self.setTabOrder(self.context_browse_btn, self.focus_file_edit)
    self.setTabOrder(self.focus_file_edit, self.focus_browse_btn)
    self.setTabOrder(self.focus_browse_btn, save_btn)
    self.setTabOrder(save_btn, close_btn)
```

## Exemplo 3: Layout Responsivo com Breakpoints

```python
class ResponsivePopupWindow(QWidget):
    """Popup window responsivo com breakpoints."""

    def __init__(self, current_agent: BaseAgent):
        super().__init__()
        self.current_agent = current_agent

        # Detectar screen size
        self.screen_width = self._get_screen_width()
        self.screen_height = self._get_screen_height()

        # Aplicar layout baseado em screen size
        self._setup_responsive_ui()

    def _get_screen_width(self) -> int:
        """Retorna largura da screen."""
        screen = QApplication.primaryScreen()
        if screen:
            return screen.availableGeometry().width()
        return 1920  # Default

    def _get_screen_height(self) -> int:
        """Retorna altura da screen."""
        screen = QApplication.primaryScreen()
        if screen:
            return screen.availableGeometry().height()
        return 1080  # Default

    def _setup_responsive_ui(self):
        """Configura UI responsiva baseado em screen size."""

        # Breakpoints
        if self.screen_width < 768:
            self._apply_mobile_layout()
        elif self.screen_width < 1024:
            self._apply_tablet_layout()
        elif self.screen_width < 1440:
            self._apply_desktop_layout()
        else:
            self._apply_large_desktop_layout()

    def _apply_mobile_layout(self):
        """Layout compacto para mobile (< 768px)."""
        # Janela portrait
        self.setFixedSize(
            int(self.screen_width * 0.95),
            int(self.screen_height * 0.8)
        )

        # Layout vertical compacto
        main_layout = QVBoxLayout()
        main_layout.setSpacing(5)
        main_layout.setContentsMargins(10, 10, 10, 10)

        # Header menor
        self.agent_label.setStyleSheet("font-size: 14px; padding: 5px;")

        # Tabs ocupam todo espaço
        self.tab_widget.setTabPosition(QTabWidget.TabPosition.North)
        self.tab_widget.setTabShape(QTabWidget.TabShape.Rounded)

        # Font sizes menores
        font = self.font()
        font.setPointSize(10)
        self.setFont(font)

        self.setLayout(main_layout)
        self.logger.info("Applied mobile layout")

    def _apply_tablet_layout(self):
        """Layout para tablet (768px - 1024px)."""
        # Janela medium
        self.setFixedSize(
            int(self.screen_width * 0.7),
            int(self.screen_height * 0.7)
        )

        # Layout padrão mas compacto
        main_layout = QVBoxLayout()
        main_layout.setSpacing(8)
        main_layout.setContentsMargins(12, 12, 12, 12)

        # Font size médio
        font = self.font()
        font.setPointSize(11)
        self.setFont(font)

        self.setLayout(main_layout)
        self.logger.info("Applied tablet layout")

    def _apply_desktop_layout(self):
        """Layout padrão desktop (1024px - 1440px)."""
        # Janela normal
        self.setFixedSize(550, 450)

        # Layout padrão
        main_layout = QVBoxLayout()
        main_layout.setSpacing(10)
        main_layout.setContentsMargins(15, 15, 15, 15)

        self.setLayout(main_layout)
        self.logger.info("Applied desktop layout")

    def _apply_large_desktop_layout(self):
        """Layout para desktop grande (> 1440px)."""
        # Janela um pouco maior
        self.setFixedSize(650, 500)

        # Layout com mais spacing
        main_layout = QVBoxLayout()
        main_layout.setSpacing(12)
        main_layout.setContentsMargins(20, 20, 20, 20)

        # Font sizes um pouco maiores
        font = self.font()
        font.setPointSize(12)
        self.setFont(font)

        self.setLayout(main_layout)
        self.logger.info("Applied large desktop layout")

    def resizeEvent(self, event):
        """Lida com redimensionamento da janela."""
        super().resizeEvent(event)

        # Recalcular layout se screen size mudou significativamente
        new_screen_width = self._get_screen_width()

        if abs(new_screen_width - self.screen_width) > 100:
            self.screen_width = new_screen_width
            self._setup_responsive_ui()
```

## Exemplo 4: Animações Suaves e Feedback Visual

```python
class AnimatedPopupWindow(QWidget):
    """Popup com animações suaves."""

    def __init__(self, current_agent: BaseAgent):
        super().__init__()
        self.current_agent = current_agent
        self.animation_group = QParallelAnimationGroup()

        self._setup_ui()
        self._setup_animations()

    def _setup_animations(self):
        """Configura animações para feedback visual."""

        # Animação de fade in ao abrir
        self._animate_fade_in()

        # Animação de hover em botões
        for button in self.findChildren(QPushButton):
            self._setup_button_animation(button)

    def _animate_fade_in(self):
        """Animação de fade in ao abrir janela."""
        from PyQt6.QtWidgets import QGraphicsOpacityEffect

        # Opacity effect
        opacity = QGraphicsOpacityEffect(self)
        self.setGraphicsEffect(opacity)
        opacity.setOpacity(0.0)

        # Animação
        fade_animation = QPropertyAnimation(opacity, b"opacity")
        fade_animation.setDuration(300)  # 300ms
        fade_animation.setStartValue(0.0)
        fade_animation.setEndValue(1.0)
        fade_animation.setEasingCurve(QEasingCurve.Type.InOutQuad)
        fade_animation.start()

        # Limpar effect após animação
        fade_animation.finished.connect(
            lambda: self.setGraphicsEffect(None)
        )

    def _setup_button_animation(self, button: QPushButton):
        """Configura animação de hover para botão."""

        def animate_hover_enter():
            """Animação ao entrar com mouse."""
            original_size = button.size()
            target_size = QtCore.QSize(
                int(original_size.width() * 1.05),
                original_size.height()
            )

            animation = QPropertyAnimation(button, b"size")
            animation.setDuration(150)
            animation.setStartValue(original_size)
            animation.setEndValue(target_size)
            animation.setEasingCurve(QEasingCurve.Type.OutCubic)
            animation.start()

        def animate_hover_leave():
            """Animação ao sair com mouse."""
            current_size = button.size()
            target_size = button.minimumSize()

            animation = QPropertyAnimation(button, b"size")
            animation.setDuration(150)
            animation.setStartValue(current_size)
            animation.setEndValue(target_size)
            animation.setEasingCurve(QEasingCurve.Type.InOutQuad)
            animation.start()

        # Conectar signals
        button.enterEvent = lambda e: animate_hover_enter()
        button.leaveEvent = lambda e: animate_hover_leave()

    def _show_success_animation(self, widget: QWidget):
        """Animação de sucesso (check verde)."""

        # Flash verde
        original_style = widget.styleSheet()

        flash_stylesheet = original_style + """
            QPushButton {
                background-color: #107c10;
                border: 2px solid #0b5c0b;
            }
        """

        widget.setStyleSheet(flash_stylesheet)

        # Voltar ao normal após 1 segundo
        QTimer.singleShot(1000, lambda: widget.setStyleSheet(original_style))

    def _show_error_animation(self, widget: QWidget):
        """Animação de erro (shake)."""

        # Shake animation
        shake_animation = QPropertyAnimation(widget, b"pos")
        shake_animation.setDuration(100)
        shake_animation.setLoopCount(3)

        original_pos = widget.pos()
        shake_distance = 10

        # Shake left/right
        for i in range(6):
            if i % 2 == 0:
                shake_animation.setKeyValueAt(
                    i / 6,
                    QtCore.QPoint(
                        original_pos.x() + shake_distance,
                        original_pos.y()
                    )
                )
            else:
                shake_animation.setKeyValueAt(
                    i / 6,
                    QtCore.QPoint(
                        original_pos.x() - shake_distance,
                        original_pos.y()
                    )
                )

        shake_animation.setEndValue(original_pos)
        shake_animation.start()

    def _save_with_animation(self):
        """Salva com animação de feedback."""

        # Mostrar loading
        self.save_btn.setText("Salvando...")
        self.save_btn.setEnabled(False)

        # Simular operação
        QTimer.singleShot(500, self._finish_save_animation)

    def _finish_save_animation(self):
        """Finaliza salvamento com animação."""
        success = True  # Resultado real

        if success:
            self.save_btn.setText("✓ Salvo!")
            self._show_success_animation(self.save_btn)
        else:
            self.save_btn.setText("✗ Erro")
            self._show_error_animation(self.save_btn)

        # Voltar ao normal após 1.5 segundos
        QTimer.singleShot(1500, self._reset_save_button)

    def _reset_save_button(self):
        """Reseta botão de salvar."""
        self.save_btn.setText("&Salvar Configuração")
        self.save_btn.setEnabled(True)
```

## Exemplo 5: High Contrast Mode Toggle

```python
class AccessiblePopupWindow(QWidget):
    """Popup com suporte a high contrast mode."""

    def __init__(self, current_agent: BaseAgent):
        super().__init__()
        self.current_agent = current_agent
        self.high_contrast = False

        self._load_accessibility_settings()
        self._setup_ui()
        self._apply_theme()

    def _load_accessibility_settings(self):
        """Carrega configurações de acessibilidade."""

        # Detectar se Windows está em high contrast mode
        import sys
        if sys.platform == 'win32':
            try:
                import winreg
                key = winreg.OpenKey(
                    winreg.HKEY_CURRENT_USER,
                    r"Control Panel\Accessibility\High Contrast"
                )
                flags = winreg.QueryValueEx(key, "Flags")
                self.high_contrast = bool(flags[0])
                winreg.CloseKey(key)
            except:
                self.high_contrast = False

    def _apply_theme(self):
        """Aplica tema baseado em configurações."""

        if self.high_contrast:
            self._apply_high_contrast_theme()
        else:
            self._apply_standard_theme()

    def _apply_standard_theme(self):
        """Aplica tema padrão."""
        self.setStyleSheet("""
            QWidget {
                background-color: #1e1e1e;
                color: #e0e0e0;
            }

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

            QPushButton:focus {
                border: 2px solid #60cdff;
            }

            QLineEdit {
                background-color: #2d2d2d;
                color: #e0e0e0;
                border: 1px solid #3a3a3a;
                padding: 6px;
            }

            QLineEdit:focus {
                border: 2px solid #0078d4;
            }
        """)

    def _apply_high_contrast_theme(self):
        """Aplica tema high contrast."""
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
                padding: 8px 16px;
            }

            QPushButton:hover {
                background-color: #ffff00;
                color: #000000;
                border: 2px solid #ffff00;
            }

            QPushButton:focus {
                border: 3px solid #ffff00;
            }

            QPushButton:pressed {
                background-color: #aaaaaa;
            }

            QLineEdit {
                background-color: #000000;
                color: #ffffff;
                border: 2px solid #ffffff;
                padding: 6px;
            }

            QLineEdit:focus {
                border: 3px solid #ffff00;
            }

            QLabel {
                color: #ffffff;
            }

            QTabWidget::pane {
                border: 2px solid #ffffff;
                background-color: #000000;
            }

            QTabBar::tab {
                background-color: #000000;
                color: #ffffff;
                border: 2px solid #ffffff;
                padding: 8px 16px;
            }

            QTabBar::tab:selected {
                background-color: #ffffff;
                color: #000000;
                font-weight: bold;
            }

            QTabBar::tab:focus {
                border: 3px solid #ffff00;
            }
        """)

    def _add_contrast_toggle(self):
        """Adiciona botão para toggle high contrast."""

        contrast_btn = QPushButton("🎨 Alto Contraste")
        contrast_btn.setCheckable(True)
        contrast_btn.setChecked(self.high_contrast)
        contrast_btn.setToolTip(
            "Alternar modo de alto contraste\n"
            "Melhora acessibilidade visual"
        )

        contrast_btn.toggled.connect(self._toggle_high_contrast)

        return contrast_btn

    def _toggle_high_contrast(self, enabled: bool):
        """Alterna high contrast mode."""
        self.high_contrast = enabled
        self._apply_theme()
```

## Exemplo 6: Tooltip Contextual Inteligente

```python
class SmartTooltipPopup(QWidget):
    """Popup com tooltips contextuais inteligentes."""

    def _setup_smart_tooltips(self):
        """Configura tooltips contextuais que se adaptam."""

        # Tooltip do Context Folder muda baseado em se está preenchido
        self.context_folder_edit.textChanged.connect(
            self._update_context_tooltip
        )

        # Tooltip do Focus File muda baseado em extensão
        self.focus_file_edit.textChanged.connect(
            self._update_focus_tooltip
        )

    def _update_context_tooltip(self, text: str):
        """Atualiza tooltip do context folder dinamicamente."""

        if not text.strip():
            # Vazio - mostrar help
            tooltip = (
                "<b>Pasta de Contexto</b><br><br>"
                "Selecione a pasta do projeto que o agente usará.<br><br>"
                "<b>Como usar:</b><br>"
                "• Clique em 'Procurar' para selecionar<br>"
                "• Ou digite o caminho diretamente<br>"
                "• O agente usará esta pasta como contexto<br>"
                "• Útil para projetos específicos<br><br>"
                "<b>Exemplos:</b><br>"
                "C:\\meu-projeto<br>"
                "C:\\Users\\nome\\Documents\\api-project"
            )
        else:
            # Preenchido - mostrar info
            import os
            folder_name = os.path.basename(text.rstrip(os.sep))

            # Verificar se pasta existe
            exists = os.path.isdir(text)

            if exists:
                # Contar arquivos
                try:
                    file_count = sum(
                        1 for _ in os.listdir(text)
                        if os.path.isfile(os.path.join(text, _))
                    )
                    folder_info = f"<br>Contém {file_count} arquivos"
                except:
                    folder_info = ""
            else:
                folder_info = "<br><b style='color: #d13438;'>⚠ Pasta não encontrada</b>"

            tooltip = (
                f"<b>Pasta de Contexto</b><br><br>"
                f"<b>Caminho:</b> {text}<br>"
                f"<b>Pasta:</b> {folder_name or 'Raiz'}"
                f"{folder_info}<br><br>"
                f"<i>O agente usará esta pasta como contexto de projeto</i>"
            )

        self.context_folder_edit.setToolTip(tooltip)

    def _update_focus_tooltip(self, text: str):
        """Atualiza tooltip do focus file dinamicamente."""

        if not text.strip():
            tooltip = (
                "<b>Arquivo Focal</b><br><br>"
                "Arquivo específico que fornece contexto adicional.<br><br>"
                "<b>Arquivos comuns:</b><br>"
                "• README.md - Documentação<br>"
                "• package.json - Deps do projeto<br>"
                "• requirements.txt - Deps Python<br>"
                "• config.yaml - Configuração<br>"
                "• .env - Variáveis de ambiente<br><br>"
                "Útil para dar contexto específico ao agente."
            )
        else:
            import os
            filename = os.path.basename(text)
            ext = os.path.splitext(filename)[1].lower()

            # Info baseada em extensão
            ext_info = {
                '.md': '📄 Documentação Markdown',
                '.txt': '📄 Arquivo de texto',
                '.json': '📋 Arquivo JSON',
                '.yaml': '⚙️ Configuração YAML',
                '.yml': '⚙️ Configuração YAML',
                '.py': '🐍 Script Python',
                '.js': '📜 Script JavaScript',
                '.ts': '📜 Script TypeScript',
                '.env': '🔐 Variáveis de ambiente',
            }

            file_type = ext_info.get(ext, '📄 Arquivo')

            # Verificar se existe
            exists = os.path.isfile(text)

            if not exists:
                exists_info = "<br><b style='color: #d13438;'>⚠ Arquivo não encontrado</b>"
            else:
                # Tamanho do arquivo
                try:
                    size_bytes = os.path.getsize(text)
                    if size_bytes < 1024:
                        size = f"{size_bytes} bytes"
                    elif size_bytes < 1024 * 1024:
                        size = f"{size_bytes / 1024:.1f} KB"
                    else:
                        size = f"{size_bytes / (1024 * 1024):.1f} MB"
                    exists_info = f"<br><b>Tamanho:</b> {size}"
                except:
                    exists_info = ""

            tooltip = (
                f"<b>Arquivo Focal</b><br><br>"
                f"<b>Tipo:</b> {file_type}<br>"
                f"<b>Arquivo:</b> {filename}<br>"
                f"<b>Caminho:</b> {text}"
                f"{exists_info}<br><br>"
                f"<i>O agente usará este arquivo para contexto adicional</i>"
            )

        self.focus_file_edit.setToolTip(tooltip)
```

## Checklist de Validação

Use este checklist para validar cada melhoria:

### Acessibilidade
- [ ] Contraste adequado (WCAG AA 4.5:1)
- [ ] Navegação por teclado funcional (Tab, Enter, Esc)
- [ ] Mnemônicos em widgets importantes (ALT+letra)
- [ ] AcessibleName e AccessibleDescription definidos
- [ ] Tooltips descritivos
- [ ] Focus indicators visuais claros
- [ ] High contrast mode support (se aplicável)

### Responsividade
- [ ] Layout se adapta a diferentes tamanhos de screen
- [ ] Breakpoints definidos (mobile, tablet, desktop)
- [ ] DPI scaling implementado
- [ ] Tamanhos mínimos/máximos definidos
- [ ] Size policies configuradas corretamente

### Feedback Visual
- [ ] Estados hover definidos
- [ ] Estados focus definidos
- [ ] Estados pressed/disabled definidos
- [ ] Animações sutis (não distrativas)
- [ ] Indicadores de progresso/loading
- [ ] Feedback de sucesso/erro claro

### Navegação
- [ ] Ordem de Tab lógica
- [ ] Atalhos de teclado consistentes
- [ ] Mnemônicos não conflitam
- [ ] Esc fecha/ cancela
- [ ] Enter confirma ações padrão
- [ ] Ajuda contextual disponível

### Geral
- [ ] Sem autenticação/logging (conforme restrições)
- [ ] Persistência local apenas (JSON)
- [ ] Performance aceitável (< 100ms para updates)
- [ ] Sem memory leaks
- [ ] Código bem documentado
- [ ] Testado em diferentes DPIs
