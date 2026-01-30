# YouTube Transcript API Patterns

## Basic Transcript Extraction
```python
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api._errors import TranscriptsDisabled, NoTranscriptFound

# Extract video ID from URL
video_id = extract_video_id(url)

# Get transcript
try:
    transcript = YouTubeTranscriptApi.get_transcript(video_id)
    # transcript is list of dicts: [{'text': '...', 'start': 0.0, 'duration': 2.5}, ...]
except TranscriptsDisabled:
    # No transcripts available
    pass
except NoTranscriptFound:
    # Specific language not found
    pass
```

## Working with Transcript Data
```python
# Combine all text
full_text = ' '.join([entry['text'] for entry in transcript])

# Get duration
total_duration = transcript[-1]['start'] + transcript[-1]['duration']

# Format timestamp for display
def format_timestamp(seconds):
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    if hours > 0:
        return f"{hours:02d}:{minutes:02d}:{secs:02d}"
    return f"{minutes:02d}:{secs:02d}"
```

## Creating YouTube Links with Timestamps
```python
def create_youtube_link(video_id, timestamp_seconds):
    return f"https://www.youtube.com/watch?v={video_id}&t={int(timestamp_seconds)}s"
```

## URL Parsing
```python
import re

def extract_video_id(url):
    """Extract video ID from various YouTube URL formats."""
    patterns = [
        r'youtube\.com/watch\?v=([^&]+)',
        r'youtu\.be/([^?]+)',
        r'youtube\.com/embed/([^?]+)',
    ]
    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)
    raise ValueError("Invalid YouTube URL")
```

## Best Practices
1. Always validate URL format before attempting extraction
2. Provide clear error messages when transcripts unavailable
3. Preserve timestamp information for creating clickable links
4. Handle both manual and auto-generated transcripts
5. Format timestamps consistently (HH:MM:SS or MM:SS)
