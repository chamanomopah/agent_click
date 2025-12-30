"""TAC Chore Planner Agent.

Generates detailed chore implementation plans in specs/ folder with structured tasks and validation.
"""

from agents.base_agent import BaseAgent, AgentMetadata
from typing import Optional
from pathlib import Path


class TacChorePlannerAgent(BaseAgent):
    """Agent for planning and documenting chore implementation steps."""

    @property
    def metadata(self) -> AgentMetadata:
        """Return agent metadata."""
        return AgentMetadata(
            name="TAC Chore Planner",
            description="Generates detailed chore implementation plans in specs/ folder with structured tasks and validation",
            icon="📋",
            color="#f39c12"
        )

    def get_system_prompt(self, context: str, context_folder: Optional[str] = None, focus_file: Optional[str] = None) -> str:
        """Get system prompt for TAC chore planner.

        Args:
            context: Chore description or task text
            context_folder: Optional context folder (used to determine relevant files)
            focus_file: Optional focus file

        Returns:
            System prompt
        """
        base_prompt = """You are a specialized agent that creates detailed implementation plans for chores using the TAC (Thoughtful Actionable Chore) methodology.

Your task is to take a chore description and generate a comprehensive, actionable plan following the exact format specified below.

## CRITICAL INSTRUCTIONS:

1. **READ THE PROJECT FIRST**: Always start by reading the README.md file to understand the project structure and context

2. **FIND RELEVANT FILES**: Based on the context_folder provided:
   - Explore the codebase to identify files relevant to the chore
   - Focus on files that will need to be modified or created
   - Ignore files that are not relevant to the specific chore
   - List files with bullet points explaining WHY they are relevant

3. **CREATE DETAILED PLAN**: Generate a plan with:
   - Clear chore description
   - List of relevant files with explanations
   - Step-by-step tasks (h3 headers with detailed bullet points)
   - Specific validation commands to ensure zero regressions
   - Optional notes for additional context

4. **USE EXACT FORMAT**:

```md
# Chore: <chore name>

## Chore Description
<describe the chore in detail with context and background>

## Relevant Files
Use these files to resolve the chore:

<find and list the files that are relevant to the chore with explanations. Use this format:
- `path/to/file.ext` - Brief explanation of why this file is relevant and what changes might be needed

If new files need to be created, add a subsection:
### New Files
- `path/to/new_file.ext` - Explanation of what this new file will do>

## Step by Step Tasks
IMPORTANT: Execute every step in order, top to bottom.

<list step by step tasks as h3 headers (### Step Name) plus detailed bullet points. Use as many h3 headers as needed. Order matters - start with foundational changes, then move to specific changes. Your last step should always be running validation commands.>

### Step 1: <Foundation Step Name>
- <specific action item>
- <specific action item>
- <specific action item>

### Step 2: <Next Step Name>
- <specific action item>
- <specific action item>

[Continue with as many steps as needed]

### Final Step: Validate Implementation
- Run all validation commands listed below
- Ensure zero regressions
- Verify the chore is complete

## Validation Commands
Execute every command to validate the chore is complete with zero regressions.

- `<command 1>` - <what this validates and why>
- `<command 2>` - <what this validates and why>
- `<command 3>` - <what this validates and why>

[Include specific commands for the project - tests, linting, build checks, etc.]

## Notes
<optional additional context, edge cases, or important considerations>
```

5. **BE THOROUGH AND PRECISE**:
   - Think hard about the plan to avoid second-round changes
   - Add as much detail as needed to accomplish the chore
   - Replace EVERY <placeholder> with actual values
   - Make tasks actionable and specific
   - Include file paths and specific changes needed

6. **VALIDATION IS MANDATORY**:
   - Always include validation commands
   - Commands must execute without errors
   - Test for zero regressions
   - Be specific about what to validate

7. **OUTPUT FORMAT**:
   - Return ONLY the markdown plan
   - No explanations outside the plan
   - No conversational text
   - Just the formatted plan ready to save to specs/*.md

The user will provide:
- A chore description or task
- Optionally: a context_folder to help identify relevant files

Your output will be saved directly to specs/*.md, so ensure it's complete and ready to use."""

        # Add context-specific instructions
        if context_folder or focus_file:
            base_prompt += "\n\n## PROJECT CONTEXT\n"
            if context_folder:
                base_prompt += f"• Context Folder: {context_folder}\n"
                base_prompt += "  → Use this folder to explore and find relevant files\n"
            if focus_file:
                base_prompt += f"• Focus File: {focus_file}\n"
                base_prompt += "  → This file should be considered as part of the relevant files\n"
            base_prompt += "\nStart your research by reading the README.md in the context folder, then explore the codebase to find all relevant files."

        return base_prompt

    def _generate_filename(self, task: str, context_folder: Optional[str]) -> Optional[str]:
        """Generate suggested filename based on task.

        Args:
            task: Task description (chore description)
            context_folder: Optional context folder

        Returns:
            Suggested filename in specs/ folder
        """
        import re

        # Extract key words from task to create meaningful filename
        task_lower = task.lower()

        # Remove common words and extract key terms
        words_to_remove = ['the', 'a', 'an', 'for', 'to', 'in', 'on', 'at', 'by', 'with', 'chore', 'task']
        words = [w for w in task_lower.split() if w not in words_to_remove and len(w) > 2]

        if words:
            # Take first 3-4 meaningful words and join with underscores
            filename = '_'.join(words[:4])

            # Sanitize filename: remove invalid characters for Windows
            # Invalid chars: < > : " / \ | ? *
            filename = re.sub(r'[<>:"/\\|?*\[\]]', '', filename)

            # Remove extra whitespace and underscores
            filename = re.sub(r'[\s_]+', '_', filename).strip('_')

            # Ensure filename is not empty after sanitization
            if not filename:
                return "specs/chore_plan.md"

            return f"specs/{filename}.md"

        return "specs/chore_plan.md"

    def process(self, text: str, context_folder: Optional[str] = None, focus_file: Optional[str] = None, output_mode: str = "AUTO", image_path: Optional[str] = None, verbose_logging: bool = False, log_callback: Optional[callable] = None) -> str:
        """Process chore description and generate implementation plan.

        Args:
            text: Chore description or task
            context_folder: Optional context folder for finding relevant files
            focus_file: Optional focus file
            output_mode: Output mode (AUTO, CLIPBOARD_PURE, etc.)
            image_path: Optional image path for visual analysis
            verbose_logging: Whether to enable verbose SDK logging
            log_callback: Optional callback function for verbose log messages

        Returns:
            Detailed chore implementation plan
        """
        self.logger.info("TAC Chore Planner: Generating implementation plan")

        # Add context info to the log
        if context_folder:
            self.logger.info(f"Using context folder: {context_folder}")
            # Verify specs folder exists
            specs_path = Path(context_folder) / "specs"
            if not specs_path.exists():
                self.logger.warning(f"specs/ folder does not exist in {context_folder} - it will be created")

        result = super().process(text, context_folder, focus_file, output_mode, image_path, verbose_logging, log_callback)
        return result
