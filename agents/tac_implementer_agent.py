"""TAC Implementer Agent.

Reads and implements TAC plans from specs/*.md files with step-by-step execution and completion reports.
"""

from agents.base_agent import BaseAgent, AgentMetadata
from typing import Optional
from pathlib import Path


class TacImplementerAgent(BaseAgent):
    """Agent for implementing TAC plans from specs/*.md files."""

    @property
    def metadata(self) -> AgentMetadata:
        """Return agent metadata."""
        return AgentMetadata(
            name="TAC Implementer",
            description="Reads and implements TAC plans from specs/*.md files with step-by-step execution and completion reports",
            icon="🚀",
            color="#3498db"
        )

    def get_system_prompt(self, context: str, context_folder: Optional[str] = None, focus_file: Optional[str] = None) -> str:
        """Get system prompt for TAC implementer.

        Args:
            context: Plan content (specs/*.md file content)
            context_folder: Optional context folder (where the codebase is)
            focus_file: Optional focus file

        Returns:
            System prompt
        """
        base_prompt = """You are a specialized agent that implements TAC plans by reading plan files and executing them step by step.

Your task is to:
1. Read and understand the provided plan (from specs/*.md)
2. Think hard about the plan requirements
3. Implement the plan by following the steps precisely
4. Report the completed work with a summary

## CRITICAL INSTRUCTIONS:

1. **READ THE PLAN FIRST**:
   - Understand the full plan before starting
   - Identify the type (Chore, Feature, or Bug)
   - Note all relevant files
   - Understand the acceptance criteria or validation requirements

2. **FOLLOW THE PLAN PRECISELY**:
   - Execute steps in the exact order specified
   - Don't skip steps or combine them
   - Follow the implementation plan as written
   - Respect any constraints mentioned (minimal changes, no decorators, etc.)

3. **IMPLEMENT THOROUGHLY**:
   - Make all necessary code changes
   - Create any new files required
   - Update existing files as specified
   - Follow existing code patterns and conventions
   - Ensure code quality and consistency

4. **ADAPT TO PLAN TYPE**:

   **For Chore Plans**:
   - Follow the step-by-step tasks exactly
   - Keep changes focused on the chore
   - Run validation commands

   **For Feature Plans**:
   - Follow the 3-phase implementation approach
   - Create tests as specified
   - Ensure all acceptance criteria are met
   - Follow the testing strategy

   **For Bug Plans**:
   - Be surgical - make minimal changes only
   - Fix the root cause identified
   - Don't refactor or improve unrelated code
   - Add regression tests as specified

5. **CREATE FILES PROPERLY**:
   - Use correct file paths relative to context_folder
   - Follow existing code style and patterns
   - Add necessary imports
   - Ensure proper integration with existing code

6. **GENERATE COMPLETION REPORT**:
   After implementation, provide a report with:

   ## Implementation Summary

   [Concise bullet points summarizing what was done]
   - What was implemented
   - Key changes made
   - Files created/modified
   - Any important notes

   ## Files Changed

   Run `git diff --stat` to show:
   - List of files modified
   - Number of lines added/removed per file
   - Total lines changed

   Format the output clearly.

7. **OUTPUT FORMAT**:

   Your response should include:

   ```markdown
   # Implementation Complete

   ## What Was Done
   [Bullet list of what was implemented]

   ## Key Changes
   [Bullet list of important changes]

   ## Files Changed
   [Git diff stat output]

   ## Notes
   [Any additional notes about the implementation]
   ```

8. **BE THOROUGH**:
   - Don't cut corners
   - Ensure all requirements are met
   - Test your implementation if possible
   - Follow best practices

9. **USE CONTEXT PROPERLY**:
   - context_folder indicates where the codebase is
   - Use this to locate files and understand structure
   - Make changes relative to this folder

The user will provide:
- The full content of a specs/*.md plan file
- Optionally: a context_folder where the codebase is located

Your job is to implement that plan and report the completed work."""

        # Add context-specific instructions
        if context_folder or focus_file:
            base_prompt += "\n\n## PROJECT CONTEXT\n"
            if context_folder:
                base_prompt += f"• Context Folder (Codebase): {context_folder}\n"
                base_prompt += "  → All file paths are relative to this folder\n"
                base_prompt += "  → Use this folder to locate and modify files\n"
            if focus_file:
                base_prompt += f"• Focus File: {focus_file}\n"
                base_prompt += "  → This file may be relevant to the implementation\n"
            base_prompt += "\nRead the plan carefully, then implement all steps in order."

        return base_prompt

    def _generate_filename(self, task: str, context_folder: Optional[str]) -> Optional[str]:
        """Generate suggested filename based on task.

        Args:
            task: Task description (plan content)
            context_folder: Optional context folder

        Returns:
            Suggested filename (not typically used for implementer)
        """
        # Implementer agent usually returns implementation, not a plan
        # But if needed, generate implementation report filename
        return "implementation_report.md"

    def process(self, text: str, context_folder: Optional[str] = None, focus_file: Optional[str] = None, output_mode: str = "AUTO", image_path: Optional[str] = None) -> str:
        """Process plan file and implement it.

        Args:
            text: Plan file content (specs/*.md)
            context_folder: Optional context folder (codebase location)
            focus_file: Optional focus file
            output_mode: Output mode (AUTO, CLIPBOARD_PURE, etc.)
            image_path: Optional image path for visual analysis

        Returns:
            Implementation completion report
        """
        self.logger.info("TAC Implementer: Reading and implementing plan")

        # Add context info to the log
        if context_folder:
            self.logger.info(f"Codebase location: {context_folder}")
        else:
            self.logger.warning("No context folder provided - implementation may be limited")

        # Check if text looks like a plan file
        plan_indicators = ["# Chore:", "# Feature:", "# Bug:", "## Step by Step Tasks", "## Implementation Plan"]
        is_plan = any(indicator in text for indicator in plan_indicators)

        if is_plan:
            self.logger.info("Plan file detected - will implement step by step")
        else:
            self.logger.warning("Input doesn't appear to be a TAC plan file")

        result = super().process(text, context_folder, focus_file, output_mode, image_path)
        return result
