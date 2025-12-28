# Criar Skill Personalizada para Claude Code

Cria Skills personalizadas para Claude Code seguindo melhores práticas da documentação oficial. Use quando precisar automatizar tarefas repetitivas, encapsular conhecimento específico do projeto, ou criar fluxos de trabalho padronizados.

**Resultado:** Estrutura completa de diretórios com arquivo SKILL.md válido, frontmatter YAML configurado corretamente, e documentação detalhada de uso.

## Contexto & Variáveis

**Localização:**
- Skills do projeto: `.claude/skills/[nome-da-skill]/` (compartilhadas com o time)
- Skills pessoais: `~/.claude/skills/[nome-da-skill]/` (uso individual)

**Contexto da Skill:**
- **Propsito:** [Descreva o que a Skill deve fazer]
- **Disparadores:** [Quando Claude deve invocar esta Skill]
- **Resultado esperado:** [O que a Skill entrega]

## Instruções Principais

### 1. Preparação & Análise

**Defina o escopo da Skill:**
- Identifique uma responsabilidade única e clara
- Liste os cenários de uso concretos
- Determine palavras-chave que disparariam a invocação

**Exemplo de escopo válido:**
- ❌ RUIM: "Skill de documentação" (muito vago)
- ✅ BOM: "Extrair texto e tabelas de PDFs, preencher formulários, mesclar documentos" (específico)

### 2. Criação da Estrutura

**Crie a estrutura de diretórios:**
```bash
.claude/skills/nome-da-skill/
├── SKILL.md              (OBRIGATÓRIO)
├── reference.md          (opcional: docs adicionais)
├── examples.md           (opcional: mais exemplos)
├── scripts/              (opcional: utilitários)
│   └── helper.py
└── templates/            (opcional: templates)
    └── template.txt
```

### 3. Configuração do Frontmatter YAML

**Crie o arquivo SKILL.md com frontmatter obrigatório:**
```yaml
---
name: nome-da-skill-minusculo-com-hifens
description: |
  Descrição ESPECÍFICA que responde:
  - O QUE a Skill faz (ações concretas)
  - QUANDO usá-la (sinais de disparo)
  - Palavras-chave que o usuário mencionaria

  Máximo 1024 caracteres.
allowed-tools: Read, Write, Bash, Grep, Glob  (opcional)
---

Conteúdo markdown com instruções detalhadas...
```

**Regras do frontmatter:**
- `name`: obrigatório, minúsculas, hífens instead of espaços
- `description`: obrigatório, específico com palavras-chave
- `allowed-tools`: opcional, use para restringir ferramentas por segurança

### 4. Descrição Efetiva

**Use o formato "O QUE + QUANDO":**
- ✅ BOM: "Extrair texto e tabelas de PDFs, preencher formulários, mesclar documentos. Use quando working with PDF files ou usuário mencionar PDFs, forms, ou document extraction."
- ❌ RUIM: "Helps with documents" (genérico, sem contexto)

**Inclua sinais de disparo:**
- Ações que o usuário executa
- Tipos de arquivos mencionados
- Problemas específicos que resolve

### 5. Conteúdo do Corpo SKILL.md

**Estrutura recomendada:**
```markdown
# Título Descritivo

## Propósito
[O que esta Skill faz em 1-2 frases]

## Quando Usar
[Critérios claros de invocação]

## Instruções
[Passo a passo detalhado]

## Exemplos
[Casos de uso concretos]

## Casos Especiais
[Edge cases e exceções]

## Referências
[Arquivos adicionais, se aplicável]
```

**Melhores práticas:**
- Instruções claras e passo-a-passo
- Exemplos concretos de uso
- Casos especiais e edge cases
- Progressive disclosure: referencie arquivos adicionais que Claude carrega sob demanda

### 6. Segurança (allowed-tools)

**Use para restringir ferramentas:**
- Skills read-only: `allowed-tools: Read, Grep, Glob`
- Skills de execução: adicione `Bash`
- Skills de modificação: adicione `Write, Edit`

**Se omitido:**
- Claude pedirá permissão normalmente para cada ferramenta

### 7. Validação & Teste

**Verifique a estrutura:**
```bash
# Valide o YAML
cat .claude/skills/nome-da-skill/SKILL.md

# Teste com debug
claude --debug
```

**Checklist de validação:**
- [ ] Frontmatter YAML válido (sem tabs, indentação correta)
- [ ] Description específica com palavras-chave relevantes
- [ ] Arquivos no caminho correto (.claude/skills/ ou ~/.claude/skills/)
- [ ] Uma responsabilidade clara por Skill
- [ ] Instruções executáveis e testáveis

**Teste de invocação:**
- Faça perguntas que correspondam à descrição
- Verifique se Claude invoca a Skill automaticamente
- Valide o resultado esperado

## Entrega & Finalização

**Entregáveis esperados:**
1. Estrutura completa de diretórios criada
2. Arquivo SKILL.md com frontmatter YAML válido
3. Conteúdo markdown com instruções detalhadas
4. Scripts/arquivos de suporte (se aplicável)
5. Comando para testar a Skill

**Documentação adicional:**
- Registrar no README do projeto (se for Skill compartilhada)
- Adicionar exemplos de uso na documentação
- Compartilhar com o time (se aplicável)

## Relatório de Progresso

Após criar a Skill:

**Confirmação de criação:**
- [ ] Estrutura de diretórios criada em `[localização]/skills/[nome]/`
- [ ] SKILL.md com frontmatter válido
- [ ] Description específica e acionável
- [ ] Instruções testadas e validadas

**Comandos úteis:**
```bash
# Verificar Skills instaladas
ls -la .claude/skills/

# Testar Skill específica
claude --help | grep [nome-da-skill]

# Debug de carregamento
claude --debug
```

## Debugging & Troubleshooting

**Skill não é invocada:**
- Verifique se a description contém palavras-chave que o usuário usaria
- Teste com perguntas que correspondam exatamente à descrição
- Confirme que o arquivo está no local correto

**Erros de YAML:**
- Use YAML validator online
- Verifique indentação (espaços, não tabs)
- Confirme que o frontmatter está entre `---`

**Permissões de ferramentas:**
- Skills sem `allowed-tools` pedem permissão normalmente
- Use `allowed-tools` apenas para restringir acesso
- Verifique se as ferramentas necessárias estão incluídas