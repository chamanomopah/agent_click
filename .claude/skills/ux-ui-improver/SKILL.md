---
name: ux-ui-improver
description: |
  Melhora UX/UI, acessibilidade e responsividade de interfaces PyQt6. Implementa navegação intuitiva, feedback visual, contraste adequado, atalhos de teclado e layouts responsivos para apps PyQt6 sem autenticação ou logging.

  Use quando usuário mencionar: UX, UI, acessibilidade, responsivo, navegação, interface visual, usabilidade, contraste, cores, layout responsivo, feedback visual, atalhos, teclas de atalho, experiência do usuário, interface intuitiva.
allowed-tools: Read, Write, Edit, Grep, Glob
---

# UX/UI Improver for PyQt6

## Propósito

Melhora a experiência do usuário (UX) e interface visual (UI) de aplicações PyQt6, focando em:
- Navegação intuitiva e discoverability
- Acessibilidade (WCAG 2.1 compliance)
- Layouts responsivos e adaptáveis
- Feedback visual claro e imediato
- Atalhos de teclado consistentes
- Contraste e legibilidade adequados

## Quando Usar

**Invocar esta Skill quando:**
- Usuário mencionar melhorias em UX/UI, acessibilidade ou responsividade
- Precisar implementar navegação mais intuitiva em popups/janelas
- Necessário adicionar feedback visual (hover, focus, active states)
- Precisar melhorar contraste de cores ou legibilidade
- Precisar tornar layout responsivo a diferentes tamanhos de tela
- Precisar adicionar atalhos de teclado ou mnemônicos
- Precisar melhorar discoverability de funcionalidades

**Não usar para:**
- Implementar autenticação ou sistemas de login
- Adicionar logging ou telemetria
- Criar funcionalidades de backend
- Modificar lógica de negócios (apenas UX/UI)

## Instruções

### 1. Análise Inicial do Contexto

**Identificar arquivos UI:**
```python
# Procurar por arquivos PyQt6
ui/*.py
**/*popup*.py
**/*window*.py
**/*widget*.py
```

**Analisar componentes existentes:**
- Ler `ui/mini_popup.py` e `ui/popup_window.py`
- Identificar widgets, layouts e estilos atuais
- Verificar hardcoded dimensions e positions
- Verificar falta de feedback visual (hover, focus, active)

### 2. Melhorias de UX/UI

#### Acessibilidade (Priority 1)

**Adicionar acessibilidade aos widgets:**
```python
# Exemplo de melhoria
widget.setAccessibleName("Botão Salvar Configuração")
widget.setAccessibleDescription("Salva as configurações do agente atual no arquivo JSON")
widget.setToolTip("Salva as configurações (Ctrl+S)")

# Adicionar mnemônicos (ALT+letra)
button.setText("&Salvar")  # ALT+S
label.setText("&Contexto:")  # ALT+C

# Navegação por teclado
widget.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
widget.setTabOrder(widget1, widget2)

# High contrast mode support
app.setStyle("Fusion")
```

**Contraste adequado (WCAG AA):**
- Foreground/background contrast mínimo 4.5:1 para texto normal
- 3:1 para texto grande (>18pt ou >14pt bold)
- Não usar cor como único indicador de estado

```python
# Exemplo de contraste adequado
label.setStyleSheet("""
    QLabel {
        color: #1a1a1a;          # Preto suave (contraste alto)
        background-color: #f5f5f5;  # Cinza claro
        font-size: 12px;
        padding: 8px;
        border: 1px solid #cccccc;
    }
""")
```

#### Responsividade (Priority 1)

**Layouts responsivos:**
```python
# Em vez de setFixedSize(), usar:
self.setMinimumSize(400, 300)
self.setMaximumSize(800, 600)

# Ou usar size policies
widget.setSizePolicy(
    QSizePolicy.Policy.Expanding,
    QSizePolicy.Policy.Expanding
)

# Layout responsivo baseado em screen size
screen = QApplication.primaryScreen()
screen_geometry = screen.availableGeometry()
if screen_geometry.width() < 1024:  # Tablet/mobile
    self.setFixedSize(screen_geometry.width() * 0.9, 400)
else:  # Desktop
    self.setFixedSize(550, 450)
```

