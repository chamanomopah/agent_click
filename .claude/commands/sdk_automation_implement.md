# Implementar Evolução do PoC - Claude Code SDK v2

Cria versão evoluída do PoC baseada nas melhorias sugeridas pelo `/sdk_automation_evolve`. Use quando você tiver um relatório de evolução pronto e quiser gerar o código funcional automaticamente com features avançadas do SDK (custom tools, hooks, MCP servers, streaming, error handling). Siga ``Instruções`` para implementação das melhorias e veja os resultados em ``Relatório``.

## Contexto & Variáveis

**Persona**: Desenvolvedor Python Sênior especializado em Claude Code SDK, expert em implementar features avançadas (custom tools, MCP servers, hooks, streaming, error handling, retry logic, padrões async complexos).

**Variáveis:**
- `$ARGUMENTS`: Caminho para o arquivo PoC original ou relatório EVOLVE_REPORT.md

**Documentação de Referência:**
- **Arquivo completo**: `C:\Users\Lofrey\test\docs\claude_code_docs\claude_sdk_py_docs.md`
- **Conhecimento avançado** (carregar seções sob demanda):
  - Custom tools & MCP servers (linhas 99-218, 1783-1866)
  - Hooks & behavior modification (linhas 940-1056, 1576-1662)
  - ClaudeSDKClient avançado (linhas 221-443, 1504-1708)
  - Error handling (linhas 879-938)
  - Sandbox & segurança (linhas 1868-2010)
  - Structured outputs (linhas 520-534)

## Análise de Contexto

- **Complexidade**: alta (implementação de features avançadas SDK)
- **Interatividade**: média (lê relatório, implementa, valida)
- **Dependências**: claude-agent-sdk (novas features conforme necessário)
- **Validação Necessária**: sim (código funcional, testável)
- **Tipo Principal**: implementação de evolução com SDK avançado

## Instruções Principais

### 1. Leitura dos Arquivos

**Ler dois arquivos:**
1. **PoC original**: `[nome].py`
2. **Relatório de evolução**: `[nome]_EVOLVE_REPORT.md` (se existir)

Se o relatório não existir, pedir ao usuário para especificar as melhorias desejadas.

### 2. Parse das Melhorias a Implementar

**Do relatório, extrair:**
- Melhorias marcadas como "selecionadas" pelo usuário
- Fases de implementação (1, 2, 3)
- Features específicas do SDK necessárias

**Se não há relatório, perguntar:**
- "Quais melhorias você deseja implementar?"
- Apresentar opções baseadas em análise rápida do código

### 3. Carregamento Dinâmico da Documentação

**Carregar seções específicas baseado nas melhorias:**

**Se precisa custom tools:**
- Ler linhas 99-157 (`@tool` decorator)
- Ler linhas 159-218 (`create_sdk_mcp_server()`)
- Ler linhas 1783-1866 (exemplo completo)

**Se precisa hooks:**
- Ler linhas 940-1002 (Hook types)
- Ler linhas 1004-1056 (Hook usage example)
- Ler linhas 1576-1662 (Using hooks)

**Se precisa ClaudeSDKClient:**
- Ler linhas 221-443 (ClaudeSDKClient class)
- Ler linhas 1504-1574 (Continuous conversation interface)

**Se precisa error handling:**
- Ler linhas 879-938 (Error types)

**Se precisa sandbox/segurança:**
- Ler linhas 1868-2010 (Sandbox configuration)

### 4. Estratégia de Implementação

**Padrão de refatoração:**

**A) Manter compatibilidade:**
- Preservar funcionalidade core do PoC original
- Adicionar features sem quebrar comportamento existente
- Usar parâmetros opcionais para novos comportamentos

**B) Modularização:**
```python
# Estrutura recomendada
# /// script
# dependencies PEP 723
# ///

import asyncio
from typing import Any
from claude_agent_sdk import ClaudeSDKClient, ClaudeAgentOptions, ...

# Configuração
def create_options() -> ClaudeAgentOptions:
    """Centraliza configuração do SDK."""
    ...

# Custom tools (se aplicável)
@tool("nome", "desc", schema)
async def custom_tool(args: dict[str, Any]) -> dict[str, Any]:
    ...

# Hooks (se aplicável)
async def meu_hook(input_data, tool_use_id, context) -> dict[str, Any]:
    ...

# Classe principal
class MeuPocEvoluido:
    def __init__(self):
        ...

    async def run(self):
        ...

# Entry point
async def main():
    poc = MeuPocEvoluido()
    await poc.run()

asyncio.run(main())
```

**C) Implementação de Features:**

**Custom Tools:**
```python
from claude_agent_sdk import tool, create_sdk_mcp_server

@tool("process_data", "Process and analyze data", {"data": dict})
async def process_data(args: dict[str, Any]) -> dict[str, Any]:
    result = await process_logic(args['data'])
    return {
        "content": [{
            "type": "text",
            "text": f"Processed: {result}"
        }]
    }

server = create_sdk_mcp_server(
    name="data_processor",
    version="1.0.0",
    tools=[process_data]
)

options = ClaudeAgentOptions(
    mcp_servers={"processor": server},
    allowed_tools=["mcp__processor__process_data", ...]
)
```

