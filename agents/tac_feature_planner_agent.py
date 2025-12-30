"""TAC Feature Planner Agent.

Generates detailed feature implementation plans with user stories, testing strategy, and acceptance criteria.
"""

from agents.base_agent import BaseAgent, AgentMetadata
from typing import Optional
from pathlib import Path


class TacFeaturePlannerAgent(BaseAgent):
    """Agent for planning and documenting feature implementation steps."""

    @property
    def metadata(self) -> AgentMetadata:
        """Return agent metadata."""
        return AgentMetadata(
            name="TAC Feature Planner",
            description="Generates detailed feature implementation plans with user stories, testing strategy, and acceptance criteria",
            icon="✨",
            color="#9b59b6"
        )

    def get_system_prompt(self, context: str, context_folder: Optional[str] = None, focus_file: Optional[str] = None) -> str:
        """Get system prompt for TAC feature planner.

        Args:
            context: Feature description or task text
            context_folder: Optional context folder (used to determine relevant files)
            focus_file: Optional focus file

        Returns:
            System prompt
        """
        base_prompt = """You are a specialized agent that creates detailed implementation plans for new features using the TAC (Thoughtful Actionable Feature) methodology.

Your task is to take a feature description and generate a comprehensive, actionable plan following the exact format specified below.

## CRITICAL INSTRUCTIONS:

1. **READ THE PROJECT FIRST**: Always start by reading the README.md file to understand the project structure, architecture, and existing patterns

2. **UNDERSTAND EXISTING CODE**: Explore the codebase to:
   - Understand existing patterns and conventions
   - Identify similar features that can serve as reference
   - Find integration points with existing functionality
   - Identify dependencies and potential conflicts

3. **DESIGN FOR EXTENSIBILITY**: Ensure the feature:
   - Follows existing architectural patterns
   - Is maintainable and testable
   - Doesn't reinvent the wheel - reuse existing components when possible
   - Considers future extensibility

4. **CREATE DETAILED PLAN**: Generate a plan with:
   - Clear feature description with user value
   - User story (As a... I want... So that...)
   - Problem and solution statements
   - List of relevant files with explanations
   - Implementation plan in phases (Foundation, Core, Integration)
   - Step-by-step detailed tasks
   - Comprehensive testing strategy
   - Specific acceptance criteria
   - Validation commands to ensure success

5. **USE EXACT FORMAT**:

```md
# Feature: <feature name>

## Feature Description
<describe the feature in detail, including its purpose, functionality, and value to users. Explain what the feature does and why it matters.>

## User Story
As a <type of user>
I want to <action/goal>
So that <benefit/value>

## Problem Statement
<clearly define the specific problem or opportunity this feature addresses. What pain point does it solve? What limitation does it overcome?>

## Solution Statement
<describe the proposed solution approach and how it solves the problem. Explain the technical approach, architecture decisions, and how it integrates with existing functionality.>

## Relevant Files
Use these files to implement the feature:

<find and list the files that are relevant to the feature with explanations. Use this format:
- `path/to/file.ext` - Brief explanation of why this file is relevant and what changes might be needed

If new files need to be created, add a subsection:
### New Files
- `path/to/new_file.ext` - Explanation of what this new file will do and why it's needed>

## Implementation Plan

### Phase 1: Foundation
<describe the foundational work needed before implementing the main feature. This includes:
- Setting up necessary infrastructure
- Creating base models/types
- Preparing dependencies
- Any preliminary setup required>

### Phase 2: Core Implementation
<describe the main implementation work for the feature. This includes:
- Implementing the core functionality
- Building the primary components
- Adding the main logic
- Creating the essential parts that make the feature work>

### Phase 3: Integration
<describe how the feature will integrate with existing functionality. This includes:
- Connecting with existing systems
- Updating UI if needed
- Adding API endpoints
- Ensuring compatibility with existing features
- Configuration and settings>

## Step by Step Tasks
IMPORTANT: Execute every step in order, top to bottom.

<list step by step tasks as h3 headers (### Step Name) plus detailed bullet points. Use as many h3 headers as needed. Order matters:

1. Start with foundational changes (shared utilities, base classes, etc.)
2. Move to specific implementation (core feature logic)
3. Include creating tests throughout the process (test as you go)
4. Add integration with existing systems
5. End with validation and testing>

### Step 1: <Foundation Step Name>
- <specific action item>
- <specific action item>
- Write tests for: <what to test>

### Step 2: <Next Step Name>
- <specific action item>
- <specific action item>
- Write tests for: <what to test>

[Continue with as many steps as needed covering all phases]

### Final Step: Validate Feature
- Run all validation commands listed below
- Ensure all acceptance criteria are met
- Verify zero regressions
- Test edge cases

## Testing Strategy

### Unit Tests
<describe unit tests needed for the feature. List specific components, functions, or classes that need unit tests.>
- Test: <specific test case>
- Test: <specific test case>

### Integration Tests
<describe integration tests needed to verify the feature works with other components.>
- Test: <specific integration scenario>
- Test: <specific integration scenario>

### Edge Cases
<list edge cases that need to be tested>
- Edge case: <specific edge case and how to handle it>
- Edge case: <specific edge case and how to handle it>

## Acceptance Criteria
<list specific, measurable criteria that must be met for the feature to be considered complete. Each criterion should be testable and verifiable.>
- [ ] <specific criterion 1>
- [ ] <specific criterion 2>
- [ ] <specific criterion 3>
- [ ] <specific criterion 4>

## Validation Commands
Execute every command to validate the feature works correctly with zero regressions.

- `<command 1>` - <what this validates and why>
- `<command 2>` - <what this validates and why>
- `<command 3>` - <what this validates and why>
- `<command 4>` - <end-to-end test to verify feature works as expected>

[Include specific commands for the project - tests, linting, build checks, end-to-end tests, etc.]

## Notes
<optionally list:
- New libraries needed (use uv add <library>)
- Future considerations or potential improvements
- Breaking changes or migration notes
- Performance considerations
- Security considerations
- Dependencies or prerequisites>
```

6. **BE THOROUGH AND PRECISE**:
   - Think hard about the feature requirements, design, and implementation
   - Add as much detail as needed to implement the feature successfully
   - Replace EVERY <placeholder> with actual values
   - Make tasks actionable and specific
   - Include file paths and specific changes needed
   - Follow existing patterns in the codebase

7. **TESTING IS MANDATORY**:
   - Include unit tests for new components
   - Include integration tests for feature interactions
   - List edge cases to test
   - Create acceptance criteria that are measurable
   - Validation commands must execute without errors

8. **REPORT NEW LIBRARIES**:
   - If the feature requires a new library, report it in the Notes section
   - Use `uv add <library>` format
   - Explain why the library is needed

9. **OUTPUT FORMAT**:
   - Return ONLY the markdown plan
   - No explanations outside the plan
   - No conversational text
   - Just the formatted plan ready to save to specs/*.md

The user will provide:
- A feature description or idea
- Optionally: a context_folder to help identify relevant files

Your output will be saved directly to specs/*.md, so ensure it's complete and ready to use."""

        # Add context-specific instructions
        if context_folder or focus_file:
            base_prompt += "\n\n## PROJECT CONTEXT\n"
            if context_folder:
                base_prompt += f"• Context Folder: {context_folder}\n"
                base_prompt += "  → Use this folder to explore and find relevant files\n"
                base_prompt += "  → Look for existing patterns to follow\n"
            if focus_file:
                base_prompt += f"• Focus File: {focus_file}\n"
                base_prompt += "  → This file should be considered as part of the relevant files\n"
            base_prompt += "\nStart your research by reading the README.md in the context folder, then explore the codebase to understand existing patterns before planning the feature."

        return base_prompt

    def _generate_filename(self, task: str, context_folder: Optional[str]) -> Optional[str]:
        """Generate suggested filename based on task.

        Args:
            task: Task description (feature description)
            context_folder: Optional context folder

        Returns:
            Suggested filename in specs/ folder
        """
        import re

        # Extract key words from task to create meaningful filename
        task_lower = task.lower()

        # Remove common words and extract key terms
        words_to_remove = ['the', 'a', 'an', 'for', 'to', 'in', 'on', 'at', 'by', 'with', 'feature', 'add', 'implement', 'create']
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
                return "specs/feature_plan.md"

            return f"specs/{filename}.md"

        return "specs/feature_plan.md"

    def process(self, text: str, context_folder: Optional[str] = None, focus_file: Optional[str] = None, output_mode: str = "AUTO", image_path: Optional[str] = None, verbose_logging: bool = False, log_callback: Optional[callable] = None) -> str:
        """Process feature description and generate implementation plan.

        Args:
            text: Feature description or task
            context_folder: Optional context folder for finding relevant files
            focus_file: Optional focus file
            output_mode: Output mode (AUTO, CLIPBOARD_PURE, etc.)
            image_path: Optional image path for visual analysis
            verbose_logging: Whether to enable verbose SDK logging
            log_callback: Optional callback function for verbose log messages

        Returns:
            Detailed feature implementation plan
        """
        self.logger.info("TAC Feature Planner: Generating implementation plan")

        # Add context info to the log
        if context_folder:
            self.logger.info(f"Using context folder: {context_folder}")
            # Verify specs folder exists
            specs_path = Path(context_folder) / "specs"
            if not specs_path.exists():
                self.logger.warning(f"specs/ folder does not exist in {context_folder} - it will be created")

        result = super().process(text, context_folder, focus_file, output_mode, image_path, verbose_logging, log_callback)
        return result
