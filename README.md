# AgentClick System v1.1

Multi-agent system with dual popup interface, multiple input types (text, file, image, screenshot), per-agent configuration management, and intelligent input filtering.

**What it does:** Mini popup shows agent → Click to configure/use → Provide input (text/file/image/screenshot) → Press Pause → Agent processes with custom context → Result delivered based on Output Mode setting.

## Features

### Main Features
- 🎯 **Mini popup** - Small, discreet indicator always visible (60x60px)
- 🖥️ **Detailed popup** - Large popup with activity log and configuration (opens on click)
- 🎯 **Click activation** - Press Pause to activate current agent
- 🔄 **Agent switching** - Press Ctrl+Pause to switch agents (updates mini popup)
- ⚙️ **Per-agent configuration** - Each agent has independent Context Folder, Focus File, and Allowed Inputs settings
- 📋 **Clipboard integration** - Automatic copy/paste
- 🤖 **Specialized agents** - Prompt Assistant for prompt refinement
- 🎨 **Visual feedback** - Color-coded agent icons
- 💾 **Persistent configuration** - Settings saved in JSON, maintained across sessions
- 🎯 **Multiple input types** - Text selection, file upload, clipboard image, screenshot

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
  - **⚙️ Config**: Per-agent configuration settings (Context Folder, Focus File, Output Mode, Allowed Inputs)
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

3. **Output Mode** (NEW)
   - How the agent delivers results
   - Options: Auto, Pure Clipboard, Rich Clipboard, File, Interactive Editor
   - Default: Auto (agent decides best output)

4. **Allowed Inputs** (NEW)
   - Which input types the agent accepts
   - Options: Text Selection, File Upload, Clipboard Image, Screenshot
   - Default: All inputs enabled
   - Customize per agent (e.g., different inputs for different use cases)

**How it works:**
- Settings are **per-agent** (each agent has independent configuration)
- Configurations persist in `C:\.agent_click\config\agent_config.json`
- When you switch agents (Ctrl+Pause), the config tab shows that agent's specific settings
- Agent receives context_folder, focus_file, and input filtering when processing

## Available Agents

### Prompt Assistant 🔧

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

## Input Types

The AgentClick system supports **multiple input types** for maximum flexibility:

### 1. ✅ Text Selection (Default)
- **How:** Select text anywhere → Copy (Ctrl+C) → Press Pause
- **Use case:** Standard text processing
- **Works in:** Any application with copy functionality
- **Example:** Select code in VSCode, copy, press Pause

### 2. 📎 File Upload (NEW)
- **How:** Drag file to mini popup → Auto-processes
- **Use case:** Processing entire files
- **Supported:** Text files, code files, JSON, YAML, etc.
- **Example:** Drag `config.json` to mini popup for analysis

### 3. 🖼️ Clipboard Image (NEW)
- **How:** Copy image (Ctrl+C) → Press Pause
- **Use case:** Visual analysis, UI debugging, screenshot processing
- **Works in:** Browser, file explorer, screenshot tools
- **Example:** Copy error screenshot, press Pause for diagnosis

### 4. 📸 Screenshot (NEW)
- **How:** Press Ctrl+Shift+Pause
- **Use case:** Capture current screen for analysis
- **Captures:** Entire screen or active window
- **Example:** Debug UI issue by taking screenshot

### 5. 📝 VSCode Active File (NEW)
- **How:** Have file open in VSCode → Press Pause
- **Use case:** Quick analysis of file you're actively working on
- **Works in:** VSCode only (Windows only)
- **Requirements:** File must be saved to disk (not Untitled)
- **Example:** Working on `app.py` in VSCode → Press Pause → Agent receives entire file
- **Supported file types:** Text files, code files (Python, JS, JSON, YAML, etc.)
- **Not supported:** Binary files, unsaved files, remote files (SSH/WSL)

### Input Type Priority (Auto-Detection)

When you press Pause, the system automatically detects the best available input:
1. **Text Selection** - If text in clipboard (most common)
2. **Selected Text** - If text selected with mouse
3. **VSCode Active File** - If VSCode is active window with a file
4. **File Upload** - If file was dragged to mini popup
5. **Clipboard Image** - If image in clipboard
6. **Screenshot** - Only when explicitly triggered (Ctrl+Shift+Pause)

### Per-Agent Input Filtering

Each agent can be configured to accept only specific input types:
- **Prompt Assistant** 🔧: All inputs available (text, file, image, screenshot)

Configure this in the **Config tab** under "Input" option.

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
- Shows current agent icon (🔧 Prompt Assistant)
- Agent loads with its saved configuration

**To process with text input:**
1. **Select text** in any application
2. **Copy text** (Ctrl+C) to clipboard
3. **Press Pause** to process with current agent
4. **Result automatically copied** to clipboard
5. **Paste result** (Ctrl+V) where needed

**To process with file upload (NEW):**
1. **Drag file** to mini popup (bottom-right)
2. File is automatically loaded and processed
3. Result is delivered according to Output Mode setting

