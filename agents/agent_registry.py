"""Agent registry for managing available agents."""

from typing import Dict, Optional, List
from pathlib import Path
import importlib.util
from agents.base_agent import BaseAgent
from utils.logger import setup_logger

logger = setup_logger('AgentRegistry')


class AgentRegistry:
    """Registry for managing and discovering agents."""

    def __init__(self):
        """Initialize agent registry."""
        self.agents: Dict[str, BaseAgent] = {}
        self.agent_names: List[str] = []
        self.current_index = 0
        self._discover_agents()

    def _discover_agents(self) -> None:
        """Discover and load all agent plugins."""
        agents_dir = Path(__file__).parent

        for agent_file in agents_dir.glob("*.py"):
            if agent_file.name.startswith('_'):
                continue

            try:
                # Load module dynamically
                module_name = f"agents.{agent_file.stem}"
                spec = importlib.util.spec_from_file_location(
                    module_name,
                    agent_file
                )
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)

                # Find agent classes
                for attr_name in dir(module):
                    attr = getattr(module, attr_name)
                    if (isinstance(attr, type) and
                        issubclass(attr, BaseAgent) and
                        attr is not BaseAgent):

                        # Instantiate and register
                        agent_instance = attr()
                        self.agents[agent_instance.metadata.name] = agent_instance
                        self.agent_names.append(agent_instance.metadata.name)
                        logger.info(
                            f"Registered agent: {agent_instance.metadata.name} "
                            f"({agent_instance.metadata.icon})"
                        )

            except Exception as e:
                logger.error(f"Error loading agent from {agent_file}: {e}")

        if not self.agents:
            logger.warning("No agents found!")

    def get_current_agent(self) -> Optional[BaseAgent]:
        """Get current agent.

        Returns:
            Current agent or None if no agents available
        """
        if not self.agent_names:
            return None
        return self.agents[self.agent_names[self.current_index]]

    def next_agent(self) -> Optional[BaseAgent]:
        """Switch to next agent.

        Returns:
            Next agent or None if no agents available
        """
        if not self.agent_names:
            return None

        self.current_index = (self.current_index + 1) % len(self.agent_names)
        agent = self.get_current_agent()
        logger.info(f"Switched to agent: {agent.metadata.name}")
        return agent

    def get_agent_by_name(self, name: str) -> Optional[BaseAgent]:
        """Get agent by name.

        Args:
            name: Agent name

        Returns:
            Agent or None if not found
        """
        return self.agents.get(name)
