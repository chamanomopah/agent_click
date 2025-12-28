# Criar Sub-Agente Especializado para Claude Code

Cria agentes personalizados (custom agents) com expertise específica, contexto isolado e ferramentas customizáveis. Use quando precisar delegar tarefas especializadas que requerem processamento isolado, instruções específicas ou conjunto de ferramentas dedicado.

## Contexto & Variáveis

**Variáveis do Comando:**
- `CONTEXTO_DO_AGENTE`: Descrição do papel e propósito do agente
- Escopo esperado (tarefa específica ou domínio completo)
- Nível de autonomia desejado

**Arquivos Relevantes:**
- Localização: `.claude/agents/` (projeto, compartilhado) ou `~/.claude/agents/` (usuário, global)
- Formato: Markdown com frontmatter YAML

**Saída Esperada:**
- Arquivo de agente configurado
- Documentação de uso
- Instruções de invocação

## Análise Contextual

**Características do Agente:**
- **Complexidade**: Média (requer compreensão de YAML + system prompts)
- **Interatividade**: Alta (requer input detalhado do usuário)
- **Dependências**: Internas (estrutura de arquivos Claude Code)
- **Validação Necessária**: Sim (sintaxe YAML + funcionalidade)
- **Tipo Principal**: Configuração + Documentação técnica

## Preparação & Análise

### 1. Compreender o Caso de Uso
Analise o contexto fornecido em `CONTEXTO_DO_AGENTE` para determinar:
- Responsabilidade principal do agente
- Tipo de tarefas que executará
- Ferramentas necessárias (seja específico)
- Nível de autonomia apropriado
- Modelo mais adequado (haiku/sonnet/opus/inherit)

### 2. Determinar Escopo e Limites
Defina claramente:
- O que o agente DEVE fazer
- O que o agente NÃO deve fazer
- Como ele deve interagir com o contexto principal
- Quando deve ser invocado (automático vs manual)

## Passos Executivos

### 3. Criar Estrutura do Arquivo

**3.1. Frontmatter YAML (Obrigatório)**

```yaml
---
name: nome-do-agent-minusculo-com-hifens
description: |
  Descrição clara e específica de QUANDO este agente deve ser invocado.
  Use linguagem natural que Claude reconheça em contextos relevantes.
  Seja específico sobre gatilhos e cenários de uso.
tools: Read, Write, Bash, Grep, Glob  # Omitir para herdar TODAS as ferramentas
model: sonnet  # OPCIONAL: sonnet|opus|haiku|inherit (padrão: sonnet)
permissionMode: default  # OPCIONAL: default|acceptEdits|bypassPermissions|plan|ignore
skills: skill1, skill2  # OPCIONAL: skills para auto-carregar no início
---
```

**Campos Explicados:**
- `name`: Identificador único (lowercase, hífens, sem espaços)
- `description`: Gatilho de invocação automática - seja específico e natural
- `tools`: Lista EXATA das ferramentas necessárias (omitir = herdar todas)
- `model`: Modelo de IA (haiku=rápido, sonnet=equilibrado, opus=complexo, inherit=mãe)
- `permissionMode`: Controle de permissões do agente
- `skills`: Skills para carregar automaticamente na inicialização

**3.2. System Prompt (Corpo do Arquivo)**

Estruture o system prompt com:

```markdown
You are a [ESPECIALIDADE] expert.

[ROLE FRAMING - Quem você é e sua expertise]

When invoked:
1. [PASSO 1 - Início imediato]
2. [PASSO 2 - Processo principal]
3. [PASSO 3 - Validação/entrega]

[DOMAIN KNOWLEDGE - Conhecimento específico do domínio]

[CHECKLIST - Critérios de qualidade/verificação]
- [Critério 1]
- [Critério 2]
- [Critério 3]

[OUTPUT FORMAT - Formato esperado do resultado]

[CONSTRAINTS - Limitações e regras importantes]
```

### 4. Definir Configuração de Ferramentas

**Ferramentas Disponíveis:**
- **Arquivos**: `Read`, `Write`, `Edit` (manipulação de arquivos)
- **Busca**: `Grep`, `Glob` (pattern matching)
- **Execução**: `Bash` (comandos terminal)
- **MCP**: Tools configuradas no servidor (se aplicável)

**Princípio de Mínimo Privilégio:**
- Liste APENAS ferramentas necessárias
- Se o agente não precisa escrever arquivos, omita `Write`
- Se não precisa executar comandos, omita `Bash`
- Omitir campo `tools` = herdar TODAS as ferramentas

### 5. Selecionar Modelo Adequado

**Critérios de Seleção:**
- **haiku**: Tarefas simples, rápidas, leitura-only, buscas
- **sonnet**: Tarefas equilibradas, código, análise (PADRÃO)
- **opus**: Tarefas complexas, raciocínio profundo, criatividade
- **inherit**: Usar mesmo modelo da conversa principal

