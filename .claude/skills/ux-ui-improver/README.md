# UX/UI Improver - Guia de Uso

## Visão Geral

Skill personalizada para melhorar UX/UI, acessibilidade e responsividade de aplicações PyQt6 do AgentClick System.

## Estrutura da Skill

```
.claude/skills/ux-ui-improver/
├── SKILL.md           # Arquivo principal da skill (obrigatório)
├── reference.md       # Referência técnica de padrões PyQt6
├── examples.md        # Exemplos práticos de implementação
└── README.md          # Este arquivo (guia de uso)
```

## Como Usar

### Invocação Automática

Claude Code invocará esta skill automaticamente quando você mencionar:

- **UX/UI:** "melhorar a interface", "tornar mais intuitivo"
- **Acessibilidade:** "acessível", "teclado", "contraste", "WCAG"
- **Responsividade:** "responsivo", "adaptar a tela", "mobile"
- **Navegação:** "atalhos", "teclas de atalho", "navegação"
- **Feedback visual:** "hover", "animação", "feedback"

### Exemplos de Uso

```
Você: "Preciso melhorar a acessibilidade do mini popup"
Claude: [Invoca skill ux-ui-improver automaticamente]

Você: "Como adicionar atalhos de teclado na janela de configuração?"
Claude: [Invoca skill ux-ui-improver automaticamente]

Você: "Tornar o layout responsivo para diferentes tamanhos de tela"
Claude: [Invoca skill ux-ui-improver automaticamente]
```

## Conteúdo da Skill

### SKILL.md (Arquivo Principal)

**Frontmatter YAML:**
- `name`: ux-ui-improver
- `description`: Palavras-chave para invocação automática
- `allowed-tools`: Read, Write, Edit, Grep, Glob

**Seções principais:**
- Propósito e escopo
- Quando usar/ não usar
- Instruções passo a passo
- Checklist de validação
- Casos especiais

### reference.md (Referência Técnica)

**Padrões documentados:**
- Estrutura base de stylesheets (dark/light mode)
- Configuração completa de acessibilidade
- High contrast mode
- Size policies e layouts responsivos
- DPI scaling
- Animações suaves
- Atalhos de teclado globais
- Toggle de temas

### examples.md (Exemplos Práticos)

**Exemplos completos:**
1. Transformar mini popup com acessibilidade
2. Popup window com navegação por teclado
3. Layout responsivo com breakpoints
4. Animações suaves e feedback visual
5. High contrast mode toggle
6. Tooltip contextual inteligente

Cada exemplo inclui:
- Código "antes" (sem melhorias)
- Código "depois" (com todas as melhorias)
- Comentários explicativos

## Casos de Uso Típicos

### 1. Melhorar Acessibilidade

**Problema:** Mini popup não tem suporte a teclado

```python
# Antes
self.icon_label = QLabel("🔍")

# Depois (com skill)
self.icon_label = QLabel("🔍")
self.icon_label.setAccessibleName("Agente Atual: Diagnostic Agent")
self.icon_label.setAccessibleDescription(
    "Diagnostic Agent - Analisa problemas e fornece diagnóstico. "
    "Clique para abrir configurações. Ctrl+Pause para alternar."
)
self.icon_label.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
```

### 2. Adicionar Responsividade

**Problema:** Popup não se adapta a diferentes tamanhos de tela

```python
# Antes
self.setFixedSize(550, 450)  # Hardcoded

# Depois (com skill)
screen = QApplication.primaryScreen()
screen_width = screen.availableGeometry().width()

if screen_width < 1024:
    self.setFixedSize(int(screen_width * 0.95), 400)
else:
    self.setFixedSize(550, 450)
```

### 3. Implementar Feedback Visual

**Problema:** Botões sem feedback visual de hover/focus

```python
# Antes
button.setStyleSheet("background-color: #0078d4;")

# Depois (com skill)
button.setStyleSheet("""
    QPushButton {
        background-color: #0078d4;
    }
    QPushButton:hover {
        background-color: #106ebe;
        border: 2px solid #005a9e;
    }
    QPushButton:focus {
        border: 2px solid #60cdff;
    }
""")
```

