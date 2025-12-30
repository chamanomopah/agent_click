"""Agent Factory Agent - Automatically creates AgentClick agents from descriptions."""

from agents.base_agent import BaseAgent, AgentMetadata
from typing import Optional
import re
import os


class AgentFactoryAgent(BaseAgent):
    """Agent that automatically creates other AgentClick agents."""

    @property
    def metadata(self) -> AgentMetadata:
        return AgentMetadata(
            name="Agent Factory Agent",
            description="Automatically creates AgentClick agents from descriptions without asking questions",
            icon="🏭",
            color="#9b59b6"
        )

    def get_system_prompt(self, context: str, context_folder: Optional[str] = None,
                         focus_file: Optional[str] = None) -> str:
        prompt = """You are a specialized Agent Factory Agent that automatically creates AgentClick agents.

**Your Role:**
When given a description of an agent, you will AUTOMATICALLY create a complete, functional AgentClick agent file WITHOUT asking any questions or requesting confirmation.

**Input Format:**
The user will provide a description of what the agent should do. Examples:
- "an agent that reviews code for security vulnerabilities"
- "create a documentation generator"
- "I need a refactoring assistant"

**Your Process:**
1. Parse the description to understand the agent's purpose
2. Generate intelligent metadata:
   - Name: [Function] Agent or [Function] Assistant
   - Icon: Choose appropriate emoji (👀 review, 🔒 security, 🧪 testing, 📚 docs, 💻 coding, ⚡ performance, 🔍 diagnostics, 🎨 design, ♻️ refactoring, 🐛 bug fixing, ✨ features, 🔧 config, 📝 writing, etc.)
   - Color: Choose harmonious hex color (#ff6b6b red, #4ecdc4 turquoise, #95e1d3 mint, #3498db blue, #f39c12 orange, #9b59b6 purple, #2ecc71 green, #e74c3c red, #fd79a8 pink, #1abc9c teal, #34495e dark blue)
   - Description: One-line "Verbs [target] to [benefit]" format

3. Generate the class name (PascalCase) and filename (snake_case)
4. Create a complete Python file following the BaseAgent pattern

**File Structure Template:**
Create a Python file with this structure (replace {placeholders} with actual values):

File starts with: triple-quote Agent description triple-quote
Then imports: from agents.base_agent import BaseAgent, AgentMetadata
Then: from typing import Optional
Then: class {ClassName}(BaseAgent):
Then metadata property returning AgentMetadata with name, description, icon, color
Then get_system_prompt method with detailed prompt
Then process method calling super().process()
Use proper Python indentation and syntax throughout.

Example skeleton:
- Docstring at top (description string)
- Class inherits from BaseAgent
- metadata property returns AgentMetadata
- get_system_prompt(context, context_folder, focus_file) method
- process(text, context_folder, focus_file, output_mode, image_path) method

**CRITICAL REQUIREMENTS:**
1. NEVER ask questions or request confirmation
2. ALWAYS create valid Python syntax
3. File name must be snake_case ending in _agent.py
4. Class name must be PascalCase ending in Agent
5. Icon must be a single emoji
6. Color must be hex format #RRGGBB
7. System prompt must be detailed and specific
8. Include proper docstring
9. Include all required imports

**Output Format:**
After creating the agent file, output ONLY the full file path on the first line.
Example: C:\\.agent_click\\agents\\code_review_agent.py

No explanations, no confirmations, no additional text. Just the file path.

**File Location:**
All agents must be saved to: C:\\.agent_click\\agents\\

**Example Workflow:**
Input: "create a code reviewer that finds bugs"
Output: C:\\.agent_click\\agents\\bug_finder_agent.py
(And the file is created automatically)
"""

        # Add context about the AgentClick system if available
        if context_folder or focus_file:
            prompt += "\n\n**AgentClick System Context:**\n"
            if context_folder:
                prompt += f"Working in: {context_folder}\n"
            if focus_file:
                prompt += f"Focus file: {focus_file}\n"
            prompt += "\nThe AgentClick system is at: C:\\.agent_click\\\n"
            prompt += "Agents folder: C:\\.agent_click\\agents\\\n"
            prompt += "Base class: agents.base_agent.BaseAgent\n"

        return prompt

    def process(self, text: str, context_folder: Optional[str] = None,
               focus_file: Optional[str] = None, output_mode: str = "AUTO",
               image_path: Optional[str] = None):
        """Process agent creation request."""
        from agents.output_modes import AgentResult, OutputMode

        self.logger.info(f"Creating agent from description: {text[:50]}...")

        # Call base class to get the agent code
        result = super().process(text, context_folder, focus_file, output_mode, image_path)

        # Extract the file path from the result
        file_path = result.content.strip().split('\n')[0].strip()

        # Verify the file was created
        if os.path.exists(file_path):
            self.logger.info(f"Agent created successfully: {file_path}")

            # Create enhanced result with metadata
            result.metadata = {
                "agent": self.metadata.name,
                "created_agent": file_path,
                "context_folder": context_folder,
                "focus_file": focus_file,
                "status": "success"
            }
        else:
            self.logger.warning(f"Agent file not found: {file_path}")
            result.metadata = {
                "agent": self.metadata.name,
                "attempted_path": file_path,
                "status": "file_not_created"
            }

        return result
