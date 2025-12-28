"""Prompt Assistant Agent.

Expands and refines user prompts with better context and structure.
"""

from agents.base_agent import BaseAgent, AgentMetadata
from typing import Optional
from pathlib import Path


class PromptAssistantAgent(BaseAgent):
    """Agent for assisting with prompt creation and refinement."""

    @property
    def metadata(self) -> AgentMetadata:
        """Return agent metadata."""
        return AgentMetadata(
            name="Prompt Assistant",
            description="Expands and refines prompts with better structure",
            icon="🔧",
            color="#107c10"
        )

    def get_system_prompt(self, context: str, context_folder: Optional[str] = None, focus_file: Optional[str] = None) -> str:
        """Get system prompt for prompt assistant.

        Args:
            context: User's original prompt text
            context_folder: Optional context folder
            focus_file: Optional focus file

        Returns:
            System prompt
        """
        base_prompt = """You are an expert at crafting clear, well-structured prompts for AI interactions.

Your task is to take the user's input and transform it into a polished, professional prompt that:
1. Has clear context and background
2. States requirements precisely
3. Provides structure and organization
4. Uses appropriate formatting (markdown, bullet points, etc.)
5. Includes relevant examples or constraints if helpful

IMPORTANT:
- Return ONLY the refined prompt, no explanations
- Make it actionable and specific
- Use professional language
- Add relevant technical context when appropriate
- Format for readability

The user's original input will be provided - transform it into an excellent prompt."""

        # Add context-specific instructions
        if context_folder or focus_file:
            base_prompt += "\n\nADDITIONAL CONTEXT:\n"
            if context_folder:
                base_prompt += f"The user is working in a project located at: {context_folder}\n"
            if focus_file:
                base_prompt += f"There is a focus file at: {focus_file}\n"
            base_prompt += "Consider this project context when refining the prompt."

        return base_prompt

    def process(self, text: str, context_folder: Optional[str] = None, focus_file: Optional[str] = None) -> str:
        """Process text with prompt assistant.

        Args:
            text: User's original prompt
            context_folder: Optional context folder
            focus_file: Optional focus file

        Returns:
            Refined, expanded prompt
        """
        self.logger.info("Prompt Assistant: Refining prompt")
        result = super().process(text, context_folder, focus_file)
        return result
