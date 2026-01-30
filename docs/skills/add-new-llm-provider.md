# Skill: Adding a New LLM Provider to PodChat

## Purpose
Guide for adding support for a new LLM provider (e.g., direct Anthropic API, Gemini, local Ollama) while maintaining the adapter pattern.

## Prerequisites
- Understanding of `podchat/integrations/llm/` architecture
- New provider's API documentation
- API credentials for testing

## Step-by-Step Process

### 1. Create Provider Client Class
Location: `podchat/integrations/llm/your_provider_client.py`

```python
from podchat.integrations.llm.base import BaseLLMClient

class YourProviderClient(BaseLLMClient):
    """Client for [Provider Name] API."""
    
    def __init__(self, api_key: str, model: str, **kwargs):
        self.api_key = api_key
        self.model = model
        # Initialize provider-specific client
        
    def generate_completion(self, system_prompt: str, user_prompt: str, 
                          temperature: float = 0.7, max_tokens: int = 4000) -> str:
        """Generate completion using [Provider]."""
        # Implement provider-specific API call
        # Return the generated text content
        pass
```

### 2. Update Configuration Model
Location: `podchat/models/config.py`

Add new provider option to LLMProvider enum:
```python
class LLMProvider(str, Enum):
    OPENROUTER = "openrouter"
    YOUR_PROVIDER = "your_provider"  # Add this
```

### 3. Update LLM Factory
Location: `podchat/core/llm_processor.py` or wherever LLM client is instantiated

```python
def get_llm_client(config: Config) -> BaseLLMClient:
    if config.llm_provider == "openrouter":
        return OpenRouterClient(...)
    elif config.llm_provider == "your_provider":
        return YourProviderClient(...)
    # Add your provider here
```

### 4. Add Environment Variables
Update `.env.example`:
```env
# For your new provider
YOUR_PROVIDER_API_KEY=your-key-here
YOUR_PROVIDER_MODEL=model-name
```

### 5. Update Configuration Parser
Location: `podchat/utils/config.py`

Add logic to read new provider's configuration.

### 6. Test Integration
Create test script:
```python
# tests/test_your_provider.py
def test_your_provider_integration():
    client = YourProviderClient(api_key="test", model="test-model")
    response = client.generate_completion(
        system_prompt="You are a helpful assistant.",
        user_prompt="Say hello"
    )
    assert response is not None
```

### 7. Update Documentation
- Update `README.md` with new provider option
- Update `docs/PRD.md` if architecturally significant
- Add provider-specific patterns to `docs/python-reference/`

## Testing Checklist
- [ ] Provider client initializes correctly
- [ ] API authentication works
- [ ] Summary generation works with new provider
- [ ] Chat generation works with new provider
- [ ] Error handling works (rate limits, network errors)
- [ ] Token usage tracking (if supported)
- [ ] Both short and long videos process correctly

## Common Pitfalls
1. **API Format Differences**: Different providers use different request/response formats
2. **Token Limits**: Ensure provider supports long transcripts (need ~50K-100K tokens)
3. **Error Handling**: Each provider has unique error types
4. **Streaming**: Some providers support streaming, adapt accordingly
5. **Cost Tracking**: Implement if provider doesn't auto-track

## Example: Direct Anthropic API
If adding direct Anthropic support:
- Use `anthropic` Python library
- API key format: `sk-ant-...`
- Model names: `claude-sonnet-4-20250514`
- Different message format than OpenAI-compatible APIs

## References
- Base class: `podchat/integrations/llm/base.py`
- Existing implementation: `podchat/integrations/llm/openrouter_client.py`
- Configuration: `podchat/models/config.py`
