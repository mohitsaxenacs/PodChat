# Implementation Plan: PodChat MVP

## Document Information

**Product Name:** PodChat  
**Version:** 1.0 (MVP)  
**Last Updated:** January 29, 2026  
**Related Documents:** [PRD.md](./PRD.md) | [ARCHITECTURE.md](./ARCHITECTURE.md)

---

## Table of Contents

1. [Overview](#1-overview)
2. [Development Approach](#2-development-approach)
3. [Phase 0: Project Setup](#phase-0-project-setup)
4. [Phase 1: Core Infrastructure](#phase-1-core-infrastructure)
5. [Phase 2: Transcript Extraction](#phase-2-transcript-extraction)
6. [Phase 3: LLM Integration](#phase-3-llm-integration)
7. [Phase 4: Summary Generation](#phase-4-summary-generation)
8. [Phase 5: Chat Mode](#phase-5-chat-mode)
9. [Phase 6: CLI Enhancement](#phase-6-cli-enhancement)
10. [Phase 7: Testing & Documentation](#phase-7-testing--documentation)
11. [Implementation Checklist](#implementation-checklist)
12. [Code Examples](#code-examples)
13. [Testing Strategy](#testing-strategy)
14. [Deployment & Delivery](#deployment--delivery)

---

## 1. Overview

### 1.1 Implementation Goals

Build a fully functional CLI tool that:
- ✅ Extracts YouTube podcast transcripts
- ✅ Generates comprehensive summaries via Claude Sonnet 4.5
- ✅ Creates chat-ready knowledge contexts
- ✅ Handles errors gracefully
- ✅ Provides excellent user experience

### 1.2 Target Timeline

**Estimated Time:** ~1 hour (using agentic coding tools)

**Breakdown:**
- Phase 0-1: Project Setup & Infrastructure (10 min)
- Phase 2: Transcript Extraction (10 min)
- Phase 3: LLM Integration (15 min)
- Phase 4-5: Summary & Chat Generation (15 min)
- Phase 6-7: CLI, Testing & Docs (10 min)

### 1.3 Success Criteria

**MVP is complete when:**
1. ✅ User can run `podchat summarize <url>` successfully
2. ✅ Generates comprehensive markdown summaries
3. ✅ Chat mode produces usable context files
4. ✅ Error messages are clear and actionable
5. ✅ README with installation and usage examples exists
6. ✅ Example summaries are included
7. ✅ All core features (P0) are implemented

---

## 2. Development Approach

### 2.1 Methodology

**Incremental Development:**
- Build vertically: Complete one feature end-to-end before moving to next
- Test immediately after each phase
- Iterate on quality (especially prompts)

**Tools:**
- Use agentic coding tools (Cursor, Claude)
- Document decisions and iterations in chat history
- Version control with Git (commit after each phase)

### 2.2 Technology Stack Summary

| Component | Technology |
|-----------|-----------|
| **Language** | Python 3.9+ |
| **CLI Framework** | Click |
| **Transcript** | youtube-transcript-api |
| **LLM Provider** | OpenRouter |
| **LLM Model** | Claude Sonnet 4.5 |
| **LLM Client** | openai (with OpenRouter base_url) |
| **Config** | python-dotenv |
| **Packaging** | setuptools / pyproject.toml |

### 2.3 Development Environment Setup

**Prerequisites:**
```bash
- Python 3.9 or higher
- pip (Python package manager)
- Git
- Text editor / IDE (VSCode, PyCharm, Cursor)
- OpenRouter API key
```

---

## Phase 0: Project Setup

**Estimated Time:** 5 minutes  
**Priority:** P0 (Must Have)

### Tasks

#### 0.1 Initialize Project Structure ✓

Create the directory structure as defined in ARCHITECTURE.md:

```bash
podchat/
├── podchat/
│   ├── __init__.py
│   ├── __main__.py
│   ├── cli/
│   │   ├── __init__.py
│   │   ├── commands.py
│   │   ├── validators.py
│   │   └── formatters.py
│   ├── core/
│   │   ├── __init__.py
│   │   ├── processor.py
│   │   ├── extractor.py
│   │   ├── llm_processor.py
│   │   └── output_formatter.py
│   ├── integrations/
│   │   ├── __init__.py
│   │   ├── youtube_client.py
│   │   └── llm/
│   │       ├── __init__.py
│   │       ├── base.py
│   │       └── openrouter_client.py
│   ├── models/
│   │   ├── __init__.py
│   │   ├── transcript.py
│   │   ├── summary.py
│   │   └── config.py
│   ├── utils/
│   │   ├── __init__.py
│   │   ├── config.py
│   │   ├── logger.py
│   │   ├── file_manager.py
│   │   └── exceptions.py
│   └── templates/
│       └── prompts/
│           ├── summary_prompt.txt
│           └── chat_prompt.txt
├── tests/
│   ├── __init__.py
│   ├── unit/
│   └── integration/
├── examples/
│   └── sample_summaries/
├── docs/
│   ├── PRD.md
│   ├── ARCHITECTURE.md
│   └── IMPLEMENTATION_PLAN.md
├── .env.example
├── .gitignore
├── pyproject.toml
├── requirements.txt
├── README.md
└── setup.py
```

**Commands:**
```bash
mkdir -p podchat/{cli,core,integrations/llm,models,utils,templates/prompts}
mkdir -p tests/{unit,integration}
mkdir -p examples/sample_summaries
mkdir -p docs
touch podchat/__init__.py
touch podchat/__main__.py
# ... (create all __init__.py files)
```

#### 0.2 Create Configuration Files ✓

**File: `.gitignore`**
```gitignore
# API Keys and Secrets
.env
.env.local
.env.*.local

# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
env/
venv/
ENV/
build/
dist/
*.egg-info/

# IDE
.vscode/
.idea/
*.swp
*.swo

# Output
summaries/
output/
*.md (except docs/*.md and README.md)

# Logs
*.log
logs/

# Testing
.pytest_cache/
.coverage
htmlcov/

# macOS
.DS_Store
```

**File: `.env.example`**
```bash
# OpenRouter API Key (Required)
OPENROUTER_API_KEY=sk-or-v1-your-api-key-here

# Optional: Override defaults
LLM_PROVIDER=openrouter
LLM_MODEL=anthropic/claude-sonnet-4.5
LLM_BASE_URL=https://openrouter.ai/api/v1
OUTPUT_DIRECTORY=./summaries
LOG_LEVEL=INFO
```

**File: `requirements.txt`**
```txt
# Core dependencies
click>=8.1.0
youtube-transcript-api>=0.6.0
openai>=1.0.0
python-dotenv>=1.0.0
requests>=2.31.0

# Development dependencies
pytest>=7.4.0
pytest-cov>=4.1.0
black>=23.0.0
flake8>=6.0.0
mypy>=1.5.0
```

**File: `pyproject.toml`**
```toml
[build-system]
requires = ["setuptools>=68.0", "wheel"]
build-backend = "setuptools.build_meta"

[project]
name = "podchat"
version = "1.0.0"
description = "CLI tool to transform YouTube podcasts into actionable knowledge"
readme = "README.md"
requires-python = ">=3.9"
license = {text = "MIT"}
authors = [
    {name = "Your Name", email = "your.email@example.com"}
]
keywords = ["podcast", "youtube", "summarization", "ai", "cli"]
classifiers = [
    "Development Status :: 4 - Beta",
    "Intended Audience :: Developers",
    "License :: OSI Approved :: MIT License",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.9",
    "Programming Language :: Python :: 3.10",
    "Programming Language :: Python :: 3.11",
]

dependencies = [
    "click>=8.1.0",
    "youtube-transcript-api>=0.6.0",
    "openai>=1.0.0",
    "python-dotenv>=1.0.0",
    "requests>=2.31.0",
]

[project.optional-dependencies]
dev = [
    "pytest>=7.4.0",
    "pytest-cov>=4.1.0",
    "black>=23.0.0",
    "flake8>=6.0.0",
    "mypy>=1.5.0",
]

[project.scripts]
podchat = "podchat.__main__:main"

[tool.black]
line-length = 100
target-version = ['py39']

[tool.mypy]
python_version = "3.9"
warn_return_any = true
warn_unused_configs = true
disallow_untyped_defs = true
```

#### 0.3 Initialize Git Repository ✓

```bash
git init
git add .
git commit -m "Initial project structure"
```

### Acceptance Criteria

- ✅ All directories created
- ✅ All configuration files in place
- ✅ Git repository initialized
- ✅ `.env.example` created (but not `.env` - user creates this)
- ✅ Requirements files complete

---

## Phase 1: Core Infrastructure

**Estimated Time:** 5 minutes  
**Priority:** P0 (Must Have)  
**Dependencies:** Phase 0

### Tasks

#### 1.1 Implement Exception Hierarchy ✓

**File: `podchat/utils/exceptions.py`**

```python
"""Custom exceptions for PodChat."""


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


# Configuration Errors
class ConfigurationError(PodChatError):
    """Configuration-related errors."""
    pass
```

#### 1.2 Implement Data Models ✓

**File: `podchat/models/transcript.py`**

```python
"""Data models for transcripts."""
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
        """End time of segment."""
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
    extracted_at: Optional[datetime] = None
    
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
```

**File: `podchat/models/config.py`**

```python
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
    output_directory: str = "./summaries"
    verbose: bool = False
    
    # Processing settings
    max_retries: int = 3
    retry_delay: float = 1.0
    timeout: int = 300  # seconds
    
    # Logging
    log_level: str = "INFO"
    log_file: Optional[str] = None
```

#### 1.3 Implement Configuration Manager ✓

**File: `podchat/utils/config.py`**

```python
"""Configuration management."""
import os
from pathlib import Path
from typing import Optional
from dotenv import load_dotenv

from ..models.config import Config
from .exceptions import ConfigurationError


class ConfigManager:
    """Manages configuration from multiple sources."""
    
    @staticmethod
    def load() -> Config:
        """Load configuration from environment and defaults."""
        # Load .env file if it exists
        env_path = Path.cwd() / ".env"
        if env_path.exists():
            load_dotenv(env_path)
        
        # Get API key
        api_key = os.getenv("OPENROUTER_API_KEY")
        if not api_key:
            raise ConfigurationError(
                "OPENROUTER_API_KEY not found. "
                "Please set it in your .env file or environment variables."
            )
        
        # Create config with overrides from environment
        config = Config(
            llm_api_key=api_key,
            llm_provider=os.getenv("LLM_PROVIDER", "openrouter"),
            llm_model=os.getenv("LLM_MODEL", "anthropic/claude-sonnet-4.5"),
            llm_base_url=os.getenv("LLM_BASE_URL", "https://openrouter.ai/api/v1"),
            output_directory=os.getenv("OUTPUT_DIRECTORY", "./summaries"),
            log_level=os.getenv("LOG_LEVEL", "INFO"),
        )
        
        return config
    
    @staticmethod
    def validate_api_key(api_key: str, provider: str = "openrouter") -> bool:
        """Validate API key format."""
        if provider == "openrouter":
            return api_key.startswith("sk-or-")
        return len(api_key) > 20
```

#### 1.4 Implement Logger ✓

**File: `podchat/utils/logger.py`**

```python
"""Logging configuration."""
import logging
import sys
from typing import Optional


def setup_logger(
    name: str = "podchat",
    level: str = "INFO",
    log_file: Optional[str] = None
) -> logging.Logger:
    """Set up logger with console and optional file handlers."""
    logger = logging.getLogger(name)
    logger.setLevel(getattr(logging, level.upper()))
    
    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)
    console_format = logging.Formatter(
        '%(levelname)s: %(message)s'
    )
    console_handler.setFormatter(console_format)
    logger.addHandler(console_handler)
    
    # File handler (optional)
    if log_file:
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(logging.DEBUG)
        file_format = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        file_handler.setFormatter(file_format)
        logger.addHandler(file_handler)
    
    return logger


def get_logger(name: str) -> logging.Logger:
    """Get a logger instance."""
    return logging.getLogger(name)
```

#### 1.5 Implement File Manager ✓

**File: `podchat/utils/file_manager.py`**

```python
"""File management utilities."""
from pathlib import Path
from typing import Optional
from datetime import datetime

from .exceptions import FileWriteError


class FileManager:
    """Handles file I/O operations."""
    
    def __init__(self, output_directory: str = "./summaries"):
        self.output_directory = Path(output_directory)
    
    def ensure_output_directory(self) -> None:
        """Create output directory if it doesn't exist."""
        self.output_directory.mkdir(parents=True, exist_ok=True)
    
    def generate_filename(
        self,
        video_id: str,
        mode: str = "summary",
        extension: str = "md"
    ) -> str:
        """Generate unique filename for output."""
        date_str = datetime.now().strftime("%Y%m%d-%H%M%S")
        return f"podcast-{mode}-{date_str}-{video_id}.{extension}"
    
    def write_output(
        self,
        content: str,
        filename: Optional[str] = None,
        video_id: Optional[str] = None,
        mode: str = "summary"
    ) -> Path:
        """Write content to file."""
        try:
            self.ensure_output_directory()
            
            if filename is None:
                if video_id is None:
                    raise ValueError("Either filename or video_id must be provided")
                filename = self.generate_filename(video_id, mode)
            
            output_path = self.output_directory / filename
            output_path.write_text(content, encoding="utf-8")
            
            return output_path
        except Exception as e:
            raise FileWriteError(f"Failed to write output file: {e}")
```

### Acceptance Criteria

- ✅ Exception hierarchy implemented
- ✅ Core data models (Transcript, Config) implemented
- ✅ Configuration manager loads from .env
- ✅ Logger configured with console output
- ✅ File manager handles output operations
- ✅ All modules importable without errors

### Testing

```bash
# Test imports
python -c "from podchat.utils.exceptions import PodChatError"
python -c "from podchat.models.transcript import Transcript"
python -c "from podchat.models.config import Config"
python -c "from podchat.utils.config import ConfigManager"
```

---

## Phase 2: Transcript Extraction

**Estimated Time:** 10 minutes  
**Priority:** P0 (Must Have)  
**Dependencies:** Phase 1

### Tasks

#### 2.1 Implement YouTube Client ✓

**File: `podchat/integrations/youtube_client.py`**

```python
"""YouTube transcript client."""
import re
from typing import List, Dict, Optional
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api._errors import (
    TranscriptsDisabled,
    NoTranscriptFound,
    VideoUnavailable
)

from ..utils.exceptions import (
    InvalidURLError,
    TranscriptNotAvailableError,
    TranscriptExtractionError
)
from ..utils.logger import get_logger


class YouTubeClient:
    """Client for fetching YouTube transcripts."""
    
    def __init__(self):
        self.logger = get_logger(__name__)
    
    def extract_video_id(self, url: str) -> str:
        """Extract video ID from YouTube URL."""
        patterns = [
            r'(?:youtube\.com\/watch\?v=)([^&\s]+)',
            r'(?:youtu\.be\/)([^&\s]+)',
            r'(?:youtube\.com\/embed\/)([^&\s]+)',
            r'(?:youtube\.com\/v\/)([^&\s]+)',
        ]
        
        for pattern in patterns:
            match = re.search(pattern, url)
            if match:
                return match.group(1)
        
        raise InvalidURLError(
            f"Invalid YouTube URL: {url}\n"
            "Expected formats:\n"
            "  - https://www.youtube.com/watch?v=VIDEO_ID\n"
            "  - https://youtu.be/VIDEO_ID\n"
            "  - https://www.youtube.com/embed/VIDEO_ID"
        )
    
    def fetch_transcript(
        self,
        video_id: str,
        languages: Optional[List[str]] = None
    ) -> List[Dict]:
        """Fetch transcript from YouTube."""
        if languages is None:
            languages = ['en', 'en-US', 'en-GB']
        
        try:
            self.logger.info(f"Fetching transcript for video: {video_id}")
            transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)
            
            # Try to get transcript in preferred languages
            try:
                transcript = transcript_list.find_transcript(languages)
            except NoTranscriptFound:
                # Fall back to any available transcript
                available = transcript_list._manually_created_transcripts
                if not available:
                    available = transcript_list._generated_transcripts
                
                if not available:
                    raise TranscriptNotAvailableError(
                        f"No transcripts available for video {video_id}"
                    )
                
                transcript = list(available.values())[0]
                self.logger.warning(
                    f"Preferred language not found. Using: {transcript.language}"
                )
            
            return transcript.fetch()
            
        except TranscriptsDisabled:
            raise TranscriptNotAvailableError(
                f"Transcripts are disabled for video {video_id}. "
                "Please enable captions on the video."
            )
        except VideoUnavailable:
            raise TranscriptExtractionError(
                f"Video {video_id} is unavailable. "
                "It may be private, deleted, or restricted."
            )
        except Exception as e:
            raise TranscriptExtractionError(
                f"Failed to fetch transcript: {str(e)}"
            )
```

#### 2.2 Implement Transcript Extractor ✓

**File: `podchat/core/extractor.py`**

```python
"""Transcript extraction logic."""
from typing import Optional

from ..integrations.youtube_client import YouTubeClient
from ..models.transcript import Transcript, TranscriptSegment, TranscriptMetadata
from ..utils.logger import get_logger


class TranscriptExtractor:
    """Handles YouTube transcript extraction."""
    
    def __init__(self):
        self.client = YouTubeClient()
        self.logger = get_logger(__name__)
    
    def extract(self, url: str) -> Transcript:
        """
        Extract transcript from YouTube video.
        
        Args:
            url: YouTube video URL
            
        Returns:
            Transcript object with text and timestamps
        """
        # Extract video ID
        video_id = self.client.extract_video_id(url)
        self.logger.info(f"Processing video ID: {video_id}")
        
        # Fetch raw transcript data
        raw_transcript = self.client.fetch_transcript(video_id)
        
        # Parse into structured format
        transcript = self._parse_transcript(raw_transcript, video_id, url)
        
        self.logger.info(
            f"Transcript extracted: {transcript.word_count} words, "
            f"{len(transcript.segments)} segments"
        )
        
        return transcript
    
    def _parse_transcript(
        self,
        raw_data: list,
        video_id: str,
        url: str
    ) -> Transcript:
        """Parse raw transcript into structured format."""
        segments = []
        total_duration = 0.0
        
        for item in raw_data:
            segment = TranscriptSegment(
                text=item['text'],
                start=item['start'],
                duration=item['duration']
            )
            segments.append(segment)
            total_duration = max(total_duration, segment.end)
        
        metadata = TranscriptMetadata(
            video_id=video_id,
            url=url,
            duration=total_duration
        )
        
        return Transcript(segments=segments, metadata=metadata)
```

### Acceptance Criteria

- ✅ YouTube URL parsing works for all common formats
- ✅ Transcript extraction succeeds for videos with transcripts
- ✅ Clear error messages for unavailable transcripts
- ✅ Timestamps preserved in segments
- ✅ Handles edge cases (private videos, no transcripts, etc.)

### Testing

```python
# Test URL validation
from podchat.integrations.youtube_client import YouTubeClient

client = YouTubeClient()
video_id = client.extract_video_id("https://www.youtube.com/watch?v=dQw4w9WgXcQ")
assert video_id == "dQw4w9WgXcQ"

# Test transcript extraction (use a real video with transcript)
from podchat.core.extractor import TranscriptExtractor

extractor = TranscriptExtractor()
transcript = extractor.extract("https://www.youtube.com/watch?v=VALID_VIDEO_ID")
print(f"Extracted {transcript.word_count} words")
```

---

## Phase 3: LLM Integration

**Estimated Time:** 15 minutes  
**Priority:** P0 (Must Have)  
**Dependencies:** Phase 1

### Tasks

#### 3.1 Implement Base LLM Client ✓

**File: `podchat/integrations/llm/base.py`**

```python
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
```

#### 3.2 Implement OpenRouter Client ✓

**File: `podchat/integrations/llm/openrouter_client.py`**

```python
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
```

#### 3.3 Create LLM Client Factory ✓

**File: `podchat/integrations/llm/__init__.py`**

```python
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
```

#### 3.4 Create Prompt Templates ✓

**File: `podchat/templates/prompts/summary_prompt.txt`**

```
You are an expert at analyzing podcast transcripts and creating comprehensive summaries that capture the full depth and nuance of the discussion.

Your task is to create a detailed markdown summary of the following podcast transcript. The summary should be so thorough that reading it is nearly equivalent to listening to the full podcast.

TRANSCRIPT:
{transcript}

VIDEO METADATA:
- Video ID: {video_id}
- URL: {url}
- Duration: {duration}
- Word Count: {word_count}

REQUIREMENTS:

1. **Overview** (2-3 sentences): Provide a concise summary of the podcast's main topic and key message.

2. **Main Themes**: Identify 3-5 main themes discussed. For each theme:
   - Provide a descriptive title
   - Explain the theme in detail (2-3 paragraphs)
   - Include relevant timestamps [HH:MM:SS]
   - Extract 1-2 key quotes with timestamps

3. **Key Takeaways**: List 5-10 actionable insights or important points that listeners should remember.

4. **Notable Quotes**: Extract 5-8 particularly insightful or memorable quotes with:
   - The exact quote
   - Timestamp [HH:MM:SS]
   - Brief context (1 sentence)

5. **Topics by Timestamp**: Create a timeline of major topics discussed with timestamps.

QUALITY GUIDELINES:
- Prioritize DEPTH over brevity
- Include specific details, examples, and explanations
- Preserve the nuance and context of discussions
- Use clear, accessible language
- Organize information logically
- Reference timestamps frequently for key points

OUTPUT FORMAT (Markdown):

# [Podcast Title or Main Topic]

## Metadata
- URL: {url}
- Duration: {duration}
- Processed: [Current Date]

## Overview
[2-3 sentence summary]

## Main Themes

### Theme 1: [Title]
[Detailed explanation with context]

Key insights:
- [Insight 1]
- [Insight 2]

Notable quote: "[Quote]" ([HH:MM:SS])

[Continue for all themes...]

## Key Takeaways
1. [Actionable takeaway 1]
2. [Actionable takeaway 2]
[...]

## Notable Quotes
- "[Quote 1]" ([HH:MM:SS]) - [Context]
- "[Quote 2]" ([HH:MM:SS]) - [Context]
[...]

## Topics by Timestamp
- [00:00:00] - [Topic]
- [00:15:30] - [Topic]
[...]

Now, create the comprehensive summary:
```

**File: `podchat/templates/prompts/chat_prompt.txt`**

```
You are an expert at extracting and structuring knowledge from podcast transcripts for use in interactive chat environments.

Your task is to analyze the following podcast transcript and create a chat-optimized knowledge context that can be loaded into a coding assistant or chat environment.

TRANSCRIPT:
{transcript}

VIDEO METADATA:
- Video ID: {video_id}
- URL: {url}
- Duration: {duration}
- Word Count: {word_count}

REQUIREMENTS:

Your output should enable someone to:
1. Ask questions about the podcast content
2. Apply the speaker's expertise to their own projects
3. Reference specific frameworks, methodologies, or concepts discussed
4. Understand the speaker's perspective and reasoning

Create a structured knowledge document that includes:

1. **Expertise Summary**: What is the speaker's main area of expertise? What unique perspective do they bring?

2. **Key Concepts & Frameworks**: List and explain the main concepts, frameworks, methodologies, or mental models discussed.

3. **Practical Guidance**: Extract actionable advice, best practices, and practical tips.

4. **Examples & Case Studies**: Summarize any specific examples, stories, or case studies mentioned.

5. **Speaker's Perspective**: Capture the speaker's philosophy, values, and approach to their domain.

6. **Quick Reference**: Create a condensed reference of key terms, concepts, and their definitions.

OUTPUT FORMAT (Markdown optimized for chat loading):

# [Podcast Title] - Expert Knowledge Context

## Source Information
- URL: {url}
- Duration: {duration}
- Processed: [Current Date]

## How to Use This Context
Load this document into your chat assistant to:
- Ask questions about the concepts discussed
- Apply the expertise to your specific projects
- Reference frameworks and methodologies
- Get advice based on the speaker's perspective

---

## Expertise Summary
[2-3 paragraphs describing the speaker's expertise and unique perspective]

## Key Concepts & Frameworks

### Concept 1: [Name]
**Definition**: [Clear explanation]
**Application**: [How to apply this]
**Timestamp**: [HH:MM:SS]

[Continue for all major concepts...]

## Practical Guidance

### On [Topic Area]:
- [Specific advice 1]
- [Specific advice 2]
- [Best practice]

[Continue for major topic areas...]

## Examples & Case Studies

**Example 1**: [Title]
- **Context**: [What it illustrates]
- **Details**: [Summary of the example]
- **Takeaway**: [What to learn from it]

[Continue for notable examples...]

## Speaker's Philosophy & Approach
[Detailed explanation of the speaker's perspective, values, and methodology]

## Quick Reference

**Key Terms**:
- **[Term 1]**: [Definition]
- **[Term 2]**: [Definition]

**Frameworks**: [List]

**Best Practices**: [List]

---

## Example Questions You Can Ask
- [Example question 1]
- [Example question 2]
- [Example question 3]

Now, create the chat-optimized knowledge context:
```

#### 3.5 Implement LLM Processor ✓

**File: `podchat/core/llm_processor.py`**

```python
"""LLM processing logic."""
from pathlib import Path
from typing import Dict

from ..integrations.llm import create_llm_client
from ..models.config import Config
from ..models.transcript import Transcript
from ..utils.logger import get_logger
from ..utils.exceptions import LLMAPIError, TokenLimitError


class LLMProcessor:
    """Handles all LLM interactions."""
    
    def __init__(self, config: Config):
        self.config = config
        self.client = create_llm_client(config)
        self.logger = get_logger(__name__)
        self.template_dir = Path(__file__).parent.parent / "templates" / "prompts"
    
    def process(self, transcript: Transcript, mode: str = "summary") -> str:
        """
        Process transcript through LLM.
        
        Args:
            transcript: Transcript object
            mode: "summary" or "chat"
            
        Returns:
            Generated content as string
        """
        # Check token limit
        estimated_tokens = self.client.count_tokens(transcript.full_text)
        max_tokens = self.client.get_max_tokens()
        
        if estimated_tokens > max_tokens * 0.8:  # 80% threshold
            self.logger.warning(
                f"Transcript is large ({estimated_tokens} tokens). "
                f"This may take longer to process."
            )
        
        # Build prompt
        prompt = self._build_prompt(transcript, mode)
        
        # Call LLM
        try:
            self.logger.info(f"Processing with LLM (mode: {mode})")
            response = self.client.generate(
                prompt,
                max_tokens=self.config.llm_max_tokens,
                temperature=self.config.llm_temperature
            )
            return response
        except Exception as e:
            raise LLMAPIError(f"LLM processing failed: {e}")
    
    def _build_prompt(self, transcript: Transcript, mode: str) -> str:
        """Build prompt from template and transcript."""
        # Load template
        template_file = self.template_dir / f"{mode}_prompt.txt"
        if not template_file.exists():
            raise ValueError(f"Template not found: {template_file}")
        
        template = template_file.read_text()
        
        # Format transcript with timestamps
        transcript_text = transcript.get_text_with_timestamps()
        
        # Format duration
        duration_seconds = transcript.metadata.duration or 0
        hours = int(duration_seconds // 3600)
        minutes = int((duration_seconds % 3600) // 60)
        seconds = int(duration_seconds % 60)
        duration_str = f"{hours:02d}:{minutes:02d}:{seconds:02d}"
        
        # Fill template
        prompt = template.format(
            transcript=transcript_text,
            video_id=transcript.metadata.video_id,
            url=transcript.metadata.url,
            duration=duration_str,
            word_count=transcript.word_count
        )
        
        return prompt
```

### Acceptance Criteria

- ✅ OpenRouter client successfully connects
- ✅ Prompt templates created for both modes
- ✅ LLM processor builds prompts correctly
- ✅ Token counting works
- ✅ Error handling for API failures

### Testing

```python
# Test LLM client
from podchat.models.config import Config
from podchat.integrations.llm import create_llm_client

config = Config(llm_api_key="your-test-key")
client = create_llm_client(config)

# Test token counting
text = "This is a test"
tokens = client.count_tokens(text)
print(f"Estimated tokens: {tokens}")
```

---

## Phase 4: Summary Generation

**Estimated Time:** 10 minutes  
**Priority:** P0 (Must Have)  
**Dependencies:** Phases 2, 3

### Tasks

#### 4.1 Implement Output Formatter ✓

**File: `podchat/core/output_formatter.py`**

```python
"""Output formatting logic."""
from datetime import datetime
from pathlib import Path

from ..models.transcript import Transcript
from ..utils.file_manager import FileManager
from ..utils.logger import get_logger


class OutputFormatter:
    """Formats LLM responses into structured output."""
    
    def __init__(self, output_directory: str = "./summaries"):
        self.file_manager = FileManager(output_directory)
        self.logger = get_logger(__name__)
    
    def format_and_save(
        self,
        llm_response: str,
        transcript: Transcript,
        mode: str = "summary",
        custom_output: str = None
    ) -> Path:
        """
        Format response and save to file.
        
        Args:
            llm_response: Raw LLM output
            transcript: Original transcript
            mode: "summary" or "chat"
            custom_output: Optional custom output path
            
        Returns:
            Path to saved file
        """
        # The LLM response should already be well-formatted markdown
        # We just need to ensure it's saved properly
        
        formatted_content = llm_response.strip()
        
        # Save to file
        if custom_output:
            output_path = Path(custom_output)
            output_path.parent.mkdir(parents=True, exist_ok=True)
            output_path.write_text(formatted_content, encoding="utf-8")
        else:
            output_path = self.file_manager.write_output(
                content=formatted_content,
                video_id=transcript.metadata.video_id,
                mode=mode
            )
        
        self.logger.info(f"Output saved to: {output_path}")
        return output_path
```

#### 4.2 Implement Main Processor (Orchestrator) ✓

**File: `podchat/core/processor.py`**

```python
"""Main processing orchestrator."""
import time
from pathlib import Path
from typing import Optional

from ..models.config import Config
from ..models.transcript import Transcript
from .extractor import TranscriptExtractor
from .llm_processor import LLMProcessor
from .output_formatter import OutputFormatter
from ..utils.logger import get_logger


class PodcastProcessor:
    """Orchestrates the entire processing pipeline."""
    
    def __init__(self, config: Config):
        self.config = config
        self.extractor = TranscriptExtractor()
        self.llm_processor = LLMProcessor(config)
        self.output_formatter = OutputFormatter(config.output_directory)
        self.logger = get_logger(__name__)
    
    def process(
        self,
        url: str,
        mode: str = "summary",
        output_path: Optional[str] = None
    ) -> dict:
        """
        Main processing pipeline.
        
        Args:
            url: YouTube video URL
            mode: "summary" or "chat"
            output_path: Optional custom output path
            
        Returns:
            Dict with results and metadata
        """
        start_time = time.time()
        
        try:
            # Step 1: Extract transcript
            self.logger.info("Step 1/3: Extracting transcript...")
            transcript = self.extractor.extract(url)
            
            if self.config.verbose:
                print(f"✓ Transcript extracted: {transcript.word_count} words")
            
            # Step 2: Process with LLM
            self.logger.info(f"Step 2/3: Processing with LLM ({mode} mode)...")
            llm_response = self.llm_processor.process(transcript, mode)
            
            if self.config.verbose:
                print(f"✓ LLM processing complete")
            
            # Step 3: Format and save output
            self.logger.info("Step 3/3: Formatting and saving output...")
            output_file = self.output_formatter.format_and_save(
                llm_response=llm_response,
                transcript=transcript,
                mode=mode,
                custom_output=output_path
            )
            
            processing_time = time.time() - start_time
            
            result = {
                "status": "success",
                "output_path": str(output_file),
                "video_id": transcript.metadata.video_id,
                "video_url": transcript.metadata.url,
                "word_count": transcript.word_count,
                "processing_time": processing_time,
                "mode": mode
            }
            
            self.logger.info(
                f"Processing complete in {processing_time:.2f}s"
            )
            
            return result
            
        except Exception as e:
            self.logger.error(f"Processing failed: {e}")
            raise
```

### Acceptance Criteria

- ✅ End-to-end pipeline works (URL → Summary file)
- ✅ Summary output is properly formatted markdown
- ✅ File saved to correct location
- ✅ Processing statistics returned
- ✅ Errors handled and logged

### Testing

#### Quick Manual Test

```python
# Test end-to-end summary generation
from podchat.models.config import Config
from podchat.utils.config import ConfigManager
from podchat.core.processor import PodcastProcessor

config = ConfigManager.load()
processor = PodcastProcessor(config)

result = processor.process(
    url="https://www.youtube.com/watch?v=VALID_VIDEO_ID",
    mode="summary"
)

print(f"✓ Summary saved to: {result['output_path']}")
print(f"✓ Processing time: {result['processing_time']:.2f}s")
```

#### 4.3 Comprehensive Phase 4 Test Suite ✓

**IMPLEMENTED:** Two comprehensive test files created to validate Phase 4.

**Test Files:**

1. **`tests/test_phase4_summary_generation.py`** - Full integration test suite
   - Import validation
   - Configuration loading
   - Component instantiation  
   - Pipeline structure verification
   - Error handling (invalid URLs, missing transcripts)
   - URL parsing (multiple formats)
   - End-to-end processing with real video
   - Quality validation (10+ checks)
   - Generates JSON test report

2. **`tests/test_phase4_quick.py`** - Quick smoke test
   - Minimal setup for rapid validation
   - Simple pass/fail result
   - Quick quality checks
   - Good for CI/CD

3. **`tests/README_PHASE4_TESTS.md`** - Testing documentation
   - Complete usage guide
   - Prerequisites and setup
   - Recommended test videos
   - Troubleshooting guide
   - Success criteria

**Running Tests:**

```bash
# Quick smoke test (recommended first)
python tests/test_phase4_quick.py "https://youtube.com/watch?v=SHORT_VIDEO"

# Comprehensive test suite (structural tests only)
python tests/test_phase4_summary_generation.py

# Comprehensive test with video (full end-to-end)
python tests/test_phase4_summary_generation.py "https://youtube.com/watch?v=VIDEO_ID"
```

**Test Coverage:**

✅ **Import Tests** - All Phase 4 modules load correctly  
✅ **Configuration Tests** - Config loading and API key validation  
✅ **Component Tests** - OutputFormatter, PodcastProcessor instantiation  
✅ **Pipeline Structure** - Method signatures and architecture  
✅ **Error Handling** - Invalid URLs, missing transcripts, exceptions  
✅ **URL Parsing** - Standard, shortened, embedded YouTube formats  
✅ **End-to-End** - Complete pipeline from URL to summary file  
✅ **Quality Validation** - 10 checks including:
   - Markdown formatting
   - Metadata presence
   - Content sections (themes, quotes, takeaways)
   - Timestamps
   - Sufficient length
   - Not truncated

**Output:**

Tests generate:
- Console output with pass/fail status
- `test_summaries/test_results.json` - Detailed JSON report
- `test_summaries/podcast-summary-*.md` - Generated summaries
- Quality validation metrics

**Success Criteria:**

- All imports pass
- Configuration loads successfully
- Components instantiate without errors
- Pipeline structure validated
- Error handling works correctly
- End-to-end processing completes (with valid API key)
- Summary file created
- Quality validation passes (8/10 minimum checks)

**Note for Phase 7:** These tests cover Phases 0-4 integration. Phase 7 testing should:
- Reference these existing tests (avoid duplication)
- Add tests for Phases 5-6 (Chat Mode, CLI)
- Add cross-phase integration tests
- Add performance benchmarks
- Add stress tests with multiple video lengths

---

## Phase 5: Chat Mode

**Estimated Time:** 5 minutes  
**Priority:** P1 (Should Have)  
**Dependencies:** Phase 4

### Tasks

#### 5.1 Verify Chat Mode Works ✓

The chat mode should already work with the existing infrastructure. Just need to test it.

```python
# Test chat mode
result = processor.process(
    url="https://www.youtube.com/watch?v=VALID_VIDEO_ID",
    mode="chat"
)

print(f"✓ Chat context saved to: {result['output_path']}")
```

#### 5.2 Create Example Chat Context ✓

Generate a sample chat context file and save it to `examples/sample_summaries/` for documentation purposes.

### Acceptance Criteria

- ✅ Chat mode generates knowledge context
- ✅ Output is optimized for chat loading
- ✅ Includes practical examples and quick reference
- ✅ Example chat context in repository

---

## Phase 6: CLI Enhancement

**Estimated Time:** 10 minutes  
**Priority:** P0 (Must Have)  
**Dependencies:** Phases 4, 5

### Tasks

#### 6.1 Implement CLI Commands ✓

**File: `podchat/cli/commands.py`**

```python
"""CLI command definitions."""
import click
from pathlib import Path

from ..core.processor import PodcastProcessor
from ..utils.config import ConfigManager
from ..utils.logger import setup_logger
from ..utils.exceptions import PodChatError


@click.group()
@click.version_option(version="1.0.0")
def cli():
    """PodChat - Transform YouTube podcasts into actionable knowledge."""
    pass


@cli.command()
@click.argument('url')
@click.option(
    '--output', '-o',
    help='Output file path',
    type=click.Path()
)
@click.option(
    '--verbose', '-v',
    is_flag=True,
    help='Enable verbose output'
)
def summarize(url: str, output: str, verbose: bool):
    """Generate a comprehensive summary of a podcast."""
    try:
        # Load configuration
        config = ConfigManager.load()
        config.verbose = verbose
        
        # Setup logger
        setup_logger(level=config.log_level if not verbose else "DEBUG")
        
        # Display header
        click.echo("🎙️  PodChat - YouTube Podcast Summarizer")
        click.echo("━" * 40)
        click.echo()
        
        # Process
        click.echo("📥 Fetching transcript...")
        processor = PodcastProcessor(config)
        
        result = processor.process(
            url=url,
            mode="summary",
            output_path=output
        )
        
        # Display results
        click.echo()
        click.echo("✅ Summary generated successfully!")
        click.echo()
        click.echo(f"📝 Output: {result['output_path']}")
        click.echo(f"📊 Stats:")
        click.echo(f"   - Words: {result['word_count']:,}")
        click.echo(f"   - Time: {result['processing_time']:.2f}s")
        click.echo()
        click.echo("✨ Done! Your podcast summary is ready.")
        
    except PodChatError as e:
        click.echo(f"❌ Error: {e}", err=True)
        raise click.Abort()
    except Exception as e:
        click.echo(f"❌ Unexpected error: {e}", err=True)
        raise click.Abort()


@cli.command()
@click.argument('url')
@click.option(
    '--output', '-o',
    help='Output file path',
    type=click.Path()
)
@click.option(
    '--verbose', '-v',
    is_flag=True,
    help='Enable verbose output'
)
def chat(url: str, output: str, verbose: bool):
    """Generate chat-ready knowledge context from a podcast."""
    try:
        # Load configuration
        config = ConfigManager.load()
        config.verbose = verbose
        
        # Setup logger
        setup_logger(level=config.log_level if not verbose else "DEBUG")
        
        # Display header
        click.echo("🎙️  PodChat - Chat Context Generator")
        click.echo("━" * 40)
        click.echo()
        
        # Process
        click.echo("📥 Fetching transcript...")
        processor = PodcastProcessor(config)
        
        result = processor.process(
            url=url,
            mode="chat",
            output_path=output
        )
        
        # Display results
        click.echo()
        click.echo("✅ Chat context generated successfully!")
        click.echo()
        click.echo(f"📝 Output: {result['output_path']}")
        click.echo(f"📊 Stats:")
        click.echo(f"   - Words: {result['word_count']:,}")
        click.echo(f"   - Time: {result['processing_time']:.2f}s")
        click.echo()
        click.echo("💡 Tip: Load this file into your chat assistant (Claude, Cursor, etc.)")
        click.echo("   to ask questions and apply the expertise to your projects.")
        
    except PodChatError as e:
        click.echo(f"❌ Error: {e}", err=True)
        raise click.Abort()
    except Exception as e:
        click.echo(f"❌ Unexpected error: {e}", err=True)
        raise click.Abort()


@cli.command()
def config():
    """Show current configuration."""
    try:
        cfg = ConfigManager.load()
        
        click.echo("⚙️  PodChat Configuration")
        click.echo("━" * 40)
        click.echo()
        click.echo("LLM Settings:")
        click.echo(f"  Provider: {cfg.llm_provider}")
        click.echo(f"  Model: {cfg.llm_model}")
        click.echo(f"  Base URL: {cfg.llm_base_url}")
        click.echo(f"  Max Tokens: {cfg.llm_max_tokens}")
        click.echo()
        click.echo("Output Settings:")
        click.echo(f"  Directory: {cfg.output_directory}")
        click.echo()
        click.echo("Processing Settings:")
        click.echo(f"  Max Retries: {cfg.max_retries}")
        click.echo(f"  Timeout: {cfg.timeout}s")
        
    except Exception as e:
        click.echo(f"❌ Error loading config: {e}", err=True)
        raise click.Abort()


if __name__ == '__main__':
    cli()
```

#### 6.2 Create Main Entry Point ✓

**File: `podchat/__main__.py`**

```python
"""Main entry point for PodChat CLI."""
from .cli.commands import cli


def main():
    """Main entry point."""
    cli()


if __name__ == '__main__':
    main()
```

#### 6.3 Update Package Init ✓

**File: `podchat/__init__.py`**

```python
"""PodChat - Transform YouTube podcasts into actionable knowledge."""

__version__ = "1.0.0"
__author__ = "Your Name"
__email__ = "your.email@example.com"

from .core.processor import PodcastProcessor
from .models.config import Config

__all__ = ['PodcastProcessor', 'Config']
```

### Acceptance Criteria

- ✅ CLI commands work: `podchat summarize`, `podchat chat`
- ✅ Help messages are clear and informative
- ✅ Progress indicators show user what's happening
- ✅ Success messages include useful statistics
- ✅ Error messages are actionable
- ✅ Package installable with `pip install -e .`

### Testing

```bash
# Install package in development mode
pip install -e .

# Test commands
podchat --help
podchat summarize --help
podchat chat --help
podchat config

# Test actual processing
podchat summarize https://www.youtube.com/watch?v=VALID_VIDEO_ID
```

---

## Phase 7: Testing & Documentation

**Estimated Time:** 10 minutes  
**Priority:** P0 (Must Have)  
**Dependencies:** All previous phases

**Note:** Phase 4 tests already implemented (see Phase 4.3 above). This phase focuses on:
- README and documentation
- Example summaries
- Additional integration tests (Phases 5-6)
- Final validation

### Tasks

#### 7.1 Create README ✓

**File: `README.md`**

```markdown
# PodChat

Transform YouTube podcasts into actionable knowledge with AI.

## Overview

PodChat is a command-line tool that extracts transcripts from YouTube podcasts and uses Claude Sonnet 4.5 (via OpenRouter) to generate:

- **Comprehensive Summaries**: Detailed markdown summaries that capture key insights, quotes, and takeaways
- **Chat-Ready Contexts**: Knowledge contexts you can load into AI assistants for Q&A and project application

## Features

- ✅ Extract transcripts from any YouTube video
- ✅ Generate in-depth summaries with timestamps
- ✅ Create chat-optimized knowledge contexts
- ✅ Support for podcasts of any length
- ✅ Beautiful, structured markdown output
- ✅ Simple CLI interface

## Installation

### Prerequisites

- Python 3.9 or higher
- OpenRouter API key ([Get one here](https://openrouter.ai/))

### Install

```bash
# Clone the repository
git clone https://github.com/yourusername/podchat.git
cd podchat

# Install dependencies
pip install -r requirements.txt

# Install package
pip install -e .
```

### Configuration

Create a `.env` file in the project root:

```bash
cp .env.example .env
```

Edit `.env` and add your OpenRouter API key:

```
OPENROUTER_API_KEY=sk-or-v1-your-api-key-here
```

## Usage

### Generate a Summary

```bash
podchat summarize https://www.youtube.com/watch?v=VIDEO_ID
```

This creates a comprehensive markdown summary in the `./summaries/` directory.

### Generate Chat Context

```bash
podchat chat https://www.youtube.com/watch?v=VIDEO_ID
```

This creates a chat-optimized knowledge context you can load into Claude, Cursor, or other AI assistants.

### Options

```bash
# Custom output location
podchat summarize https://... --output ./my-summaries/podcast.md

# Verbose output
podchat summarize https://... --verbose

# Show current configuration
podchat config

# Show help
podchat --help
podchat summarize --help
```

## Examples

See the `examples/sample_summaries/` directory for example outputs.

## How It Works

1. **Extract**: Fetches the transcript from YouTube
2. **Process**: Sends transcript to Claude Sonnet 4.5 via OpenRouter
3. **Format**: Generates structured markdown output
4. **Save**: Writes to file with metadata and statistics

## Architecture

PodChat uses a modular architecture with clear separation of concerns:

- **CLI Layer**: Command parsing and user interaction
- **Core Layer**: Processing orchestration and business logic
- **Integration Layer**: YouTube and LLM API clients
- **Model Layer**: Data structures and configuration

See [ARCHITECTURE.md](docs/ARCHITECTURE.md) for detailed design documentation.

## Development

### Setup Development Environment

```bash
# Install development dependencies
pip install -r requirements.txt
pip install -e ".[dev]"

# Run tests
pytest

# Format code
black podchat/

# Lint
flake8 podchat/
```

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

## Configuration

Configure via environment variables in `.env`:

```bash
# Required
OPENROUTER_API_KEY=sk-or-v1-...

# Optional
LLM_PROVIDER=openrouter
LLM_MODEL=anthropic/claude-sonnet-4.5
LLM_BASE_URL=https://openrouter.ai/api/v1
OUTPUT_DIRECTORY=./summaries
LOG_LEVEL=INFO
```

## Troubleshooting

### Transcript Not Available

If you get a "transcript not available" error:
- Ensure the video has captions enabled
- Check if the video is public and accessible
- Try a different video

### API Key Issues

- Ensure your `.env` file exists and contains the API key
- Verify your API key is valid at [OpenRouter](https://openrouter.ai/)
- Check that the key starts with `sk-or-v1-`

### Rate Limits

If you hit rate limits:
- Wait a few moments and try again
- Check your OpenRouter account for usage limits

## Cost Estimates

Using Claude Sonnet 4.5 via OpenRouter:
- ~$0.10-0.50 per 1-hour podcast (varies by length and detail)
- Check current pricing at [OpenRouter](https://openrouter.ai/models)

## Roadmap

Future enhancements (post-MVP):
- Batch processing multiple URLs
- Summary caching to avoid re-processing
- Additional output formats (PDF, HTML)
- Custom summary templates
- Multi-language support
- Web interface

## Contributing

Contributions welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## License

MIT License - see LICENSE file for details

## Acknowledgments

- Built with [Claude Sonnet 4.5](https://www.anthropic.com/claude) via [OpenRouter](https://openrouter.ai/)
- Uses [youtube-transcript-api](https://github.com/jdepoix/youtube-transcript-api)
- CLI powered by [Click](https://click.palletsprojects.com/)

## Support

- Documentation: [docs/](docs/)
- Issues: [GitHub Issues](https://github.com/yourusername/podchat/issues)

---

Made with ❤️ using agentic coding tools
```

#### 7.2 Create Example Summaries ✓

Generate 2-3 example summaries from real podcasts and save them to `examples/sample_summaries/` directory.

#### 7.3 Phase 0-4 Tests (Already Implemented) ✓

**NOTE:** Comprehensive tests for Phases 0-4 have already been implemented in Phase 4.3.

**Existing Test Files:**
- `tests/test_phase4_summary_generation.py` - Full integration test suite
- `tests/test_phase4_quick.py` - Quick smoke test
- `tests/README_PHASE4_TESTS.md` - Complete testing guide

**Coverage:**
- ✅ Import validation
- ✅ Configuration loading
- ✅ Component instantiation
- ✅ Pipeline structure
- ✅ Error handling (invalid URLs, missing transcripts)
- ✅ URL parsing (multiple formats)
- ✅ End-to-end processing
- ✅ Quality validation

**To run existing tests:**
```bash
# Quick test
python tests/test_phase4_quick.py "https://youtube.com/watch?v=VIDEO_ID"

# Full test suite
python tests/test_phase4_summary_generation.py "https://youtube.com/watch?v=VIDEO_ID"
```

#### 7.4 Additional Unit Tests (Phase 7 Specific)

**File: `tests/unit/test_url_validation.py`** - Pytest format for CI/CD

```python
"""Test URL validation with pytest."""
import pytest
from podchat.integrations.youtube_client import YouTubeClient
from podchat.utils.exceptions import InvalidURLError


def test_valid_youtube_urls():
    """Test valid YouTube URL formats."""
    client = YouTubeClient()
    
    test_cases = [
        ("https://www.youtube.com/watch?v=dQw4w9WgXcQ", "dQw4w9WgXcQ"),
        ("https://youtu.be/dQw4w9WgXcQ", "dQw4w9WgXcQ"),
        ("https://www.youtube.com/embed/dQw4w9WgXcQ", "dQw4w9WgXcQ"),
    ]
    
    for url, expected_id in test_cases:
        video_id = client.extract_video_id(url)
        assert video_id == expected_id


def test_invalid_youtube_urls():
    """Test invalid YouTube URLs."""
    client = YouTubeClient()
    
    invalid_urls = [
        "https://www.example.com/watch?v=123",
        "not a url",
        "https://vimeo.com/123456",
    ]
    
    for url in invalid_urls:
        with pytest.raises(InvalidURLError):
            client.extract_video_id(url)
```

#### 7.5 CLI Integration Tests (Phase 7 Specific)

**Note:** End-to-end tests for core pipeline already exist (Phase 4.3).
These tests focus on CLI-specific functionality (Phase 6).

**File: `tests/integration/test_cli.py`**

```python
"""CLI integration tests."""
import pytest
from click.testing import CliRunner
from podchat.cli.commands import cli


def test_cli_help():
    """Test CLI help command."""
    runner = CliRunner()
    result = runner.invoke(cli, ['--help'])
    assert result.exit_code == 0
    assert 'PodChat' in result.output


def test_summarize_help():
    """Test summarize command help."""
    runner = CliRunner()
    result = runner.invoke(cli, ['summarize', '--help'])
    assert result.exit_code == 0
    assert 'summary' in result.output.lower()


def test_config_command():
    """Test config command."""
    runner = CliRunner()
    result = runner.invoke(cli, ['config'])
    # May succeed or fail depending on .env, but shouldn't crash
    assert result.exit_code in [0, 1]
```

#### 7.6 Legacy End-to-End Test ✓

**File: `tests/integration/test_end_to_end.py`**

```python
"""End-to-end integration test."""
import pytest
import os
from pathlib import Path
from podchat.core.processor import PodcastProcessor
from podchat.models.config import Config


@pytest.mark.skipif(
    not os.getenv("OPENROUTER_API_KEY"),
    reason="Requires OPENROUTER_API_KEY"
)
def test_end_to_end_summary(tmp_path):
    """Test complete summary generation."""
    # Use a short, known video with transcript
    test_url = "https://www.youtube.com/watch?v=SHORT_VIDEO_WITH_TRANSCRIPT"
    
    config = Config(
        llm_api_key=os.getenv("OPENROUTER_API_KEY"),
        output_directory=str(tmp_path)
    )
    
    processor = PodcastProcessor(config)
    result = processor.process(test_url, mode="summary")
    
    assert result["status"] == "success"
    assert Path(result["output_path"]).exists()
    assert result["word_count"] > 0
```

### Acceptance Criteria

- ✅ README is comprehensive and includes all necessary info
- ✅ Example summaries demonstrate output quality
- ✅ Basic unit tests pass
- ✅ Integration test works (when API key available)
- ✅ All documentation is up-to-date

---

## Implementation Checklist

Use this checklist to track your progress:

### Phase 0: Project Setup
- [ ] Directory structure created
- [ ] Configuration files (.gitignore, .env.example, requirements.txt, pyproject.toml)
- [ ] Git repository initialized
- [ ] Dependencies installable

### Phase 1: Core Infrastructure
- [ ] Exception hierarchy implemented
- [ ] Data models (Transcript, Config) created
- [ ] Configuration manager working
- [ ] Logger configured
- [ ] File manager implemented

### Phase 2: Transcript Extraction
- [ ] YouTube client with URL parsing
- [ ] Transcript extractor implemented
- [ ] Error handling for unavailable transcripts
- [ ] Tested with real YouTube URLs

### Phase 3: LLM Integration
- [ ] Base LLM client interface defined
- [ ] OpenRouter client implemented
- [ ] Prompt templates created (summary and chat)
- [ ] LLM processor implemented
- [ ] Tested API connection

### Phase 4: Summary Generation
- [x] Output formatter implemented
- [x] Main processor (orchestrator) implemented
- [x] End-to-end summary generation working
- [x] Output files properly formatted
- [x] Comprehensive test suite created (test_phase4_summary_generation.py)
- [x] Quick smoke test created (test_phase4_quick.py)
- [x] Testing documentation created (README_PHASE4_TESTS.md)

### Phase 5: Chat Mode
- [ ] Chat mode tested and working
- [ ] Example chat context generated

### Phase 6: CLI Enhancement
- [ ] CLI commands implemented (summarize, chat, config)
- [ ] Main entry point created
- [ ] Package installable with pip
- [ ] Help messages clear and useful
- [ ] Error messages actionable

### Phase 7: Testing & Documentation
- [ ] README completed
- [ ] Example summaries added
- [ ] Unit tests created
- [ ] Integration test created
- [ ] All documentation current

### Final Steps
- [ ] Full manual test of both modes
- [ ] Verify .env.example is correct
- [ ] Clean up any temporary files
- [ ] Commit all changes
- [ ] Tag release v1.0.0

---

## 12. Code Examples

### Running the Full Pipeline

```python
from podchat.core.processor import PodcastProcessor
from podchat.utils.config import ConfigManager

# Load configuration
config = ConfigManager.load()

# Create processor
processor = PodcastProcessor(config)

# Process podcast
result = processor.process(
    url="https://www.youtube.com/watch?v=VIDEO_ID",
    mode="summary"
)

print(f"Summary saved to: {result['output_path']}")
```

### Using Individual Components

```python
# Extract transcript only
from podchat.core.extractor import TranscriptExtractor

extractor = TranscriptExtractor()
transcript = extractor.extract("https://youtube.com/...")
print(f"Extracted {transcript.word_count} words")

# Process with LLM
from podchat.core.llm_processor import LLMProcessor
from podchat.utils.config import ConfigManager

config = ConfigManager.load()
llm_processor = LLMProcessor(config)
summary = llm_processor.process(transcript, mode="summary")
```

---

## 13. Testing Strategy

### Unit Tests

Focus areas:
- URL validation and parsing
- Data model functionality
- Configuration loading
- File operations
- Error handling

### Integration Tests

Test complete flows:
- URL → Transcript extraction
- Transcript → LLM processing
- LLM response → File output
- End-to-end: URL → Summary file

### Manual Testing

Test with various podcasts:
- Short (< 30 min)
- Medium (30-90 min)
- Long (2+ hours)
- Different topics (technical, business, narrative)

### Edge Cases

- Videos without transcripts
- Private/unavailable videos
- Very long transcripts (token limits)
- Network errors
- API rate limits

---

## 14. Deployment & Delivery

### For MVP Submission

**Required Deliverables:**

1. **GitHub Repository**
   - All code committed
   - Clean commit history
   - Tagged release v1.0.0

2. **Chat History**
   - Export complete development chat history
   - Save as `DEVELOPMENT_CHAT_HISTORY.txt`
   - Include in repository or separate file

3. **Documentation**
   - README.md with installation and usage
   - ARCHITECTURE.md (complete)
   - IMPLEMENTATION_PLAN.md (this document)
   - Example summaries

4. **Working Demo**
   - Ability to run `podchat summarize <url>` live
   - At least 2 example summaries in repo

### Installation Test

Before submission, test installation from scratch:

```bash
# Fresh clone
git clone <your-repo-url>
cd podchat

# Create virtual environment
python -m venv venv
source venv/bin/activate  # or `venv\Scripts\activate` on Windows

# Install
pip install -r requirements.txt
pip install -e .

# Configure
cp .env.example .env
# Edit .env with API key

# Test
podchat summarize https://www.youtube.com/watch?v=TEST_VIDEO_ID
```

### Success Criteria Checklist

Before declaring MVP complete, verify:

- ✅ Can process YouTube URL to summary in < 3 minutes
- ✅ Summary quality is comprehensive (depth over brevity)
- ✅ Chat mode works and produces usable context
- ✅ Error messages are clear and actionable
- ✅ README has all necessary information
- ✅ Code is clean and well-organized
- ✅ Example summaries demonstrate value
- ✅ Can be installed and run by another developer

---

## Appendix A: Quick Start Commands

```bash
# Setup
mkdir podchat && cd podchat
python -m venv venv
source venv/bin/activate
pip install click youtube-transcript-api openai python-dotenv

# Create .env
echo "OPENROUTER_API_KEY=your-key-here" > .env

# Run
podchat summarize https://www.youtube.com/watch?v=VIDEO_ID
```

## Appendix B: Troubleshooting Guide

| Issue | Solution |
|-------|----------|
| Import errors | Ensure `pip install -e .` was run |
| API key not found | Check `.env` file exists and has correct key |
| Transcript unavailable | Try different video with captions |
| Slow processing | Normal for long podcasts, be patient |
| Rate limit errors | Wait 60s and retry |

## Appendix C: Time Tracking

Log your actual time spent on each phase for learning:

| Phase | Estimated | Actual | Notes |
|-------|-----------|--------|-------|
| 0 | 5 min | | |
| 1 | 5 min | | |
| 2 | 10 min | | |
| 3 | 15 min | | |
| 4 | 10 min | | |
| 5 | 5 min | | |
| 6 | 10 min | | |
| 7 | 10 min | | |
| **Total** | **70 min** | | |

---

**Document Version:**
- v1.0 (2026-01-29): Initial implementation plan

**Next Steps:**
1. Begin Phase 0: Project Setup
2. Work through phases sequentially
3. Test after each phase
4. Document any deviations or improvements
5. Commit after each phase completion

Good luck with your implementation! 🚀
