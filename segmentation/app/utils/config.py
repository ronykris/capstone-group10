import os
import yaml
from pathlib import Path
from typing import Any, Dict
from app.utils.logger import get_logger
from dotenv import load_dotenv

logger = get_logger(__name__)

class ConfigManager:
    """
    Manages application configuration from YAML files and environment variables.
    """
    _instance = None
    _config: Dict[str, Any] = {}

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        if not self._config:
            self.load_config()

    def load_config(self):
        """Load configuration from YAML file and environment variables."""
        try:
            # Get the project root directory
            project_root = Path(__file__).parent.parent.parent
            
            # Load environment variables from .env file
            env_file = project_root / ".env"
            load_dotenv(env_file)
            
            # Load YAML configuration
            config_path = project_root / "config" / "settings.yaml"
            with open(config_path, 'r') as f:
                self._config = yaml.safe_load(f)

            # Override with environment variables
            self._override_from_env()

            logger.info("Configuration loaded successfully")
        except Exception as e:
            logger.error(f"Error loading configuration: {str(e)}")
            raise

    def _override_from_env(self):
        """Override configuration with environment variables."""
        env_mappings = {
            "FAL_KEY": ("fal", "api_key"),
            "APP_PORT": ("app", "port"),
            "APP_HOST": ("app", "host"),
            "LOG_LEVEL": ("logging", "level"),
        }

        for env_var, config_path in env_mappings.items():
            env_value = os.getenv(env_var)
            if env_value:
                self._set_nested_value(self._config, config_path, env_value)

    def _set_nested_value(self, config: dict, path: tuple, value: Any):
        """Set a value in nested dictionary using a path tuple."""
        current = config
        for key in path[:-1]:
            current = current.setdefault(key, {})
        current[path[-1]] = value

    def get(self, *keys: str, default: Any = None) -> Any:
        """
        Get a configuration value using dot notation.
        
        :param keys: Sequence of keys to access nested configuration
        :param default: Default value if key doesn't exist
        :return: Configuration value
        """
        current = self._config
        for key in keys:
            if isinstance(current, dict):
                current = current.get(key, default)
            else:
                return default
        return current

# Create a singleton instance
config = ConfigManager() 