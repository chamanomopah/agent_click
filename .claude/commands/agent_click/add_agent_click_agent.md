---
description: Create new AgentClick agents with automatic metadata suggestions and confirmation
argument-hint: [agent-description]
allowed-tools: Read, Write, AskUserQuestion, Glob, Bash
---

# Add AgentClick Agent

Create a new specialized agent for the AgentClick system with automatic metadata suggestions and interactive confirmation.

## High-Level Context

**AgentClick v1.0** is a multi-agent system activated by keyboard shortcuts (Pause/Ctrl+Pause) with:
- **Automatic agent discovery** from `C:\.agent_click\agents\` folder
- **Per-agent configuration** via singleton config manager
- **Multiple input types**: Text Selection, Selected Text (mouse), File Upload, Clipboard Image, Screenshot
- **Multiple output modes**: Auto, Clipboard (Pure/Rich), File, Interactive Editor, Paste Text (at cursor)
- **Qt6-based UI** with mini popup and detailed configuration window

**Current Agents:**
- Prompt Assistant 🔧 (default agent)

Each agent:
- Inherits from `BaseAgent` class
- Defines metadata (name, description, icon, color)
- Implements `get_system_prompt()` method
- Is automatically detected by `agent_registry.py` on system startup
- Has independent configuration (context folder, focus file, input/output modes)

## Your Task

Create a new AgentClick agent based on the user's description by following these steps:

### Step 1: Analyze User Request

**Input:** `"{{agent-description}}"` (all arguments after command name)

Analyze the request to understand:
- What the agent should do
- Category (diagnostics, documentation, testing, implementation, refactoring, etc.)
- Target use cases
- Recommended input/output modes for this agent

### Step 2: Generate Intelligent Suggestions

Based on the agent's purpose, suggest:

**1. Agent Name (Display Name)**
- Format: `[Function] Agent` or `[Function] Assistant`
- Example: "Code Review Agent", "Documentation Generator", "Testing Assistant"
- Should be concise and descriptive

**2. File Name (snake_case)**
- Format: `{function}_agent.py`
- Example: `code_review_agent.py`, `documentation_agent.py`
- Location: `C:\.agent_click\agents\{filename}`
- Must not conflict with existing agents

**3. Class Name (PascalCase)**
- Format: `{Function}Agent`
- Example: `CodeReviewAgent`, `DocumentationAgent`
- Valid Python identifier (no spaces, special chars)

**4. Icon (Emoji)**
Choose appropriate emoji based on function:
- 👀 Code review/analysis
- 🔒 Security/auditing
- 🧪 Testing/quality
- 📚 Documentation
- 💻 Implementation
- ⚡ Performance/optimization
- 🔍 Diagnostics/debugging
- 🎨 Design/UI
- ♻️ Refactoring/cleanup
- 🐛 Bug fixing
- 📖 README/docs
- ✨ Features/enhancement
- 🔧 Configuration/setup
- 📝 Prompts/writing
- 🎯 Targets/goals
- 🌐 Internationalization
- 📊 Analytics/metrics

**5. Color (Hex #RRGGBB)**
Choose harmonious colors:
- #ff6b6b (soft red) - review, bugs, critical
- #4ecdc4 (turquoise) - documentation, writing
- #95e1d3 (mint) - testing, quality
- #3498db (blue) - implementation, coding
- #f39c12 (orange) - performance, optimization
- #9b59b6 (purple) - advanced features, architecture
- #2ecc71 (green) - refactoring, improvement
- #e74c3c (red) - security, vulnerabilities
- #fd79a8 (pink) - UI/design, frontend
- #6c5ce7 (purple) - accessibility, UX
- #1abc9c (teal) - database, backend
- #34495e (dark blue) - infrastructure, DevOps

**6. Description (Short)**
One-line description: what the agent does and its main benefit.
- Format: "Verbs [target] to [benefit]"
- Example: "Analyzes code quality to identify improvement opportunities"

**7. System Prompt (Detailed)**
Create a specialized system prompt that:
- Defines the agent's role and expertise
- Specifies how it should process text
- Explains how to use context_folder and focus_file (if provided)
- Specifies output format expectations
- Follows the pattern of existing agents
- Is detailed enough for consistent behavior

**8. Recommended Input/Output Modes** (NEW)
Based on agent function, suggest:

**Input Options:**
- Text Selection (clipboard) - default, works with copied text
- Selected Text (mouse) - captures selection without Ctrl+C
- File Upload (drag & drop) - for processing entire files
- Clipboard Image - for visual analysis/screenshots
- Screenshot (Ctrl+Shift+Pause) - for capturing UI

**Output Options:**
- 🤖 Auto (Agent Decide) - agent chooses best output
- 📋 Clipboard (Pure) - raw content only
- 📋 Clipboard (Rich) - with metadata/formatting
- 💾 Save to File - saves to project folder
- ✏️ Interactive Editor - preview and edit before output
- 📝 Paste Text (at cursor) - auto-paste at insertion point

### Step 3: Verify and Validate

Before presenting to user, verify:
- [ ] `C:\.agent_click\agents\` directory exists
- [ ] Suggested filename doesn't conflict with existing agents
- [ ] Color format is valid (#RRGGBB hex)
- [ ] Icon is a single emoji
- [ ] Class name is valid Python identifier
- [ ] File name is snake_case
- [ ] Agent name doesn't conflict with existing agents

Read `C:\.agent_click\agents\base_agent.py` if needed to verify structure.

Check existing agents:
```bash
ls C:\.agent_click\agents\*.py
```

### Step 4: Present Suggestions and Get Confirmation

**Use AskUserQuestion tool** to present suggestions and get confirmation with 3 options:

```
✨ Suggestions for New Agent:

