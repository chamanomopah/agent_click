"""Diagnostic Agent.

Analyzes problems and provides detailed diagnosis with implementation plans.
"""

from typing import Optional
from agents.base_agent import BaseAgent, AgentMetadata


class DiagnosticAgent(BaseAgent):
    """Agent for diagnosing problems and creating action plans."""

    @property
    def metadata(self) -> AgentMetadata:
        """Return agent metadata."""
        return AgentMetadata(
            name="Diagnostic Agent",
            description="Analyzes problems and creates implementation plans",
            icon="🔍",
            color="#d83b01"
        )

    def get_system_prompt(self, context: str, context_folder: Optional[str] = None, focus_file: Optional[str] = None) -> str:
        """Get system prompt for diagnostic agent.

        Args:
            context: Problem description
            context_folder: Optional context folder
            focus_file: Optional focus file

        Returns:
            System prompt
        """
        base_prompt = """You are an expert software architect and debugging specialist.

Your task is to analyze the problem described and provide:
1. **Root Cause Analysis**: Identify the underlying cause of the problem
2. **Impact Assessment**: Explain what systems/components are affected
3. **Solution Approaches**: Present 2-3 viable approaches to fix it
4. **Implementation Plan**: Detailed step-by-step plan with:
   - Specific tasks in execution order
   - Dependencies between tasks
   - Risk considerations
   - Testing/validation steps

Format your response clearly with sections and bullet points.
Be specific and actionable.
Focus on practical solutions that can be implemented immediately.

IMPORTANT:
- Return ONLY the diagnosis and plan, no meta-commentary
- Use markdown formatting for readability
- Prioritize solutions by practicality
- Include code examples if relevant"""

        # Add context-specific instructions
        if context_folder or focus_file:
            base_prompt += "\n\nPROJECT CONTEXT:\n"
            if context_folder:
                base_prompt += f"Project folder: {context_folder}\n"
            if focus_file:
                base_prompt += f"Focus file: {focus_file}\n"
            base_prompt += "Consider this project context when analyzing the problem."

        return base_prompt

    def process(self, text: str, context_folder: Optional[str] = None, focus_file: Optional[str] = None, output_mode: str = "AUTO", image_path: Optional[str] = None) -> str:
        """Process problem description.

        Args:
            text: Problem description
            context_folder: Optional context folder
            focus_file: Optional focus file
            output_mode: Output mode (AUTO, CLIPBOARD_PURE, etc.)
            image_path: Optional image path for visual analysis

        Returns:
            Detailed diagnosis and implementation plan
        """
        self.logger.info("Diagnostic Agent: Analyzing problem")
        result = super().process(text, context_folder, focus_file, output_mode, image_path)
        return result
