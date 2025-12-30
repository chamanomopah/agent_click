"""Testing Agent.

Generates comprehensive test cases and testing strategies.
"""

from typing import Optional
from agents.base_agent import BaseAgent, AgentMetadata


class TestingAgent(BaseAgent):
    """Agent for generating test plans and test cases."""

    @property
    def metadata(self) -> AgentMetadata:
        """Return agent metadata."""
        return AgentMetadata(
            name="Testing Assistant Agent",
            description="Generates comprehensive test cases and testing strategies",
            icon="🧪",
            color="#95e1d3"
        )

    def get_system_prompt(self, context: str, context_folder: Optional[str] = None, focus_file: Optional[str] = None) -> str:
        """Get system prompt for testing agent.

        Args:
            context: Code, feature, or requirements to test
            context_folder: Optional context folder
            focus_file: Optional focus file

        Returns:
            System prompt
        """
        base_prompt = """You are an expert QA engineer and testing specialist.

Your task is to analyze code, features, or requirements and provide:
1. **Test Strategy**: Overall testing approach and methodology
2. **Test Cases**: Detailed test cases with:
   - Test description
   - Preconditions
   - Test steps
   - Expected results
   - Edge cases to cover
3. **Test Coverage**: What areas/components need testing
4. **Testing Tools**: Suggestions for frameworks and tools

IMPORTANT:
- Return ONLY the test plan and test cases
- Include unit, integration, and E2E tests as appropriate
- Consider edge cases, error scenarios, and boundary conditions
- Suggest appropriate testing frameworks (pytest, jest, junit, etc.)
- Include both positive and negative test scenarios
- Consider performance and security testing if relevant
- Use clear formatting with markdown for readability"""

        # Add context-specific instructions
        if context_folder or focus_file:
            base_prompt += "\n\nPROJECT CONTEXT:\n"
            if context_folder:
                base_prompt += f"Project folder: {context_folder}\n"
            if focus_file:
                base_prompt += f"Focus file: {focus_file}\n"
            base_prompt += "Consider this project context when designing tests."

        return base_prompt

    def process(self, text: str, context_folder: Optional[str] = None, focus_file: Optional[str] = None) -> str:
        """Process code/requirements and generate tests.

        Args:
            text: Code, feature, or requirements to test
            context_folder: Optional context folder
            focus_file: Optional focus file

        Returns:
            Comprehensive test plan and test cases
        """
        self.logger.info("Testing Agent: Generating test plan")
        result = super().process(text, context_folder, focus_file)
        return result
