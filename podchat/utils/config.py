"""Configuration management."""
import os
from pathlib import Path
from typing import Optional
from dotenv import load_dotenv

from ..models.config import Config
from .exceptions import ConfigurationError


class ConfigManager:
    """Manages configuration from multiple sources."""
    
    @staticmethod
    def load() -> Config:
        """Load configuration from environment and defaults."""
        # Load .env file if it exists
        env_path = Path.cwd() / ".env"
        if env_path.exists():
            load_dotenv(env_path)
        
        # Get API key
        api_key = os.getenv("OPENROUTER_API_KEY")
        if not api_key:
            raise ConfigurationError(
                "OPENROUTER_API_KEY not found. "
                "Please set it in your .env file or environment variables."
            )
        
        # Create config with overrides from environment
        config = Config(
            llm_api_key=api_key,
            llm_provider=os.getenv("LLM_PROVIDER", "openrouter"),
            llm_model=os.getenv("LLM_MODEL", "anthropic/claude-sonnet-4.5"),
            llm_base_url=os.getenv("LLM_BASE_URL", "https://openrouter.ai/api/v1"),
            output_directory=os.getenv("OUTPUT_DIRECTORY", "./summaries"),
            log_level=os.getenv("LOG_LEVEL", "INFO"),
        )
        
        return config
    
    @staticmethod
    def validate_api_key(api_key: str, provider: str = "openrouter") -> bool:
        """Validate API key format."""
        if provider == "openrouter":
            return api_key.startswith("sk-or-")
        return len(api_key) > 20
