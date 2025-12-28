# Debug PoC - Claude Code SDK

Depura e resolve problemas em scripts Python que usam Claude Code SDK. Use quando o PoC estiver falhando, retornando erros, ou comportamento inesperado. Foca em diagnosticar issues com CLI connection, process errors, MCP servers, custom tools, hooks e configuração do SDK.

## Contexto & Variáveis

**Persona**: Especialista em debugging Python/Claude Code SDK, expert em rastrear erros de CLI, MCP, async/await, hooks, custom tools e configurações do SDK.

**Variáveis:**
- `$ARGUMENTS`: Caminho para o script Python com problema (ex: `meu_poc.py`)

**Documentação de Referência:**
- **SDK completo**: `C:\Users\Lofrey\test\docs\claude_code_docs\claude_sdk_py_docs.md`
- **Error handling** (linhas 879-938)
- **Common issues** (linhas 1150-1250)
- **CLI connection** (linreas 221-443)

## Análise de Contexto

- **Complexidade**: variável (depende do erro)
- **Interatividade**: alta (diagnóstico iterativo)
- **Dependências**: claude-agent-sdk, estrutura do PoC
- **Validação Necessária**: sim (encontrar root cause)
- **Tipo Principal**: debugging e resolução de problemas

## Instruções Principais

### 1. Leitura e Análise Inicial

**Ler o script com problema:**
1. Verificar sintaxe Python básica
2. Identificar imports do SDK usados
3. Verificar estrutura async/await
4. Checar configuração `ClaudeAgentOptions`

**Perguntas chave:**
- "Qual erro você está vendo?" (se usuário não informou)
- "Em que linha falha?"
- "Qual comando você usa para rodar?"

### 2. Execução de Diagnóstico

**Rodar o script e capturar output:**
```bash
python [script].py
# ou
uv run [script].py
```

**Capturar traceback completo** para análise.

### 3. Categorização do Problema

**A) CLI Connection Issues:**
- Erro: `CLINotFoundError`, `CLIConnectionError`
- Sintomas: "Claude Code CLI not found", "Failed to connect"
- Causas comuns:
  - CLI não instalado ou não no PATH
  - Versão incompatível do CLI
  - Permissões insuficientes

**B) Process Errors:**
- Erro: `ProcessError`, timeout, subprocess failure
- Sintomas: "Process terminated unexpectedly", hanging
- Causas comuns:
  - Script inválido no CLI
  - Timeout de execução
  - Recursos insuficientes

**C) MCP Server Issues:**
- Erro: Ferramentas MCP não funcionam
- Sintomas: "Tool not found", "MCP server error"
- Causas comuns:
  - `create_sdk_mcp_server()` mal configurado
  - Tool names incorretos em `allowed_tools`
  - Server não registrado em `mcp_servers`

**D) Custom Tool Issues:**
- Erro: `@tool` decorator falha
- Sintomas: "Tool validation failed", "Invalid tool schema"
- Causas comuns:
  - Schema JSON incorreto
  - Função não é async
  - Return type incorreto

**E) Hook Issues:**
- Erro: Hooks não executam ou quebram
- Sintomas: Comportamento inesperado, erros em hooks
- Causas comuns:
  - `HookMatcher` mal configurado
  - Return type incorreto do hook
  - Event name errado em `hooks={}`

**F) Async/Await Issues:**
- Erro: RuntimeWarning, coroutine não awaited
- Sintomas: "coroutine was never awaited"
- Causas comuns:
  - Falta `await` em funções async
  - `asyncio.run()` não chamado
  - Mixed sync/async code

**G) Dependency Issues:**
- Erro: ImportError, ModuleNotFoundError
- Sintomas: "No module named 'claude_agent_sdk'"
- Causas comuns:
  - SDK não instalado
  - Versão errada no PEP 723
  - Virtual environment não ativado

### 4. Estratégia de Debug por Categoria

**Para CLI Connection:**
1. Verificar instalação:
   ```bash
   claude --version
   ```
2. Checar PATH:
   ```bash
   where claude  # Windows
   which claude  # Linux/Mac
   ```
3. Testar connection manual:
   ```python
   from claude_agent_sdk import ClaudeSDKClient, ClaudeAgentOptions
   options = ClaudeAgentOptions()
   client = ClaudeSDKClient(options=options)
   await client.connect()
   print("Connected!")
   ```

**Para Process Errors:**
1. Adicionar timeout explícito:
   ```python
   options = ClaudeAgentOptions(
       timeout_ms=30000  # 30 segundos
   )
   ```
2. Verificar script que está sendo passado:
   ```python
   # Log do script gerado
   print("Generated script:", script_content)
   ```

**Para MCP Servers:**
1. Verificar server registration:
   ```python
   # Errado
   options = ClaudeAgentOptions(
       mcp_servers={"my_server": server},
       allowed_tools=["my_tool"]  # ❌ Faltou prefixo
   )

   # Correto
   options = ClaudeAgentOptions(
       mcp_servers={"my_server": server},
       allowed_tools=["mcp__my_server__my_tool"]  # ✅
   )
   ```