**Posicionamento inteligente:**
```python
def _position_window(self):
    """Posiciona janela considerando screen size e posições ocupadas."""
    screen = QApplication.primaryScreen()
    if not screen:
        return

    screen_geometry = screen.availableGeometry()
    window_width = self.width()
    window_height = self.height()

    # Default: bottom-right
    x = screen_geometry.width() - window_width - 20
    y = screen_geometry.height() - window_height - 50

    # Verificar se está muito próximo de outra janela
    # (implementar collision detection se necessário)

    self.move(x, y)
```

#### Feedback Visual (Priority 1)

**Estados interativos completos:**
```python
# Botão com todos os estados
button.setStyleSheet("""
    QPushButton {
        background-color: #0078d4;
        color: #ffffff;
        border: none;
        padding: 10px;
        border-radius: 5px;
    }
    QPushButton:hover {
        background-color: #106ebe;
        border: 2px solid #005a9e;
    }
    QPushButton:pressed {
        background-color: #005a9e;
    }
    QPushButton:focus {
        border: 2px solid #000000;
        outline: 2px solid #000000;
    }
    QPushButton:disabled {
        background-color: #cccccc;
        color: #666666;
    }
""")
```

**Animações sutis:**
```python
# Transição suave (hover em mini popup)
from PyQt6.QtCore import QPropertyAnimation, QEasingCurve

def enterEvent(self, event):
    """Hover - cresce suavemente."""
    self._animate_size(65, 65)

def _animate_size(self, target_width, target_height):
    """Animação suave de tamanho."""
    self.animation = QPropertyAnimation(self, b"size")
    self.animation.setDuration(150)  # 150ms
    self.animation.setStartValue(self.size())
    self.animation.setEndValue(QSize(target_width, target_height))
    self.animation.setEasingCurve(QEasingCurve.Type.OutCubic)
    self.animation.start()
```

#### Navegação Intuitiva (Priority 2)

**Descoberta de funcionalidades:**
```python
# Adicionar tooltips úteis
widget.setToolTip("Pressione Ctrl+S para salvar rapidamente")

# Adicionar texto de ajuda contextual
help_label = QLabel(
    "💡 Dica: Use Tab para navegar entre campos, "
    "Enter para salvar, Esc para cancelar"
)

# Indicadores visuais de funcionalidades ocultas
more_button.setText("▼ Mais opções")
more_button.setToolTip("Clique para revelar opções avançadas")
```

**Atalhos de teclado consistentes:**
```python
# Padrões de desktop
- Ctrl+S: Salvar
- Ctrl+O: Abrir arquivo
- Ctrl+W: Fechar janela
- Esc: Cancelar/fechar
- F1: Ajuda
- Tab/Shift+Tab: Navegação
- Enter: Confirmar
- Space: Ativar botão focado
```

### 3. Implementação

**Passo a passo:**

1. **Ler arquivos UI existentes** (`ui/*.py`)
2. **Identificar áreas de melhoria:**
   - Falta de estados hover/focus/active
   - Hardcoded sizes sem responsividade
   - Falta de mnemônicos e acessibilidade
   - Contraste inadequado
   - Falta de feedback visual
3. **Aplicar melhorias priorizadas**
4. **Testar manualmente** se possível (descrever como testar)
5. **Documentar mudanças** em comentários no código

### 4. Validação

**Checklist de qualidade:**
- [ ] Contraste adequado (WCAG AA)
- [ ] Layout responsivo (adapta a diferentes tamanhos)
- [ ] Feedback visual em todos os estados interativos
- [ ] Navegação por teclado funcional (Tab, Enter, Esc)
- [ ] Tooltips descritivos em widgets importantes
- [ ] Mnemônicos (ALT+letra) em ações principais
- [ ] Tamanhos de fonte legíveis (>11px)
- [ ] Animações sutis (não distrativas)
- [ ] Indicadores visuais de estado (loading, erro, sucesso)
- [ ] Sem autenticação/logging (conforme restrição do usuário)

## Exemplos

