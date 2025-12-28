"""Base agent class for AgentClick system."""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Optional, Dict, Any
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

    def process(self, text: str, context_folder: Optional[str] = None, focus_file: Optional[str] = None) -> str:
        """Process text with this agent.

        Args:
            text: Text to process
            context_folder: Optional context folder path
            focus_file: Optional focus file path

        Returns:
            Processed result
        """
        self.logger.info(f"Processing with {self.metadata.name}")
        self.logger.debug(f"Input text: {text[:100]}...")

        if context_folder:
            self.logger.info(f"Context folder: {context_folder}")
        if focus_file:
            self.logger.info(f"Focus file: {focus_file}")

        try:
            # Create SDK options
            system_prompt = self.get_system_prompt(text, context_folder, focus_file)
            options = create_sdk_options(system_prompt)

            # Build prompt with context
            prompt = self._build_prompt(text, context_folder, focus_file)

            # Query Claude SDK
            result_text = self._query_sdk(prompt, options)

            self.logger.info(f"Processing complete: {len(result_text)} chars")
            return result_text

        except Exception as e:
            self.logger.error(f"Error processing: {e}", exc_info=True)
            raise

    def _build_prompt(self, text: str, context_folder: Optional[str] = None, focus_file: Optional[str] = None) -> str:
        """Build prompt for Claude SDK.

        Args:
            text: Input text
            context_folder: Optional context folder
            focus_file: Optional focus file

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

        # Add the main task
        prompt_parts.append("TASK:")
        prompt_parts.append(f"Process the following text:\n{text}")
        prompt_parts.append("\nProvide only the result, no explanations.")

        return "\n".join(prompt_parts)

    def _query_sdk(self, prompt: str, options: ClaudeAgentOptions) -> str:
        """Query Claude SDK.

        Args:
            prompt: Prompt to send
            options: SDK options

        Returns:
            Response text
        """
        result_parts = []

        try:
            import asyncio

            async def run_query():
                async for message in query(prompt=prompt, options=options):
                    if hasattr(message, 'content'):
                        for block in message.content:
                            if hasattr(block, 'text'):
                                result_parts.append(block.text)

            asyncio.run(run_query())

        except Exception as e:
            self.logger.error(f"SDK query error: {e}")
            raise

        return ''.join(result_parts)
