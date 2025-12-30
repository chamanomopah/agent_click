# AgentClick V2 - Decisões Completas

**Data**: 2025-12-28
**Status**: Todas as decisões definidas ✅
**Versão**: 2.0

---

## 📋 Visão Geral

Versão mais robusta do AgentClick com suporte a:
- `.claude/commands` (arquivos .md diretos)
- `.claude/skills` (diretórios com SKILL.md)
- `.claude/agents` (arquivos .md - NOVO!)
- Sistema de Workspaces
- Inputs templatables

**IMPORTANTE:** Todos são arquivos `.md`, sem agents Python!

---

## ✅ Decisões Definidas - Completo

### 1. Sistema de Workspaces

**O que é:**
- Workspace = Contexto de trabalho específico
- Cada workspace tem:
  - Pasta específica
  - Agents/Commands específicos
  - Configurações isoladas

**Como alternar:**
- `Ctrl+Shift+Pause` = Mudar de workspace

**UX/UI:**
- **Opção B**: Texto no Detailed Popup
- Nova aba "Workspaces" (além de Activity e Config)

---

### 2. Input Templates

**O que é Input do Usuário:**
- Texto selecionado ✅
- Arquivo selecionado ✅
- Input vazio ✅
- Múltiplos arquivos ✅
- URL ✅

**Como configurar templates:**
- **Opção Híbrida**:
  - Configuração via UI (Config Tab)
  - E via arquivo separado `input_templates.yaml`

---

### 3. Descoberta de Commands/Skills/Agents

**Como o sistema descobre:**
- **Opção C (Híbrida)**:
  - Scan automático na inicialização
  - Usuário pode ativar/desativar
  - Todos aparecem, mas usuário escolhe quais estão ativos

---

### 4. Tipos Suportados

**IMPORTANTE: Sem agents Python!**

**Tipos de Arquivos:**
- `.claude/commands/*.md` - Commands diretos
- `.claude/skills/*/SKILL.md` - Skills complexos
- `.claude/agents/*.md` - Agents customizados

**Diferenças:**

| Tipo | Formato | Comportamento | Configurações |
|------|---------|---------------|---------------|
| **Commands** | `.md` simples | Executa e pronto | Input template |
| **Skills** | Diretório com `SKILL.md` | Pode ter múltiplas fases | Input template |
| **Agents** | `.md` | Lógica customizada | Input template |

**NOTA:** Sistema precisa ter noção do tipo diferente!

---

### 5. UX/UI Detalhada

**Layout do Detailed Popup:**
```
┌─────────────────────────────────────┐
│ [📋 Activity] [⚙️ Config] [💼 Workspaces] ← NOVA ABA
├─────────────────────────────────────┤
│                                     │
│ Current: Python Workspace           │
│ Folder: C:\python-projects          │
│ Agents Available:                   │
│   ☑ 📝 verify-python                │
│   ☑ 📝 diagnose                     │
│   ☐ 📝 review-code                  │
│   ☑ 🎯 ux-ui-improver               │
│                                     │
│ [Switch Workspace] [Add Workspace]  │
└─────────────────────────────────────┘
```

**Diferenciação Visual:**
- Commands: 📝
- Skills: 🎯
- Agents: 🤖

**Ativação/Desativação:**
```
Config Tab → Sub-section "Available Agents"
┌──────────────────────────────────────┐
│ Available Agents in Python Workspace│
│                                      │
│ ☑ verify-python (Command)           │
│ ☑ diagnose (Command)                │
│ ☐ review-code (Command)             │
│ ☑ ux-ui-improver (Skill)            │
│                                      │
│ [Scan for New Agents]               │
└──────────────────────────────────────┘
```

---

### 6. Tipos de Inputs

**Tipos Suportados:**

1. **Texto selecionado** ✅
   - Usuário seleciona texto em qualquer app
   - Pressiona Pause
   - Sistema usa texto selecionado

2. **Arquivo selecionado** ✅
   - Sistema abre file dialog
   - Usuário escolhe arquivo
   - Sistema lê conteúdo

3. **Input vazio** ✅
   - Usuário pressiona Pause sem selecionar nada
   - Sistema abre popup pedindo input

4. **Múltiplos arquivos** ✅
   - Sistema processa um por um

5. **URL** ✅
   - Sistema baixa conteúdo
   - OU usa URL como texto (depende da capacidade do agente)

---

### 7. Formato dos Arquivos de Configuração

**`workspaces.yaml`:**
```yaml
workspaces:
  python:
    name: "Python Projects"
    folder: "C:/python-projects"
    agents:
      - type: command
        id: verify-python
        enabled: true
        icon: "📝"
      - type: command
        id: diagnose
        enabled: true
        icon: "📝"

  web-dev:
    name: "Web Development"
    folder: "C:/web-projects"
    agents:
      - type: skill
        id: ux-ui-improver
        enabled: true
        icon: "🎯"
```

**`input_templates.yaml`:**
```yaml
# Templates para cada agent/command
verify-python:
  template: |
    Arquivo: {{input}}
    Contexto: {{context_folder}}
  enabled: true

diagnose:
  template: |
    Problema: {{input}}
    Analisar: {{context_folder}}
  enabled: true

ux-ui-improver:
  template: |
    Melhorar: {{input}}
    Projeto: {{context_folder}}
  enabled: true
```

---

### 8. Diferenças Command vs Skill vs Agent

**Commands (`.claude/commands/*.md`):**
- "Direto ao ponto"
- "Sem muitos pontos de mudança"
- Executa e pronto
- Ex: verify-python, diagnose

**Skills (`.claude/skills/*/SKILL.md`):**
- Podem ter abordagem diferente
- Configurações específicas
- Podem ser mais complexos
- Ex: ux-ui-improver

**Agents (`.claude/agents/*.md`):**
- Lógica customizada
- Configurações específicas
- Semelhantes a skills mas em arquivo único
- NOVO tipo na V2!

---

### 9. Workspaces vs Context Folder

**Status:** ❌ Ainda não definido
**Decisão:** Abordar depois de testar sistema

---

## 🎯 Resumo de Decisões

### UX/UI ✅
- Nova aba "Workspaces"
- Ícones: 📝 Commands, 🎯 Skills, 🤖 Agents
- Checkboxes para ativar/desativar
- File dialog tradicional para arquivos

### Inputs ✅
- Texto selecionado
- Arquivo selecionado (dialog)
- Input vazio → Popup pedindo input
- Múltiplos arquivos → Processa um por um
- URL → Baixa ou usa como texto

### Sistema de Arquivos ✅
- `.claude/commands/*.md`
- `.claude/skills/*/SKILL.md`
- `.claude/agents/*.md` (NOVO!)
- `workspaces.yaml`
- `input_templates.yaml`

### Workspaces ✅
- Ctrl+Shift+Pause para alternar
- Cada workspace tem pasta + agents específicos
- Mostrado no Detailed Popup (aba Workspaces)

### Tipos ✅
- Commands: Simples, diretos
- Skills: Mais complexos, diretórios
- Agents: Customizados, arquivo único
- TODOS são `.md` (sem Python!)

---

## 🚀 Próximo Passo

**Criar PRD completo baseado nestas decisões!**

---

**Última atualização**: 2025-12-28
**Status**: Todas as decisões definidas ✅
**Pronto para PRD**: SIM ✅