### 6. Definir Modo de Invocação

**Automática (via description):**
- Claude detecta contexto e invoca automaticamente
- A `description` deve ser específica e natural

**Explícita (via menção):**
- Usuário menciona: "Use the [agent-name] agent para..."

**Manual (via /agents):**
- Interface interativa para gerenciar agentes

## Validação & Qualidade

### Checklist de Validação

**Estrutura do Arquivo:**
- [ ] Frontmatter YAML válido (sintaxe correta)
- [ ] Campo `name` presente (lowercase, hífens)
- [ ] Campo `description` específico e natural
- [ ] System prompt detalhado e claro
- [ ] Sem formatação inconsistente

**Funcionalidade:**
- [ ] System prompt define papel claramente
- [ ] Instruções passo-a-passo presentes
- [ ] Checklist de verificação incluído
- [ ] Formato de output especificado
- [ ] Constraints documentadas

**Configuração:**
- [ ] Ferramentas limitadas ao necessário
- [ ] Modelo apropriado ao tipo de tarefa
- [ ] Permissões adequadas ao escopo

**Usabilidade:**
- [ ] Descrição ativa em contexto relevante
- [ ] Instruções são executáveis
- [ ] Exemplos práticos incluídos (se aplicável)

### Teste de Sintaxe

Verifique:
1. Valide YAML (frontmatter deve ter `---` no início e fim)
2. Teste invocação automática via descrição
3. Teste invocação explícita pelo nome
4. Verifique se ferramentas funcionam conforme esperado

## Entrega & Finalização

### Arquivo de Agente (Estrutura Completa)

```markdown
---
name: [NOME-UNICO]
description: |
  [DESCRIÇÃO ESPECÍFICA do contexto de invocação]
tools: [LISTA DE FERRAMENTAS]
model: [MODELO APROPRIADO]
---

You are a [ESPECIALIDADE] expert.

[SYSTEM PROMPT COMPLETO]

When invoked:
1. [First action]
2. [Second action]
3. [Third action]

[DOMAIN KNOWLEDGE]

Checklist:
- [ ] [Item 1]
- [ ] [Item 2]
- [ ] [Item 3]

[OUTPUT FORMAT]
```

### Documentação de Uso

**Instruções de Invocação:**
- Automática: contextos que correspondem à `description`
- Explícita: "Use the [agent-name] agent para..."
- Via /agents: Interface interativa de gerenciamento

**Exemplos de Uso:**
Forneça 2-3 cenários específicos onde o agente deve ser usado

### Gerenciamento do Agente

**Criar/Editar:**
- Manual: Edite diretamente em `.claude/agents/` ou `~/.claude/agents/`
- Interativo: Use `/agents` para interface guiada

**Versionamento:**
- Agents de projeto: Commitar no git (compartilhado com time)
- Agents de usuário: Backup manual (pessoal)

**Resumable Agents (Avançado):**
- Cada execução gera `agentId` único
- Transcrição salva em `agent-{agentId}.jsonl`
- Resumir: passar `agentId` via parâmetro `resume`
- Use case: Análises longas, refinamento iterativo

## Relatório de Progresso

**Após criar o agente, confirme:**

✅ Arquivo criado em localização apropriada (`.claude/agents/` ou `~/.claude/agents/`)
✅ Frontmatter YAML válido
✅ System prompt completo e específico
✅ Ferramentas limitadas ao necessário
✅ Modelo selecionado adequadamente
✅ Descrição clara para invocação automática

**Próximos Passos:**
1. Testar o agente em cenário real
2. Ajustar `description` se invocação automática não funcionar
3. Refinar system prompt baseado em uso
4. Documentar casos de uso específicos
5. Considerar version control se for agente de projeto

## Referências Rápidas

**Campos Obrigatórios:**
- `name`: Identificador único
- `description`: Gatilho de invocação

**Campos Opcionais:**
- `tools`: Lista de ferramentas (omitir = todas)
- `model`: Modelo de IA (padrão: sonnet)
- `permissionMode`: Controle de permissões
- `skills`: Skills para auto-load

**Exemplos Built-in:**
- `general-purpose`: Tarefas complexas multi-step
- `plan`: Pesquisa durante plan mode
- `explore`: Busca rápida read-only

**Melhores Práticas:**
- ✅ Uma responsabilidade clara por agente
- ✅ Prompts detalhados com instruções e exemplos
- ✅ Limitar ferramentas ao estritamente necessário
- ✅ Versionar agents de projeto no git
- ❌ Evitar agentes genéricos "faz tudo"
- ❌ Evitar ferramentas desnecessárias
