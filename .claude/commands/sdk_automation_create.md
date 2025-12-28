# Criar PoC com Claude Code SDK Python

Cria scripts Python autocontidos para proof of concepts rápidos usando o Claude Code SDK em Python. Otimizado para funcionar imediatamente com Astral uv através de PEP 723 (inline dependencies). Carrega dinamicamente apenas as seções relevantes da documentação do SDK baseado no tipo de projeto do usuário, evitando sobrecarga de contexto. importante: não use EMOJIS

**Quando usar**: Use este comando quando precisar criar rapidamente um PoC funcional que interaja com Claude Code SDK Python, seja para automação simples, conversação contínua, custom tools, hooks ou MCP servers.

**Resultado esperado**: Script Python `.py` autocontido com PEP 723 que executa com `uv run script.py` sem configuração prévia de ambiente.

## Contexto & Variáveis

**Persona**: Engenheiro Python especializado em Claude Code SDK, focado em PoCs rápidos e funcionais. Domina async/await, streams, MCP servers, hooks e estruturas de dados do SDK.

**Gerenciador de Pacotes Padrão**: Astral UV (sempre usar em vez de pip/venv)

**Variáveis:**
- `$ARGUMENTS`: Descrição do PoC que o usuário quer criar

**Documentação de Referência:**
- **Arquivo completo**: `C:\Users\Lofrey\test\docs\claude_code_docs\claude_sdk_py_docs.md` (~2000 linhas)
- **Padrão UV**: `C:\Users\Lofrey\test\docs\uv_project_docs.md`
- **Estrutura principal** (sempre disponível):
  - **Installation**: `uv add claude-agent-sdk` (ou PEP 723 inline para scripts)
  - **query() vs ClaudeSDKClient**: escolha baseada em tipo de interação
    - `query()`: tasks one-off, sessões independentes
    - `ClaudeSDKClient`: conversas contínuas, multi-turn, contexto mantido
  - **ClaudeAgentOptions**: configuração principal (allowed_tools, system_prompt, mcp_servers, permission_mode, etc.)
  - **Message Types**: UserMessage, AssistantMessage, ResultMessage, TextBlock, ToolUseBlock
  - **Tools customizadas**: decorator `@tool` + `create_sdk_mcp_server()`
  - **Hooks**: PreToolUse, PostToolUse, UserPromptSubmit para modificar comportamento

## Instruções Principais

### 1. Análise da Requisição

Identifique o tipo de PoC:
- **Automação simples**: task único, execução independente
- **Conversação contínua**: multi-turn com contexto mantido
- **Custom tools**: ferramentas personalizadas via MCP
- **Hooks**: modificação de comportamento do SDK
- **MCP server**: servidor MCP customizado

Determine qual abordagem usar:
- `query()` para automação simples
- `ClaudeSDKClient` para conversação contínua
- `@tool` decorator para custom tools
- `HookMatcher` para hooks

### 2. Padrão de Gerenciamento de Projetos com UV

**SEMPRE usar Astral UV** em vez de pip/venv/poetry:

**A) Scripts Autocontidos (PEP 723 - Preferido para PoCs)**:
- Usar inline dependencies no próprio script
- Executar com `uv run script.py` (cria ambiente temporário automaticamente)
- Sem necessidade de venv ou setup prévio

**B) Projetos completos**:
```bash
uv init nome-do-projeto
cd nome-do-projeto
uv add claude-agent-sdk
uv run python script.py
```

**C) Instalação do UV** (se não tiver):
```bash
# Windows
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"

# macOS/Linux
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### 3. Carregamento Seletivo da Documentação

Carregue APENAS as seções relevantes de `claude_sdk_py_docs.md`:

**Para automação simples** → ler:
- Installation (linha 9-11)
- query() function (linha 52-97)
- ClaudeAgentOptions básico (linha 453-518)

**Para conversação contínua** → ler:
- ClaudeSDKClient class (linha 221-443)
- Continuing conversation example (linha 272-309)
- Advanced features (linha 1504-1708)

**Para custom tools/MCP** → ler:
- tool decorator (linha 99-157)
- create_sdk_mcp_server() (linha 159-218)
- Custom tools example (linha 1783-1866)

**Para hooks** → ler:
- Hook types (linha 940-1002)
- Hook usage example (linha 1004-1056)
- Using hooks section (linha 1576-1662)

### 4. Estrutura do Script Padrão

**PEP 723 (Obrigatório):**
```python
# /// script
requires-python = ">=3.10"
dependencies = [
    "claude-agent-sdk",
    "pydantic",
]
# ///
```

**Padrão de Imports:**
```python
import asyncio
from claude_agent_sdk import query, ClaudeAgentOptions  # ou ClaudeSDKClient
from typing import Any
```

### 5. Implementação Específica com UV

**A) Task One-Off (query) com PEP 723:**
```python
# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "claude-agent-sdk",
# ]
# ///