2. Debug MCP server:
   ```python
   server = create_sdk_mcp_server(
       name="debug_server",
       version="1.0.0",
       tools=[my_tool]
   )
   print("Server tools:", server.tools)
   ```

**Para Custom Tools:**
1. Validar schema:
   ```python
   from typing import Any
   import json

   @tool("nome", "descrição", {"param": "string"})
   async def my_tool(args: dict[str, Any]) -> dict[str, Any]:
       # Schema deve ser JSON válido
       # Return deve ter estrutura correta
       return {
           "content": [{
               "type": "text",
               "text": "Resultado"
           }]
       }
   ```
2. Testar tool isolado:
   ```python
   result = await my_tool({"param": "teste"})
   print(result)
   ```

**Para Hooks:**
1. Verificar hook structure:
   ```python
   async def my_hook(input_data, tool_use_id, context):
       # Deve retornar dict vazio se não veto
       return {}

       # OU veto
       return {
           'hookSpecificOutput': {
               'hookEventName': 'PreToolUse',
               'permissionDecision': 'deny',
               'permissionDecisionReason': 'Razão'
           }
       }
   ```
2. Debug hook execution:
   ```python
   async def debug_hook(input_data, tool_use_id, context):
       print(f"[HOOK DEBUG] input_data: {input_data}")
       print(f"[HOOK DEBUG] tool_use_id: {tool_use_id}")
       print(f"[HOOK DEBUG] context: {context}")
       return {}
   ```

**Para Async/Await:**
1. Verificar entry point:
   ```python
   # Errado
   async def main():
       ...
   main()  # ❌

   # Correto
   async def main():
       ...
   asyncio.run(main())  # ✅
   ```
2. Verificar todas as chamadas async:
   ```python
   # Errado
   result = query(...)  # ❌

   # Correto
   async for msg in query(...):  # ✅
       print(msg)
   ```

### 5. Geração de Script Corrigido

**Nome**: `[nome]_fixed.py`

**Adicionar debug logging:**
```python
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

logger.debug("Iniciando configuração...")
logger.debug(f"Options: {options}")
```

**Adicionar error handling robusto:**
```python
from claude_agent_sdk import (
    CLINotFoundError,
    ProcessError,
    CLIConnectionError
)

async def safe_main():
    try:
        await run_poc()
    except CLINotFoundError as e:
        print(f"❌ CLI não encontrado: {e}")
        print("💡 Instale com: npm install -g @anthropic-ai/claude-code")
    except CLIConnectionError as e:
        print(f"❌ Erro de conexão: {e}")
        print("💡 Verifique: claude --version")
    except ProcessError as e:
        print(f"❌ Erro no processo: {e}")
        if e.stderr:
            print(f"Stderr: {e.stderr}")
    except Exception as e:
        print(f"❌ Erro inesperado: {type(e).__name__}: {e}")
        raise

asyncio.run(safe_main())
```

### 6. Validação da Correção

**Testar script corrigido:**
```bash
python [nome]_fixed.py
```

**Verificar:**
- [ ] Executa sem crashes
- [ ] Produz output esperado
- [ ] Mensagens de erro claras se houver problemas
- [ ] Logs úteis para debug futuro

### 7. Documentação do Problema

**Criar `[nome]_DEBUG_REPORT.md`:**
```markdown
# Debug Report: [nome].py

## Problema Encontrado
- **Tipo**: [CLI Connection / Process Error / MCP / etc]
- **Erro Original**: `[traceback]`
- **Root Cause**: `[explicação]`

## Solução Aplicada
- **Mudança 1**: `[descrição]`
- **Mudança 2**: `[descrição]`

## Validação
- ✅ Script corrigido: `[nome]_fixed.py`
- ✅ Teste executado com sucesso

## Lições Aprendidas
- `[o que evitar no futuro]`
```

## Critérios de Qualidade

- Identifica root cause corretamente
- Aplica solução mínima e efetiva
- Preserva funcionalidade existente
- Adiciona logging útil sem excesso
- Error handling robusto
- Documenta problema e solução
- Script corrigido é testável

## Entrega & Finalização

Após debug, apresente:

1. **Problema identificado**: [tipo e descrição]
2. **Root cause**: [explicação técnica]
3. **Script corrigido**: `[nome]_fixed.py`
4. **Mudanças aplicadas**:
   - Linha X: [mudança]
   - Linha Y: [mudança]
5. **Comando para testar**: `python [nome]_fixed.py`
6. **Debug report** (se aplicável): `[nome]_DEBUG_REPORT.md`
7. **Recomendações** para evitar no futuro

## Relatório

Ao final, confirme:

1. **Script original**: `[nome].py`
2. **Problema**: `[tipo]`
3. **Causa raiz**: `[explicação]`
4. **Script corrigido**: `[nome]_fixed.py`
5. **Teste**: `[✅ passou / ❌ falhou]`
6. **Próximos passos**: `[validação, monitoramento, etc]`
