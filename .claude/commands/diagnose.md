---
description: Analisa app inteiro, identifica problema e cria checklist de solução
argument-hint: "[descrição-do-problema]"
allowed-tools: Read, Glob, Grep, Bash, TodoWrite, Write
---

# Diagnóstico Técnico e Plano de Ação

Realiza análise completa do código fonte para identificar a causa raiz de problemas e gera um plano estruturado de resolução sem fazer modificações automáticas. Use este comando quando encontrar bugs, comportamentos inesperados, ou precisar entender como uma funcionalidade está implementada antes de modificá-la.

O resultado inclui análise detalhada, localização exata do problema, e um checklist executável. Consulte ``Instruções Principais`` para o fluxo de trabalho e ``Relatório de Diagnóstico`` para ver o formato de saída.

## Contexto & Variáveis

**Descrição do Problema**: Argumento fornecido pelo usuário descrevendo o sintoma ou problema encontrado

**Escopo da Análise**: Codebase completa do projeto no diretório atual

**Output Esperado**:
1. Relatório detalhado de diagnóstico
2. Checklist de tarefas para resolução
3. Arquivo de diagnóstico salvo em disco

## Instruções Principais

### 1. Compreensão do Problema

Analise a descrição fornecida pelo usuário e documente:
- **Sintoma**: O que está acontecendo de errado
- **Comportamento Esperado**: O que deveria acontecer
- **Comportamento Atual**: O que está realmente acontecendo
- **Contexto de Uso**: Quando/em que situação o problema ocorre
- **Componentes Suspeitos**: Quais partes do sistema podem estar envolvidas

### 2. Análise da Codebase

Execute investigação sistemática da arquitetura:

**Stack Tecnológico:**
- Identifique linguagens, frameworks e bibliotecas principais
- Liste dependências críticas (package.json, requirements.txt, go.mod, etc.)
- Determine padrões arquiteturais (MVC, microservices, monolito, etc.)

**Estrutura do Projeto:**
- Mapeie diretórios principais e seus propósitos
- Identifique pontos de entrada (main.js, index.py, app.go, etc.)
- Encontre arquivos de configuração relevantes
- Localize rotas, controllers, models, views

### 3. Localização da Causa Raiz

Use ferramentas de busca para rastrear o problema:

**Busca por Palavras-chave:**
```bash
# Termos relacionados ao sintoma
Grep: <termos-do-problema>

# Funções ou métodos suspeitos
Grep: <nome-funcao-ou-metodo>

# Mensagens de erro ou log
Grep: <mensagem-erro-específica>
```

**Rastreamento de Fluxo:**
- Identifique onde a funcionalidade problemática é chamada
- Siga o fluxo de execução através dos arquivos
- Encontre onde o comportamento inesperado ocorre
- Aponte arquivo:linha específica do problema

**Análise de Código:**
- Leia os arquivos relevantes completamente
- Identifique lógica incorreta, edge cases, ou bugs
- Verifique tratamento de erros, validações, e edge cases

### 4. Pesquisa de Soluções

Busque referências internas e externas:

**Dentro da Codebase:**
- Encontre soluções similares já implementadas
- Identifique padrões de código usados no projeto
- Veja como problemas parecidos foram resolvidos
- Consulte documentação local (README, docs/, etc.)

**Boas Práticas:**
- Considere padrões da linguagem/framework usado
- Avalie abordagens comuns para este tipo de problema
- Considere implicações de performance e segurança

### 5. Criação do Checklist de Solução

Use a ferramenta ``TodoWrite`` para criar plano estruturado:

**Estrutura das Tarefas:**
- **Título**: Descrição clara e acionável
- **Arquivos Específicos**: Quais arquivos modificar
- **Alterações Necessárias**: O que mudar em cada arquivo
- **Ordem Lógica**: Dependências entre tarefas
- **Validação**: Como verificar que funcionou

**Exemplo de Tarefa:**
```
content: "Corrigir validação de entrada no formulário de login"
activeForm: "Corrigindo validação de entrada no formulário de login"
status: "pending"
```

### 6. Geração do Relatório de Diagnóstico

Crie arquivo estruturado com todos os resultados:

**Nome do Arquivo:**
```
diagnostic_<timestamp>_<problema-resumido>.md
```

**Conteúdo do Relatório:**
- Resumo executivo do problema
- Análise da arquitetura
- Localização exata da causa raiz
- Estratégia de solução proposta
- Checklist completo de tarefas
- Arquivos analisados durante o diagnóstico
- Referências e notas adicionais

### 7. Apresentação dos Resultados

Apresente ao usuário:

1. **Resumo Visual**: Breve explicação do que foi encontrado
2. **Localização do Problema**: Arquivo:linha específico
3. **Plano de Ação**: Checklist criado com ``TodoWrite``
4. **Arquivo Gerado**: Caminho completo do relatório salvo
5. **Próximos Passos**: Como proceder com a resolução

## Restrições de Execução

**O QUE FAZER:**
- ✅ Analisar código completamente
- ✅ Identificar causa raiz do problema
- ✅ Buscar soluções e referências
- ✅ Criar checklist detalhado
- ✅ Gerar relatório em arquivo
- ✅ Usar TodoWrite para organizar tarefas

