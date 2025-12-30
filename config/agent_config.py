"""Agent configuration management with persistence."""

import json
from pathlib import Path
from dataclasses import dataclass, asdict
from typing import Optional
from utils.logger import setup_logger

logger = setup_logger('AgentConfig')


# Singleton instance
_instance = None

def get_config_manager() -> 'AgentConfigManager':
    """Get the singleton instance of AgentConfigManager.

    Returns:
        The singleton AgentConfigManager instance
    """
    global _instance
    if _instance is None:
        _instance = AgentConfigManager()
    return _instance


@dataclass
class AgentSettings:
    """Settings for a specific agent."""
    context_folder: Optional[str] = None
    focus_file: Optional[str] = None
    output_mode: str = "AUTO"
    allowed_inputs: list[str] = None  # NOVO: List of allowed input types
    verbose_logging: bool = False  # NOVO: Enable verbose SDK logging

    def __post_init__(self):
        """Initialize allowed_inputs with defaults if not provided."""
        if self.allowed_inputs is None:
            # Default: all input types allowed
            self.allowed_inputs = ["text_selection", "selected_text", "vscode_active_file", "file_upload", "clipboard_image", "screenshot"]

    def to_dict(self) -> dict:
        """Convert to dictionary."""
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict) -> 'AgentSettings':
        """Create from dictionary."""
        return cls(
            context_folder=data.get('context_folder'),
            focus_file=data.get('focus_file'),
            output_mode=data.get('output_mode', 'AUTO'),
            allowed_inputs=data.get('allowed_inputs', ["text_selection", "selected_text", "vscode_active_file", "file_upload", "clipboard_image", "screenshot"]),
            verbose_logging=data.get('verbose_logging', False)
        )


class AgentConfigManager:
    """Manages agent configuration with persistence (Singleton)."""

    _instance = None
    _initialized = False

    def __new__(cls, config_file: Optional[Path] = None):
        """Create or return singleton instance."""
        if cls._instance is None:
            cls._instance = super(AgentConfigManager, cls).__new__(cls)
        return cls._instance

    def __init__(self, config_file: Optional[Path] = None):
        r"""Initialize config manager (only once due to singleton).

        Args:
            config_file: Path to config file (default: C:\.agent_click\config\agent_config.json)
        """
        # Only initialize once
        if AgentConfigManager._initialized:
            return

        if config_file is None:
            config_dir = Path(__file__).parent.parent / 'config'
            config_dir.mkdir(exist_ok=True)
            config_file = config_dir / 'agent_config.json'

        self.config_file = config_file
        self.configs: dict[str, AgentSettings] = {}
        self._load()
        logger.info(f"Config manager initialized: {self.config_file}")
        AgentConfigManager._initialized = True

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

    def set_output_mode(self, agent_name: str, mode: str) -> None:
        """Set output mode for an agent.

        Args:
            agent_name: Name of the agent
            mode: Output mode string (AUTO, CLIPBOARD_PURE, etc.)
        """
        from agents.output_modes import OutputMode

        # Validate mode
        try:
            OutputMode.from_string(mode)
        except ValueError as e:
            logger.error(f"Invalid output mode: {mode}")
            raise ValueError(f"Invalid output mode: {mode}. Must be one of: {[m.value for m in OutputMode]}")

        settings = self.get_settings(agent_name)
        settings.output_mode = mode
        self._save()
        logger.info(f"Set output mode for {agent_name}: {mode}")

    def get_output_mode(self, agent_name: str) -> str:
        """Get output mode for an agent.

        Args:
            agent_name: Name of the agent

        Returns:
            Output mode string
        """
        settings = self.get_settings(agent_name)
        return settings.output_mode

    # NOVO: Métodos para gerenciar inputs permitidos

    def get_allowed_inputs(self, agent_name: str) -> list[str]:
        """Get allowed input types for an agent.

        Args:
            agent_name: Name of the agent

        Returns:
            List of allowed input types (e.g., ["text_selection", "file_upload"])
        """
        settings = self.get_settings(agent_name)
        return settings.allowed_inputs

    def set_allowed_inputs(self, agent_name: str, allowed_inputs: list[str]) -> None:
        """Set allowed input types for an agent.

        Args:
            agent_name: Name of the agent
            allowed_inputs: List of allowed input types
                           Options: "text_selection", "file_upload", "clipboard_image", "screenshot"
        """
        from core.input_strategy import InputType

        # Validate input types
        valid_types = [t.value for t in InputType]
        for input_type in allowed_inputs:
            if input_type not in valid_types:
                raise ValueError(f"Invalid input type: {input_type}. Must be one of: {valid_types}")

        settings = self.get_settings(agent_name)
        settings.allowed_inputs = allowed_inputs
        self._save()
        logger.info(f"Set allowed inputs for {agent_name}: {allowed_inputs}")

    def is_input_allowed(self, agent_name: str, input_type: str) -> bool:
        """Check if an input type is allowed for an agent.

        Args:
            agent_name: Name of the agent
            input_type: Input type to check (e.g., "text_selection")

        Returns:
            True if input type is allowed
        """
        settings = self.get_settings(agent_name)
        return input_type in settings.allowed_inputs

    def toggle_input(self, agent_name: str, input_type: str) -> None:
        """Toggle an input type on/off for an agent.

        Args:
            agent_name: Name of the agent
            input_type: Input type to toggle
        """
        settings = self.get_settings(agent_name)

        if input_type in settings.allowed_inputs:
            # Remove if present
            settings.allowed_inputs = [i for i in settings.allowed_inputs if i != input_type]
            logger.info(f"Disabled input '{input_type}' for {agent_name}")
        else:
            # Add if not present
            settings.allowed_inputs.append(input_type)
            logger.info(f"Enabled input '{input_type}' for {agent_name}")

        self._save()

    def get_verbose_logging(self, agent_name: str) -> bool:
        """Get verbose logging setting for an agent.

        Args:
            agent_name: Name of the agent

        Returns:
            True if verbose logging is enabled
        """
        settings = self.get_settings(agent_name)
        return settings.verbose_logging

    def set_verbose_logging(self, agent_name: str, enabled: bool) -> None:
        """Set verbose logging for an agent.

        Args:
            agent_name: Name of the agent
            enabled: Whether to enable verbose logging
        """
        settings = self.get_settings(agent_name)
        settings.verbose_logging = enabled
        self._save()
        logger.info(f"Set verbose logging for {agent_name}: {enabled}")
