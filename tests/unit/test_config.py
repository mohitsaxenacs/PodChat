"""Test configuration loading with pytest."""
import pytest
import os
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from podchat.utils.config import ConfigManager
from podchat.models.config import Config


def test_config_loads_successfully():
    """Test that configuration loads without errors."""
    config = ConfigManager.load()
    assert isinstance(config, Config)


def test_config_has_required_fields():
    """Test that config has all required fields."""
    config = ConfigManager.load()
    
    # LLM settings
    assert hasattr(config, 'llm_provider')
    assert hasattr(config, 'llm_model')
    assert hasattr(config, 'llm_base_url')
    assert hasattr(config, 'llm_api_key')
    assert hasattr(config, 'llm_max_tokens')
    assert hasattr(config, 'llm_temperature')
    
    # Output settings
    assert hasattr(config, 'output_directory')
    
    # Processing settings
    assert hasattr(config, 'max_retries')
    assert hasattr(config, 'timeout')
    assert hasattr(config, 'log_level')


def test_config_default_values():
    """Test that config has sensible default values."""
    config = ConfigManager.load()
    
    assert config.llm_provider == "openrouter"
    assert config.llm_max_tokens > 0
    assert config.llm_temperature >= 0 and config.llm_temperature <= 2
    assert config.max_retries > 0
    assert config.timeout > 0


def test_config_api_key_present():
    """Test that API key is loaded (if .env exists)."""
    config = ConfigManager.load()
    
    # If .env file exists, API key should be present
    env_file = Path(".env")
    if env_file.exists():
        assert config.llm_api_key is not None
        assert len(config.llm_api_key) > 0


def test_config_output_directory():
    """Test output directory configuration."""
    config = ConfigManager.load()
    
    assert config.output_directory is not None
    assert isinstance(config.output_directory, str)
    assert len(config.output_directory) > 0


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