## Validação de Qualidade

Use o checklist da skill para validar melhorias:

### Acessibilidade (WCAG 2.1)
- ✅ Contraste mínimo 4.5:1 para texto normal
- ✅ Navegação completa por teclado
- ✅ Mnemônicos (ALT+letra) em ações principais
- ✅ AcessibleName e AccessibleDescription
- ✅ Tooltips descritivos

### Responsividade
- ✅ Breakpoints definidos (mobile, tablet, desktop)
- ✅ DPI scaling implementado
- ✅ Size policies configuradas
- ✅ Layouts adaptáveis

### Feedback Visual
- ✅ Estados hover/focus/active definidos
- ✅ Animações sutis (< 200ms)
- ✅ Indicadores de progresso
- ✅ Feedback de sucesso/erro

### Navegação
- ✅ Ordem lógica de Tab
- ✅ Atalhos consistentes (Ctrl+S, Esc, etc.)
- ✅ Mnemônicos não conflitam
- ✅ Ajuda contextual

## Restrições Específicas

**Conforme sua solicitação:**
- ❌ Sem autenticação ou sistemas de login
- ❌ Sem logging ou telemetria
- ❌ Sem analytics ou tracking
- ✅ Foco puramente em UX/UI local
- ✅ Persistência local (JSON) é permitida
- ✅ Feedback visual ao usuário local

## Testando a Skill

### 1. Teste Básico de Invocação

```
Prompt: "Melhorar a acessibilidade dos popups"
Esperado: Skill é invocada automaticamente
```

### 2. Teste de Implementação

```
Prompt: "Adicionar atalhos de teclado na janela de configuração"
Esperado: Skill fornece código completo com:
- Mnemônicos (ALT+letra)
- Shortcuts (Ctrl+S, Esc)
- Ordem de Tab
- Tooltips explicativos
```

### 3. Teste de Responsividade

```
Prompt: "Tornar o popup responsivo para tablets"
Esperado: Skill fornece código com:
- Detecção de screen size
- Breakpoints para tablet
- Layout adaptável
- DPI scaling
```

## Arquivos do Projeto Relacionados

A skill trabalha principalmente com:

- `ui/mini_popup.py` - Mini popup (60x60px, bottom-right)
- `ui/popup_window.py` - Janela principal (550x450px, tabs)
- `ui/__init__.py` - Módulo UI
- `README.md` - Contexto geral do sistema

## Contribuindo com a Skill

Para adicionar novos padrões ou exemplos:

1. Adicione em `reference.md` se for um padrão reutilizável
2. Adicione em `examples.md` se for um exemplo completo de uso
3. Atualize `SKILL.md` se adicionar novas instruções ou casos de uso
4. Mantenha o foco em PyQt6 e WCAG 2.1

## Troubleshooting

**Skill não é invocada:**
- Verifique se o frontmatter YAML está válido
- Confirme que `description` contém palavras-chave relevantes
- Teste com termos que correspondem exatamente à descrição

**Erros de implementação:**
- Siga os exemplos completos em `examples.md`
- Verifique imports do PyQt6
- Teste incrementalmente (uma melhoria por vez)

**Problemas de acessibilidade:**
- Use o checklist de validação
- Teste navegação por teclado (Tab, Enter, Esc)
- Verifique contraste com ferramentas online (ex: WebAIM Contrast Checker)

## Recursos Adicionais

**Documentação PyQt6:**
- https://www.riverbankcomputing.com/static/Docs/PyQt6/

**WCAG 2.1 Guidelines:**
- https://www.w3.org/WAI/WCAG21/quickref/

**Python Accessibility:**
- https://pyqt.readthedocs.io/en/stable/accessible.html

**High Contrast Mode (Windows):**
- https://learn.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-systemparametersinfoa

## Versão

**v1.0** - 2025-12-28
- Skill inicial para UX/UI no AgentClick System
- Foco em PyQt6, acessibilidade e responsividade
- Sem autenticação/logging (conforme requisito do usuário)
