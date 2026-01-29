"""Configuration data model."""
from dataclasses import dataclass, field
from typing import Optional


@dataclass
class Config:
    """Application configuration."""
    # LLM settings (MVP uses OpenRouter)
    llm_provider: str = "openrouter"
    llm_model: str = "anthropic/claude-sonnet-4.5"
    llm_api_key: Optional[str] = None
    llm_base_url: str = "https://openrouter.ai/api/v1"
    llm_max_tokens: int = 8192
    llm_temperature: float = 0.7
    
    # Output settings
    output_directory: str = "./output"
    verbose: bool = False
    
    # Processing settings
    max_retries: int = 3
    retry_delay: float = 1.0
    timeout: int = 300  # seconds
    
    # Logging
    log_level: str = "INFO"
    log_file: Optional[str] = None
