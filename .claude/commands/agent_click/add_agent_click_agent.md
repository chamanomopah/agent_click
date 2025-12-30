---
description: Create new AgentClick agents with automatic metadata suggestions and confirmation
argument-hint: [agent-description]
allowed-tools: Read, Write, AskUserQuestion, Glob, Bash
---

# Add AgentClick Agent

Create a new specialized agent for the AgentClick system with automatic metadata suggestions and interactive confirmation.

## Context

The AgentClick system automatically discovers agents from `C:\.agent_click\agents\` folder. Each agent:
- Inherits from `BaseAgent` class
- Defines metadata (name, description, icon, color)
- Implements `get_system_prompt()` and `process()` methods
- Is automatically detected by `agent_registry.py` on system startup

## Your Task

Create a new AgentClick agent based on the user's description by following these steps:

### Step 1: Analyze User Request

**Input:** `"{{agent-description}}"` (all arguments after command name)

Analyze the request to understand:
- What the agent should do
- Category (diagnostics, documentation, testing, implementation, etc.)
- Target use cases

### Step 2: Generate Intelligent Suggestions

Based on the agent's purpose, suggest:

**1. Agent Name (Display Name)**
- Format: `[Function] Agent` or `[Function] Assistant`
- Example: "Code Review Agent", "Documentation Generator", "Testing Assistant"

**2. File Name (snake_case)**
- Format: `{function}_agent.py`
- Example: `code_review_agent.py`, `documentation_agent.py`
- Location: `C:\.agent_click\agents\{filename}`

**3. Class Name (PascalCase)**
- Format: `{Function}Agent`
- Example: `CodeReviewAgent`, `DocumentationAgent`

**4. Icon (Emoji)**
Choose appropriate emoji based on function:
- 👀 Code review/analysis
- 🔒 Security
- 🧪 Testing
- 📚 Documentation
- 💻 Implementation
- ⚡ Performance
- 🔍 Diagnostics
- 🎨 Design/UI
- ♻️ Refactoring
- 🐛 Bug fixing
- 📖 README/docs
- ✨ Features
- 🔧 Configuration
- 📝 Prompts
- 🎯 Targets/goals

**5. Color (Hex #RRGGBB)**
Choose harmonious colors:
- #ff6b6b (soft red) - review, bugs
- #4ecdc4 (turquoise) - documentation
- #95e1d3 (mint) - testing
- #3498db (blue) - implementation
- #f39c12 (orange) - performance
- #9b59b6 (purple) - advanced features
- #2ecc71 (green) - refactoring
- #e74c3c (red) - security
- #fd79a8 (pink) - UI/design
- #6c5ce7 (purple) - accessibility

**6. Description (Short)**
One-line description: what the agent does and its main benefit.

**7. System Prompt (Detailed)**
Create a specialized system prompt that:
- Defines the agent's role and expertise
- Specifies how it should process text
- Explains how to use context_folder and focus_file (if provided)
- Follows the pattern of existing agents

### Step 3: Verify and Validate

Before presenting to user, verify:
- [ ] `C:\.agent_click\agents\` directory exists
- [ ] Suggested filename doesn't conflict with existing agents
- [ ] Color format is valid (#RRGGBB hex)
- [ ] Icon is a single emoji
- [ ] Class name is valid Python identifier
- [ ] File name is snake_case

Read `C:\.agent_click\agents\base_agent.py` if needed to verify structure.

### Step 4: Present Suggestions and Get Confirmation

**Use AskUserQuestion tool** to present suggestions and get confirmation:

```
✨ Suggestions for New Agent:

📝 Name: {suggested_name}
🎨 Icon: {suggested_icon}
🔤 Color: {suggested_color}
📄 Description: {suggested_description}

💾 File: C:\.agent_click\agents\{suggested_filename}
🧩 Class: {suggested_class}

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

**If user selects "Cancel":**
- Thank user and exit

**If user selects "Yes, create agent":**
- Proceed to Step 5

### Step 5: Create Agent File

Create the agent file at `C:\.agent_click\agents\{suggested_filename}` with this template:

```python
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
"""

        # Add project context if available
        if context_folder or focus_file:
            prompt += f"\n\nProject Context:\n"
            if context_folder:
                prompt += f"Context Folder: {context_folder}\n"
            if focus_file:
                prompt += f"Focus File: {focus_file}\n"

        return prompt

    def process(self, text: str, context_folder: Optional[str] = None,
               focus_file: Optional[str] = None) -> str:
        # Use base class implementation that calls Claude SDK
        return super().process(text, context_folder, focus_file)
```

### Step 6: Confirm Success and Provide Next Steps

After creating the file, provide:

```markdown
✅ Agent created successfully!

📁 File: C:\.agent_click\agents\{filename}
🚀 Agent Name: {name}
{icon} Icon: {icon}

🎮 Next Steps:

1. Start the AgentClick system:
   ```bash
   cd C:\.agent_click
   uv run agent_click.py
   ```

2. The agent will be automatically discovered!

3. Switch to your new agent:
   - Press Ctrl+Pause until you see {icon}
   - Or click the mini popup and select from the list

4. Configure your agent (optional):
   - Click the mini popup (bottom-right)
   - Go to "⚙️ Config" tab
   - Set Context Folder and Focus File for project-specific context

5. Use your agent:
   - Select any text
   - Copy (Ctrl+C)
   - Press Pause
   - Result copied to clipboard - paste where needed!

🎉 Your custom agent is ready to use!
```

## Important Notes

1. **File Naming:** Always use snake_case for filenames (e.g., `code_review_agent.py`)
2. **Class Naming:** Always use PascalCase for class names (e.g., `CodeReviewAgent`)
3. **Uniqueness:** Ensure agent names don't conflict with existing agents
4. **System Prompt:** Make it detailed and specific to the agent's function
5. **Context Support:** Always include the context_folder/focus_file block in system prompt
6. **No Manual Registration:** The `agent_registry.py` automatically discovers all agents

## Example Interactions

**Example 1: Documentation Agent**
```
User: /add_agent_click_agent create agent for generating code documentation

Claude suggests:
- Name: Documentation Generator Agent
- Icon: 📚
- Color: #4ecdc4
- File: documentation_agent.py
- Class: DocumentationAgent

User confirms → Agent created
```

**Example 2: Security Review Agent**
```
User: /add_agent_click_agent security auditor

Claude suggests:
- Name: Security Audit Agent
- Icon: 🔒
- Color: #e74c3c
- File: security_audit_agent.py
- Class: SecurityAuditAgent

User wants to modify → User changes icon to 🛡️ → Confirms → Agent created
```

## Troubleshooting

If issues occur:
- Check that `C:\.agent_click\agents\` exists
- Verify `base_agent.py` structure hasn't changed
- Ensure file permissions allow writing
- Check for conflicting agent names
- Verify Python syntax in generated code

---

**AgentClick System** - Multi-agent system with per-agent configuration
For more info, see: C:\.agent_click\README.md
