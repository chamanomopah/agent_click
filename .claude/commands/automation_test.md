---
description: Testa arquivos criados/selecionados e limpa após conclusão
argument-hint: [arquivos]
allowed-tools: Bash, Read, Write, Edit, Delete
---

# Especialista em Testes e Limpeza

## Contexto
Você deve testar os arquivos especificados pelo usuário e garantir que tudo funcione corretamente antes de limpar.

## Arquivos para Testar
{{args}}

## Seu Trabalho

### 1. IDENTIFICAÇÃO
Liste todos os arquivos que serão testados:
- Arquivos passados como argumento
- Arquivos criados recentemente (se nenhum argumento)

### 2. TESTE OBRIGATÓRIO
Para cada arquivo identificado, execute:

**Arquivos de Código (.js, .py, .ts, .java, etc):**
- Verificar sintaxe
- Testar execução básica
- Validar imports/dependências

**Arquivos de Configuração (.json, .yaml, .xml, etc):**
- Validar estrutura
- Verificar campos obrigatórios
- Testar parse

**Arquivos de Texto/Markdown (.md, .txt):**
- Verificar formatação
- Validar links/referências

**Outros tipos:**
- Validar integridade do arquivo
- Verificar se abre corretamente

### 3. RELATÓRIO
Apresente resultados em formato claro:
```
✅ nome_arquivo.js - Sintaxe válida, executa sem erros
❌ config.json - Erro: campo 'api_key' ausente
⚠️  script.py - Aviso: dependência 'requests' não instalada
```

### 4. CONFIRMAÇÃO
Pergunte ao usuário:
```
Todos os testes foram concluídos.
Resultados: [X] aprovados, [Y] reprovados
Deseja limpar os arquivos de teste? (s/n)
```

### 5. LIMPEZA
Se usuário confirmar:
- Apagar TODOS os arquivos testados
- Remover diretórios temporários criados
- Deixar workspace limpo

## IMPORTANTE
- NÃO pule testes
- NÃO limpe ANTES de confirmar com usuário
- NÃO deixe arquivos temporários após limpeza
- SEMPRE mostre resultados antes de perguntar sobre limpeza
