# PodChat - AI Agent Context

## Project Overview
PodChat is a Python 3.9+ CLI tool that transforms YouTube podcast transcripts into actionable knowledge using Claude Sonnet 4.5 via OpenRouter.

**Core Purpose**: Extract maximum value from podcast content with minimal time investment through AI-powered summarization and chat context generation.

## Tech Stack
- **Language**: Python 3.9+
- **LLM**: Claude Sonnet 4.5 (via OpenRouter API)
- **Key Libraries**: 
  - `youtube-transcript-api` - Transcript extraction
  - `click` - CLI framework
  - `openai` - LLM client (OpenRouter uses OpenAI-compatible API)
  - `python-dotenv` - Environment variable management

## Architecture Pattern
```
CLI Layer (podchat/cli/)
    ↓
Core Processing (podchat/core/)
    ↓
Integrations (podchat/integrations/)
    ↓
Output (organized by mode: summaries/ or chats/)
```

**Key Design Principle**: Adapter pattern for LLM providers - enables future migration without core logic changes.

## Project Structure
```
podchat/
├── cli/              # Command-line interface (commands.py)
├── core/             # Core processing logic
│   ├── processor.py      # Main orchestrator
│   ├── extractor.py      # Transcript extraction
│   ├── llm_processor.py  # LLM interaction
│   └── output_formatter.py
├── integrations/     # External API clients
│   ├── youtube_client.py
│   └── llm/              # LLM provider adapters
├── models/           # Data structures (config, transcript)
├── templates/        # Prompt templates
│   └── prompts/
│       ├── chat_prompt.txt
│       └── summary_prompt.txt
└── utils/            # Utilities (config, logger, file_manager)
```

## Development Workflows

### When modifying LLM integration:
1. Use the adapter pattern in `podchat/integrations/llm/`
2. Maintain provider flexibility (currently OpenRouter, but designed for swapping)
3. Test with sample videos from `examples/`

### When editing prompt templates:
1. Edit files in `podchat/templates/prompts/`
2. Test with both short (5-10 min) and long (1+ hour) videos
3. Validate output quality manually against examples in `examples/sample_outputs/`

### When adding new features:
1. Update both `README.md` and `docs/PRD.md`
2. Follow modular architecture (keep separation of concerns)
3. Add tests following patterns in `tests/` directory
4. Update relevant `RUN_PHASE*_TESTS.md` guides

### When debugging issues:
1. Use `--verbose` flag for detailed logging
2. Check `.env` file for API key configuration
3. Test with known-good YouTube URLs from examples
4. Review logs in `.cursor/debug.log` if needed

## Best Practices

### Code Organization
- Maintain clear separation: CLI → Core → Integrations
- Keep prompt templates in separate files for easy iteration
- Use proper error handling for API calls and transcript extraction
- Follow existing output formatting (sanitized filenames, organized directories)

### Python Conventions
- Use type hints for function signatures
- Follow existing naming conventions (snake_case for functions/variables)
- Keep functions focused and single-purpose
- Use descriptive variable names that reflect domain concepts

### Testing Strategy
- Manual testing with various podcast lengths (30 min, 1 hour, 3+ hours)
- Test different YouTube URL formats
- Validate both summary and chat output modes
- Follow test guides in `RUN_PHASE*_TESTS.md` files

## Key Files to Know

### Core Processing
- `podchat/core/processor.py` - Main orchestrator, entry point for processing
- `podchat/core/llm_processor.py` - Handles all LLM API interactions
- `podchat/integrations/llm/openrouter_client.py` - OpenRouter API client

### Configuration & Utilities
- `.env` - API keys and configuration (never commit!)
- `podchat/utils/config.py` - Configuration management
- `podchat/models/config.py` - Configuration data models

### CLI
- `podchat/cli/commands.py` - CLI command definitions
- `podchat/__main__.py` - Entry point for module execution

