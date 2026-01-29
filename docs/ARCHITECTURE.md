# Architecture Document: PodChat

## Document Information

**Product Name:** PodChat  
**Version:** 1.0 (MVP)  
**Last Updated:** January 29, 2026  
**Related Documents:** [PRD.md](./PRD.md)

---

## Table of Contents

1. [System Overview](#1-system-overview)
2. [High-Level Architecture](#2-high-level-architecture)
3. [Component Architecture](#3-component-architecture)
4. [Data Flow](#4-data-flow)
5. [Module Design](#5-module-design)
6. [Technology Stack](#6-technology-stack)
7. [Data Models](#7-data-models)
8. [Interface Definitions](#8-interface-definitions)
9. [Error Handling Strategy](#9-error-handling-strategy)
10. [Configuration Management](#10-configuration-management)
11. [Performance Considerations](#11-performance-considerations)
12. [Security Considerations](#12-security-considerations)
13. [Design Decisions](#13-design-decisions)
14. [Future Architecture Considerations](#14-future-architecture-considerations)

---

## 1. System Overview

### 1.1 Purpose

PodChat is a command-line application that processes YouTube podcast transcripts through Large Language Models (LLMs) to generate comprehensive summaries or chat-ready knowledge contexts.

### 1.2 Architecture Goals

- **Simplicity:** Minimal dependencies, straightforward flow
- **Modularity:** Clear separation of concerns for easy maintenance
- **Extensibility:** Easy to add new output formats or LLM providers
- **Reliability:** Robust error handling and graceful degradation
- **Performance:** Efficient processing of long transcripts

### 1.3 Constraints

- MVP scope: CLI-only, no web interface
- Single-user operation (no concurrent processing)
- Stateless operation (no database persistence)
- Internet dependency for YouTube and LLM APIs
- Token limits of chosen LLM provider

---

## 2. High-Level Architecture

### 2.1 System Context Diagram

```
┌─────────────┐
│    User     │
└──────┬──────┘
       │ CLI Commands
       ▼
┌─────────────────────────────────────┐
│          PodChat CLI                │
│  ┌───────────────────────────────┐  │
│  │   Command Parser & Router     │  │
│  └───────────┬───────────────────┘  │
│              │                       │
│  ┌───────────▼───────────────────┐  │
│  │   Core Processing Pipeline    │  │
│  │  ┌──────┐ ┌──────┐ ┌──────┐  │  │
│  │  │ Ext  │→│ LLM  │→│ Out  │  │  │
│  │  └──────┘ └──────┘ └──────┘  │  │
│  └───────────────────────────────┘  │
└─────────────────────────────────────┘
       │              │
       │              │
       ▼              ▼
┌─────────────┐  ┌──────────────────┐
│  YouTube    │  │  OpenRouter API  │
│  Transcript │  │  (Claude Sonnet  │
│  API        │  │   4.5)           │
└─────────────┘  └──────────────────┘
```

### 2.2 Deployment View

```
┌──────────────────────────────────────┐
│     User's Local Machine             │
│  ┌────────────────────────────────┐  │
│  │  Python 3.9+ Runtime           │  │
│  │  ┌──────────────────────────┐  │  │
│  │  │  PodChat Package         │  │  │
│  │  │  - CLI Entry Point       │  │  │
│  │  │  - Core Modules          │  │  │
│  │  │  - Configuration         │  │  │
│  │  └──────────────────────────┘  │  │
│  │                                 │  │
│  │  Dependencies:                  │  │
│  │  - youtube-transcript-api       │  │
│  │  - openai (OpenRouter client)   │  │
│  │  - click (CLI framework)        │  │
│  │  - python-dotenv                │  │
│  └────────────────────────────────┘  │
│                                       │
│  Configuration Files:                 │
│  - .env (API keys)                    │
│  - config.yaml (optional settings)    │
│                                       │
│  Output Directory:                    │
│  - ./summaries/ (default)             │
└──────────────────────────────────────┘
```

---

## 3. Component Architecture

### 3.1 Component Diagram

```
┌─────────────────────────────────────────────────────────┐
│                    PodChat Application                   │
├─────────────────────────────────────────────────────────┤
│                                                          │
│  ┌────────────────────────────────────────────────────┐ │
│  │              CLI Layer                             │ │
│  │  ┌──────────────┐  ┌──────────────────────────┐  │ │
│  │  │ Command      │  │  Argument Validator      │  │ │
│  │  │ Parser       │  │  & URL Parser            │  │ │
│  │  └──────┬───────┘  └──────────────────────────┘  │ │
│  └─────────┼─────────────────────────────────────────┘ │
│            │                                            │
│  ┌─────────▼─────────────────────────────────────────┐ │
│  │              Core Service Layer                   │ │
│  │  ┌────────────────────────────────────────────┐  │ │
│  │  │   PodcastProcessor (Orchestrator)          │  │ │
│  │  └────────────────────────────────────────────┘  │ │
│  └──────────────────────────────────────────────────┘ │
│            │                                            │
│  ┌─────────▼─────────────────────────────────────────┐ │
│  │           Business Logic Layer                    │ │
│  │  ┌──────────────┐  ┌────────────┐  ┌──────────┐ │ │
│  │  │  Transcript  │  │    LLM     │  │  Output  │ │ │
│  │  │  Extractor   │  │  Processor │  │  Formatter│ │ │
│  │  └──────────────┘  └────────────┘  └──────────┘ │ │
│  └──────────────────────────────────────────────────┘ │
│            │                │              │           │
│  ┌─────────▼────────────────▼──────────────▼────────┐ │
│  │              Integration Layer                    │ │
│  │  ┌──────────────┐  ┌────────────────────────┐   │ │
│  │  │  YouTube     │  │   LLM Provider         │   │ │
│  │  │  Client      │  │   Adapter (Factory)    │   │ │
│  │  │              │  │   - OpenRouter (MVP)   │   │ │
│  │  │              │  │   - Future: Direct     │   │ │
│  │  │              │  │     provider APIs      │   │ │
│  │  └──────────────┘  └────────────────────────┘   │ │
│  └──────────────────────────────────────────────────┘ │
│            │                │                          │
│  ┌─────────▼────────────────▼────────────────────────┐ │
│  │           Utility Layer                           │ │
│  │  ┌─────────┐  ┌─────────┐  ┌────────────────┐   │ │
│  │  │ Config  │  │ Logger  │  │ File Manager   │   │ │
│  │  │ Manager │  │         │  │                │   │ │
│  │  └─────────┘  └─────────┘  └────────────────┘   │ │
│  └──────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────┘
```

### 3.2 Component Responsibilities

| Component | Responsibility |
|-----------|---------------|
| **CLI Layer** | Parse commands, validate arguments, route to appropriate handlers |
| **PodcastProcessor** | Orchestrate the entire processing pipeline |
| **TranscriptExtractor** | Fetch and parse YouTube transcripts |
| **LLMProcessor** | Send prompts to LLM, handle responses, retry logic |
| **OutputFormatter** | Format data into markdown/chat-ready output |
| **YouTubeClient** | Interface with YouTube transcript API |
| **LLMProviderAdapter** | Abstract LLM provider differences, factory pattern (MVP: OpenRouter) |
| **ConfigManager** | Load and manage configuration from .env and config files |
| **Logger** | Structured logging for debugging and monitoring |
| **FileManager** | Handle file I/O operations, directory management |

---

## 4. Data Flow

### 4.1 Summary Generation Flow

```
┌─────────────────────────────────────────────────────────────────┐
│                   Summary Generation Flow                        │
└─────────────────────────────────────────────────────────────────┘

1. User Input
   │
   ├─→ podchat summarize https://youtube.com/watch?v=xyz
   │
   ▼

2. Command Parsing & Validation
   │
   ├─→ Parse URL: Extract video ID
   ├─→ Validate format
   ├─→ Parse options: --output, --verbose
   │
   ▼

3. Transcript Extraction
   │
   ├─→ Request transcript from YouTube API
   ├─→ Handle multiple language options
   ├─→ Parse timestamps and text
   │
   ├─→ SUCCESS: Transcript object with timestamps
   └─→ FAILURE: Error → User-friendly message
   │
   ▼

4. Transcript Preprocessing
   │
   ├─→ Calculate word count and duration
   ├─→ Chunk long transcripts if needed (>100K tokens)
   ├─→ Format for LLM consumption
   │
   ▼

5. LLM Processing
   │
   ├─→ Load prompt template (summary mode)
   ├─→ Inject transcript into prompt
   ├─→ Send to LLM API
   ├─→ Stream response (if supported)
   │
   ├─→ SUCCESS: Structured summary JSON/text
   └─→ FAILURE: Retry with backoff → Error if max retries
   │
   ▼

6. Output Formatting
   │
   ├─→ Parse LLM response
   ├─→ Apply markdown formatting
   ├─→ Add metadata (URL, duration, date)
   ├─→ Format timestamps
   ├─→ Structure sections (themes, quotes, takeaways)
   │
   ▼

7. File Output
   │
   ├─→ Generate filename: podcast-summary-{date}-{id}.md
   ├─→ Create output directory if needed
   ├─→ Write file
   ├─→ Display success message with stats
   │
   ▼

8. User receives markdown file
```

### 4.2 Chat Mode Flow

```
┌─────────────────────────────────────────────────────────────────┐
│                     Chat Mode Flow                               │
└─────────────────────────────────────────────────────────────────┘

1. User Input
   │
   ├─→ podchat chat https://youtube.com/watch?v=xyz
   │
   ▼

2-4. [Same as Summary Flow: Parse → Extract → Preprocess]
   │
   ▼

5. LLM Processing (Chat Mode)
   │
   ├─→ Load prompt template (chat/expertise mode)
   ├─→ Extract key concepts, frameworks, insights
   ├─→ Structure for Q&A format
   ├─→ Send to LLM API
   │
   ▼

6. Chat Context Formatting
   │
   ├─→ Generate structured context document
   ├─→ Include:
   │   - Domain expertise summary
   │   - Key frameworks and methodologies
   │   - Speaker's perspective and reasoning
   │   - Practical examples and case studies
   │   - Quick reference index
   │
   ▼

7. Output Generation
   │
   ├─→ Create chat-optimized markdown
   ├─→ Add context loading instructions
   ├─→ Include example queries
   │
   ▼

8. User loads context into chat environment (Claude, Cursor, etc.)
```

### 4.3 Sequence Diagram: Summary Generation

```
User        CLI         Processor    Extractor    LLMProcessor    OutputFormatter    FileManager
 │           │              │            │              │               │                │
 │ command   │              │            │              │               │                │
 ├──────────>│              │            │              │               │                │
 │           │ validate     │            │              │               │                │
 │           ├─────────────>│            │              │               │                │
 │           │              │ extract    │              │               │                │
 │           │              ├───────────>│              │               │                │
 │           │              │            │ API call     │               │                │
 │           │              │            ├──────────────>               │                │
 │           │              │            │   (YouTube)  │               │                │
 │           │              │            │<─────────────┘               │                │
 │           │              │<───────────┤ transcript   │               │                │
 │           │              │            │              │               │                │
 │           │              │ process    │              │               │                │
 │           │              ├────────────┼──────────────>               │                │
 │           │              │            │              │ API call      │                │
 │           │              │            │              ├───────────────>                │
 │           │              │            │              │   (LLM)       │                │
 │           │              │            │              │<──────────────┘                │
 │           │              │<───────────┼──────────────┤ summary       │                │
 │           │              │            │              │               │                │
 │           │              │ format     │              │               │                │
 │           │              ├────────────┼──────────────┼──────────────>│                │
 │           │              │<───────────┼──────────────┼───────────────┤ markdown       │
 │           │              │            │              │               │                │
 │           │              │ save       │              │               │                │
 │           │              ├────────────┼──────────────┼───────────────┼───────────────>│
 │           │              │<───────────┼──────────────┼───────────────┼────────────────┤
 │           │<─────────────┤ success    │              │               │                │
 │<──────────┤ display      │            │              │               │                │
 │  result   │              │            │              │               │                │
```

---

## 5. Module Design

### 5.1 Project Structure

```
podchat/
├── podchat/
│   ├── __init__.py
│   ├── __main__.py              # Entry point for CLI
│   │
│   ├── cli/
│   │   ├── __init__.py
│   │   ├── commands.py          # CLI command definitions
│   │   ├── validators.py        # Input validation
│   │   └── formatters.py        # Console output formatting
│   │
│   ├── core/
│   │   ├── __init__.py
│   │   ├── processor.py         # Main orchestrator
│   │   ├── extractor.py         # Transcript extraction
│   │   ├── llm_processor.py     # LLM interaction
│   │   └── output_formatter.py  # Output generation
│   │
│   ├── integrations/
│   │   ├── __init__.py
│   │   ├── youtube_client.py    # YouTube API client
│   │   └── llm/
│   │       ├── __init__.py
│   │       ├── base.py          # Abstract base class
│   │       ├── openrouter_client.py  # MVP: OpenRouter implementation
│   │       └── future_providers/     # Future: Direct provider clients
│   │           ├── openai_client.py
│   │           ├── anthropic_client.py
│   │           └── gemini_client.py
│   │
│   ├── models/
│   │   ├── __init__.py
│   │   ├── transcript.py        # Transcript data model
│   │   ├── summary.py           # Summary data model
│   │   └── config.py            # Configuration model
│   │
│   ├── utils/
│   │   ├── __init__.py
│   │   ├── config.py            # Config management
│   │   ├── logger.py            # Logging setup
│   │   ├── file_manager.py      # File I/O operations
│   │   └── exceptions.py        # Custom exceptions
│   │
│   └── templates/
│       ├── prompts/
│       │   ├── summary_prompt.txt
│       │   └── chat_prompt.txt
│       └── output/
│           ├── summary_template.md
│           └── chat_template.md
│
├── tests/
│   ├── unit/
│   ├── integration/
│   └── fixtures/
│
├── docs/
│   ├── PRD.md
│   ├── ARCHITECTURE.md
│   └── API.md
│
├── examples/
│   └── sample_summaries/
│
├── .env.example
├── .gitignore
├── pyproject.toml
├── requirements.txt
├── README.md
└── setup.py
```

### 5.2 Core Modules

#### 5.2.1 Processor Module

```python
# podchat/core/processor.py

class PodcastProcessor:
    """
    Orchestrates the entire processing pipeline.
    Coordinates between extractor, LLM processor, and output formatter.
    """
    
    def __init__(self, config: Config):
        self.config = config
        self.extractor = TranscriptExtractor(config)
        self.llm_processor = LLMProcessor(config)
        self.output_formatter = OutputFormatter(config)
        self.logger = get_logger(__name__)
    
    def process(self, url: str, mode: str = "summary", output_path: str = None) -> ProcessResult:
        """
        Main processing pipeline.
        
        Args:
            url: YouTube video URL
            mode: "summary" or "chat"
            output_path: Optional custom output path
            
        Returns:
            ProcessResult with success status and metadata
            
        Raises:
            TranscriptExtractionError: If transcript cannot be extracted
            LLMProcessingError: If LLM processing fails
            OutputFormattingError: If output generation fails
        """
        pass
    
    def _extract_transcript(self, url: str) -> Transcript:
        """Extract transcript from YouTube."""
        pass
    
    def _process_with_llm(self, transcript: Transcript, mode: str) -> LLMResponse:
        """Process transcript through LLM."""
        pass
    
    def _generate_output(self, llm_response: LLMResponse, mode: str) -> str:
        """Generate formatted output."""
        pass
```

#### 5.2.2 Extractor Module

```python
# podchat/core/extractor.py

class TranscriptExtractor:
    """
    Handles YouTube transcript extraction.
    Manages different transcript formats and error cases.
    """
    
    def __init__(self, config: Config):
        self.client = YouTubeClient(config)
        self.logger = get_logger(__name__)
    
    def extract(self, url: str) -> Transcript:
        """
        Extract transcript from YouTube video.
        
        Args:
            url: YouTube video URL
            
        Returns:
            Transcript object with text and timestamps
            
        Raises:
            InvalidURLError: If URL is not valid YouTube URL
            TranscriptNotAvailableError: If transcript is not available
            NetworkError: If network request fails
        """
        pass
    
    def _validate_url(self, url: str) -> str:
        """Validate and extract video ID from URL."""
        pass
    
    def _fetch_transcript(self, video_id: str) -> list[dict]:
        """Fetch raw transcript data."""
        pass
    
    def _parse_transcript(self, raw_data: list[dict]) -> Transcript:
        """Parse raw transcript into structured format."""
        pass
```

#### 5.2.3 LLM Processor Module

```python
# podchat/core/llm_processor.py

class LLMProcessor:
    """
    Handles all LLM interactions.
    Manages prompt construction, API calls, and response parsing.
    """
    
    def __init__(self, config: Config):
        self.client = self._create_llm_client(config)
        self.prompt_loader = PromptLoader()
        self.logger = get_logger(__name__)
    
    def process(self, transcript: Transcript, mode: str) -> LLMResponse:
        """
        Process transcript through LLM.
        
        Args:
            transcript: Transcript object
            mode: "summary" or "chat"
            
        Returns:
            LLMResponse with generated content
            
        Raises:
            LLMAPIError: If API call fails
            TokenLimitError: If transcript exceeds token limits
            RateLimitError: If rate limit is hit
        """
        pass
    
    def _build_prompt(self, transcript: Transcript, mode: str) -> str:
        """Construct prompt from template and transcript."""
        pass
    
    def _call_llm(self, prompt: str, max_retries: int = 3) -> str:
        """Call LLM API with retry logic."""
        pass
    
    def _parse_response(self, raw_response: str) -> LLMResponse:
        """Parse and validate LLM response."""
        pass
    
    def _create_llm_client(self, config: Config) -> BaseLLMClient:
        """Factory method to create appropriate LLM client."""
        pass
```

#### 5.2.4 Output Formatter Module

```python
# podchat/core/output_formatter.py

class OutputFormatter:
    """
    Formats LLM responses into structured output.
    Handles markdown generation and file operations.
    """
    
    def __init__(self, config: Config):
        self.config = config
        self.file_manager = FileManager(config)
        self.template_loader = TemplateLoader()
        self.logger = get_logger(__name__)
    
    def format_and_save(self, llm_response: LLMResponse, 
                       transcript_meta: TranscriptMetadata,
                       output_path: str = None) -> OutputResult:
        """
        Format response and save to file.
        
        Args:
            llm_response: Processed LLM response
            transcript_meta: Original transcript metadata
            output_path: Optional custom output path
            
        Returns:
            OutputResult with file path and statistics
            
        Raises:
            FormattingError: If formatting fails
            FileWriteError: If file cannot be written
        """
        pass
    
    def _format_summary(self, response: LLMResponse, meta: TranscriptMetadata) -> str:
        """Format as comprehensive summary."""
        pass
    
    def _format_chat_context(self, response: LLMResponse, meta: TranscriptMetadata) -> str:
        """Format as chat-ready context."""
        pass
    
    def _generate_filename(self, video_id: str, mode: str) -> str:
        """Generate appropriate filename."""
        pass
    
    def _make_timestamps_clickable(self, content: str, video_url: str) -> str:
        """
        Convert timestamp text [HH:MM:SS] to clickable YouTube links.
        
        Matches patterns like [HH:MM:SS] or [HH:MM:SS - HH:MM:SS] and converts
        them to markdown links that navigate to the video at that timestamp.
        
        Example: [00:01:21] → [[00:01:21]](https://www.youtube.com/watch?v=ID&t=81s)
        """
        pass
```

### 5.3 Integration Layer

#### 5.3.1 LLM Provider Adapter Pattern

```python
# podchat/integrations/llm/base.py

from abc import ABC, abstractmethod

class BaseLLMClient(ABC):
    """
    Abstract base class for LLM clients.
    Implements adapter pattern for different LLM providers.
    """
    
    @abstractmethod
    def generate(self, prompt: str, **kwargs) -> str:
        """Generate response from prompt."""
        pass
    
    @abstractmethod
    def count_tokens(self, text: str) -> int:
        """Count tokens in text."""
        pass
    
    @abstractmethod
    def get_max_tokens(self) -> int:
        """Get maximum token limit."""
        pass


# podchat/integrations/llm/openrouter_client.py

class OpenRouterClient(BaseLLMClient):
    """
    OpenRouter implementation (MVP).
    Uses OpenAI SDK with custom base_url for OpenRouter compatibility.
    """
    
    def __init__(self, api_key: str, model: str = "anthropic/claude-sonnet-4.5"):
        from openai import OpenAI
        
        self.client = OpenAI(
            api_key=api_key,
            base_url="https://openrouter.ai/api/v1"
        )
        self.model = model
    
    def generate(self, prompt: str, **kwargs) -> str:
        """Generate response using OpenRouter."""
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            **kwargs
        )
        return response.choices[0].message.content
    
    def count_tokens(self, text: str) -> int:
        """Estimate token count (Claude uses ~4 chars per token)."""
        return len(text) // 4
    
    def get_max_tokens(self) -> int:
        """Get maximum token limit for Claude Sonnet 4.5."""
        return 200000  # Claude Sonnet 4.5 context window
    
    # ... implement other methods


# Factory pattern for client creation
def create_llm_client(provider: str, config: Config) -> BaseLLMClient:
    """Factory function to create appropriate LLM client."""
    clients = {
        "openrouter": OpenRouterClient,  # MVP default
        # Future providers:
        # "openai": OpenAIClient,
        # "anthropic": AnthropicClient,
        # "gemini": GeminiClient,
    }
    
    client_class = clients.get(provider)
    if not client_class:
        raise ValueError(f"Unsupported LLM provider: {provider}")
    
    return client_class(
        api_key=config.llm_api_key,
        model=config.llm_model
    )
```

---

## 6. Technology Stack

### 6.1 Core Technologies

| Category | Technology | Version | Justification |
|----------|-----------|---------|---------------|
| **Language** | Python | 3.9+ | Rich ecosystem, excellent LLM libraries, cross-platform |
| **CLI Framework** | Click | 8.1+ | User-friendly, decorator-based, excellent help generation |
| **Transcript API** | youtube-transcript-api | 0.6+ | Maintained, supports multiple languages, handles edge cases |
| **LLM Provider** | OpenRouter | API | Unified interface to multiple LLM providers, flexible model selection |
| **LLM Model (MVP)** | Claude Sonnet 4.5 | via OpenRouter | State-of-the-art reasoning, excellent for long-form content analysis |
| **LLM Client** | openai | 1.x | OpenRouter uses OpenAI-compatible API, well-documented SDK |
| **Config** | python-dotenv | 1.0+ | Simple .env file management |
| **HTTP** | requests | 2.31+ | Reliable, widely used |
| **Logging** | Python logging | stdlib | Built-in, sufficient for MVP |

### 6.1.1 Why OpenRouter for MVP?

**OpenRouter Benefits:**
- **Unified API:** Single API interface for accessing multiple LLM providers
- **Model Flexibility:** Easy to switch between Claude, GPT-4, Gemini, etc. without code changes
- **Cost Management:** Transparent pricing, pay-as-you-go
- **Reliability:** Built-in fallback mechanisms
- **Future-Proof:** Adapter pattern allows easy migration to direct provider APIs later

**MVP Configuration:**
- Primary Model: `anthropic/claude-sonnet-4.5`
- API Endpoint: `https://openrouter.ai/api/v1`
- Compatible with OpenAI SDK (base_url override)

### 6.2 Development Dependencies

| Tool | Purpose |
|------|---------|
| **pytest** | Unit and integration testing |
| **black** | Code formatting |
| **flake8** | Linting |
| **mypy** | Static type checking |
| **pre-commit** | Git hooks for quality checks |

### 6.3 Dependency Graph

```
podchat
├── click (CLI)
├── youtube-transcript-api (Transcript)
├── openai (OpenRouter client - OpenAI-compatible)
├── python-dotenv (Config)
├── requests (HTTP)
└── [Python stdlib]
    ├── logging
    ├── json
    ├── pathlib
    ├── datetime
    └── typing

Note: OpenRouter accessed via OpenAI SDK with custom base_url
```

---

## 7. Data Models

### 7.1 Core Data Structures

```python
# podchat/models/transcript.py

from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional

@dataclass
class TranscriptSegment:
    """Individual transcript segment with timestamp."""
    text: str
    start: float  # seconds
    duration: float
    
    @property
    def end(self) -> float:
        return self.start + self.duration
    
    def format_timestamp(self) -> str:
        """Format as HH:MM:SS."""
        hours = int(self.start // 3600)
        minutes = int((self.start % 3600) // 60)
        seconds = int(self.start % 60)
        return f"{hours:02d}:{minutes:02d}:{seconds:02d}"


@dataclass
class TranscriptMetadata:
    """Metadata about the video and transcript."""
    video_id: str
    url: str
    title: Optional[str] = None
    duration: Optional[float] = None  # seconds
    language: str = "en"
    extracted_at: datetime = None
    
    def __post_init__(self):
        if self.extracted_at is None:
            self.extracted_at = datetime.now()


@dataclass
class Transcript:
    """Complete transcript with segments and metadata."""
    segments: List[TranscriptSegment]
    metadata: TranscriptMetadata
    
    @property
    def full_text(self) -> str:
        """Get complete transcript as single string."""
        return " ".join(seg.text for seg in self.segments)
    
    @property
    def word_count(self) -> int:
        """Count total words in transcript."""
        return len(self.full_text.split())
    
    @property
    def char_count(self) -> int:
        """Count total characters."""
        return len(self.full_text)
    
    def get_text_with_timestamps(self) -> str:
        """Get formatted text with timestamps."""
        return "\n".join(
            f"[{seg.format_timestamp()}] {seg.text}"
            for seg in self.segments
        )


# podchat/models/summary.py

@dataclass
class Theme:
    """A main theme from the podcast."""
    title: str
    description: str
    timestamps: List[str]
    key_quotes: List[str]


@dataclass
class Quote:
    """A notable quote from the podcast."""
    text: str
    timestamp: str
    speaker: Optional[str] = None
    context: Optional[str] = None


@dataclass
class Summary:
    """Structured summary of podcast."""
    overview: str
    main_themes: List[Theme]
    key_takeaways: List[str]
    notable_quotes: List[Quote]
    topics_by_timestamp: List[dict]  # [{"timestamp": "00:15:30", "topic": "..."}]
    metadata: TranscriptMetadata
    
    def to_markdown(self) -> str:
        """Convert summary to markdown format."""
        pass


@dataclass
class ChatContext:
    """Chat-optimized context from podcast."""
    expertise_summary: str
    key_concepts: List[str]
    frameworks: List[dict]
    practical_examples: List[str]
    speaker_perspective: str
    quick_reference: dict
    metadata: TranscriptMetadata
    
    def to_markdown(self) -> str:
        """Convert to chat-friendly markdown."""
        pass


# podchat/models/config.py

@dataclass
class Config:
    """Application configuration."""
    # LLM settings (MVP uses OpenRouter)
    llm_provider: str = "openrouter"  # MVP: openrouter; Future: openai, anthropic, etc.
    llm_model: str = "anthropic/claude-sonnet-4.5"  # OpenRouter model identifier
    llm_api_key: str = None  # OpenRouter API key
    llm_base_url: str = "https://openrouter.ai/api/v1"  # OpenRouter endpoint
    llm_max_tokens: int = 8192  # Claude Sonnet 4.5 supports large context
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
    
    @classmethod
    def from_env(cls) -> "Config":
        """Load configuration from environment variables."""
        pass
    
    @classmethod
    def from_file(cls, path: str) -> "Config":
        """Load configuration from YAML/JSON file."""
        pass
```

### 7.2 Result Types

```python
# podchat/models/results.py

from dataclasses import dataclass
from typing import Optional
from enum import Enum

class ProcessStatus(Enum):
    """Status of processing operation."""
    SUCCESS = "success"
    FAILED = "failed"
    PARTIAL = "partial"


@dataclass
class ProcessResult:
    """Result of podcast processing."""
    status: ProcessStatus
    output_path: Optional[str] = None
    error_message: Optional[str] = None
    
    # Statistics
    transcript_word_count: int = 0
    summary_word_count: int = 0
    processing_time: float = 0.0  # seconds
    
    # Metadata
    video_id: str = ""
    video_title: str = ""
    video_duration: float = 0.0
    
    def __bool__(self) -> bool:
        """Allow boolean evaluation."""
        return self.status == ProcessStatus.SUCCESS
```

---

## 8. Interface Definitions

### 8.1 CLI Interface

```bash
# Command structure
podchat [OPTIONS] COMMAND [ARGS]...

# Commands:
#   summarize  Generate comprehensive summary
#   chat       Generate chat-ready context
#   config     Manage configuration
#   version    Show version information

# Options:
#   --help     Show help message
#   --version  Show version


# Summarize command
podchat summarize [OPTIONS] URL

Options:
  --output, -o PATH          Output directory or file path
  --verbose, -v              Enable verbose output
  --provider TEXT            LLM provider (openai|anthropic|gemini)
  --model TEXT              LLM model name
  --max-tokens INTEGER      Maximum tokens for LLM response
  --help                    Show this message


# Chat command
podchat chat [OPTIONS] URL

Options:
  --output, -o PATH          Output file path
  --verbose, -v              Enable verbose output
  --provider TEXT            LLM provider
  --model TEXT              LLM model name
  --help                    Show this message


# Config command
podchat config [OPTIONS] COMMAND

Commands:
  show      Show current configuration
  set       Set configuration value
  init      Initialize configuration file


# Examples:
podchat summarize https://youtube.com/watch?v=abc123
podchat summarize https://youtube.com/watch?v=abc123 --output ./my-summaries/
podchat summarize https://youtube.com/watch?v=abc123 --provider anthropic --model claude-3-opus
podchat chat https://youtube.com/watch?v=abc123
podchat config show
podchat config set llm_provider anthropic
```

### 8.2 Python API (Internal)

```python
# Public API for potential library use

from podchat import PodcastProcessor, Config

# Initialize with configuration
config = Config.from_env()
processor = PodcastProcessor(config)

# Process podcast
result = processor.process(
    url="https://youtube.com/watch?v=abc123",
    mode="summary",
    output_path="./output.md"
)

if result:
    print(f"Success! Saved to {result.output_path}")
    print(f"Processing time: {result.processing_time:.2f}s")
else:
    print(f"Failed: {result.error_message}")
```

### 8.3 Configuration File Format

```yaml
# config.yaml

# LLM Configuration (MVP uses OpenRouter)
llm:
  provider: openrouter
  model: anthropic/claude-sonnet-4.5  # OpenRouter model identifier
  base_url: https://openrouter.ai/api/v1
  max_tokens: 8192
  temperature: 0.7

# Output Configuration
output:
  directory: ./output
  filename_format: "{title}_{mode}.md"  # Title-based with mode suffix

# Processing Configuration
processing:
  max_retries: 3
  retry_delay: 1.0
  timeout: 300

# Logging Configuration
logging:
  level: INFO
  file: null  # or path to log file
  format: "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
```

```bash
# .env file

# Required: OpenRouter API Key (MVP)
OPENROUTER_API_KEY=sk-or-v1-...

# Optional: Override defaults
LLM_PROVIDER=openrouter
LLM_MODEL=anthropic/claude-sonnet-4.5
LLM_BASE_URL=https://openrouter.ai/api/v1
OUTPUT_DIRECTORY=./output
LOG_LEVEL=INFO

# Future: Direct provider API keys
# OPENAI_API_KEY=sk-...
# ANTHROPIC_API_KEY=sk-ant-...
# GOOGLE_API_KEY=...
```

---

## 9. Error Handling Strategy

### 9.1 Exception Hierarchy

```python
# podchat/utils/exceptions.py

class PodChatError(Exception):
    """Base exception for all PodChat errors."""
    pass


# Input/Validation Errors
class ValidationError(PodChatError):
    """Base class for validation errors."""
    pass

class InvalidURLError(ValidationError):
    """Invalid YouTube URL provided."""
    pass

class InvalidArgumentError(ValidationError):
    """Invalid command-line argument."""
    pass


# Transcript Errors
class TranscriptError(PodChatError):
    """Base class for transcript-related errors."""
    pass

class TranscriptNotAvailableError(TranscriptError):
    """Transcript not available for video."""
    pass

class TranscriptExtractionError(TranscriptError):
    """Failed to extract transcript."""
    pass


# LLM Errors
class LLMError(PodChatError):
    """Base class for LLM-related errors."""
    pass

class LLMAPIError(LLMError):
    """LLM API call failed."""
    pass

class TokenLimitError(LLMError):
    """Content exceeds token limit."""
    pass

class RateLimitError(LLMError):
    """API rate limit exceeded."""
    pass


# Output Errors
class OutputError(PodChatError):
    """Base class for output-related errors."""
    pass

class FormattingError(OutputError):
    """Failed to format output."""
    pass

class FileWriteError(OutputError):
    """Failed to write output file."""
    pass


# Network Errors
class NetworkError(PodChatError):
    """Network-related errors."""
    pass
```

### 9.2 Error Handling Strategy

| Error Type | Handling Strategy | User Message |
|------------|-------------------|--------------|
| **InvalidURLError** | Validate early, fail fast | "Invalid YouTube URL. Expected format: https://youtube.com/watch?v=..." |
| **TranscriptNotAvailableError** | Check transcript availability | "Transcript not available for this video. Please enable captions or try another video." |
| **RateLimitError** | Retry with exponential backoff (3 attempts) | "API rate limit reached. Retrying in {delay}s... (Attempt {n}/3)" |
| **TokenLimitError** | Suggest chunking (future feature) | "Transcript too long ({tokens} tokens). Maximum: {max_tokens}. Consider a shorter video." |
| **LLMAPIError** | Retry, then fail with details | "LLM API error: {error_message}. Please check your API key and try again." |
| **NetworkError** | Retry, check connectivity | "Network error. Please check your internet connection." |
| **FileWriteError** | Check permissions, create directories | "Cannot write to {path}. Please check permissions." |

### 9.3 Retry Logic

```python
# podchat/utils/retry.py

import time
from functools import wraps
from typing import Type, Tuple

def retry_with_backoff(
    max_retries: int = 3,
    initial_delay: float = 1.0,
    backoff_factor: float = 2.0,
    exceptions: Tuple[Type[Exception], ...] = (Exception,)
):
    """
    Decorator for retrying operations with exponential backoff.
    
    Args:
        max_retries: Maximum number of retry attempts
        initial_delay: Initial delay in seconds
        backoff_factor: Multiplier for delay on each retry
        exceptions: Tuple of exception types to catch and retry
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            delay = initial_delay
            last_exception = None
            
            for attempt in range(max_retries + 1):
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    last_exception = e
                    if attempt < max_retries:
                        logger.warning(
                            f"Attempt {attempt + 1}/{max_retries} failed: {e}. "
                            f"Retrying in {delay}s..."
                        )
                        time.sleep(delay)
                        delay *= backoff_factor
                    else:
                        logger.error(f"All {max_retries} retry attempts failed.")
            
            raise last_exception
        
        return wrapper
    return decorator


# Usage example
@retry_with_backoff(max_retries=3, exceptions=(LLMAPIError, NetworkError))
def call_llm_api(prompt: str) -> str:
    # API call implementation
    pass
```

---

## 10. Configuration Management

### 10.1 Configuration Priority

Configuration sources are loaded in the following priority order (highest to lowest):

1. **Command-line arguments** (highest priority)
2. **Environment variables** (.env file)
3. **Configuration file** (config.yaml)
4. **Default values** (lowest priority)

### 10.2 Configuration Loading

```python
# podchat/utils/config.py

import os
from pathlib import Path
from typing import Optional
from dotenv import load_dotenv
import yaml

class ConfigManager:
    """Manages configuration from multiple sources."""
    
    DEFAULT_CONFIG = {
        "llm": {
            "provider": "openai",
            "model": "gpt-4",
            "max_tokens": 4096,
            "temperature": 0.7,
        },
        "output": {
            "directory": "./summaries",
        },
        "processing": {
            "max_retries": 3,
            "retry_delay": 1.0,
            "timeout": 300,
        },
        "logging": {
            "level": "INFO",
        }
    }
    
    def __init__(self):
        self.config = self.DEFAULT_CONFIG.copy()
        self._load_from_file()
        self._load_from_env()
    
    def _load_from_file(self, path: Optional[str] = None):
        """Load configuration from YAML file."""
        if path is None:
            # Look for config.yaml in standard locations
            locations = [
                Path.cwd() / "config.yaml",
                Path.home() / ".podchat" / "config.yaml",
            ]
            for loc in locations:
                if loc.exists():
                    path = str(loc)
                    break
        
        if path and Path(path).exists():
            with open(path) as f:
                file_config = yaml.safe_load(f)
                self._merge_config(file_config)
    
    def _load_from_env(self):
        """Load configuration from environment variables."""
        load_dotenv()
        
        env_mappings = {
            "OPENROUTER_API_KEY": ["llm", "api_key"],  # MVP
            "LLM_PROVIDER": ["llm", "provider"],
            "LLM_MODEL": ["llm", "model"],
            "LLM_BASE_URL": ["llm", "base_url"],
            "OUTPUT_DIRECTORY": ["output", "directory"],
            "LOG_LEVEL": ["logging", "level"],
            # Future direct provider keys:
            # "OPENAI_API_KEY": ["llm", "openai_api_key"],
            # "ANTHROPIC_API_KEY": ["llm", "anthropic_api_key"],
            # "GOOGLE_API_KEY": ["llm", "google_api_key"],
        }
        
        for env_var, config_path in env_mappings.items():
            value = os.getenv(env_var)
            if value:
                self._set_nested(self.config, config_path, value)
    
    def override_from_cli(self, **kwargs):
        """Override configuration from CLI arguments."""
        for key, value in kwargs.items():
            if value is not None:
                # Map CLI arguments to config structure
                self._set_from_cli_key(key, value)
    
    def get(self, *path, default=None):
        """Get configuration value by path."""
        value = self.config
        for key in path:
            if isinstance(value, dict) and key in value:
                value = value[key]
            else:
                return default
        return value
```

---

## 11. Performance Considerations

### 11.1 Performance Requirements

| Metric | Target | Measurement |
|--------|--------|-------------|
| **Transcript Extraction** | <5 seconds | Time from URL input to transcript ready |
| **LLM Processing (1hr podcast)** | <2 minutes | Time for LLM API call and response |
| **File Output** | <1 second | Time to write formatted output |
| **Total Processing Time** | <3 minutes | End-to-end for 1-hour podcast |
| **Memory Usage** | <500 MB | Peak memory during processing |

### 11.2 Optimization Strategies

#### 11.2.1 Transcript Processing

```python
# Efficient transcript handling for long podcasts

def chunk_transcript(transcript: Transcript, max_tokens: int) -> List[str]:
    """
    Chunk long transcripts to fit within token limits.
    Preserve semantic boundaries where possible.
    """
    chunks = []
    current_chunk = []
    current_tokens = 0
    
    for segment in transcript.segments:
        segment_tokens = estimate_tokens(segment.text)
        
        if current_tokens + segment_tokens > max_tokens:
            # Save current chunk
            chunks.append(" ".join(current_chunk))
            current_chunk = [segment.text]
            current_tokens = segment_tokens
        else:
            current_chunk.append(segment.text)
            current_tokens += segment_tokens
    
    if current_chunk:
        chunks.append(" ".join(current_chunk))
    
    return chunks
```

#### 11.2.2 API Call Optimization

```python
# Use streaming for faster perceived performance

async def stream_llm_response(prompt: str) -> AsyncIterator[str]:
    """
    Stream LLM response as it's generated.
    Allows progressive output display.
    """
    async for chunk in llm_client.stream(prompt):
        yield chunk
        # Update progress indicator
        update_progress(chunk)
```

#### 11.2.3 Caching Strategy (Future)

```python
# Cache processed transcripts to avoid re-processing

class TranscriptCache:
    """
    Cache processed transcripts to avoid redundant API calls.
    Key by video_id and processing parameters.
    """
    
    def get_cache_key(self, video_id: str, mode: str, model: str) -> str:
        return f"{video_id}_{mode}_{model}"
    
    def get(self, video_id: str, mode: str, model: str) -> Optional[ProcessResult]:
        cache_key = self.get_cache_key(video_id, mode, model)
        cache_file = self.cache_dir / f"{cache_key}.json"
        
        if cache_file.exists():
            # Check if cache is fresh (e.g., < 7 days old)
            if self._is_cache_fresh(cache_file):
                return self._load_from_cache(cache_file)
        
        return None
```

### 11.3 Resource Management

- **Memory:** Stream large responses instead of loading entirely into memory
- **API Costs:** Implement token estimation to warn users about costly operations
- **Rate Limiting:** Implement client-side rate limiting to avoid hitting API limits
- **Timeouts:** Set appropriate timeouts for all network operations

---

## 12. Security Considerations

### 12.1 API Key Management

```python
# Secure API key handling

class SecureConfig:
    """Secure configuration management."""
    
    @staticmethod
    def load_api_key(provider: str) -> str:
        """
        Load API key securely from environment.
        Never log or expose API keys.
        """
        key_name = f"{provider.upper()}_API_KEY"
        api_key = os.getenv(key_name)
        
        if not api_key:
            raise ConfigurationError(
                f"API key not found for {provider}. "
                f"Please set {key_name} in .env file."
            )
        
        # Validate key format (basic check)
        if not SecureConfig._is_valid_key_format(api_key, provider):
            raise ConfigurationError(
                f"Invalid API key format for {provider}."
            )
        
        return api_key
    
    @staticmethod
    def _is_valid_key_format(key: str, provider: str) -> bool:
        """Validate API key format without exposing the key."""
        patterns = {
            "openrouter": lambda k: k.startswith("sk-or-"),  # MVP
            "openai": lambda k: k.startswith("sk-"),
            "anthropic": lambda k: k.startswith("sk-ant-"),
            "gemini": lambda k: len(k) > 20,
        }
        return patterns.get(provider, lambda k: True)(key)
```

### 12.2 Security Best Practices

| Risk | Mitigation |
|------|------------|
| **API Key Exposure** | Store in .env, never commit to git, validate .gitignore |
| **Command Injection** | Sanitize all user inputs, use parameterized commands |
| **Path Traversal** | Validate output paths, restrict to allowed directories |
| **Data Leakage** | Don't log sensitive data, sanitize error messages |
| **Dependency Vulnerabilities** | Regular dependency updates, use `pip audit` |

### 12.3 .gitignore Configuration

```gitignore
# API Keys and Secrets
.env
.env.local
.env.*.local
config.local.yaml

# API keys accidentally committed
*_api_key*
*_secret*

# Output files (may contain sensitive content)
summaries/
output/
*.md (except docs/*.md)

# Cache and temporary files
__pycache__/
*.pyc
.cache/
.pytest_cache/

# Development
.vscode/
.idea/
*.swp
*.swo

# Logs
*.log
logs/
```

---

## 13. Design Decisions

### 13.1 Key Architectural Decisions

#### Decision 1: Python as Primary Language

**Context:** Need to choose implementation language for CLI tool.

**Decision:** Use Python 3.9+

**Rationale:**
- Excellent LLM library ecosystem (openai, anthropic, google-generativeai)
- Mature YouTube transcript libraries
- Cross-platform compatibility
- Fast development with agentic tools
- Strong typing support with type hints

**Alternatives Considered:**
- Node.js: Good LLM support but less mature transcript libraries
- Go: Fast but less rich LLM ecosystem

---

#### Decision 2: Adapter Pattern for LLM Providers + OpenRouter for MVP

**Context:** Need to support LLM processing with flexibility for future provider changes.

**Decision:** 
- Implement adapter pattern with abstract base class
- Use OpenRouter as MVP provider
- Model: Claude Sonnet 4.5 (`anthropic/claude-sonnet-4.5`)

**Rationale:**

**Why Adapter Pattern:**
- Allows easy addition of new providers in the future
- Decouples business logic from provider-specific APIs
- Enables provider switching without code changes
- Testable with mock implementations

**Why OpenRouter for MVP:**
- **Unified Gateway:** Single API for multiple LLM providers (Claude, GPT-4, Gemini, etc.)
- **Simplified Setup:** One API key instead of managing multiple provider accounts
- **Cost Transparency:** Clear, unified pricing across providers
- **Easy Migration:** Can switch to direct provider APIs later without changing core logic
- **Flexibility:** Can test different models (Claude, GPT-4, etc.) with simple config change
- **OpenAI-Compatible:** Uses OpenAI SDK with base_url override, minimal learning curve

**Why Claude Sonnet 4.5:**
- State-of-the-art reasoning capabilities
- Excellent long-form content analysis
- Large context window (200K tokens) handles long podcasts
- Strong at structured output generation
- Nuanced understanding for expertise extraction

**Trade-offs:**
- Additional abstraction layer adds slight complexity (worth it for flexibility)
- OpenRouter adds intermediary vs direct API (acceptable for MVP, easy to change later)
- Dependency on OpenRouter service (mitigated by adapter pattern allowing future migration)

---

#### Decision 3: Stateless Operation (No Database)

**Context:** Should the application persist processed summaries?

**Decision:** No database or persistence layer for MVP.

**Rationale:**
- Simpler architecture for MVP
- Reduced dependencies and setup complexity
- File-based output is sufficient for primary use case
- Can add caching/database in future iterations

**Trade-offs:**
- Re-processing same video requires new API calls
- No built-in summary management
- Future enhancement: Add optional caching layer

---

#### Decision 4: Synchronous Processing

**Context:** Should processing be asynchronous/concurrent?

**Decision:** Synchronous processing for MVP.

**Rationale:**
- Simpler implementation and debugging
- Single-video processing is primary use case
- API calls are the bottleneck (not CPU)
- Batch processing is out of scope for MVP

**Future:** Add async support for batch processing

---

#### Decision 5: Markdown as Output Format

**Context:** What format should summaries use?

**Decision:** Markdown as primary output format.

**Rationale:**
- Universal, human-readable, version-control friendly
- Supported by all modern editors and note-taking apps
- Easy to convert to HTML, PDF, or other formats
- Perfect for chat environment integration

**Alternatives:**
- JSON: Too technical for end users
- HTML: Requires rendering, less portable
- PDF: Not editable, harder to work with

---

#### Decision 6: Click for CLI Framework

**Context:** Which CLI framework to use?

**Decision:** Use Click over argparse.

**Rationale:**
- More user-friendly API
- Better help generation
- Built-in validation support
- Industry standard for Python CLIs

---

#### Decision 7: Template-Based Prompts

**Context:** How to manage LLM prompts?

**Decision:** External template files for prompts.

**Rationale:**
- Easy to iterate and improve prompts
- No code changes needed for prompt updates
- Version control for prompt evolution
- Can support multiple prompt variants

**Implementation:**
```
templates/
├── prompts/
│   ├── summary_prompt.txt
│   └── chat_prompt.txt
```

---

### 13.2 Trade-offs Summary

| Decision | Benefit | Trade-off |
|----------|---------|-----------|
| **Python** | Rich ecosystem, fast development | Slower execution vs compiled languages |
| **Adapter Pattern** | Flexibility, testability | Additional abstraction layer |
| **OpenRouter (MVP)** | Unified API, easy provider switching | Intermediary service dependency |
| **Claude Sonnet 4.5** | Excellent reasoning, large context | Cost per token (mitigated by quality) |
| **No Database** | Simple architecture | No persistence, re-processing needed |
| **Synchronous** | Simpler implementation | No concurrent processing |
| **Markdown Output** | Universal, portable | Less structured than JSON |
| **Template Prompts** | Easy iteration | Additional file management |

---

## 14. Future Architecture Considerations

### 14.1 Post-MVP Enhancements

#### 14.1.1 Caching Layer

```python
# Future: Add caching to avoid re-processing

class CacheManager:
    """
    Cache processed summaries.
    Use SQLite for lightweight persistence.
    """
    
    def __init__(self, cache_dir: str):
        self.db = sqlite3.connect(f"{cache_dir}/cache.db")
        self._init_schema()
    
    def get_cached_summary(self, video_id: str, mode: str) -> Optional[str]:
        """Retrieve cached summary if available and fresh."""
        pass
    
    def cache_summary(self, video_id: str, mode: str, summary: str):
        """Store processed summary in cache."""
        pass
```

#### 14.1.2 Batch Processing

```python
# Future: Process multiple videos concurrently

async def process_batch(urls: List[str], mode: str) -> List[ProcessResult]:
    """
    Process multiple podcasts concurrently.
    Use asyncio for parallel API calls.
    """
    tasks = [process_video_async(url, mode) for url in urls]
    results = await asyncio.gather(*tasks, return_exceptions=True)
    return results
```

#### 14.1.3 Plugin System

```python
# Future: Support custom output formatters and processors

class OutputPlugin(ABC):
    """Abstract base for output plugins."""
    
    @abstractmethod
    def format(self, summary: Summary) -> str:
        """Format summary to custom output format."""
        pass

# Users can create custom plugins:
# - PDF generator
# - Notion exporter
# - Obsidian formatter
# - Audio summary generator
```

#### 14.1.4 Web Interface

```
Future Architecture with Web Interface:

┌─────────────────────────────────────┐
│         Web Frontend                │
│       (React/Next.js)               │
└─────────────┬───────────────────────┘
              │ REST API
┌─────────────▼───────────────────────┐
│         API Server                  │
│        (FastAPI/Flask)              │
└─────────────┬───────────────────────┘
              │
┌─────────────▼───────────────────────┐
│      Core PodChat Library           │
│    (Refactored as library)          │
└─────────────────────────────────────┘
```

### 14.2 Scalability Considerations

For production-scale deployment:

1. **Queue System:** Use Celery/RQ for async job processing
2. **Database:** PostgreSQL for persistent storage
3. **Caching:** Redis for fast caching layer
4. **API Gateway:** Rate limiting, authentication
5. **Monitoring:** Prometheus, Grafana for metrics
6. **Logging:** ELK stack for centralized logging

---

## Appendix

### A. System Requirements

**Minimum:**
- Python 3.9+
- 2 GB RAM
- 100 MB disk space
- Internet connection

**Recommended:**
- Python 3.11+
- 4 GB RAM
- 500 MB disk space (for multiple summaries)
- Stable broadband connection

### B. Glossary

| Term | Definition |
|------|------------|
| **Transcript** | Text version of podcast audio with timestamps |
| **LLM** | Large Language Model (GPT, Claude, Gemini) |
| **OpenRouter** | Unified API gateway for accessing multiple LLM providers |
| **Claude Sonnet 4.5** | Anthropic's advanced language model with 200K token context window |
| **Adapter Pattern** | Design pattern for interface compatibility |
| **Token** | Unit of text processed by LLM (roughly 0.75 words for Claude) |
| **Rate Limiting** | Restricting API call frequency |
| **Streaming** | Progressive response delivery |
| **Chunking** | Splitting large content into smaller pieces |

### C. References

- [YouTube Transcript API Documentation](https://github.com/jdepoix/youtube-transcript-api)
- [OpenRouter API Documentation](https://openrouter.ai/docs)
- [OpenRouter Supported Models](https://openrouter.ai/models)
- [Claude Sonnet 4.5 Model Details](https://openrouter.ai/models/anthropic/claude-sonnet-4.5)
- [OpenAI API Documentation](https://platform.openai.com/docs) (OpenRouter uses compatible format)
- [Anthropic Claude Documentation](https://docs.anthropic.com/)
- [Click Documentation](https://click.palletsprojects.com/)
- [Python Design Patterns](https://refactoring.guru/design-patterns/python)

---

**Document Version History:**
- v1.0 (2026-01-29): Initial architecture document for MVP
