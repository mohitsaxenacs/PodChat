# PodChat

Transform YouTube podcasts into actionable knowledge with AI.

## Overview

PodChat is a command-line tool that extracts transcripts from YouTube podcasts and uses Claude Sonnet 4.5 (via OpenRouter) to generate:

- **Comprehensive Summaries**: Detailed markdown summaries that capture key insights, quotes, and takeaways
- **Chat-Ready Contexts**: Knowledge contexts you can load into AI assistants for Q&A and project application

## Features

- ✅ Extract transcripts from any YouTube video with captions
- ✅ Generate in-depth summaries with clickable timestamps
- ✅ Clickable timestamps that link directly to YouTube video sections
- ✅ Create chat-optimized knowledge contexts
- ✅ Support for podcasts of any length
- ✅ Beautiful, structured markdown output
- ✅ Organized output: separate directories for summaries and chats
- ✅ Human-readable filenames based on video titles
- ✅ Simple CLI interface
- ✅ Verbose mode for debugging

## Installation

### Prerequisites

- Python 3.9 or higher
- OpenRouter API key ([Get one here](https://openrouter.ai/))

### Quick Start

```bash
# Clone the repository
git clone https://github.com/yourusername/podchat.git
cd podchat

# Install dependencies
pip install -r requirements.txt

# Configure your API key
cp .env.example .env
# Edit .env and add your OPENROUTER_API_KEY
```

### Optional: Install as Command

```bash
# Install package (enables 'podchat' command)
pip install -e .
```

**Note:** If you encounter SSL certificate errors during installation, you can skip this step and use `python3 -m podchat` instead (see Usage below).

## Configuration

Create a `.env` file in the project root:

```bash
cp .env.example .env
```

Edit `.env` and add your OpenRouter API key:

```env
OPENROUTER_API_KEY=sk-or-v1-your-api-key-here
```

**Required:**
- `OPENROUTER_API_KEY` - Your OpenRouter API key

**Optional Settings:**
```env
LLM_PROVIDER=openrouter
LLM_MODEL=anthropic/claude-sonnet-4.5
LLM_BASE_URL=https://openrouter.ai/api/v1
OUTPUT_DIRECTORY=./output
LOG_LEVEL=INFO
```

## Usage

### Generate a Summary

```bash
# If installed with pip install -e .
podchat summarize "https://www.youtube.com/watch?v=VIDEO_ID"

# Alternative (no installation required)
python3 -m podchat summarize "https://www.youtube.com/watch?v=VIDEO_ID"
```

This creates a comprehensive markdown summary in `./output/summaries/` with:
- Main themes and key insights
- Clickable timestamps linking directly to video sections
- Notable quotes
- Detailed analysis
- Human-readable filename based on video title

**Example output:**
```
🎙️  PodChat - YouTube Podcast Summarizer
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📥 Fetching transcript...
✓ Transcript extracted: 4,714 words
✓ LLM processing complete

✅ Summary generated successfully!

📝 Output: output/summaries/the_path_to_advanced_machine_intelligence_summary.md
📊 Stats:
   - Words: 4,714
   - Time: 164.18s

✨ Done! Your podcast summary is ready.
```

### Generate Chat Context

```bash
podchat chat "https://www.youtube.com/watch?v=VIDEO_ID"
```

This creates a chat-optimized knowledge context you can load into Claude, Cursor, or other AI assistants for:
- Interactive Q&A
- Applying expert knowledge to your projects
- Quick reference lookups
- Concept exploration

The chat context includes:
- Expert expertise summary
- Key concepts with definitions
- Practical guidance
- Quick reference section
- Example questions to ask

### Command Options

```bash
# Custom output location
podchat summarize URL --output ./my-summaries/podcast.md
podchat chat URL -o my_context.md

# Verbose output (shows detailed logs)
podchat summarize URL --verbose
podchat chat URL -v

# Show current configuration
podchat config

# Show help
podchat --help
podchat summarize --help
podchat chat --help
```

### Command Reference

| Command | Description |
|---------|-------------|
| `podchat summarize URL` | Generate comprehensive summary |
| `podchat chat URL` | Generate chat-ready context |
| `podchat config` | Display current configuration |
| `podchat --help` | Show all commands |

## Examples

### Example Summary Output

```markdown
# Podcast Title

## Metadata
- URL: https://www.youtube.com/watch?v=...
- Duration: 00:29:07
- Processed: 2025

## Overview
[Comprehensive overview paragraph]

## Main Themes

### Theme 1: [Title]
[Detailed analysis with timestamps]

### Theme 2: [Title]
[Detailed analysis with timestamps]
...
```

See [`examples/sample_outputs/example_summary.md`](examples/sample_outputs/example_summary.md) for a complete example.

## Output Structure

PodChat organizes output into mode-specific directories:

```
./output/
├── summaries/
│   ├── video_title_1_summary.md
│   └── video_title_2_summary.md
└── chats/
    ├── video_title_1_chat.md
    └── video_title_2_chat.md
```

**Features:**
- **Organized by Mode**: Summaries and chats in separate directories
- **Human-Readable Names**: Filenames based on video titles (sanitized, max 50 chars)
- **Clickable Timestamps**: All timestamps in summaries link directly to YouTube
- **Duplicate Handling**: Automatically adds date suffix if file exists
- **Backward Compatible**: Old `./summaries/` directory remains untouched

**Example Filename Transformation:**
- Video: "Cursor 2.0: Expert Tips and Hacks for AI-Assisted Development"
- Summary: `cursor_20_expert_tips_and_hacks_for_ai_assisted_de_summary.md`
- Chat: `cursor_20_expert_tips_and_hacks_for_ai_assisted_de_chat.md`

### Example Chat Context Output

```markdown
# Expert Knowledge Context

## How to Use This Context
Load this document to ask questions about concepts discussed...

## Expertise Summary
[Speaker background and perspective]

## Key Concepts & Frameworks

### Concept 1: [Name]
**Definition**: [Clear explanation]
**Application**: [How to apply]
**Timestamp**: [HH:MM:SS]

## Quick Reference
**Key Terms**: ...
**Best Practices**: ...
```

See [`examples/sample_outputs/example_chat_context.md`](examples/sample_outputs/example_chat_context.md) for a complete example.

## How It Works

1. **Extract**: Fetches the YouTube transcript using youtube-transcript-api
2. **Process**: Sends transcript to Claude Sonnet 4.5 via OpenRouter API
3. **Generate**: Creates structured markdown with LLM
4. **Enhance**: Converts timestamps to clickable YouTube links
5. **Organize**: Saves to mode-specific directory (`output/summaries/` or `output/chats/`)
6. **Name**: Uses sanitized video title for human-readable filename

## Architecture

PodChat uses a modular architecture with clear separation of concerns:

```
podchat/
├── cli/              # Command-line interface
├── core/             # Core processing logic
│   ├── processor.py      # Main orchestrator
│   ├── extractor.py      # Transcript extraction
│   ├── llm_processor.py  # LLM interaction
│   └── output_formatter.py
├── integrations/     # External API clients
│   ├── youtube_client.py
│   └── llm/
├── models/           # Data structures
├── templates/        # Prompt templates
└── utils/            # Utilities
```

See [ARCHITECTURE.md](docs/ARCHITECTURE.md) for detailed design documentation.

## Development

### Setup Development Environment

```bash
# Install with development dependencies
pip install -r requirements.txt

# Run tests
python tests/test_phase4_quick.py "URL"
python tests/test_phase5_chat.py "URL"

# Format code
black podchat/

# Lint
flake8 podchat/
```

### Running Tests

```bash
# Quick smoke test
python tests/test_phase4_quick.py "https://www.youtube.com/watch?v=MWMe7yjPYpE"

# Full Phase 4 test suite
python tests/test_phase4_summary_generation.py "https://www.youtube.com/watch?v=MWMe7yjPYpE"

# Phase 5 chat mode test
python tests/test_phase5_chat.py "https://www.youtube.com/watch?v=MWMe7yjPYpE"
```

See testing guides:
- [Phase 4 Tests](RUN_PHASE4_TESTS.md)
- [Phase 5 Tests](RUN_PHASE5_TESTS.md)
- [Phase 6 Tests](RUN_PHASE6_TESTS.md)

### Project Structure

```
podchat/
├── podchat/          # Main package
│   ├── cli/          # CLI commands
│   ├── core/         # Core processing logic
│   ├── integrations/ # External API clients
│   ├── models/       # Data models
│   ├── utils/        # Utilities
│   └── templates/    # Prompt templates
├── tests/            # Test suite
├── examples/         # Example outputs
└── docs/             # Documentation
```

## Troubleshooting

### Transcript Not Available

If you get a "transcript not available" error:
- Ensure the video has captions/subtitles enabled
- Check if the video is public and accessible
- Some videos may have auto-generated captions disabled
- Try a different video

### API Key Issues

- Ensure your `.env` file exists in the project root
- Verify your API key is valid at [OpenRouter](https://openrouter.ai/)
- Check that the key starts with `sk-or-v1-`
- Make sure the `.env` file has proper formatting (no quotes around the key)

### Rate Limits

If you hit rate limits:
- Wait a few moments and try again
- Check your OpenRouter account for usage limits
- Consider upgrading your OpenRouter plan for higher limits

### Installation Issues

If `pip install -e .` fails with SSL errors:
- This is a system-level certificate issue, not a PodChat problem
- You can use `python3 -m podchat` instead of the `podchat` command
- All functionality works the same way

### Processing Takes Too Long

- Typical processing time: 1-3 minutes for a 30-minute podcast
- Very long podcasts (>2 hours) may take 5-10 minutes
- Network speed affects transcript fetching
- LLM API response time varies

## Cost Estimates

Using Claude Sonnet 4.5 via OpenRouter:
- **Typical 30-min podcast**: ~$0.05-0.15 (15K-20K tokens)
- **1-hour podcast**: ~$0.10-0.30 (25K-40K tokens)
- **2-hour podcast**: ~$0.20-0.50 (40K-70K tokens)

Check current pricing at [OpenRouter Models](https://openrouter.ai/models/anthropic/claude-sonnet-4.5).

## Roadmap

Future enhancements (post-MVP):
- [ ] Batch processing multiple URLs
- [ ] Summary caching to avoid re-processing
- [ ] Additional output formats (PDF, HTML)
- [ ] Custom summary templates
- [ ] Multi-language support
- [ ] Web interface
- [ ] Local LLM support (Ollama, etc.)
- [ ] Audio file input (not just YouTube)
- [ ] Podcast series tracking

## Contributing

Contributions welcome! Please:
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Add tests for new functionality
5. Ensure all tests pass
6. Submit a pull request

## License

MIT License - see LICENSE file for details

## Acknowledgments

- Built with [Claude Sonnet 4.5](https://www.anthropic.com/claude) via [OpenRouter](https://openrouter.ai/)
- Uses [youtube-transcript-api](https://github.com/jdepoix/youtube-transcript-api) for transcript extraction
- CLI powered by [Click](https://click.palletsprojects.com/)
- Prompt engineering inspired by best practices from the AI community

## Support

- **Documentation**: See [`docs/`](docs/) folder
- **Test Guides**: See `RUN_PHASE*_TESTS.md` files
- **Issues**: [GitHub Issues](https://github.com/yourusername/podchat/issues)
- **Architecture**: [ARCHITECTURE.md](docs/ARCHITECTURE.md)
- **Implementation**: [IMPLEMENTATION_PLAN.md](docs/IMPLEMENTATION_PLAN.md)

## FAQ

### Can I use a different LLM?

Yes! The architecture supports different LLM providers. You can modify `LLM_PROVIDER`, `LLM_MODEL`, and `LLM_BASE_URL` in your `.env` file. Currently configured for OpenRouter, but you can adapt it for:
- Direct Anthropic API
- OpenAI API
- Local models via Ollama
- Other OpenAI-compatible APIs

### Does it work with non-English videos?

Yes, as long as the video has transcripts available in that language. The LLM can process transcripts in multiple languages.

### Can I process private/unlisted videos?

Only if you have access to view them. The video must be accessible via its URL.

### How accurate are the summaries?

Summaries are generated by Claude Sonnet 4.5, one of the most capable LLMs available. Accuracy depends on:
- Transcript quality (auto-generated vs. manual)
- Speaker clarity
- Podcast structure

### Can I customize the summary format?

Yes! Edit the prompt templates in `podchat/templates/prompts/`:
- `summary_prompt.txt` - Controls summary generation
- `chat_prompt.txt` - Controls chat context generation

---

**Made with ❤️ using agentic coding tools (Cursor + Claude)**

*PodChat v1.0.0 - January 2026*
