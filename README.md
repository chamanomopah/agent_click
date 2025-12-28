# AgentClick System v1.0

Multi-agent system with dual popup interface - mini indicator always visible, detailed view on demand, and per-agent configuration management.

**What it does:** Mini popup shows agent → Click to configure/use → Select text → Press Pause → Agent processes with custom context → Result copied to clipboard.

## Features

### Main Features
- 🎯 **Mini popup** - Small, discreet indicator always visible (60x60px)
- 🖥️ **Detailed popup** - Large popup with activity log and configuration (opens on click)
- 🎯 **Click activation** - Press Pause to activate current agent
- 🔄 **Agent switching** - Press Ctrl+Pause to switch agents (updates mini popup)
- ⚙️ **Per-agent configuration** - Each agent has independent Context Folder and Focus File settings
- 📋 **Clipboard integration** - Automatic copy/paste
- 🤖 **3 specialized agents** - Prompt Assistant, Diagnostic, Implementation
- 🎨 **Visual feedback** - Color-coded agent icons
- 💾 **Persistent configuration** - Settings saved in JSON, maintained across sessions

### Popup System

**Mini Popup (Always Visible):**
- Position: Bottom-right corner
- Size: 60x60 pixels (very discreet)
- Shows: Agent icon only
- Behavior: Enlarges slightly on hover
- Click: Opens detailed popup

**Detailed Popup (On Demand):**
- Position: Bottom-right corner (above mini popup)
- Size: 550x450 pixels
- Two tabs:
  - **📋 Activity**: Real-time activity log
  - **⚙️ Config**: Per-agent configuration settings
- Opens: When clicking mini popup
- Closes: Via X button

### Configuration System

**Each agent has independent settings:**

1. **Context Folder**
   - Project folder the agent can work in
   - Provides project context for processing
   - Optional: Leave empty if not needed

2. **Focus File**
   - Specific file that provides project context
   - Agent uses this file for additional context
   - Optional: Leave empty if not needed

**How it works:**
- Settings are **per-agent** (Diagnostic Agent can have different config than Prompt Assistant)
- Configurations persist in `C:\.agent_click\config\agent_config.json`
- When you switch agents (Ctrl+Pause), the config tab shows that agent's specific settings
- Agent receives context_folder and focus_file when processing

## Available Agents

### 1. Prompt Assistant 🔧

**Purpose:** Expands and refines user prompts with better structure and context.

**Use when:** You need better, more detailed prompts for AI interactions

**Example:**
```
Input: "create login function"
Output: Well-structured prompt with context, requirements, and formatting

With Configuration:
- Context Folder: C:\my-react-app
- Focus File: C:\my-react-app\package.json

Result: Prompt considers React project structure and dependencies!
```

### 2. Diagnostic Agent 🔍

**Purpose:** Analyzes problems and provides detailed diagnosis with implementation plans.

**Use when:** You need to understand and fix bugs or issues

**Example:**
```
Input: "Bug: login fails with special characters"
Output:
- Root cause analysis
- Impact assessment
- Solution approaches
- Step-by-step implementation plan
```

### 3. Implementation Agent 💻

**Purpose:** Executes code implementations directly in project files.

**Use when:** You need concrete code implementations

**Example:**
```
Input: "Add validation for special characters in password"
Output: Production-ready code with file paths and exact changes
```

## Installation

### Install Astral UV

