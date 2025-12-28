"""Agent configuration management with persistence."""

import json
from pathlib import Path
from dataclasses import dataclass, asdict
from typing import Optional
from utils.logger import setup_logger

logger = setup_logger('AgentConfig')


@dataclass
class AgentSettings:
    """Settings for a specific agent."""
    context_folder: Optional[str] = None
    focus_file: Optional[str] = None

    def to_dict(self) -> dict:
        """Convert to dictionary."""
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict) -> 'AgentSettings':
        """Create from dictionary."""
        return cls(
            context_folder=data.get('context_folder'),
            focus_file=data.get('focus_file')
        )


class AgentConfigManager:
    """Manages agent configuration with persistence."""

    def __init__(self, config_file: Optional[Path] = None):
        """Initialize config manager.

        Args:
            config_file: Path to config file (default: C:\.agent_click\config\agent_config.json)
        """
        if config_file is None:
            config_dir = Path(__file__).parent.parent / 'config'
            config_dir.mkdir(exist_ok=True)
            config_file = config_dir / 'agent_config.json'

        self.config_file = config_file
        self.configs: dict[str, AgentSettings] = {}
        self._load()
        logger.info(f"Config manager initialized: {self.config_file}")

    def _load(self) -> None:
        """Load configurations from file."""
        if not self.config_file.exists():
            logger.info("No existing config file, starting fresh")
            return

        try:
            with open(self.config_file, 'r', encoding='utf-8') as f:
                data = json.load(f)

            for agent_name, settings_data in data.items():
                self.configs[agent_name] = AgentSettings.from_dict(settings_data)

            logger.info(f"Loaded configs for {len(self.configs)} agents")

        except Exception as e:
            logger.error(f"Error loading config: {e}")

    def _save(self) -> None:
        """Save configurations to file."""
        try:
            # Ensure directory exists
            self.config_file.parent.mkdir(parents=True, exist_ok=True)

            # Convert to dict
            data = {
                agent_name: settings.to_dict()
                for agent_name, settings in self.configs.items()
            }

            # Save
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)

            logger.info(f"Saved configs for {len(self.configs)} agents")

        except Exception as e:
            logger.error(f"Error saving config: {e}")

    def get_settings(self, agent_name: str) -> AgentSettings:
        """Get settings for an agent.

        Args:
            agent_name: Name of the agent

        Returns:
            AgentSettings for the agent
        """
        if agent_name not in self.configs:
            self.configs[agent_name] = AgentSettings()

        return self.configs[agent_name]

    def update_settings(self, agent_name: str, settings: AgentSettings) -> None:
        """Update settings for an agent.

        Args:
            agent_name: Name of the agent
            settings: New settings to save
        """
        self.configs[agent_name] = settings
        self._save()
        logger.info(f"Updated settings for {agent_name}")

    def set_context_folder(self, agent_name: str, folder: Optional[str]) -> None:
        """Set context folder for an agent.

        Args:
            agent_name: Name of the agent
            folder: Path to context folder (None to clear)
        """
        settings = self.get_settings(agent_name)
        settings.context_folder = folder
        self._save()
        logger.info(f"Set context folder for {agent_name}: {folder}")

    def set_focus_file(self, agent_name: str, file: Optional[str]) -> None:
        """Set focus file for an agent.

        Args:
            agent_name: Name of the agent
            file: Path to focus file (None to clear)
        """
        settings = self.get_settings(agent_name)
        settings.focus_file = file
        self._save()
        logger.info(f"Set focus file for {agent_name}: {file}")

    def get_context_folder(self, agent_name: str) -> Optional[str]:
        """Get context folder for an agent.

        Args:
            agent_name: Name of the agent

        Returns:
            Path to context folder or None
        """
        settings = self.get_settings(agent_name)
        return settings.context_folder

    def get_focus_file(self, agent_name: str) -> Optional[str]:
        """Get focus file for an agent.

        Args:
            agent_name: Name of the agent

        Returns:
            Path to focus file or None
        """
        settings = self.get_settings(agent_name)
        return settings.focus_file
