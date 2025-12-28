---
description: Cria atalhos de teclado globais no VS Code editando o keybindings.json
---

# Criação de Atalhos de Teclado VS Code

Este comando configura atalhos de teclado globais no VS Code, editando diretamente o arquivo `keybindings.json` com base na solicitação do usuário. Use quando precisar mapear combinações de teclas para comandos específicos do VS Code.

## Contexto & Variáveis

**Arquivos Relevantes**
- `keybindings_path`: Caminho para o arquivo de configuração (Windows: `%APPDATA%\Code\User\keybindings.json`)

**Variáveis do Sistema**
- OS: Windows (detectado automaticamente)
- VS Code config path: `%APPDATA%\Code\User\`

## Estrutura de um Keybinding

Cada regra JSON deve seguir este formato:

```json
{
  "key": "TECLA",
  "command": "COMANDO_ID",
  "when": "CONTEXTO_OPCIONAL",
  "args": { "ARGUMENTOS_OPCIONAIS": "valor" }
}
```

**Teclas Aceitas**
- **Modificadores**: `ctrl+`, `shift+`, `alt+`, `win+` (Windows/Linux) ou `cmd+` (macOS)
- **Teclas válidas**: `f1-f19`, `a-z`, `0-9`, `enter`, `tab`, `escape`, `space`, `backspace`, `delete`, `left`, `up`, `right`, `down`, `pageup`, `pagedown`, `home`, `end`
- **Chord (sequência)**: Separe com espaço (ex: `ctrl+k ctrl+c`)

**Contextos Comuns para "when"**
- `editorTextFocus`: Cursor no editor
- `terminalFocus`: Terminal integrado ativo
- `!inDebugMode`: Fora do modo debug
- `editorLangId == python`: Arquivo Python aberto

## Instruções Principais

1. **Ler keybindings.json existente** para preservar configurações atuais
2. **Validar a tecla escolhida** para evitar conflitos com atalhos existentes
3. **Adicionar o novo keybinding** ao array JSON existente
4. **Usar o comando correto** baseado no que o usuário quer:
   - Novo terminal: `workbench.action.terminal.new`
   - Terminal com profile: `workbench.action.terminal.newWithProfile`
   - Executar task: `workbench.action.tasks.runTask`
   - Múltiplos comandos: `runCommands`

## Exemplo de Resposta

Para solicitção "criar F10 que abre terminal com Claude":

```json
[
  {
    "key": "f10",
    "command": "workbench.action.terminal.newWithProfile",
    "args": { "profileName": "Claude" }
  }
]
```

**Nota**: Verifique/crie o profile no `settings.json` se necessário.

## Relatório de Execução

- Confirme se o keybinding foi adicionado com sucesso
- Liste os comandos adicionados/alterados
- Verifique se não há conflitos com atalhos existentes
