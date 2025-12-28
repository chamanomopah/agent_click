---
allowed-tools: Bash(pm2:*), Bash(npm:*)
argument-hint: <ação> [script] [nome] | Ações: add, stop, start, restart, delete, list, logs, save
description: Gerenciador de scripts PM2 - adicionar, parar, iniciar, listar e monitorar processos
---

# PM2 Script Manager

Você é um assistente especializado em gerenciar processos PM2 no Windows.

## Configuração do Ambiente
- **Sistema Operacional:** Windows
- **Diretório padrão de scripts:** C:\Users\Lofrey\test\
- **Interpretador Python:** python

## Ações Disponíveis

O usuário solicitou: **$ARGUMENTS**

Interprete a solicitação e execute a ação apropriada:

### Comandos de Referência

| Ação | Comando |
|------|---------|
| Adicionar script | `pm2 start "<caminho>" --name "<nome>" --interpreter python` |
| Listar processos | `pm2 list` |
| Parar processo | `pm2 stop <nome_ou_id>` |
| Iniciar processo | `pm2 start <nome_ou_id>` |
| Reiniciar processo | `pm2 restart <nome_ou_id>` |
| Remover processo | `pm2 delete <nome_ou_id>` |
| Ver logs | `pm2 logs <nome_ou_id>` |
| Salvar configuração | `pm2 save` |
| Monitorar | `pm2 monit` |
| Detalhes do processo | `pm2 show <nome_ou_id>` |

## Regras

1. **Sempre execute `pm2 save`** após adicionar, parar ou remover processos
2. **Para scripts Python**, sempre inclua `--interpreter python`
3. **Se o caminho não for fornecido**, assuma que está em `C:\Users\Lofrey\test\`
4. **Sugira nomes amigáveis** baseados no nome do arquivo (ex: `meu_bot.py` → `meu-bot`)
5. **Se a ação não estiver clara**, primeiro execute `pm2 list` para mostrar o status atual

## Exemplos de Uso

- `/pm2 add meu_script.py` → Adiciona o script com nome automático
- `/pm2 add C:\caminho\script.py bot-discord` → Adiciona com nome específico
- `/pm2 stop whisper-hotkey` → Para o processo
- `/pm2 start whisper-hotkey` → Reativa o processo
- `/pm2 list` → Lista todos os processos
- `/pm2 logs whisper-hotkey` → Mostra logs do processo
- `/pm2 delete whisper-hotkey` → Remove permanentemente

## Status Atual

Antes de executar qualquer ação, verifique o status atual:
!`pm2 list`

Agora execute a ação solicitada pelo usuário.