**Hooks:**
```python
from claude_agent_sdk import HookMatcher

async def logging_hook(input_data, tool_use_id, context):
    tool_name = input_data.get('tool_name')
    print(f"[HOOK] Executing: {tool_name}")
    return {}

async def security_hook(input_data, tool_use_id, context):
    if input_data.get('tool_name') == 'Bash':
        cmd = input_data.get('tool_input', {}).get('command', '')
        if 'rm -rf' in cmd:
            return {
                'hookSpecificOutput': {
                    'hookEventName': 'PreToolUse',
                    'permissionDecision': 'deny',
                    'permissionDecisionReason': 'Dangerous command'
                }
            }
    return {}

options = ClaudeAgentOptions(
    hooks={
        'PreToolUse': [
            HookMatcher(hooks=[logging_hook]),
            HookMatcher(matcher='Bash', hooks=[security_hook])
        ]
    }
)
```

**ClaudeSDKClient com Contexto:**
```python
class ConversationManager:
    def __init__(self):
        self.client = ClaudeSDKClient(options=options)

    async def interactive_session(self):
        await self.client.connect()

        while True:
            user_input = input("\nYou: ")

            if user_input.lower() == 'exit':
                break

            # Claude mantém contexto de conversas anteriores
            await self.client.query(user_input)

            async for msg in self.client.receive_response():
                print(msg)

        await self.client.disconnect()
```

**Error Handling Avançado:**
```python
from claude_agent_sdk import CLINotFoundError, ProcessError, CLIConnectionError

async def safe_query(prompt: str, options: ClaudeAgentOptions, max_retries: int = 3):
    """Query com retry logic e error handling."""

    for attempt in range(max_retries):
        try:
            async for message in query(prompt=prompt, options=options):
                yield message
            return  # Sucesso, sair do retry loop

        except CLIConnectionError as e:
            print(f"Connection error (tentativa {attempt + 1}): {e}")
            if attempt < max_retries - 1:
                await asyncio.sleep(2 ** attempt)  # Exponential backoff
            else:
                raise

        except ProcessError as e:
            print(f"Process failed: {e.stderr}")
            raise
```

### 5. Geração do Novo Script

**Nome do arquivo**: `[nome]_evolved.py`

**Estrutura completa:**
1. Header PEP 723 com todas as dependências
2. Imports organizados
3. Docstring explicando evolução
4. Constantes de configuração
5. Custom tools (se aplicável)
6. Hooks (se aplicável)
7. Classes/funções modulares
8. Entry point robusto
9. Comentários explicando features SDK usadas

### 6. Validação e Testes

**Verificações automáticas:**
- [ ] Sintaxe Python válida
- [ ] Dependencies completas no PEP 723
- [ ] Imports corretos
- [ ] Async/await bem estruturado
- [ ] Error handling presente
- [ ] Type hints em funções públicas
- [ ] Docstrings em classes/funções principais

**Sugestão de teste manual:**
```bash
# Testar basic sanity
uv run [nome]_evolved.py --help  # se aplicável

# Testar execução normal
uv run [nome]_evolved.py
```

### 7. Documentação de Mudanças

**No topo do script evoluído, adicionar:**
```python
"""
PoC Evoluído: [Nome Original]

Evoluções Implementadas:
- ✅ [Melhoria 1] (CRÍTICA)
- ✅ [Melhoria 2] (IMPORTANTE)
- ✅ [Melhoria 3] (NICE-TO-HAVE)

Features do SDK Utilizadas:
- ClaudeSDKClient (sessões contínuas)
- Custom tools: [lista]
- Hooks: [lista]
- MCP servers: [lista]
- Error handling: [tipos]

Baseado em: [nome_original.py]
Relatório de evolução: [nome]_EVOLVE_REPORT.md
"""
```

## Critérios de Qualidade

- Código funcional e testável mentalmente
- Preserva funcionalidade do PoC original
- Adiciona features SDK de forma limpa
- Modular e reutilizável
- Error handling robusto
- Type hints e docstrings
- PEP 723 completo e correto
- Comentários explicando features SDK
- Executa com `uv run` sem issues

## Entrega & Finalização

Após implementação, apresente:

1. **Novo script**: `[nome]_evolved.py`
2. **Comando de execução**: `uv run [nome]_evolved.py`
3. **Resumo das evoluções**:
   - Melhorias implementadas (checklist)
   - Features SDK adicionadas
   - Impacto esperado
4. **Diff principal** (o que mudou)
5. **Próximos passos** (testes, validação)

## Relatório

Ao final, confirme:

1. **PoC original**: `[nome].py`
2. **Script evoluído**: `[nome]_evolved.py`
3. **Melhorias implementadas**: `[X críticas, Y importantes, Z nice-to-have]`
4. **Features SDK adicionadas**: `[lista]`
5. **Comando para testar**: `uv run [nome]_evolved.py`
6. **Diff resumido**: `[principais mudanças]`
