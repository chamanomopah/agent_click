---
description: Debug e teste de processos PM2 com análise de logs e correção automática
argument-hint: [nome-processo] [acao]
allowed-tools: Bash(pm2:*), Read, Edit, TodoWrite
---

# Debug PM2 - Teste e Correção de Processos

Comando para debug interativo de processos PM2. Analisa logs, identifica problemas, sugere correções e testa novamente. IMPORTANTE: SEMPRE QUE MODIFICAR UM ARQUIVO REINICIE-O NO PM2 USANDO O pm2 restart

## Uso
- `/pm2-debug [nome-processo]` - Analisa logs e status do processo
- `/pm2-debug [nome-processo] fix` - Tenta corrigir problemas automaticamente
- `/pm2-debug [nome-processo] restart` - Reinicia o processo e monitora

## Processo Ativo
**Nome do processo**: `$ARGUMENTS`

## 1. Análise Inicial

Verificar status atual do processo PM2:

\`\`\`bash
pm2 list | grep -i "$ARGUMENTS"
pm2 logs $ARGUMENTS --lines 50 --nostream
\`\`\`

## 2. Identificação de Problemas

Analisar os logs acima procurando por:

### Erros Comuns em Python
1. **UnicodeEncodeError** - Caracteres especiais em print()
   - Solução: Substituir caracteres unicode por ASCII
   - Localização: Procurar por `print("\u25")` ou caracteres especiais

2. **ModuleNotFoundError** - Dependências faltando
   - Solução: Instalar pacote com pip/pipx
   - Verificar requirements.txt ou pyproject.toml

3. **IndentationError/SyntaxError** - Erro de código
   - Solução: Ler arquivo, identificar linha com erro, corrigir

4. **Memory/CPU Issues** - Alto consumo de recursos
   - Comparar com outros processos
   - Verificar se há vazamento de memória

### Erros Comuns em Node.js
1. **Cannot find module** - Dependências faltando
   - Solução: npm install ou yarn install

2. **Port already in use** - Porta ocupada
   - Solução: Matar processo na porta ou trocar porta

3. **UnhandledPromiseRejection** - Erro assíncrono
   - Solução: Adicionar try/catch ou .catch()

## 3. Diagnóstico

Responda:

- **Status do processo**: [online/stopped/erro restarting]
- **Uptime**: [tempo de execução]
- **Restarts (↺)**: [número de reinícios]
- **Memória**: [consumo atual]
- **Erro identificado**: [descrição do erro]
- **Arquivo com erro**: [caminho completo se identificado]

## 4. Correção (se solicitado)

Se o usuário pediu `fix` ou se erro for óbvio:

### Passos para Corrigir

1. **Ler o arquivo** com o erro identificado
2. **Aplicar correção** usando Edit tool
3. **Reiniciar processo**:
   \`\`\`bash
   pm2 restart $ARGUMENTS
   pm2 save
   \`\`\`
4. **Aguardar 3 segundos** e verificar se estabilizou
5. **Verificar logs** novamente para confirmar

### Técnicas de Correção

**Para UnicodeEncodeError:**
\`\`\`python
# ANTES (com erro)
print("━━━━━━━━━━━━━━━━━━")

# DEPOIS (corrigido)
print("=" * 50)
\`\`\`

**Para quebras de linha quebrando comandos:**
\`\`\`python
# ANTES
prompt_completo = f"{texto}{contexto}"  # contexto tem \n\n

# DEPOIS
prompt_completo = f"{texto}{contexto}".replace('\n', ' ')
\`\`\`

## 5. Validação e Teste

Após correção, executar:

\`\`\`bash
pm2 list | grep -i "$ARGUMENTS"
\`\`\`

### Critérios de Sucesso
- ✓ Processo estável sem reinícios constantes
- ✓ Uptime crescente (não resetando para 0s)
- ✓ Memória dentro do esperado (comparar com processos similares)
- ✓ Sem erros no log de erro
- ✓ Logs de output mostrando funcionamento normal

### Critérios de Falha
- ✗ Processo reiniciando infinitamente (↺ aumentando)
- ✗ Uptime travado em 0s
- ✗ Memória anormalmente baixa (não carregou) ou alta (vazamento)
- ✗ Erros recorrentes no log

## 6. Relatório Final

Após análise/correção, apresente:

### Resumo
- **Processo**: $ARGUMENTS
- **Status Final**: [Funcionando/Com problemas/Corrigido]
- **Ações Realizadas**: [lista de mudanças]

### Mudanças Aplicadas
- [ ] Arquivo(s) modificado(s)
- [ ] Linha(s) alterada(s)
- [ ] Motivo da mudança

### Próximos Passos
- Se funcionando: Monitorar por 1-2 minutos para confirmar estabilidade
- Se com problemas: Investigar causa raiz mais profundamente
- Sugerir melhorias de código ou arquitetura se aplicável

## 7. Monitoramento Contínuo

Para monitoramento em tempo real:
\`\`\`bash
pm2 monit
\`\`\`

Para logs em tempo real:
\`\`\`bash
pm2 logs $ARGUMENTS
\`\`\`

## Exemplo de Uso Completo

\`\`\`
/pm2-debug personal-agent
→ Analisa logs, encontra UnicodeEncodeError na linha 260
→ Lê arquivo 4_personal_agent.py
→ Substitui caracteres especiais por ASCII
→ Reinicia processo
→ Confirma que uptime agora é estável
→ Relata sucesso
\`\`\`

## Notas Importantes

- **Sempre usar `pm2 save`** após mudanças
- **Documentar mudanças** para referência futura
- **Comparar com processos similares** para identificar anomalias
- **Verificar consumo de memória** após restart inicial (modelos IA levam tempo para carregar)
- **Logs do PM2 ficam** em `C:\.pm2\logs\` no Windows
