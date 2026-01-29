"""LLM client factory."""
from .base import BaseLLMClient
from .openrouter_client import OpenRouterClient
from ...models.config import Config
from ...utils.exceptions import ConfigurationError


def create_llm_client(config: Config) -> BaseLLMClient:
    """Factory function to create appropriate LLM client."""
    if config.llm_provider == "openrouter":
        return OpenRouterClient(
            api_key=config.llm_api_key,
            model=config.llm_model,
            base_url=config.llm_base_url
        )
    else:
        raise ConfigurationError(
            f"Unsupported LLM provider: {config.llm_provider}"
        )


__all__ = ['BaseLLMClient', 'OpenRouterClient', 'create_llm_client']
