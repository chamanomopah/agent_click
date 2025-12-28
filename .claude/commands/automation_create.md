# Criar Scripts de Automação Zero-Config com Astral uv

Cria scripts Python autocontidos para automação global no Windows (hotkeys e comandos de voz) que invocam o Claude Code CLI. Os scripts seguem o padrão PEP 723 para gerenciamento de dependências via Astral uv, permitindo execução imediata sem configuração prévia. Este comando é ideal quando você precisa criar gatilhos físicos (teclas) ou virtuais (voz) para ativar agentes de IA de forma transparente e em background.

Siga as `Instruções Principais` para entender o fluxo de análise e criação. Consulte `Variáveis` para personalizar o comportamento do script. O resultado final é entregue conforme `Relatório de Entrega`.

## Análise de Contexto do Comando

- **Complexidade**: média (envolve hooks de sistema, processamento de áudio e subprocessos)
- **Interatividade**: híbrido (requer input do usuário para especificar a ideia, mas execução é automática)
- **Dependências**: externas (bibliotecas Python: keyboard, sounddevice, openai-whisper, numpy)
- **Validação Necessária**: parcial (requer teste do hook global e execução independente)
- **Tipo Principal**: implementação de automação + configuração de ambiente

## Contexto & Variáveis

**Persona**: Engenheiro de Automação de Sistemas Sênior, especializado em arquitetura de software para produtividade e integração profunda entre Hardware-SO-IA. Filosofia: scripts "zero-config", alto desempenho (low latency) e portabilidade total via Astral uv.

**Variáveis:**
- `$ARGUMENTS`: Ideia do usuário para o script de automação (descrição do trigger desejado)

**Objetivo Operacional**: Criar scripts Python que sirvam como gatilhos (triggers) globais no Windows para ativar o Claude Code (CLI) ou outros agentes. Scripts devem rodar em segundo plano e reagir a inputs físicos (teclas/áudio) sem necessidade de interação manual com o terminal até que a IA seja invocada.

## Instruções Principais

### 1. Análise da Requisição
- Ler a ideia fornecida em `$ARGUMENTS`
- Identificar o tipo de trigger (hotkey, comando de voz, ou híbrido)
- Determinar bibliotecas necessárias para o caso de uso específico

### 2. Arquitetura do Script
Aplicar as **Diretrizes Técnicas Obrigatórias (The Golden Rules)**:

**Gerenciamento de Dependências (PEP 723):**
- Todo script deve conter o bloco de metadados `# /// script` no topo
- Listar rigorosamente todas as dependências necessárias
- Garantir execução com `uv run script.py` (sem instalação prévia)

**Interface de Sistema (Windows):**
- Utilizar `subprocess.run` para invocar o Claude Code
- Prefixar comando com `start cmd /k` para nova janela de terminal independente
- Manter script de automação rodando em background

**Captura Global (Hotkeys):**
- Utilizar biblioteca `keyboard` para registrar ganchos (hooks) de sistema
- Garantir funcionamento independentemente de qual janela está em foco

**Pipeline de Áudio (Whisper):**
- Utilizar `openai-whisper` (modelo 'base') + `sounddevice`
- Processamento via arrays Numpy (In-Memory)
- Evitar dependência de FFmpeg para acelerar resposta

### 3. Implementação
- Escrever código Python seguindo padrões de Clean Code
- Incluir comentários explicativos sobre a lógica de integração
- Organizar código em funções modulares quando aplicável
- Implementar tratamento de erros básico

### 4. Fluxo de Execução Padrão
```
1. Aguardar Trigger (Hotkey ou Tecla Pressionada)
2. Capturar Input (Gravação de áudio ou Prompt de texto)
3. Transcrever/Processar (Se necessário)
4. Despachar comando para o CLI do Claude
```

### 5. Instruções de Resposta ao Usuário
Fornecer:
1. **Código completo** do script com todas as dependências PEP 723
2. **Comando exato** para execução: `uv run nome_do_arquivo.py`
3. **Breves comentários** explicativos sobre a lógica de integração utilizada

## Critérios de Qualidade

- Script deve ser autocontido (single-file)
- Todas as dependências declaradas no bloco PEP 723
- Código funcional e testado mentalmente para execução imediata
- Interface com Windows CLI implementada corretamente (`start cmd /k`)
- Tratamento adequado de inputs globais (keyboard hooks ou áudio)
- Performance otimizada (low latency, in-memory processing)

## Relatório de Entrega

Após criar o script, apresente:

1. **Código Fonte Completo**: Script Python com bloco PEP 723 e implementação
2. **Comando de Execução**: Linha de comando exata para rodar com `uv run`
3. **Explicação da Integração**: Breve descrição de como o script funciona no contexto Windows-IA
4. **Dependências Utilizadas**: Lista de bibliotecas e por que foram escolhidas
5. **Notas de Uso**: Quaisquer considerações importantes para execução (permissões, configurações, etc.)

## Próximos Passos (Opcional)

Se aplicável, sugerir:
- Melhorias de performance ou funcionalidades extras
- Tratamentos de erro mais robustos
- Possíveis extensões do script para outros casos de uso