📝 Name: {suggested_name}
🎨 Icon: {suggested_icon}
🔤 Color: {suggested_color}
📄 Description: {suggested_description}

💾 File: C:\.agent_click\agents\{suggested_filename}
🧩 Class: {suggested_class}

🎮 Recommended Input: {input_mode}
📤 Recommended Output: {output_mode}

🤖 System Prompt (excerpt):
{first_3_lines_of_system_prompt}...

Ready to create this agent?

Options:
- ✅ Yes, create agent
- ✏️ Modify fields
- ❌ Cancel
```

**If user selects "Modify fields":**
- Ask which fields to modify
- Present new suggestions
- Ask for confirmation again
- Loop until user confirms or cancels

**If user selects "Cancel":**
- Thank user and exit gracefully

**If user selects "Yes, create agent":**
- Proceed to Step 5

### Step 5: Create Agent File

Create the agent file at `C:\.agent_click\agents\{suggested_filename}` with this template:

```python
"""Agent description (one line)."""

from agents.base_agent import BaseAgent, AgentMetadata
from typing import Optional

class {SuggestedClass}(BaseAgent):
    @property
    def metadata(self) -> AgentMetadata:
        return AgentMetadata(
            name="{SuggestedName}",
            description="{SuggestedDescription}",
            icon="{SuggestedIcon}",
            color="{SuggestedColor}"
        )

    def get_system_prompt(self, context: str, context_folder: Optional[str] = None,
                         focus_file: Optional[str] = None) -> str:
        prompt = """You are a specialized agent that {does_what}.

{Detailed_instructions_for_how_to_process_text}

{Instructions_about_using_context_folder_and_focus_file_if_provided}

{Output_format_expectations}
"""

        # Add project context if available
        if context_folder or focus_file:
            prompt += "\n\nPROJECT CONTEXT:\n"
            if context_folder:
                prompt += f"• Context Folder: {context_folder}\n"
            if focus_file:
                prompt += f"• Focus File: {focus_file}\n"
            prompt += "\nConsider this project context when processing."

        return prompt

    def process(self, text: str, context_folder: Optional[str] = None,
               focus_file: Optional[str] = None, output_mode: str = "AUTO",
               image_path: Optional[str] = None) -> str:
        # Use base class implementation that calls Claude SDK
        return super().process(text, context_folder, focus_file, output_mode, image_path)
```

### Step 6: Confirm Success and Provide Next Steps

After creating the file, provide:

```markdown
✅ Agent created successfully!

📁 File: C:\.agent_click\agents\{filename}
🚀 Agent Name: {name}
{icon} Icon: {icon}
🔤 Color: {color}

🎮 Next Steps:

1. Restart the AgentClick system (if running):
   - Press Ctrl+C in the terminal to stop
   - Run: cd C:\.agent_click && uv run agent_click.py

2. The agent will be automatically discovered!
   - Check log: "Registered agent: {name} ({icon})"

3. Switch to your new agent:
   - Press Ctrl+Pause until you see {icon} in mini popup
   - Or click the mini popup (bottom-right corner)

4. Configure your agent (optional but recommended):
   - Click the mini popup
   - Go to "⚙️ Config" tab
   - Set:
     • Input: {recommended_input}
     • Output: {recommended_output}
     • Context Folder: (your project path)
     • Focus File: (specific file if needed)
   - Click "💾 Save Configuration"

5. Use your agent:
   - Select text based on your input mode
   - Press Pause
   - Result delivered based on output mode!

🎉 Your custom agent is ready to use!

💡 Tip: Each agent has independent configuration. Switch between agents
   with Ctrl+Pause and each will remember its own settings.
