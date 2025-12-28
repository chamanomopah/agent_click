"""Implementation Agent.

Executes code implementations directly in project files.
"""

from typing import Optional
from agents.base_agent import BaseAgent, AgentMetadata
from pathlib import Path


class ImplementationAgent(BaseAgent):
    """Agent for implementing code changes."""

    @property
    def metadata(self) -> AgentMetadata:
        """Return agent metadata."""
        return AgentMetadata(
            name="Implementation Agent",
            description="Implements code changes in project files",
            icon="💻",
            color="#0078d4"
        )

    def get_system_prompt(self, context: str, context_folder: Optional[str] = None, focus_file: Optional[str] = None) -> str:
        """Get system prompt for implementation agent.

        Args:
            context: File path or implementation context
            context_folder: Optional context folder
            focus_file: Optional focus file

        Returns:
            System prompt
        """
        base_prompt = """You are an expert software developer with deep knowledge across multiple programming languages and frameworks.

Your task is to implement the requested changes following these principles:

**Code Quality:**
- Follow existing project conventions and style
- Write clean, readable, maintainable code
- Add appropriate comments where needed
- Handle errors gracefully

**Implementation:**
- Make precise, surgical changes to existing files
- Preserve existing functionality unless explicitly asked to modify
- Create new files following project structure
- Use appropriate design patterns

**Language/Framework Expertise:**
- Identify the language/framework from context
- Apply best practices specific to that technology
- Follow idiomatic patterns for the language

**Output Format:**
Provide the implementation in a clear, actionable format:
- For existing files: show the exact changes needed (diff format or specific blocks)
- For new files: provide the complete file content
- Include file paths clearly
- Add brief explanations for complex logic

IMPORTANT:
- Return ONLY the implementation details, no meta-commentary
- Be precise and complete
- Ensure code is production-ready
- Include imports and dependencies if needed"""

        # Add context-specific instructions
        if context_folder or focus_file:
            base_prompt += "\n\nPROJECT CONTEXT:\n"
            if context_folder:
                base_prompt += f"Project folder: {context_folder}\n"
                base_prompt += "Create/modify files within this project structure.\n"
            if focus_file:
                base_prompt += f"Focus file: {focus_file}\n"
                base_prompt += "Consider this file's patterns and conventions.\n"
            base_prompt += "Ensure implementation matches project style."

        return base_prompt

    def process(self, text: str, context_folder: Optional[str] = None, focus_file: Optional[str] = None) -> str:
        """Process implementation request.

        Args:
            text: Implementation instructions
            context_folder: Optional context folder
            focus_file: Optional focus file

        Returns:
            Implementation details and code
        """
        self.logger.info("Implementation Agent: Processing implementation")
        result = super().process(text, context_folder, focus_file)
        return result