### Exemplo 1: Melhorar Mini Popup com Acessibilidade

**Antes (sem acessibilidade):**
```python
self.icon_label.setStyleSheet("""
    QLabel {
        font-size: 32px;
        background-color: %s;
        border-radius: 30px;
    }
""" % color)
```

**Depois (com acessibilidade + responsividade):**
```python
# Acessibilidade
self.icon_label.setAccessibleName(
    f"Agente Atual: {self.current_agent.metadata.name}"
)
self.icon_label.setAccessibleDescription(
    f"Clique para abrir configurações de {self.current_agent.metadata.name}. "
    f"Pressione Ctrl+Pause para alternar agentes."
)

# Responsividade
screen = QApplication.primaryScreen()
screen_size = screen.availableGeometry()
if screen_size.width() < 1024:
    self.setFixedSize(50, 50)  # Tablet
else:
    self.setFixedSize(60, 60)  # Desktop

# Feedback visual melhorado
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
""" % (color, self._lighten_color(color)))
```

### Exemplo 2: Adicionar Navegação por Teclado

```python
# Configurar ordem de Tab
self.setTabOrder(self.context_folder_edit, self.focus_file_edit)
self.setTabOrder(self.focus_file_edit, save_btn)

# Adicionar atalhos
save_btn.setShortcut("Ctrl+S")
save_btn.setToolTip("Salvar (Ctrl+S)")

close_btn.setShortcut("Esc")
close_btn.setToolTip("Fechar (Esc)")

# Mnemônicos
context_label.setText("Conte&xto Folder:")  # ALT+X
focus_label.setText("F&ocus File:")  # ALT+O
save_btn.setText("&Salvar")  # ALT+S
```

### Exemplo 3: Layout Responsivo

```python
# Em vez de setFixedSize(550, 450):
self.setMinimumSize(400, 350)
self.setMaximumSize(700, 550)

# Ajustar layout baseado em screen size
def _setup_responsive_layout(self):
    """Configura layout responsivo."""
    screen = QApplication.primaryScreen()
    screen_width = screen.availableGeometry().width()

    if screen_width < 1024:  # Tablet
        self.setFixedSize(screen_width * 0.95, 400)
        self._apply_compact_layout()
    else:  # Desktop
        self.setFixedSize(550, 450)
        self._apply_standard_layout()
```

## Casos Especiais

**Apps sem autenticação/logging:**
- Não adicionar trackers ou analytics
- Focar puramente em UX/UI local
- Melhorar feedback local ao usuário
- Persistência local (JSON) é OK

**Popups muito pequenos (mini popup):**
- Mantenha discreto mas acessível
- Adicione tooltip informativo
- Garanta área de clique adequada (mínimo 44x44px - WCAG)
- Feedback visual claro no hover

**Janelas com múltiplas tabs:**
- Indicador visual de tab ativa forte
- Atalhos Ctrl+Tab para navegação
- Teclas de atalho por tab (ALT+1, ALT+2, etc.)
- Mnemônicos em cada widget importante

**Dark mode:**
- Se implementar, garantir toggle fácil
- Mantém contraste adequado em ambos modos
- Transição suave entre modos
- Persistir preferência do usuário

## Referências

**Arquivos do projeto:**
- `ui/mini_popup.py` - Mini popup (60x60px, bottom-right)
- `ui/popup_window.py` - Janela principal com tabs (550x450px)
- `README.md` - Contexto geral do sistema

**Documentação adicional:**
- `reference.md` - Padrões de design PyQt6
- `examples.md` - Exemplos adicionais de UX/UI

**WCAG 2.1 Guidelines:**
- Contrast: https://www.w3.org/WAI/WCAG21/Understanding/contrast-minimum.html
- Keyboard: https://www.w3.org/WAI/WCAG21/Understanding/keyboard
- Resize: https://www.w3.org/WAI/WCAG21/Understanding/resize-no-loss

**PyQt6 Best Practices:**
- Use QStylesheet para estilos consistentes
- Evite hardcoded pixels, use size policies
- Sempre implemente focus policies
- Use signals/slots para comunicação
- Teste com diferentes DPI settings
