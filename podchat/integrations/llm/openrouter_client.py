"""OpenRouter LLM client implementation."""
from openai import OpenAI

from .base import BaseLLMClient
from ...utils.logger import get_logger


class OpenRouterClient(BaseLLMClient):
    """
    OpenRouter implementation using Claude Sonnet 4.5.
    Uses OpenAI SDK with custom base_url.
    """
    
    def __init__(
        self,
        api_key: str,
        model: str = "anthropic/claude-sonnet-4.5",
        base_url: str = "https://openrouter.ai/api/v1"
    ):
        self.client = OpenAI(
            api_key=api_key,
            base_url=base_url
        )
        self.model = model
        self.logger = get_logger(__name__)
    
    def generate(self, prompt: str, **kwargs) -> str:
        """Generate response using OpenRouter."""
        try:
            self.logger.info(f"Sending request to {self.model}")
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                **kwargs
            )
            
            content = response.choices[0].message.content
            
            # Log token usage if available
            if hasattr(response, 'usage'):
                usage = response.usage
                self.logger.info(
                    f"Token usage - "
                    f"Input: {usage.prompt_tokens}, "
                    f"Output: {usage.completion_tokens}, "
                    f"Total: {usage.total_tokens}"
                )
            
            return content
            
        except Exception as e:
            self.logger.error(f"LLM API error: {e}")
            raise
    
    def count_tokens(self, text: str) -> int:
        """Estimate token count (Claude uses ~4 chars per token)."""
        return len(text) // 4
    
    def get_max_tokens(self) -> int:
        """Get maximum token limit for Claude Sonnet 4.5."""
        return 200000  # 200K context window