```powershell
# Windows PowerShell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

## Usage

### Start the System

```bash
cd C:\.agent_click
uv run agent_click.py
```

### Basic Operation

**When system starts:**
- Mini popup appears in bottom-right corner
- Shows current agent icon (🔍 Diagnostic Agent initially)
- All agents load with their saved configurations

**To process text:**
1. **Select text** in any application
2. **Copy text** (Ctrl+C) to clipboard
3. **Press Pause** to process with current agent
4. **Result automatically copied** to clipboard
5. **Paste result** (Ctrl+V) where needed

**To configure agents:**
1. **Click the mini popup** (bottom-right)
2. Detailed popup opens
3. **Go to "⚙️ Config" tab**
4. **Configure for current agent:**
   - Click "📁 Browse" to select Context Folder
   - Click "📄 Browse" to select Focus File
5. **Click "💾 Save Configuration"**
6. **Settings persist** - will be loaded next time you use this agent

**To switch agents:**
1. **Press Ctrl+Pause** to cycle through agents
2. Mini popup icon changes immediately
3. Agent switches: 🔍 → 💻 → 🔧 → 🔍 ...
4. If detailed popup is open, config tab shows new agent's settings
5. Each agent maintains its own independent configuration

### Mini Popup Behavior

- **Always visible** (60x60px, bottom-right)
- **Shows agent icon** in color-coded circle
- **Hover effect**: Enlarges slightly with border
- **Click**: Opens detailed popup
- **No distraction**: Minimal footprint

### Detailed Popup Interface

**Tab 1: 📋 Activity**
- Real-time activity log
- Shows processing progress
- Success/error messages
- Timestamps for each action

**Tab 2: ⚙️ Config**
- Context Folder field + Browse button
- Focus File field + Browse button
- Save Configuration button
- Info box explaining each setting

**Activity icons:**
- ✨ Agent ready
- 📖 Processing/Reading
- ✅ Success
- ⚠️ Warning
- ❌ Error
- 🔄 Switching agents

## Project Structure

```
C:\.agent_click\
├── agent_click.py              # ENTRY POINT (PEP 723)
├── README.md                   # This file
│
├── core/                       # Core system components
│   ├── __init__.py
│   ├── system.py               # Main coordinator
│   ├── click_processor.py      # Keyboard shortcuts (Pause, Ctrl+Pause)
│   └── selection_manager.py    # Clipboard operations
│
├── agents/                     # Agent implementations
│   ├── __init__.py
│   ├── base_agent.py           # Abstract base class
│   ├── agent_registry.py       # Agent discovery and management
│   ├── prompt_assistant_agent.py   # 🔧 Refines prompts
│   ├── diagnostic_agent.py         # 🔍 Diagnoses problems
│   └── implementation_agent.py     # 💻 Implements code
│
├── ui/                         # User interface
│   ├── __init__.py
│   ├── popup_window.py         # Large detailed popup (550x450)
│   │   ├── Activity tab (log)
│   │   └── Config tab (settings)
│   └── mini_popup.py           # Mini indicator popup (60x60)
│
├── config/                     # Configuration management
│   ├── __init__.py
│   ├── sdk_config.py           # Claude SDK factory
│   ├── agent_config.py         # Agent configuration manager
│   └── agent_config.json       # Saved configurations (auto-created)
│
└── utils/                      # Utilities
    ├── __init__.py
    └── logger.py               # Logging setup
```

## Configuration System Deep Dive

### How Per-Agent Configuration Works

**1. Each Agent Has Independent Settings:**
```
Diagnostic Agent settings:
{
  "context_folder": "C:\\api-project",
  "focus_file": "C:\\api-project\\api.py"
}

Prompt Assistant settings:
{
  "context_folder": "C:\\docs-project",
  "focus_file": "C:\\docs-project\\guide.md"
}

Implementation Agent settings:
{
  "context_folder": null,
  "focus_file": null
}
```

**2. Settings Impact Processing:**
```
User selects text: "add error handling"
User presses Pause

System:
1. Detects current agent: "Diagnostic Agent"
2. Loads Diagnostic Agent's config
3. Passes context_folder and focus_file to agent
4. Agent uses config to customize processing
5. Result considers project context!
```

**3. Automatic Context Injection:**
```
When processing with config:
- Agent receives context_folder and focus_file
- System prompt includes project context
- Prompt shows: "CONTEXT INFORMATION: Context Folder: ..., Focus File: ..."
- Claude SDK processes with custom context
- Result is tailored to specific project!
```

### Configuration File

**Location:** `C:\.agent_click\config\agent_config.json`

**Format:**
```json
{
  "Diagnostic Agent": {
    "context_folder": "C:\\my-project\\src",
    "focus_file": "C:\\my-project\\README.md"
  },
  "Prompt Assistant": {
    "context_folder": "C:\\docs",
    "focus_file": null
  },
  "Implementation Agent": {
    "context_folder": null,
    "focus_file": null
  }
}
```

**Persistence:**
- Auto-created when you save first config
- Maintained across sessions
- Backed up automatically (simple JSON format)

## Technology Stack

### Dependencies (PEP 723)

**Core:**
- `claude-agent-sdk` - Claude Code SDK Python
- `keyboard` - Global hotkey capture with hook system
- `pyperclip` - Clipboard access

**Interface:**
- `PyQt6` - Popup window GUI with tabs and file dialogs

### Design Patterns

- **Strategy Pattern** - BaseAgent (ABC) for different agents
- **Registry Pattern** - AgentRegistry for discovery and management
- **Facade Pattern** - AgentClickSystem coordinates components
- **Factory Pattern** - create_sdk_options() for SDK config
- **Observer Pattern** - Qt signals/slots for thread-safe GUI updates
- **Configuration Manager Pattern** - AgentConfigManager for settings

## Hotkeys

| Hotkey | Action | Description |
|--------|--------|-------------|
| **Pause** | Activate agent | Process selected text with current agent |
| **Ctrl+Pause** | Switch agent | Cycle to next agent (🔍→💻→🔧→🔍) |
| **Click mini popup** | Open details | Open large popup with activity + config |

## Workflow Examples

### Example 1: Configure and Use Prompt Assistant

```
1. Start system
2. Click mini popup (🔍)
3. Press Ctrl+Pause until Prompt Assistant (🔧) shows
4. Go to Config tab
5. Set Context Folder: C:\my-react-app
6. Set Focus File: C:\my-react-app\package.json
7. Click "Save Configuration"
8. Close popup
9. Select text: "create user profile component"
10. Copy text (Ctrl+C)
11. Press Pause
12. Result: Detailed prompt considering React context!
13. Paste where needed (Ctrl+V)
```

### Example 2: Multi-Agent Workflow

```
Scenario: Debugging API issue

