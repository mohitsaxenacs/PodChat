# OpenRouter Integration Patterns

## Authentication
```python
from openai import OpenAI

client = OpenAI(
    api_key=os.getenv("OPENROUTER_API_KEY"),
    base_url="https://openrouter.ai/api/v1"
)
```

## Chat Completion Request
```python
response = client.chat.completions.create(
    model="anthropic/claude-sonnet-4.5",
    messages=[
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_content}
    ],
    temperature=0.7,
    max_tokens=4000
)

content = response.choices[0].message.content
```

## Error Handling for LLM Calls
```python
from openai import APIError, RateLimitError, APIConnectionError

try:
    response = client.chat.completions.create(...)
except RateLimitError:
    # Handle rate limits - retry with backoff
    pass
except APIConnectionError:
    # Network issues
    pass
except APIError as e:
    # General API errors
    pass
```

## Token Usage Tracking
```python
response = client.chat.completions.create(...)
usage = response.usage
print(f"Tokens used: {usage.total_tokens}")
print(f"Cost estimate: ${usage.total_tokens * 0.000003:.4f}")
```

## Best Practices
1. Always use environment variables for API keys
2. Implement retry logic for transient failures
3. Track token usage for cost monitoring
4. Use appropriate temperature (0.7 for creative, 0.3 for factual)
5. Set reasonable max_tokens based on expected output length