```

## Important Implementation Details

### 1. File Naming Convention
- **Filenames**: snake_case (e.g., `code_review_agent.py`)
- **Class names**: PascalCase (e.g., `CodeReviewAgent`)
- **Display names**: Title Case with spaces (e.g., "Code Review Agent")

### 2. Agent Uniqueness
- Agent names must be unique
- Check existing agents before suggesting
- Avoid generic names like "Helper" or "Assistant"

### 3. System Prompt Best Practices
- **Be specific**: Define exactly what the agent does
- **Set expectations**: Output format, tone, level of detail
- **Handle context**: Explain how to use context_folder/focus_file
- **Define boundaries**: What the agent should and shouldn't do
- **Quality focus**: Emphasize accuracy, clarity, and usefulness

### 4. Input/Output Recommendations

**For Analysis Agents** (code review, diagnostics):
- Input: Text Selection or Selected Text
- Output: Clipboard (Rich) for detailed reports

**For Implementation Agents** (code generation, refactoring):
- Input: Text Selection, File Upload
- Output: Clipboard (Pure) or File

**For Documentation Agents**:
- Input: Text Selection, File Upload, Screenshot
- Output: Clipboard (Rich) or File

**For Interactive Tasks**:
- Input: Any
- Output: Interactive Editor (for preview/edit)

**For Direct Paste** (ChatGPT, Claude, etc.):
- Input: Any
- Output: Paste Text (at cursor)

### 5. Configuration System
- **Singleton pattern**: Config manager is shared across system
- **Per-agent settings**: Each agent has independent config
- **Persistent**: Saved to `C:\.agent_click\config\agent_config.json`
- **Auto-load**: Settings loaded when agent is activated

### 6. No Manual Registration Needed
The `agent_registry.py` automatically discovers all agents:
- Scans `C:\.agent_click\agents\` on startup
- Finds all `*Agent` classes inheriting from `BaseAgent`
- Instantiates and registers them automatically
- Just create the file - that's it!

## Example Interactions

**Example 1: Documentation Generator Agent**
```
User: /add_agent_click_agent create agent for generating code documentation

Claude suggests:
- Name: Documentation Generator Agent
- Icon: 📚
- Color: #4ecdc4
- File: documentation_generator_agent.py
- Class: DocumentationGeneratorAgent
- Input: File Upload, Text Selection
- Output: File, Clipboard (Rich)

User confirms → Agent created → Instructions provided
```

**Example 2: Security Review Agent**
```
User: /add_agent_click_agent security auditor that checks for vulnerabilities

Claude suggests:
- Name: Security Audit Agent
- Icon: 🔒
- Color: #e74c3c
- File: security_audit_agent.py
- Class: SecurityAuditAgent
- Input: Text Selection, File Upload
- Output: Clipboard (Rich) with detailed findings

User wants to modify → Changes icon to 🛡️ → Confirms → Agent created
```

**Example 3: Code Refactoring Agent**
```
User: /add_agent_click_agent refactoring helper

Claude suggests:
- Name: Code Refactoring Agent
- Icon: ♻️
- Color: #2ecc71
- File: code_refactoring_agent.py
- Class: CodeRefactoringAgent
- Input: Selected Text (mouse)
- Output: Paste Text (at cursor) for direct replacement

User confirms → Agent created → Ready to use
```

## Troubleshooting

### Common Issues

**Issue**: Agent not discovered
- **Solution**: Check file is in `C:\.agent_click\agents\`
- **Solution**: Verify class inherits from `BaseAgent`
- **Solution**: Restart AgentClick system
- **Solution**: Check logs for import errors

**Issue**: Import error
- **Solution**: Verify Python syntax in generated file
- **Solution**: Check all imports are correct
- **Solution**: Run `python -m py_compile agents\your_file.py`

**Issue**: Agent name conflict
- **Solution**: Check existing agents: `ls C:\.agent_click\agents\*.py`
- **Solution**: Use more specific name

**Issue**: Config not saving
- **Solution**: Check write permissions to `C:\.agent_click\config\`
- **Solution**: Verify JSON format in agent_config.json

**Issue**: Input/output not working
- **Solution**: Verify recommended modes match agent function
- **Solution**: Check agent configuration in UI
- **Solution**: Test with different input/output modes

### Verification Commands

```bash
# List existing agents
ls C:\.agent_click\agents\*.py

# Check syntax
python -m py_compile C:\.agent_click\agents\your_agent.py

# Test import
python -c "from agents.your_agent import YourAgent; print('OK')"

# Check config
cat C:\.agent_click\config\agent_config.json
```

## Advanced Customization

### Custom Processing Logic

If the agent needs custom processing beyond base class:

```python
def process(self, text: str, context_folder: Optional[str] = None,
           focus_file: Optional[str] = None, output_mode: str = "AUTO",
           image_path: Optional[str] = None) -> str:
    # Custom pre-processing
    if text and len(text) > 10000:
        self.logger.info("Processing large text, optimizing...")

    # Call base class for SDK interaction
    result = super().process(text, context_folder, focus_file, output_mode, image_path)

    # Custom post-processing
    self.logger.info(f"Processed {len(result.content)} chars")
    return result
```

### Context-Aware Processing

```python
def get_system_prompt(self, context: str, context_folder: Optional[str] = None,
                     focus_file: Optional[str] = None) -> str:
    base_prompt = """You are a specialized agent..."""

    # Add project-specific context
    if context_folder:
        project_name = Path(context_folder).name
        base_prompt += f"\n\nWorking in project: {project_name}"

    if focus_file:
        file_ext = Path(focus_file).suffix
        base_prompt += f"\n\nFocus file type: {file_ext}"

    return base_prompt
```

---

**AgentClick v1.0** - Multi-agent system with per-agent configuration
- Project: C:\.agent_click\
- Documentation: C:\.agent_click\README.md
- Agents Directory: C:\.agent_click\agents\
- Config: C:\.agent_click\config\agent_config.json

For system architecture details, see: C:\.agent_click\README.md
