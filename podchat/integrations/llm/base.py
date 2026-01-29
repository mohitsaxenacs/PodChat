"""Base LLM client interface."""
from abc import ABC, abstractmethod


class BaseLLMClient(ABC):
    """Abstract base class for LLM clients."""
    
    @abstractmethod
    def generate(self, prompt: str, **kwargs) -> str:
        """Generate response from prompt."""
        pass
    
    @abstractmethod
    def count_tokens(self, text: str) -> int:
        """Estimate token count in text."""
        pass
    
    @abstractmethod
    def get_max_tokens(self) -> int:
        """Get maximum token limit."""
        pass