1. Configure Diagnostic Agent:
   - Context Folder: C:\api-project
   - Focus File: C:\api-project\api\auth.py

2. Use Diagnostic Agent:
   - Select: "401 error on POST /login"
   - Press Pause (with Diagnostic Agent)
   - Get: Root cause analysis + implementation plan

3. Switch to Implementation Agent:
   - Press Ctrl+Pause
   - Configure same context folder
   - Select the plan text
   - Press Pause
   - Get: Actual code implementation!

4. Done! Both agents used same project context.
```

## Adding New Agents

### Step 1: Create Agent File

Create `C:\.agent_click\agents\my_agent.py`:

```python
from agents.base_agent import BaseAgent, AgentMetadata
from typing import Optional

class MyAgent(BaseAgent):
    @property
    def metadata(self) -> AgentMetadata:
        return AgentMetadata(
            name="My Agent",
            description="Does something awesome",
            icon="⭐",
            color="#ff00ff"
        )

    def get_system_prompt(self, context: str, context_folder: Optional[str] = None, focus_file: Optional[str] = None) -> str:
        prompt = """You are a specialized agent that..."""
        if context_folder or focus_file:
            prompt += f"\n\nProject Context:\n"
            if context_folder:
                prompt += f"Folder: {context_folder}\n"
            if focus_file:
                prompt += f"File: {focus_file}\n"
        return prompt

    def process(self, text: str, context_folder: Optional[str] = None, focus_file: Optional[str] = None) -> str:
        # Custom processing logic
        return super().process(text, context_folder, focus_file)
```

### Step 2: Run System

The agent is automatically discovered and loaded on startup!

## Troubleshooting

### Keyboard Shortcuts Not Working
- Run as Administrator if needed
- Check if Pause key is not disabled in Windows
- Verify keyboard module has permissions
- Look for logs showing "Ctrl PRESSED" and "PAUSE DOWN"

### Mini Popup Not Appearing
- Check logs for "Mini popup initialized"
- Try running with elevated permissions
- Look for Qt errors in console

### Ctrl+Pause Not Switching
- Check console logs for Ctrl detection
- Ensure you're holding Ctrl BEFORE pressing Pause
- Look for "Ctrl PRESSED" message in logs
- Try both left and right Ctrl keys

### Configuration Not Saving
- Check if `C:\.agent_click\config\` directory exists
- Verify write permissions
- Look for "Saved configs" message in logs
- Check if `agent_config.json` is created

### Agent Not Using Configuration
- Ensure you clicked "Save Configuration"
- Verify config is loaded (check fields when opening Config tab)
- Check logs for "Using config - Folder: ..., File: ..."
- Make sure you're using the correct agent

### Popup Not Opening
- Check PyQt6 is installed: `uv pip list`
- Look for error messages in console logs
- Verify mini popup is clickable (cursor changes)
- Try clicking mini popup again

## Requirements

- Python 3.10+
- Windows 10/11
- Internet connection (for Claude SDK)
- Administrator privileges (may be required for global hotkeys)

## Performance

- **Memory:** ~50-100MB (varies by agent usage)
- **CPU:** Minimal when idle
- **Startup:** <2 seconds
- **Processing:** Depends on Claude SDK response time
- **Config load:** <100ms (JSON file)

## Roadmap

### v1.1 (Future)
- [ ] Import/export configurations
- [ ] Configuration templates
- [ ] Recent configurations quick-select
- [ ] Validation of context folder/file paths
- [ ] Visual indicator when agent has config

### v2.0 (Future)
- [ ] Voice input option (like Swiss Knife)
- [ ] File drag-and-drop support
- [ ] Agent chaining (pipeline processing)
- [ ] Custom tools integration
- [ ] MCP server integration
- [ ] More built-in agents (Code Review, Testing, Documentation)

## License

MIT

## Version

**Version:** 1.0
**Date:** 2025-12-27
**Author:** Generated with Claude Code SDK + Astral UV + PyQt6

## Changelog

### v1.0 (2025-12-27) - Initial Release
- ✨ Dual popup system (mini + detailed)
- ✨ 3 specialized agents (Prompt Assistant, Diagnostic, Implementation)
- ✨ Per-agent configuration system
- ✨ Context Folder and Focus File settings
- ✨ Persistent configuration (JSON)
- ✨ Global keyboard hook for reliable Ctrl+Pause detection
- ✨ Tabbed interface (Activity + Config)
- ✨ Independent settings per agent
- ✨ Real-time agent switching with config reload