**O QUE NÃO FAZER:**
- ❌ NÃO execute código automaticamente
- ❌ NÃO faça modificações nos arquivos
- ❌ NÃO instale dependências
- ❌ NÃO rode testes automaticamente
- ❌ NÃO aplique correções sem aprovação

## Relatório de Diagnóstico

O relatório gerado deve seguir esta estrutura:

```markdown
# 📋 Relatório de Diagnóstico Técnico

**Data**: YYYY-MM-DD HH:MM:SS
**Problema**: <descrição-original-do-problema>
**Arquivo**: diagnostic_<timestamp>_<problema-resumido>.md

---

## 🎯 Resumo Executivo

<Descrição clara e concisa do problema em 2-3 frases>

---

## 🏗️ Análise da Arquitetura

### Stack Tecnológico
- **Linguagem**: <lang>
- **Framework**: <framework>
- **Dependências Principais**: <lista>

### Estrutura do Projeto
```
<arvore-simplificada-do-projeto>
```

### Componentes Principais
- <Componente 1>: <descrição>
- <Componente 2>: <descrição>

---

## 🔍 Investigação Realizada

### Sintomas Observados
- <Sintoma 1>
- <Sintoma 2>

### Fluxo de Execução Rastreado
1. <Ponto A>: <o que acontece>
2. <Ponto B>: <o que acontece>
3. <Ponto C>: <o que falha>

### Arquivos Analisados
- `caminho/arquivo1.ext`: <motivo da análise>
- `caminho/arquivo2.ext`: <motivo da análise>

---

## 🎯 Causa Raiz Identificada

### Localização Exata
- **Arquivo**: `caminho/do/arquivo.ext:linha`
- **Função/Método**: `nomeFuncao()`
- **Classe/Componente**: `NomeClasse`

### Explicação Técnica
<Descrição detalhada de por que o problema ocorre>

### Código Problemático
```linguagem
<snippet do código com bug>
```

### Análise do Problema
- <O que está errado>
- <Por que está errado>
- <Quando acontece>

---

## 💡 Estratégia de Solução Proposta

### Abordagem Geral
<Descrição da estratégia para corrigir o problema>

### Por Que Esta Solução
<Justificativa da abordagem escolhida>

### Impactos Esperados
- **Mudanças**: <quais arquivos serão modificados>
- **Riscos**: <riscos potenciais>
- **Benefícios**: <melhorias esperadas>

---

## ✅ Checklist de Execução

<TODO list gerada com TodoWrite - cada item com título, descrição, arquivos envolvidos, validação>

### Ordem de Execução
1. <Tarefa 1>: <descrição>
2. <Tarefa 2>: <descrição>
3. <Tarefa 3>: <descrição>

### Validação por Tarefa
- <Tarefa 1>: <como verificar que funcionou>
- <Tarefa 2>: <como verificar que funcionou>

---

## 📚 Referências e Padrões

### Soluções Similares no Projeto
- `caminho/arquivo.similar`: <como resolveu problema parecido>

### Boas Práticas Aplicadas
- <Prática 1>: <referência>
- <Prática 2>: <referência>

### Documentação Consultada
- <doc1>: <link ou caminho>
- <doc2>: <link ou caminho>

---

## 📝 Notas Adicionais

<Observações importantes, edge cases, considerações de performance, segurança, etc>

---

## 🚀 Próximos Passos

1. **Revisar Checklist**: Avaliar as tarefas propostas
2. **Aprovar Plano**: Confirmar que a estratégia está correta
3. **Executar Tarefas**: Seguir o checklist em ordem
4. **Validar Cada Passo**: Testar após cada modificação
5. **Testes Completos**: Executar suite de testes ao final

---

**Relatório gerado automaticamente pelo comando /diagnose**
**Análise realizada por**: Claude (Sonnet 4.5)
```

## Validação da Qualidade

Antes de finalizar, verifique:

- [ ] Problema foi claramente entendido e documentado
- [ ] Codebase foi explorada adequadamente
- [ ] Causa raiz foi localizada com arquivo:linha específico
- [ ] Soluções similares foram pesquisadas no projeto
- [ ] Checklist está detalhado e executável
- [ ] Relatório foi salvo em arquivo com nome apropriado
- [ ] Nenhuma modificação foi feita automaticamente
- [ ] Usuário recebeu explicação clara do próximo passo

## Exemplo de Uso

```bash
# Usuário encontra um bug
/diagnose "O formulário de login não está validando email incorreto"

# Comando irá:
# 1. Analisar a codebase para encontrar formulários/login
# 2. Identificar onde está a validação de email
# 3. Localizar o bug exato (arquivo:linha)
# 4. Buscar outras validações no projeto como referência
# 5. Criar checklist com passos para corrigir
# 6. Salvar relatório completo em arquivo
# 7. Apresentar plano de ação ao usuário
# 8. Aguardar aprovação para executar correções
```

## Notas Importantes

- Este comando é **apenas para diagnóstico e planejamento**
- Nenhuma modificação automática é feita nos arquivos
- O usuário mantém controle total sobre quando executar correções
- O arquivo de diagnóstico serve como documentação permanente
- O checklist criado pode ser executado passo a passo
