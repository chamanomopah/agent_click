# 🧪 Lista Completa de Testes - AgentClick v1.1

> **Guia abrangente de testes para validar todas as funcionalidades implementadas**
> - Sistema de Múltiplos Inputs (Agente 1)
> - Sistema de Múltiplos Outputs (Agente 2)

**Data de Criação**: 2025-12-30
**Versão**: 1.1
**Status**: ✅ Pronto para Execução

---

## 📋 ÍNDICE

1. [Testes de Input - Sistema de Múltiplos Tipos](#1-testes-de-input)
2. [Testes de Output - Modos de Entrega](#2-testes-de-output)
3. [Testes Integrados - Input + Output](#3-testes-integrados)
4. [Testes de Interface e Usabilidade](#4-testes-de-interface)
5. [Testes de Performance e Estabilidade](#5-testes-de-performance)
6. [Casos de Teste Edge Cases](#6-casos-edge-cases)
7. [Testes de Regressão](#7-testes-de-regressão)
8. [Checklist Final de Validação](#8-checklist-final)

---

## 1. TESTES DE INPUT

### 1.1 Text Selection (Seleção de Texto) ✅

#### Teste 1.1.1: Texto Curto Simples
**Descrição**: Copiar e processar texto curto simples
**Passos**:
1. Selecione texto: "Hello World"
2. Pressione Ctrl+C
3. Pressione Pause
**Resultado Esperado**:
- ✅ Log mostra "Input type: text_selection"
- ✅ Texto é processado pelo agente
- ✅ Resultado no clipboard (ou arquivo se configurado)

**Status**: ⬜ Não Testado | ✅ Passou | ❌ Falhou

---

#### Teste 1.1.2: Texto Longo (+1000 caracteres)
**Descrição**: Processar texto longo
**Passos**:
1. Selecione parágrafo de 1000+ caracteres
2. Pressione Ctrl+C
3. Pressione Pause
**Resultado Esperado**:
- ✅ Log mostra "char_count" correto
- ✅ Texto completo processado sem truncamento
- ✅ Metadata contém word_count

**Status**: ⬜ Não Testado | ✅ Passou | ❌ Falhou

---

#### Teste 1.1.3: Texto com Caracteres Especiais
**Descrição**: Testar encoding e caracteres especiais
**Passos**:
1. Selecione texto com emojis, acentos, símbolos: "café, 日本語, 🚀, ©, ™"
2. Pressione Ctrl+C
3. Pressione Pause
**Resultado Esperado**:
- ✅ Caracteres mantidos corretamente (UTF-8)
- ✅ Sem erros de encoding

**Status**: ⬜ Não Testado | ✅ Passou | ❌ Falhou

---

#### Teste 1.1.4: Clipboard Vazio
**Descrição**: Tentar processar sem texto selecionado
**Passos**:
1. Não selecione nada ou limpe clipboard
2. Pressione Pause
**Resultado Esperado**:
- ⚠️ Log mostra "No input available"
- ⚠️ Mini popup mostra warning visual
- ✅ Sistema não trava

**Status**: ⬜ Não Testado | ✅ Passou | ❌ Falhou

---

### 1.2 File Upload (Upload de Arquivos) 📎

#### Teste 1.2.1: Upload Arquivo Texto Simples (.txt)
**Descrição**: Arrastar arquivo .txt para mini popup
**Passos**:
1. Crie arquivo `test.txt` com conteúdo "Test file content"
2. Arraste arquivo para mini popup (círculo colorido)
**Resultado Esperado**:
- ✅ Mini popup aumenta para 70x70 durante drag
- ✅ Log mostra "File dropped: test.txt"
- ✅ Log mostra "Input type: file_upload"
- ✅ Metadata contém file_name, file_size, extension
- ✅ Conteúdo processado automaticamente

**Status**: ⬜ Não Testado | ✅ Passou | ❌ Falhou

---

#### Teste 1.2.2: Upload Arquivo Código (.py)
**Descrição**: Upload de arquivo Python
**Passos**:
1. Crie arquivo `script.py` com código Python
2. Arraste para mini popup
**Resultado Esperado**:
- ✅ Arquivo lido corretamente
- ✅ Metadata mostra extension=".py"
- ✅ line_count calculado corretamente

**Status**: ⬜ Não Testado | ✅ Passou | ❌ Falhou

---

#### Teste 1.2.3: Upload Arquivo JSON
**Descrição**: Upload de arquivo JSON estruturado
**Passos**:
1. Crie arquivo `data.json` com JSON válido
2. Arraste para mini popup
**Resultado Esperado**:
- ✅ JSON mantém formatação
- ✅ Conteúdo disponível para processamento

**Status**: ⬜ Não Testado | ✅ Passou | ❌ Falhou

---

#### Teste 1.2.4: Upload Arquivo Binário (Deve Falhar Graciosamente)
**Descrição**: Tentar upload de arquivo binário
**Passos**:
1. Tente arrastar arquivo .exe ou .zip
**Resultado Esperado**:
- ❌ Log mostra "Binary file detected (not supported)"
- ✅ Sistema não trava
- ✅ Mensagem de erro clara

**Status**: ⬜ Não Testado | ✅ Passou | ❌ Falhou

---

#### Teste 1.2.5: Upload Arquivo Inexistente
**Descrição**: Tentar ler arquivo que não existe
**Passos**:
1. Configure file path manualmente para arquivo inexistente
2. Tente processar
**Resultado Esperado**:
- ❌ Log mostra "File not found"
- ✅ Sistema não trava

**Status**: ⬜ Não Testado | ✅ Passou | ❌ Falhou

---

#### Teste 1.2.6: Upload Arquivo Grande (+1MB)
**Descrição**: Testar performance com arquivo grande
**Passos**:
1. Crie arquivo .txt com 1MB+ de texto
2. Arraste para mini popup
**Resultado Esperado**:
- ✅ Arquivo lido sem travar
- ✅ Processamento completo
- ⏱️ Tempo resposta aceitável (<10s)

**Status**: ⬜ Não Testado | ✅ Passou | ❌ Falhou

---

### 1.3 Clipboard Image (Imagens do Clipboard) 🖼️

#### Teste 1.3.1: Imagem do Navegador
**Descrição**: Copiar imagem do navegador
**Passos**:
1. Abra imagem no navegador (clique direito → Copiar Imagem)
2. Pressione Pause (auto-detect deve pegar imagem)
**Resultado Esperado**:
- ✅ Log mostra "Auto-detected input: clipboard_image"
- ✅ Imagem salva em temp/agent_click_images/
- ✅ Metadata contém width, height, file_size
- ✅ image_path definido corretamente

**Status**: ⬜ Não Testado | ✅ Passou | ❌ Falhou

---

#### Teste 1.3.2: Imagem do Explorer
**Descrição**: Copiar imagem do Windows Explorer
**Passos**:
1. Navegue até pasta com imagens
2. Clique direito em imagem → Copiar
3. Pressione Pause
**Resultado Esperado**:
- ✅ Imagem capturada do clipboard
- ✅ Salvamento temporário bem-sucedido

**Status**: ⬜ Não Testado | ✅ Passou | ❌ Falhou

---

#### Teste 1.3.3: Screenshot Tool para Clipboard
**Descrição**: Usar ferramenta de screenshot do Windows
**Passos**:
1. Use Win+Shift+S para tirar screenshot
2. Pressione Pause
**Resultado Esperado**:
- ✅ Imagem capturada do clipboard
- ✅ Processamento com contexto visual

**Status**: ⬜ Não Testado | ✅ Passou | ❌ Falhou

---

#### Teste 1.3.4: Clipboard Sem Imagem
**Descrição**: Tentar capturar imagem quando não há imagem
**Passos**:
1. Copie apenas texto
2. Force capture_input(CLIPBOARD_IMAGE)
**Resultado Esperado**:
- ⚠️ Log mostra "Clipboard does not contain image"
- ✅ Sistema faz fallback para texto ou retorna None

**Status**: ⬜ Não Testado | ✅ Passou | ❌ Falhou

---

#### Teste 1.3.5: Múltiplas Imagens (Deve Pegar Primeira)
**Descrição**: Copiar múltiplas imagens
**Passos**:
1. Selecione 2+ imagens e copie
2. Pressione Pause
**Resultado Esperado**:
- ✅ Primeira imagem é capturada
- ✅ Não há crashes

**Status**: ⬜ Não Testado | ✅ Passou | ❌ Falhou

---

### 1.4 Screenshot (Captura de Tela) 📸

#### Teste 1.4.1: Screenshot Tela Cheia
**Descrição**: Capturar tela inteira
**Passos**:
1. Pressione Ctrl+Shift+Pause
**Resultado Esperado**:
- ✅ Log mostra "Screenshot hotkey pressed"
- ✅ Imagem salva em temp/agent_click_screenshots/
- ✅ Log mostra "Screenshot saved: screenshot_TIMESTAMP.png"
- ✅ Metadata contém resolução completa
- ✅ Processamento automático

**Status**: ⬜ Não Testado | ✅ Passou | ❌ Falhou

---

#### Teste 1.4.2: Screenshot com Janela Ativa
**Descrição**: Capturar tela com aplicação específica ativa
**Passos**:
1. Abra VSCode/Chrome/notebook
2. Pressione Ctrl+Shift+Pause
**Resultado Esperado**:
- ✅ Screenshot captura janela correta
- ✅ Aplicação visível na imagem

**Status**: ⬜ Não Testado | ✅ Passou | ❌ Falhou

---

#### Teste 1.4.3: Screenshot em Sequência Rápida
**Descrição**: Tirar múltiplos screenshots consecutivos
**Passos**:
1. Pressione Ctrl+Shift+Pause 5 vezes rapidamente
**Resultado Esperado**:
- ✅ 5 screenshots criados com timestamps únicos
- ✅ Nenhum overwrite de arquivos
- ✅ Sistema permanece estável

**Status**: ⬜ Não Testado | ✅ Passou | ❌ Falhou

---

#### Teste 1.4.4: Screenshot Region (Se Implementado)
**Descrição**: Capturar região específica da tela
**Passos**:
1. Se suportado, configure region=(x, y, width, height)
2. Pressione hotkey de screenshot com region
**Resultado Esperado**:
- ✅ Apenas região especificada capturada
- ✅ Metadata contém region info

**Status**: ⬜ Não Testado | ✅ Passou | ❌ Falhou | ⚠️ Não Implementado

---

### 1.5 Auto-Detect (Detecção Automática) 🔍

#### Teste 1.5.1: Prioridade Texto > Imagem
**Descrição**: Verificar prioridade correta
**Passos**:
1. Copie texto para clipboard
2. Copie imagem para clipboard
3. Pressione Pause
**Resultado Esperado**:
- ✅ Texto tem prioridade
- ✅ Log mostra "Auto-detected input: text_selection"

**Status**: ⬜ Não Testado | ✅ Passou | ❌ Falhou

---

#### Teste 1.5.2: Detect File Upload Configurado
**Descrição**: Auto-detectar arquivo configurado
**Passos**:
1. Arraste arquivo para mini popup
2. Arquivo deve ser processado automaticamente
**Resultado Esperado**:
- ✅ Sistema detecta file_upload disponível
- ✅ Processa sem precisar pressionar Pause

**Status**: ⬜ Não Testado | ✅ Passou | ❌ Falhou

---

#### Teste 1.5.3: Detect Nenhum Input Disponível
**Descrição**: Tentar processar sem nenhum input
**Passos**:
1. Limpe clipboard
2. Não configure arquivo
3. Pressione Pause
**Resultado Esperado**:
- ⚠️ Log mostra "No input available from any source"
- ✅ Warning visual no popup
- ✅ Sistema não trava

**Status**: ⬜ Não Testado | ✅ Passou | ❌ Falhou

---

#### Teste 1.5.4: Mudança de Tipo de Input Dinâmico
**Descrição**: Sistema deve detectar mudança de input
**Passos**:
1. Comece com texto no clipboard
2. Pressione Pause → deve processar texto
3. Arraste arquivo → deve processar arquivo
4. Tire screenshot → deve processar screenshot
**Resultado Esperado**:
- ✅ Cada tipo de input é corretamente detectado
- ✅ Logs mostram tipos diferentes

**Status**: ⬜ Não Testado | ✅ Passou | ❌ Falhou

---

## 2. TESTES DE OUTPUT

### 2.1 Modo AUTO (Agente Decide) 🤖

#### Teste 2.1.1: Curto → Clipboard Pure
**Descrição**: Texto curto deve ir para clipboard
**Passos**:
1. Configure agente com output_mode=AUTO
2. Selecione texto curto: "Olá mundo"
3. Pressione Pause
**Resultado Esperado**:
- ✅ Log mostra "AUTO: Using CLIPBOARD_PURE"
- ✅ Conteúdo no clipboard (sem formatação extra)

**Status**: ⬜ Não Testado | ✅ Passou | ❌ Falhou

---

#### Teste 2.1.2: Código Grande (>50 linhas) → FILE
**Descrição**: Código grande deve ser salvo em arquivo
**Passos**:
1. Configure agente com AUTO e context_folder
2. Selecione código com 60+ linhas
3. Pressione Pause
**Resultado Esperado**:
- ✅ Log mostra "AUTO: Large content (>50 lines), using FILE mode"
- ✅ Arquivo criado: output.txt
- ✅ Conteúdo também copiado para clipboard

**Status**: ⬜ Não Testado | ✅ Passou | ❌ Falhou

---

#### Teste 2.1.3: Com Suggested Filename → FILE
**Descrição**: Se agente sugerir filename, deve salvar
**Passos**:
1. Selecione prompt: "Crie um arquivo JSON de configuração"
2. Pressione Pause
**Resultado Esperado**:
- ✅ Log mostra "AUTO: Detected filename + context, using FILE mode"
- ✅ Arquivo criado: config.json

**Status**: ⬜ Não Testado | ✅ Passou | ❌ Falhou

---

#### Teste 2.1.4: Com Reasoning → Clipboard Rich
**Descrição**: Se agente gerar thoughts, usar rich format
**Passos**:
1. Selecione tarefa complexa que gere reasoning
2. Pressione Pause
**Resultado Esperado**:
- ✅ Log mostra "AUTO: Has reasoning, using CLIPBOARD_RICH"
- ✅ Clipboard contém seção "# Reasoning" separada

**Status**: ⬜ Não Testado | ✅ Passou | ❌ Falhou

---

#### Teste 2.1.5: Sem Context Folder → Clipboard (Fallback)
**Descrição**: AUTO deve fazer fallback se não pode salvar arquivo
**Passos**:
1. Configure agente com AUTO mas SEM context_folder
2. Selecione código grande
3. Pressione Pause
**Resultado Esperado**:
- ✅ Fallback para clipboard (não falha)
- ✅ Log mostra warning sobre context folder ausente

**Status**: ⬜ Não Testado | ✅ Passou | ❌ Falhou

---

### 2.2 Modo CLIPBOARD_PURE (Clipboard Puro) 📋

#### Teste 2.2.1: Texto Simples
**Descrição**: Copiar texto puro sem formatação
**Passos**:
1. Configure agente com CLIPBOARD_PURE
2. Process qualquer tarefa
3. Cole resultado (Ctrl+V)
**Resultado Esperado**:
- ✅ Texto colado é "cru" (sem markdown de reasoning)
- ✅ Sem seções extras ou metadados

**Status**: ⬜ Não Testado | ✅ Passou | ❌ Falhou

---

#### Teste 2.2.2: Sem Raw Thoughts
**Descrição**: Verificar que reasoning não está incluído
**Passos**:
1. Configure agente com CLIPBOARD_PURE
2. Processe tarefa que gera reasoning
3. Cole resultado
**Resultado Esperado**:
- ✅ Apenas conteúdo principal (sem thoughts)

**Status**: ⬜ Não Testado | ✅ Passou | ❌ Falhou

---

#### Teste 2.2.3: Performance Clipboard
**Descrição**: Verificar que operação é rápida
**Passos**:
1. Processe tarefa simples
2. Meça tempo até cópia
**Resultado Esperado**:
- ⏱️ Operação concluída em <2s

**Status**: ⬜ Não Testado | ✅ Passou | ❌ Falhou

---

### 2.3 Modo CLIPBOARD_RICH (Clipboard Rico) 📋✨

#### Teste 2.3.1: Com Reasoning
**Descrição**: Copiar com formatação e reasoning
**Passos**:
1. Configure agente com CLIPBOARD_RICH
2. Processe tarefa complexa
3. Cole resultado
**Resultado Esperado**:
- ✅ Clipboard contém "# Reasoning" como header
- ✅ Separator "---" entre reasoning e output
- ✅ Ambas seções presentes

**Status**: ⬜ Não Testado | ✅ Passou | ❌ Falhou

---

#### Teste 2.3.2: Sem Reasoning (Apenas Conteúdo)
**Descrição**: Se não houver reasoning, comportamento normal
**Passos**:
1. Configure CLIPBOARD_RICH
2. Processe tarefa simples
3. Cole resultado
**Resultado Esperado**:
- ✅ Apenas conteúdo (sem seção de reasoning vazia)

**Status**: ⬜ Não Testado | ✅ Passou | ❌ Falhou

---

#### Teste 2.3.3: Markdown Formatação
**Descrição**: Verificar formatação markdown correta
**Passos**:
1. Processe tarefa que gera código
2. Cole resultado
**Resultado Esperado**:
- ✅ Markdown formatting preservado
- ✅ Headers com # corretos

**Status**: ⬜ Não Testado | ✅ Passou | ❌ Falhou

---

### 2.4 Modo FILE (Salvar em Arquivo) 💾

#### Teste 2.4.1: Salvar Arquivo Simples
**Descrição**: Salvar output em arquivo
**Passos**:
1. Configure agente com FILE e context_folder
2. Processe tarefa
3. Verifique pasta do projeto
**Resultado Esperado**:
- ✅ Arquivo criado: output.txt (ou sugerido)
- ✅ Log mostra "✅ Saved to file: CAMINHO"
- ✅ Clipboard também contém conteúdo (conveniência)

**Status**: ⬜ Não Testado | ✅ Passou | ❌ Falhou

---

#### Teste 2.4.2: Salvar com Filename Sugerido
**Descrição**: Usar filename sugerido pelo agente
**Passos**:
1. Processe "crie arquivo Python"
2. Verifique filename gerado
**Resultado Esperado**:
- ✅ Arquivo criado: script.py (não output.txt)
- ✅ Extensão correta baseada na tarefa

**Status**: ⬜ Não Testado | ✅ Passou | ❌ Falhou

---

#### Teste 2.4.3: Sobrescrever Arquivo Existente
**Descrição**: Comportamento ao salvar arquivo existente
**Passos**:
1. Crie arquivo output.txt
2. Processe tarefa que gera mesmo filename
3. Verifique resultado
**Resultado Esperado**:
- ✅ Arquivo é sobrescrito
- ✅ Sem erros ou warnings

**Status**: ⬜ Não Testado | ✅ Passou | ❌ Falhou

---

#### Teste 2.4.4: Sem Context Folder → Fallback
**Descrição**: FILE sem context_folder deve fazer fallback
**Passos**:
1. Configure FILE mas deixe context_folder vazio
2. Processe tarefa
**Resultado Esperado**:
- ⚠️ Log mostra "No context folder for FILE mode, falling back to clipboard"
- ✅ Conteúdo vai para clipboard (não falha)

**Status**: ⬜ Não Testado | ✅ Passou | ❌ Falhou

---

#### Teste 2.4.5: Criar Diretório Se Não Existir
**Descrição**: Sistema deve criar pasta se necessário
**Passos**:
1. Configure context_folder para pasta inexistente
2. Processe tarefa
**Resultado Esperado**:
- ✅ Diretório criado automaticamente
- ✅ Arquivo salvo com sucesso

**Status**: ⬜ Não Testado | ✅ Passou | ❌ Falhou

---

### 2.5 Modo INTERACTIVE_EDITOR (Editor Interativo) ✏️

#### Teste 2.5.1: Abrir Editor Interativo
**Descrição**: Janela de preview deve abrir
**Passos**:
1. Configure agente com INTERACTIVE_EDITOR
2. Processe tarefa
**Resultado Esperado**:
- ✅ Janela "✏️ AgentClick - Output Editor" abre
- ✅ Título "📝 Preview & Edit Output"
- ✅ Conteúdo preenchido no editor
- ✅ Botões "❌ Cancel" e "✅ Confirm & Output" visíveis

**Status**: ⬜ Não Testado | ✅ Passou | ❌ Falhou

---

#### Teste 2.5.2: Editar Conteúdo
**Descrição**: Deve ser possível editar o output
**Passos**:
1. Abra editor interativo
2. Modifique texto na caixa de edição
3. Confirme
**Resultado Esperado**:
- ✅ Texto pode ser editado (QTextEdit funcional)
- ✅ Output final contém edições

**Status**: ⬜ Não Testado | ✅ Passou | ❌ Falhou

---

#### Teste 2.5.3: Escolher Clipboard vs File
**Descrição**: Dropdown permite escolher ação final
**Passos**:
1. Abra editor interativo
2. Mude dropdown "Choose output" para "💾 Save to File"
3. Verifique que campo "Filename" aparece
**Resultado Esperado**:
- ✅ Dropdown mostra opções
- ✅ Campo "Filename" aparece quando "File" selecionado
- ✅ Campo desaparece quando "Clipboard" selecionado

**Status**: ⬜ Não Testado | ✅ Passou | ❌ Falhou

---

#### Teste 2.5.4: Editar Filename
**Descrição**: Deve ser possível editar filename sugerido
**Passos**:
1. Abra editor interativo
2. Selecione "Save to File"
3. Clique no botão de filename
4. Mude nome no dialog
**Resultado Esperado**:
- ✅ QInputDialog abre para editar filename
- ✅ Novo nome refletido no botão

**Status**: ⬜ Não Testado | ✅ Passou | ❌ Falhou

---

#### Teste 2.5.5: Mostrar Reasoning (Read-Only)
**Descrição**: Se houver reasoning, mostrar como read-only
**Passos**:
1. Processe tarefa que gera reasoning
2. Abra editor interativo
**Resultado Esperado**:
- ✅ Seção "🤔 Agent's Reasoning:" aparece
- ✅ Thoughts são read-only (cinza/amarelo)
- ✅ Content principal é editável

**Status**: ⬜ Não Testado | ✅ Passou | ❌ Falhou

---

#### Teste 2.5.6: Confirmar → Output
**Descrição**: Confirmar deve executar ação escolhida
**Passos**:
1. Abra editor, edite texto
2. Escolha "Save to File"
3. Clique "✅ Confirm & Output"
**Resultado Esperado**:
- ✅ Janela fecha
- ✅ Arquivo criado com conteúdo editado
- ✅ Log mostra "✅ Interactive editor confirmed"

**Status**: ⬜ Não Testado | ✅ Passou | ❌ Falhou

---

#### Teste 2.5.7: Cancelar → Sem Output
**Descrição**: Cancelar não deve gerar output
**Passos**:
1. Abra editor interativo
2. Clique "❌ Cancel"
**Resultado Esperado**:
- ✅ Janela fecha
- ✅ Nenhum arquivo criado ou clipboard modificado
- ✅ Log mostra "❌ Interactive editor cancelled"

**Status**: ⬜ Não Testado | ✅ Passou | ❌ Falhou

---

#### Teste 2.5.8: Sem Context Folder → Apenas Clipboard
**Descrição**: Editor não deve mostrar opção File sem context
**Passos**:
1. Configure INTERACTIVE_EDITOR sem context_folder
2. Abra editor
**Resultado Esperado**:
- ✅ Dropdown mostra apenas "📋 Copy to Clipboard"
- ✅ Opção "💾 Save to File" não disponível

**Status**: ⬜ Não Testado | ✅ Passou | ❌ Falhou

---

## 3. TESTES INTEGRADOS

### 3.1 Input Text + Output AUTO

#### Teste 3.1.1: Texto Curto + AUTO
**Descrição**: Fluxo completo simples
**Passos**:
1. Configure agente: context_folder=None, output_mode=AUTO
2. Selecione "Olá, como você está?"
3. Pressione Pause
**Resultado Esperado**:
- ✅ Input: text_selection detectado
- ✅ Output: CLIPBOARD_PURE usado (AUTO decid)
- ✅ Clipboard contém resposta

**Status**: ⬜ Não Testado | ✅ Passou | ❌ Falhou

---

### 3.2 Input File + Output FILE

#### Teste 3.2.1: Upload Código + Salvar Novo Código
**Descrição**: Ler código de arquivo e gerar novo arquivo
**Passos**:
1. Configure: context_folder="C:/projeto", output_mode=FILE
2. Arraste script.py para mini popup
3. Agente processa e gera código melhorado
**Resultado Esperado**:
- ✅ Input: FILE_UPLOAD detectado
- ✅ Arquivo lido corretamente
- ✅ Output: novo arquivo criado na pasta
- ✅ Nomes de arquivo diferentes (sem overwrite do original)

**Status**: ⬜ Não Testado | ✅ Passou | ❌ Falhou

---

### 3.3 Input Image + Output Rich

#### Teste 3.3.1: Screenshot + Análise Visual
**Descrição**: Tirar screenshot e analisar com reasoning
**Passos**:
1. Configure: output_mode=CLIPBOARD_RICH
2. Pressione Ctrl+Shift+Pause (screenshot)
3. Cole resultado
**Resultado Esperado**:
- ✅ Input: SCREENSHOT capturado
- ✅ Imagem passada ao agente
- ✅ Output: clipboard contém análise visual
- ✅ Seção "# Reasoning" presente

**Status**: ⬜ Não Testado | ✅ Passou | ❌ Falhou

---

### 3.4 Input Image + Output Editor Interativo

#### Teste 3.4.1: Imagem + Preview e Edição
**Descrição**: Processar imagem com editor interativo
**Passos**:
1. Configure: output_mode=INTERACTIVE_EDITOR
2. Copie imagem do navegador
3. Pressione Pause
4. Edite análise no editor
5. Confirme
**Resultado Esperado**:
- ✅ Input: CLIPBOARD_IMAGE
- ✅ Editor abre com análise
- ✅ Pode editar antes de output final

**Status**: ⬜ Não Testado | ✅ Passou | ❌ Falhou

---

## 4. TESTES DE INTERFACE E USABILIDADE

### 4.1 Mini Popup

#### Teste 4.1.1: Visual Inicial
**Descrição**: Mini popup aparece corretamente
**Passos**:
1. Inicie AgentClick
**Resultado Esperado**:
- ✅ Círculo 60x60 visível
- ✅ Ícone do agente atual mostrado
- ✅ Cor do agente aplicada
- ✅ Sempre visível (topo da tela)

**Status**: ⬜ Não Testado | ✅ Passou | ❌ Falhou

---

#### Teste 4.1.2: Drag Over Visual Feedback
**Descrição**: Feedback visual ao arrastar arquivo
**Passos**:
1. Arraste arquivo sobre mini popup (sem soltar)
**Resultado Esperado**:
- ✅ Mini popup aumenta para 70x70
- ✅ Borda azul aparece (border: 3px solid #0078d4)
- ✅ Retorna ao normal ao sair

**Status**: ⬜ Não Testado | ✅ Passou | ❌ Falhou

---

#### Teste 4.1.3: Clique Abre Popup Detalhado
**Descrição**: Clicar no mini popup abre janela principal
**Passos**:
1. Clique no mini popup
**Resultado Esperado**:
- ✅ PopupWindow 550x450 abre
- ✅ Abas: Overview, Activity Log, Config
- ✅ Informações do agente atual mostradas

**Status**: ⬜ Não Testado | ✅ Passou | ❌ Falhou

---

### 4.2 Popup Detalhado

#### Teste 4.2.1: Aba Config - Output Mode Dropdown
**Descrição**: Dropdown de output mode funcional
**Passos**:
1. Abra popup detalhado
2. Vá para aba Config
3. Clique no dropdown "Output Mode"
**Resultado Esperado**:
- ✅ 5 opções visíveis:
  - 🤖 Auto (Agent Decide)
  - 📋 Clipboard (Pure)
  - 📋 Clipboard (Rich)
  - 💾 Save to File
  - ✏️ Interactive Editor
- ✅ Modo atual selecionado

**Status**: ⬜ Não Testado | ✅ Passou | ❌ Falhou

---

#### Teste 4.2.2: Salvar Configuração
**Descrição**: Configurações persistem
**Passos**:
1. Mude output_mode para FILE
2. Clique "Save Configuration"
3. Feche popup
4. Reabra popup
**Resultado Esperado**:
- ✅ Dropdown ainda mostra FILE
- ✅ agent_config.json atualizado
- ✅ Log mostra "✅ Configuration saved"

**Status**: ⬜ Não Testado | ✅ Passou | ❌ Falhou

---

#### Teste 4.2.3: Info Label Atualizado
**Descrição**: Label informativo mostra output modes
**Passos**:
1. Abra aba Config
2. Leia info label
**Resultado Esperado**:
- ✅ Texto explica cada modo de output
- ✅ Formatação legível

**Status**: ⬜ Não Testado | ✅ Passou | ❌ Falhou

---

### 4.3 Atalhos de Teclado

#### Teste 4.3.1: Pause (Ativar Agente)
**Descrição**: Atalho principal funciona
**Passos**:
1. Selecione texto
2. Pressione Pause
**Resultado Esperado**:
- ✅ Agente processa texto
- ✅ Popup detalhado NÃO abre (apenas log)

**Status**: ⬜ Não Testado | ✅ Passou | ❌ Falhou

---

#### Teste 4.3.2: Ctrl+Pause (Alternar Agente)
**Descrição**: Alternar entre agentes
**Passos**:
1. Pressione Ctrl+Pause
**Resultado Esperado**:
- ✅ Mini popup muda ícone/cor
- ✅ Log mostra "Switched to [novo agente]"

**Status**: ⬜ Não Testado | ✅ Passou | ❌ Falhou

---

#### Teste 4.3.3: Ctrl+Shift+Pause (Screenshot)
**Descrição**: Atalho de screenshot
**Passos**:
1. Pressione Ctrl+Shift+Pause
**Resultado Esperado**:
- ✅ Screenshot capturado
- ✅ Processamento iniciado

**Status**: ⬜ Não Testado | ✅ Passou | ❌ Falhou

---

## 5. TESTES DE PERFORMANCE E ESTABILIDADE

### 5.1 Performance

#### Teste 5.1.1: Tempo Resposta Texto Curto
**Descrição**: Medir latência para tarefas simples
**Passos**:
1. Selecione texto curto
2. Pressione Pause
3. Meça tempo até output
**Resultado Esperado**:
- ⏱️ <3 segundos para tarefas simples

**Status**: ⬜ Não Testado | ✅ Passou | ❌ Falhou

---

#### Teste 5.1.2: Tempo Resposta Imagem
**Descrição**: Medir latência para imagens
**Passos**:
1. Copie imagem
2. Pressione Pause
3. Meça tempo até output
**Resultado Esperado**:
- ⏱️ <10 segundos para análise visual

**Status**: ⬜ Não Testado | ✅ Passou | ❌ Falhou

---

#### Teste 5.1.3: Uso de Memória
**Descrição**: Verificar memory leaks
**Passos**:
1. Execute 20 processamentos consecutivos
2. Monitore uso de memória
**Resultado Esperado**:
- ✅ Memória estável (sem crescimento contínuo)
- ✅ Cleanup de temp files funcionando

**Status**: ⬜ Não Testado | ✅ Passou | ❌ Falhou

---

### 5.2 Estabilidade

#### Teste 5.2.1: Processamento Simultâneo
**Descrição**: Tentar processar enquanto outro processa
**Passos**:
1. Inicie tarefa demorada
2. Tente Pressione Pause novamente antes de terminar
**Resultado Esperado**:
- ✅ Sistema gere concorrência adequadamente
- ✅ Sem crashes ou race conditions

**Status**: ⬜ Não Testado | ✅ Passou | ❌ Falhou

---

#### Teste 5.2.2: Cleanup Temp Files
**Descrição**: Limpeza automática de arquivos temporários
**Passos**:
1. Tire 10 screenshots
2. Chame cleanup_temp_files(hours=0)
**Resultado Esperado**:
- ✅ Arquivos antigos deletados
- ✅ Log mostra contagem de arquivos deletados

**Status**: ⬜ Não Testado | ✅ Passou | ❌ Falhou

---

#### Teste 5.2.3: Recuperação de Erro SDK
**Descrição**: Sistema deve se recuperar de erros do SDK
**Passos**:
1. Simule erro de conexão com SDK
2. Tente processar novamente
**Resultado Esperado**:
- ✅ Erro logado corretamente
- ✅ Sistema permanece funcional
- ✅ Próxima tentativa funciona

**Status**: ⬜ Não Testado | ✅ Passou | ❌ Falhou

---

## 6. CASOS EDGE CASES

### 6.1 Inputs Inválidos

#### Teste 6.1.1: Arquivo Vazio (0 bytes)
**Descrição**: Upload de arquivo vazio
**Passos**:
1. Crie arquivo vazio .txt
2. Arraste para mini popup
**Resultado Esperado**:
- ⚠️ Arquivo lido (mas vazio)
- ✅ Agente recebe string vazia
- ✅ Sistema não trava

**Status**: ⬜ Não Testado | ✅ Passou | ❌ Falhou

---

#### Teste 6.1.2: Texto Unicode Complexo
**Descrição**: Caracteres unicode complexos
**Passos**:
1. Selecione texto com: emojis, RTL scripts, símbolos matemáticos
2. Pressione Pause
**Resultado Esperado**:
- ✅ Unicode preservado corretamente
- ✅ Sem erros de encoding

**Status**: ⬜ Não Testado | ✅ Passou | ❌ Falhou

---

#### Teste 6.1.3: Imagem Corrompida
**Descrição**: Tentar ler imagem corrompida do clipboard
**Passos**:
1. Simule clipboard com imagem inválida
2. Pressione Pause
**Resultado Esperado**:
- ❌ Erro logado
- ✅ Sistema não trava

**Status**: ⬜ Não Testado | ✅ Passou | ❌ Falhou

---

### 6.2 Outputs Extremos

#### Teste 6.2.1: Output Vazio do Agente
**Descrição**: Agente retorna string vazia
**Passos**:
1. Processe tarefa que pode gerar output vazio
**Resultado Esperado**:
- ⚠️ Log mostra "Agent returned empty result"
- ✅ Warning no popup
- ✅ Sem clipboard modificado

**Status**: ⬜ Não Testado | ✅ Passou | ❌ Falhou

---

#### Teste 6.2.2: Output Muito Grande (>1MB)
**Descrição**: Agente gera output enorme
**Passos**:
1. Processe tarefa que gera muito texto
2. Verifique clipboard
**Resultado Esperado**:
- ✅ Output completo no clipboard
- ✅ Sem truncamento

**Status**: ⬜ Não Testado | ✅ Passou | ❌ Falhou

---

#### Teste 6.2.3: Filename Inválido
**Descrição**: Agente sugere filename com caracteres inválidos
**Passos**:
1. Configure output_mode=FILE
2. Processe tarefa que gera filename com: /, \, :, *, ?, ", <, >, |
**Resultado Esperado**:
- ✅ Sistema sanitiza filename
- ✅ Arquivo salvo com nome válido

**Status**: ⬜ Não Testado | ✅ Passou | ❌ Falhou

---

## 7. TESTES DE REGRESSÃO

### 7.1 Funcionalidades Legadas

#### Teste 7.1.1: Text Selection Ainda Funciona
**Descrição**: Verificar que refatoração não quebrou texto
**Passos**:
1. Use sistema como antes (selecionar texto + Pause)
**Resultado Esperado**:
- ✅ Comportamento idêntico à versão 1.0
- ✅ Sem regressões

**Status**: ⬜ Não Testado | ✅ Passou | ❌ Falhou

---

#### Teste 7.1.2: Configuração de Agentes
**Descrição**: Configurar context_folder e focus_file
**Passos**:
1. Abra popup
2. Configure context e focus file
3. Salve
**Resultado Esperado**:
- ✅ Configurações persistem
- ✅ Usadas no processamento

**Status**: ⬜ Não Testado | ✅ Passou | ❌ Falhou

---

#### Teste 7.1.3: Alternância de Agentes
**Descrição**: Ctrl+Pause ainda funciona
**Passos**:
1. Pressione Ctrl+Pause múltiplas vezes
**Resultado Esperado**:
- ✅ Cicla pelos agentes corretamente
- ✅ Mini popup atualiza

**Status**: ⬜ Não Testado | ✅ Passou | ❌ Falhou

---

## 8. CHECKLIST FINAL DE VALIDAÇÃO

### 8.1 Funcionalidades Implementadas

#### Sistema de Inputs (Agente 1)
- [ ] Text Selection (Texto Selecionado)
- [ ] File Upload (Drag & Drop)
- [ ] Clipboard Image (Ctrl+C em imagem)
- [ ] Screenshot (Ctrl+Shift+Pause)
- [ ] Auto-Detection (detecta melhor input)
- [ ] InputManager coordena estratégias
- [ ] Mini popup com drag & drop

#### Sistema de Outputs (Agente 2)
- [ ] OutputMode.AUTO (agente decide)
- [ ] OutputMode.CLIPBOARD_PURE (conteúdo cru)
- [ ] OutputMode.CLIPBOARD_RICH (com reasoning)
- [ ] OutputMode.FILE (salvar em arquivo)
- [ ] OutputMode.INTERACTIVE_EDITOR (preview)
- [ ] OutputHandler processa resultados
- [ ] UI dropdown de output mode
- [ ] Persistência de configuração

#### Integrações
- [ ] BaseAgent suporta image_path
- [ ] AgentResult estrutura de dados
- [ ] Sistema passa image_path para SDK
- [ ] Log detalhado de operações

---

### 8.2 Documentação e Logs

- [ ] Logs mostram tipo de input detectado
- [ ] Logs mostram modo de output usado
- [ ] Erros têm mensagens claras
- [ ] Warnings têm contexto útil
- [ ] Debug mode disponível

---

### 8.3 Usabilidade

- [ ] Mini popup intuitivo (ícone + cor)
- [ ] Visual feedback em drag & drop
- [ ] Popup detalhado organizado
- [ ] Atalhos de teclado documentados
- [ ] Mensagens de erro user-friendly

---

### 8.4 Performance

- [ ] Tempo de resposta aceitável (<10s)
- [ ] Sem memory leaks
- [ ] Cleanup de temp files funciona
- [ ] Sistema permanece estável

---

### 8.5 Segurança e Robustez

- [ ] Validação de inputs (arquivos binários rejeitados)
- [ ] Tratamento de erros (try/except adequado)
- [ ] Fallbacks implementados (context folder vazio)
- [ ] Sanitização de filenames
- [ ] Sem crashes em edge cases

---

## 📊 RESUMO EXECUTIVO

**Total de Testes**: 80+

**Distribuição**:
- Input Tests: 30
- Output Tests: 25
- Integrated Tests: 5
- UI/UX Tests: 10
- Performance/Stability: 6
- Edge Cases: 4

**Prioridade Alta**:
- Teste 1.1.1 (Texto simples)
- Teste 1.2.1 (Upload arquivo)
- Teste 1.4.1 (Screenshot)
- Teste 2.1.1 (AUTO decision)
- Teste 2.4.1 (FILE save)
- Teste 2.5.1 (Interactive editor)

**Critérios de Sucesso**:
- ✅ 90%+ dos testes passam
- ✅ Zero crashes em edge cases
- ✅ Performance aceitável
- ✅ UI responsiva
- ✅ Logs claros e úteis

---

## 🔧 TROUBLESHOOTING RÁPIDO

### Problema: Drag & Drop não funciona
- Verifique: `setAcceptDrops(True)` chamado em mini_popup.py
- Verifique: Sinal `file_dropped` conectado em system.py
- Verifique: Eventos dragEnterEvent, dropEvent implementados

### Problema: Screenshot falha
- Verifique: Pillow instalado (`pip install Pillow`)
- Verifique: Handler registrado em click_processor.py
- Verifique: Permissões de tela no OS

### Problema: Output FILE não salva
- Verifique: context_folder configurado
- Verifique: Permissões de escrita na pasta
- Verifique: Log mostra caminho completo

### Problema: Editor interativo não abre
- Verifique: PyQt6 instalado corretamente
- Verifique: OutputHandler importado
- Verifique: Método `_handle_interactive` implementado

---

## 📝 COMO USAR ESTE DOCUMENTO

1. **Marque testes executados**: Use ⬜ → ✅ ou ❌
2. **Anote bugs encontrados**: Adicione comentários nos testes que falham
3. **Track progresso**: Conte testes passados vs total
4. **Report final**: Use Resumo Executivo para validação

**Exemplo de marcação**:
```markdown
**Status**: ⬜ Não Testado | ✅ Passou | ❌ Falhou
```

Mude para:
```markdown
**Status**: ✅ Passou - Testado em 30/12/2025 às 14:30
```

---

**Fim do Documento de Testes**

Para dúvidas ou problemas, consulte:
- IMPLEMENTACAO_INPUTS.md (detalhes de inputs)
- output_implementation.md (detalhes de outputs)
- agents/debug_agentclick_agent.py (debugging specialist)