### Templates
- `podchat/templates/prompts/summary_prompt.txt` - Summary generation prompt
- `podchat/templates/prompts/chat_prompt.txt` - Chat context generation prompt

## Current State
✅ **MVP Complete** - Both summary and chat modes fully functional
✅ **Validated** - Phase 4-7 tests passing (see VALIDATION_COMPLETE.md)
✅ **Production Ready** - Release summary available in RELEASE_READY_SUMMARY.md

## Future Enhancement Areas
- Batch processing multiple URLs
- Summary caching to avoid re-processing
- Additional output formats (PDF, HTML)
- Custom summary templates
- Multi-language support
- Local LLM support (Ollama, etc.)

## Python-Specific Guidance

### When working with async operations:
Currently synchronous design. If adding async, maintain backward compatibility.

### When handling API errors:
- Use custom exceptions from `podchat/utils/exceptions.py`
- Provide clear user-facing error messages
- Log technical details for debugging

### When processing long videos:
- Claude Sonnet 4.5 has 200K token context window
- Current design handles 3+ hour podcasts
- Monitor token usage for cost optimization

## Environment Setup
```bash
# Install dependencies
pip install -r requirements.txt

# Configure API key
cp .env.example .env
# Edit .env and add OPENROUTER_API_KEY

# Optional: Install as command
pip install -e .

# Run
python -m podchat summarize "YOUTUBE_URL"
```

## Documentation
- Primary: `README.md` - User-facing documentation
- Architecture: `docs/ARCHITECTURE.md` - Detailed design
- PRD: `docs/PRD.md` - Product requirements
- Implementation: `docs/IMPLEMENTATION_PLAN.md` - Development phases
- Testing: `RUN_PHASE*_TESTS.md` files - Test execution guides

## Python Framework Documentation Index
**IMPORTANT**: When working with these libraries, always reference the patterns in `docs/python-reference/`:

### Click CLI Framework
- File: `docs/python-reference/click-cli-patterns.md`
- Use for: Adding commands, options, arguments, error handling, styled output
- Key patterns: Command decorators, progress bars, error handling, emoji styling

### OpenRouter/LLM Integration
- File: `docs/python-reference/openrouter-patterns.md`
- Use for: LLM API calls, error handling, token tracking, authentication
- Key patterns: Chat completions, retry logic, cost estimation

### YouTube Transcript API
- File: `docs/python-reference/youtube-transcript-patterns.md`
- Use for: Transcript extraction, URL parsing, timestamp handling
- Key patterns: Video ID extraction, transcript retrieval, error handling, timestamp formatting

**Before modifying integrations**: Read the relevant reference doc to follow established patterns.

## Project-Specific Skills
**For common development tasks**, refer to these detailed guides in `docs/skills/`:

### Adding LLM Provider Support
- File: `docs/skills/add-new-llm-provider.md`
- Use when: Adding support for new LLM API (Anthropic, Gemini, Ollama, etc.)
- Covers: Adapter pattern, configuration, testing, common pitfalls

### Modifying Prompt Templates
- File: `docs/skills/modify-prompt-templates.md`
- Use when: Improving summary/chat output quality, changing format, adding sections
- Covers: Testing strategy, prompt engineering, A/B testing, troubleshooting

### Debugging Transcript Issues
- File: `docs/skills/debug-transcript-issues.md`
- Use when: Transcript extraction fails, incomplete data, URL parsing problems
- Covers: Systematic debugging, error messages, validation, testing commands

**When starting a complex task**: Check if a relevant skill exists before proceeding.

---

**Note for AI Agents**: 
1. **Always start by reading agents.md** (this file) to understand project context
2. **For common tasks**, invoke the relevant skill from `docs/skills/`
3. **Before working with a specific library**, check `docs/python-reference/` for established patterns
4. **Review relevant existing code** to maintain consistency
5. Follow the modular architecture and existing patterns
6. Check examples in `examples/sample_outputs/` for expected output quality