async def main():
    options = ClaudeAgentOptions(
        allowed_tools=["Read", "Write", "Bash"],
        permission_mode="acceptEdits",
        cwd="."
    )

    async for message in query(
        prompt="$DESCRICAO_DO_USUARIO",
        options=options
    ):
        print(message)

asyncio.run(main())
```

**Execução:**
```bash
uv run meu_script.py
```

**B) Conversação Contínua (ClaudeSDKClient) com PEP 723:**
```python
# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "claude-agent-sdk",
# ]
# ///

async def main():
    async with ClaudeSDKClient() as client:
        await client.query("$PRIMEIRA_PERGUNTA")

        async for message in client.receive_response():
            print(message)

        # Follow-up no mesmo contexto
        await client.query("$SEGUINDA_PERGUNTA")

        async for message in client.receive_response():
            print(message)

asyncio.run(main())
```

**Execução:**
```bash
uv run chat_conversation.py
```

**C) Custom Tools com PEP 723:**
```python
# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "claude-agent-sdk",
#     "pydantic",
# ]
# ///

from claude_agent_sdk import tool, create_sdk_mcp_server

@tool("nome", "descrição", {"param": tipo})
async def minha_tool(args: dict[str, Any]) -> dict[str, Any]:
    # implementação
    return {"content": [{"type": "text", "text": "resultado"}]}

server = create_sdk_mcp_server(
    name="meu-server",
    tools=[minha_tool]
)
```

**Execução:**
```bash
uv run custom_tools.py
```

**D) Hooks com PEP 723:**
```python
# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "claude-agent-sdk",
# ]
# ///

from claude_agent_sdk import HookMatcher

async def meu_hook(input_data, tool_use_id, context):
    # lógica do hook
    return {}

options = ClaudeAgentOptions(
    hooks={'PreToolUse': [HookMatcher(hooks=[meu_hook])]}
)
```

**Execução:**
```bash
uv run hooks_example.py
```

### 6. Diretrizes Técnicas com UV

**Async/Await:**
- Sempre usar `async def` para funções que chamam o SDK
- Usar `asyncio.run(main())` para entry point
- Iterar sobre responses com `async for`

**Gerenciamento de Dependências com UV:**
- **Scripts PEP 723**: Dependências inline no arquivo (recomendado para PoCs)
- **Projetos completos**: `uv init projeto && cd projeto && uv add claude-agent-sdk`
- **Execução**: `uv run script.py` (gerencia venv automaticamente)
- **Performance**: 10-100x mais rápido que pip

**Permission Mode:**
- `"acceptEdits"`: auto-aceita mudanças em arquivos
- `"bypassPermissions"`: sem prompts (cuidado)
- `"default"`: modo padrão interativo
- `"plan"`: planejamento apenas, sem execução

**Allowed Tools:**
- Comuns: `["Read", "Write", "Edit", "Bash", "Grep", "Glob"]`
- Custom tools: `["mcp__server__tool"]`

**CWD:**
- Sempre definir `cwd` em `ClaudeAgentOptions` para operar no diretório correto

## Validação & Qualidade

- [ ] Script autocontido (single-file) com PEP 723
- [ ] Usa Astral UV para gerenciamento de dependências (NUNCA pip/venv)
- [ ] Usa apenas features necessárias do SDK (não sobrecarregar)
- [ ] Código assíncrono correto com `async def` e `asyncio.run()`
- [ ] Permission mode apropriado para o PoC
- [ ] Executa com `uv run script.py` sem configuração prévia
- [ ] Comentários explicando integração com SDK e uso de UV

## Relatório de Entrega

Após criar o PoC, apresente:

1. **Script completo** com dependências PEP 723 (inline metadata)
2. **Comando exato** para execução com `uv run`
3. **Comandos UV** usados (se projeto completo)
4. **Partições da doc** consultadas (ex: "query() linhas 52-97")
5. **Explicação** de como o SDK e UV integram no PoC
6. **Notas importantes**: permissões, PEP 723, performance UV

**Exemplo de Estrutura:**

```markdown
## Script Criado: meu_poc.py

[CÓDIGO COMPLETO COM PEP 723 INLINE]

## Execução com UV
```bash
# Execução direta (PEP 723 cria venv temporário automaticamente)
uv run meu_poc.py
```

## Partições do SDK Usadas
- query() (linhas 52-97 da doc)
- ClaudeAgentOptions básico (linhas 453-518)
- Message types (linhas 764-843)

## Como Funciona
[EXPLICAÇÃO CONCISA INCLUINDO VANTAGENS DO UV]

## Notas Importantes
- PEP 723 elimina necessidade de venv manual
- UV é 10-100x mais rápido que pip
- Ambiente isolado criado automaticamente na execução
```
