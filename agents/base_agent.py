"""Base agent class for AgentClick system."""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Optional, Dict, Any, Tuple
from claude_agent_sdk import query, ClaudeAgentOptions
from config.sdk_config import create_sdk_options
from utils.logger import setup_logger

logger = setup_logger('BaseAgent')


@dataclass
class AgentMetadata:
    """Metadata for an agent."""
    name: str
    description: str
    icon: str
    color: str = "#0078d4"


class BaseAgent(ABC):
    """Abstract base class for all agents."""

    def __init__(self):
        """Initialize agent."""
        self.logger = setup_logger(self.__class__.__name__)

    @property
    @abstractmethod
    def metadata(self) -> AgentMetadata:
        """Return agent metadata."""
        pass

    @abstractmethod
    def get_system_prompt(self, context: str) -> str:
        """Get system prompt for this agent.

        Args:
            context: Context text (selected text or additional info)

        Returns:
            System prompt string
        """
        pass

    def process(self, text: str, context_folder: Optional[str] = None, focus_file: Optional[str] = None, output_mode: str = "AUTO", image_path: Optional[str] = None, verbose_logging: bool = False, log_callback: Optional[callable] = None):
        """Process text with this agent.

        Args:
            text: Text to process
            context_folder: Optional context folder path
            focus_file: Optional focus file path
            output_mode: Output mode (AUTO, CLIPBOARD_PURE, etc.)
            image_path: NOVO - Optional image path for visual analysis
            verbose_logging: Whether to enable verbose SDK logging
            log_callback: Optional callback function for verbose log messages

        Returns:
            AgentResult with content and metadata
        """
        from agents.output_modes import OutputMode, AgentResult

        self.logger.info(f"Processing with {self.metadata.name}")
        self.logger.debug(f"Input text: {text[:100]}...")
        self.logger.info(f"Output mode: {output_mode}")

        # NOVO: Log se tiver imagem
        if image_path:
            self.logger.info(f"Image provided: {image_path}")

        if context_folder:
            self.logger.info(f"Context folder: {context_folder}")
        if focus_file:
            self.logger.info(f"Focus file: {focus_file}")

        try:
            # Create SDK options
            system_prompt = self.get_system_prompt(text, context_folder, focus_file)
            options = create_sdk_options(system_prompt, cwd=context_folder)

            # Build prompt with context (NOVO: Pass image_path)
            prompt = self._build_prompt(text, context_folder, focus_file, image_path)

            # Query Claude SDK with verbose logging support
            result_text = self._query_sdk(prompt, options, verbose_logging=verbose_logging, log_callback=log_callback)

            # Parse output to extract thoughts and content (if formatted)
            content, raw_thoughts = self._parse_output(result_text)

            # Generate suggested filename based on task
            suggested_filename = self._generate_filename(text, context_folder)

            self.logger.info(f"Processing complete: {len(result_text)} chars")

            # Create structured result
            result = AgentResult(
                content=content,
                output_mode=OutputMode.from_string(output_mode),
                metadata={
                    "agent": self.metadata.name,
                    "context_folder": context_folder,
                    "focus_file": focus_file,
                    "image_path": image_path  # NOVO: Include in metadata
                },
                raw_thoughts=raw_thoughts,
                suggested_filename=suggested_filename
            )

            return result

        except Exception as e:
            self.logger.error(f"Error processing: {e}", exc_info=True)
            raise


    def _parse_output(self, output: str) -> Tuple[str, Optional[str]]:
        """Parse output to extract thoughts and main content.

        Args:
            output: Raw output from SDK

        Returns:
            Tuple of (content, thoughts) where thoughts may be None
        """
        # Check if output has thought markers (---, ###, etc)
        separators = ["\n---\n", "\n\n### Reasoning", "\n\n## Thoughts"]

        for sep in separators:
            if sep in output:
                parts = output.split(sep, 1)
                if len(parts) == 2:
                    # First part is content, second is thoughts (or vice versa)
                    # Usually: content first, then thoughts
                    return parts[0].strip(), parts[1].strip()

        # No separation found
        return output.strip(), None


    def _generate_filename(self, task: str, context_folder: Optional[str]) -> Optional[str]:
        """Generate suggested filename based on task.

        Args:
            task: Task description
            context_folder: Optional context folder

        Returns:
            Suggested filename or None
        """
        task_lower = task.lower()

        # Detect task type and generate appropriate filename
        if "json" in task_lower:
            return "output.json"
        elif "config" in task_lower or "yaml" in task_lower:
            return "config.yaml"
        elif "markdown" in task_lower or "md" in task_lower:
            return "output.md"
        elif "python" in task_lower or ".py" in task_lower:
            return "script.py"
        elif "javascript" in task_lower or ".js" in task_lower:
            return "script.js"
        elif "readme" in task_lower:
            return "README.md"
        elif "test" in task_lower:
            return "test_output.txt"

        return None

    def _build_prompt(self, text: str, context_folder: Optional[str] = None, focus_file: Optional[str] = None, image_path: Optional[str] = None) -> str:
        """Build prompt for Claude SDK.

        Args:
            text: Input text
            context_folder: Optional context folder
            focus_file: Optional focus file
            image_path: NOVO - Optional image path

        Returns:
            Formatted prompt
        """
        prompt_parts = []

        # Add context information if available
        if context_folder or focus_file:
            prompt_parts.append("CONTEXT INFORMATION:")

            if context_folder:
                prompt_parts.append(f"• Context Folder: {context_folder}")

            if focus_file:
                prompt_parts.append(f"• Focus File: {focus_file}")

            prompt_parts.append("")  # Empty line

        # NOVO: Add image information if available
        if image_path:
            prompt_parts.append("VISUAL CONTEXT:")
            prompt_parts.append(f"• Image attached: {image_path}")
            prompt_parts.append(f"• Use this image for visual analysis if needed")
            prompt_parts.append("")  # Empty line

        # Add the main task
        prompt_parts.append("TASK:")
        prompt_parts.append(f"Process the following:\n{text}")
        prompt_parts.append("\nProvide only the result, no explanations.")

        return "\n".join(prompt_parts)

    def _query_sdk(self, prompt: str, options: ClaudeAgentOptions, verbose_logging: bool = False, log_callback: Optional[callable] = None) -> str:
        """Query Claude SDK.

        Args:
            prompt: Prompt to send
            options: SDK options
            verbose_logging: Whether to enable verbose logging
            log_callback: Optional callback for verbose log messages

        Returns:
            Response text
        """
        result_parts = []

        try:
            import asyncio

            async def run_query():
                # Create the query generator
                query_gen = query(prompt=prompt, options=options)

                # Use verbose wrapper if enabled
                if verbose_logging:
                    from agents.sdk_logger import create_verbose_wrapper
                    wrapper = create_verbose_wrapper(
                        query_gen,
                        log_callback=log_callback,
                        enabled=True
                    )
                    # Use the wrapped query
                    async for message in wrapper.wrapped_query():
                        if hasattr(message, 'content'):
                            for block in message.content:
                                if hasattr(block, 'text'):
                                    result_parts.append(block.text)
                else:
                    # Original behavior without verbose logging
                    async for message in query_gen:
                        if hasattr(message, 'content'):
                            for block in message.content:
                                if hasattr(block, 'text'):
                                    result_parts.append(block.text)

            asyncio.run(run_query())

        except Exception as e:
            self.logger.error(f"SDK query error: {e}")
            raise

        return ''.join(result_parts)