**To process with image/screenshot (NEW):**
1. **Copy image** to clipboard (Ctrl+C on any image)
2. **Press Pause** to analyze the image
3. OR press **Ctrl+Shift+Pause** to take screenshot
4. Agent receives image path for visual analysis

**To configure agents:**
1. **Click the mini popup** (bottom-right)
2. Detailed popup opens
3. **Go to "⚙️ Config" tab**
4. **Configure for current agent:**
   - Click "📁 Browse" to select Context Folder
   - Click "📄 Browse" to select Focus File
   - Select Output Mode from dropdown
   - Check/uncheck Allowed Input Types
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
- Output Mode dropdown
- Allowed Input Types checkboxes (Text, File, Image, Screenshot)
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
│   ├── click_processor.py      # Keyboard shortcuts (Pause, Ctrl+Pause, Ctrl+Shift+Pause)
│   ├── selection_manager.py    # Clipboard operations
│   ├── input_manager.py        # Input strategy manager (NEW)
│   ├── input_strategy.py       # Input strategy base classes (NEW)
│   └── input_strategies/       # Input type implementations (NEW)
│       ├── __init__.py
│       ├── text_selection_strategy.py
│       ├── file_upload_strategy.py
│       ├── clipboard_image_strategy.py
│       └── screenshot_strategy.py
│
├── agents/                     # Agent implementations
│   ├── __init__.py
│   ├── base_agent.py           # Abstract base class
│   ├── agent_registry.py       # Agent discovery and management
│   ├── prompt_assistant_agent.py   # 🔧 Refines prompts
│   └── output_modes.py         # Output mode definitions
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
Prompt Assistant settings:
{
  "context_folder": "C:\\my-project",
  "focus_file": "C:\\my-project\\main.py",
  "output_mode": "CLIPBOARD_PURE",
  "allowed_inputs": ["text_selection"]
}
```

**2. Settings Impact Processing:**
```
User selects text: "add error handling"
User presses Pause

System:
1. Detects current agent: "Prompt Assistant"
2. Loads agent's config
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
  "Prompt Assistant": {
    "context_folder": "C:\\my-project",
    "focus_file": "C:\\my-project\\main.py",
    "output_mode": "CLIPBOARD_PURE",
    "allowed_inputs": ["text_selection"]
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

**System Integration:**
- `pywin32` - Windows API access for VSCode window detection

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
| **Pause** | Activate agent | Process input (auto-detects best available input type) |
| **Ctrl+Pause** | Switch agent | Cycle to next agent (🔍→💻→🔧→🔍) |
| **Ctrl+Shift+Pause** | Screenshot | Take screenshot for analysis (NEW) |
| **Drag file to mini popup** | File upload | Load and process file (NEW) |
| **Click mini popup** | Open details | Open large popup with activity + config |

## Workflow Examples

### Example 1: Use File Upload for Code Analysis (NEW)

```
1. Start system
2. Switch to Diagnostic Agent (Ctrl+Pause until 🔍 shows)
3. Drag file: C:\my-project\buggy_function.py
4. System auto-processes file
5. Result: Detailed analysis of the entire file!
```

### Example 2: Configure Input Types per Agent (NEW)

```
1. Open Config tab for Prompt Assistant (🔧)
2. Uncheck: File Upload, Clipboard Image, Screenshot
3. Check: Text Selection only
4. Save Configuration
5. Now Prompt Assistant only accepts text input!
   (Prevents accidental image/file processing)
```

### Example 4: Configure and Use Prompt Assistant

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

**Version:** 1.1
**Date:** 2025-12-30
**Author:** Generated with Claude Code SDK + Astral UV + PyQt6

## Changelog

### v1.1 (2025-12-30) - Multiple Input Types
- ✨ Multiple input types support (Text, File, Image, Screenshot)
- ✨ File upload via drag & drop to mini popup
- ✨ Clipboard image processing
- ✨ Screenshot capture (Ctrl+Shift+Pause)
- ✨ Per-agent input filtering (Allowed Inputs configuration)
- ✨ Output Mode configuration (Auto, Pure, Rich, File, Editor)
- ✨ Strategy Pattern for input handling
- ✨ Input auto-detection with priority system
- ✨ Visual feedback for drag & drop
- ✨ Enhanced configuration UI with checkboxes

### v1.0 (2025-12-27) - Initial Release
- ✨ Dual popup system (mini + detailed)
- ✨ Prompt Assistant agent for prompt refinement
- ✨ Per-agent configuration system
- ✨ Context Folder and Focus File settings
- ✨ Persistent configuration (JSON)
- ✨ Multiple input types (text, file, image, screenshot)
- ✨ Multiple output modes (clipboard, file, paste at cursor)
- ✨ Global keyboard hook for reliable Ctrl+Pause detection
- ✨ Tabbed interface (Activity + Config)
- ✨ Independent settings per agent
- ✨ Real-time agent switching with config reload
