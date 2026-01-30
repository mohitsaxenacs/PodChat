# Skill: Debugging Transcript Extraction Issues

## Purpose
Systematic approach to diagnosing and fixing YouTube transcript extraction problems.

## Common Issues & Solutions

### Issue 1: "Transcript Not Available"

#### Possible Causes:
1. **Video has no captions**: Not all videos have transcripts
2. **Wrong video ID extraction**: URL parsing failed
3. **Private/restricted video**: Not publicly accessible
4. **Age-restricted content**: Requires authentication

#### Debugging Steps:
```python
# Test URL parsing
from podchat.integrations.youtube_client import extract_video_id

url = "YOUR_TEST_URL"
try:
    video_id = extract_video_id(url)
    print(f"✓ Extracted video ID: {video_id}")
except Exception as e:
    print(f"✗ URL parsing failed: {e}")

# Test transcript availability
from youtube_transcript_api import YouTubeTranscriptApi

try:
    transcript = YouTubeTranscriptApi.get_transcript(video_id)
    print(f"✓ Transcript available: {len(transcript)} entries")
except Exception as e:
    print(f"✗ Transcript error: {e}")
    
    # Try listing available transcripts
    try:
        available = YouTubeTranscriptApi.list_transcripts(video_id)
        print(f"Available languages: {[t.language_code for t in available]}")
    except:
        print("No transcripts available at all")
```

#### Solutions:
1. **User error**: Provide clear error message suggesting to check if video has captions
2. **URL parsing**: Add support for new URL format if pattern not recognized
3. **Language support**: Add language selection if video has non-English transcripts

### Issue 2: Malformed Transcript Data

#### Symptoms:
- Empty text fields
- Missing timestamps
- Garbled characters

#### Debugging:
```python
# Inspect transcript structure
transcript = YouTubeTranscriptApi.get_transcript(video_id)
print("First 3 entries:")
for entry in transcript[:3]:
    print(f"  Text: {entry.get('text', 'MISSING')}")
    print(f"  Start: {entry.get('start', 'MISSING')}")
    print(f"  Duration: {entry.get('duration', 'MISSING')}")
    print()
```

#### Solutions:
1. **Encoding issues**: Ensure proper UTF-8 handling
2. **Data validation**: Add checks in `extractor.py` before processing
3. **Fallback**: Try different transcript languages if available

### Issue 3: Incomplete Transcripts

#### Symptoms:
- Transcript ends abruptly
- Missing sections of video

#### Possible Causes:
1. Auto-generated captions incomplete
2. Live stream or premiere video (transcripts added later)
3. API rate limiting

#### Solutions:
1. **Validate duration**: Compare transcript end time with video duration
2. **Retry logic**: Wait and retry for recent videos
3. **Warning to user**: Inform if transcript seems incomplete

### Issue 4: URL Format Not Recognized

#### Test Various Formats:
```python
test_urls = [
    "https://www.youtube.com/watch?v=VIDEO_ID",
    "https://youtu.be/VIDEO_ID",
    "https://www.youtube.com/watch?v=VIDEO_ID&t=123s",
    "https://www.youtube.com/embed/VIDEO_ID",
    "https://m.youtube.com/watch?v=VIDEO_ID",
]

for url in test_urls:
    try:
        video_id = extract_video_id(url)
        print(f"✓ {url[:40]}... → {video_id}")
    except:
        print(f"✗ {url[:40]}... → FAILED")
```

#### Add Missing Patterns:
Location: `podchat/integrations/youtube_client.py`

```python
def extract_video_id(url: str) -> str:
    patterns = [
        r'youtube\.com/watch\?v=([^&]+)',
        r'youtu\.be/([^?]+)',
        r'youtube\.com/embed/([^?]+)',
        r'm\.youtube\.com/watch\?v=([^&]+)',  # Add mobile
        # Add more patterns as needed
    ]
    # ... matching logic
```

## Testing Workflow

### Step 1: Isolate the Issue
```bash
# Test with known-good video
python -m podchat summarize "https://youtube.com/watch?v=dQw4w9WgXcQ" --verbose

# Test with problematic video
python -m podchat summarize "PROBLEM_URL" --verbose
```

### Step 2: Check Logs
- Look for error messages in console output
- Check `--verbose` output for detailed info
- Review any exception tracebacks

### Step 3: Manual Verification
1. Open video in browser
2. Check if captions/subtitles are available
3. Try playing video to ensure it's accessible
4. Check video age (very new videos may not have transcripts yet)

### Step 4: Unit Test
Create minimal reproduction:
```python
# tests/test_transcript_debug.py
from podchat.integrations.youtube_client import extract_video_id
from youtube_transcript_api import YouTubeTranscriptApi

def test_specific_video():
    url = "PROBLEM_URL"
    video_id = extract_video_id(url)
    transcript = YouTubeTranscriptApi.get_transcript(video_id)
    assert len(transcript) > 0
    assert all('text' in entry for entry in transcript)
```

## Error Messages to Users

### Good Error Messages:
```python
✗ No transcript available for this video.
  
  Possible reasons:
  - Video doesn't have captions/subtitles enabled
  - Video is private or restricted
  - Video is too new (transcripts added after processing)
  
  Try:
  - Check if captions are available on YouTube
  - Try a different video
```

### Bad Error Messages:
```python
✗ Error: TranscriptsDisabled
```

## Code Locations
- URL parsing: `podchat/integrations/youtube_client.py`
- Transcript extraction: `podchat/core/extractor.py`
- Error handling: `podchat/cli/commands.py`
- Custom exceptions: `podchat/utils/exceptions.py`

## Prevention
Add validation in `extractor.py`:
```python
def validate_transcript(transcript: List[Dict]) -> bool:
    """Validate transcript structure and completeness."""
    if not transcript:
        return False
    
    # Check required fields
    required_fields = {'text', 'start', 'duration'}
    if not all(required_fields.issubset(entry.keys()) for entry in transcript):
        return False
    
    # Check for reasonable content
    total_text = ' '.join(entry['text'] for entry in transcript)
    if len(total_text) < 100:  # Suspiciously short
        return False
    
    return True
```

## Quick Reference Commands

```bash
# Test URL extraction only
python -c "from podchat.integrations.youtube_client import extract_video_id; print(extract_video_id('YOUR_URL'))"

# Test transcript API directly
python -c "from youtube_transcript_api import YouTubeTranscriptApi; t = YouTubeTranscriptApi.get_transcript('VIDEO_ID'); print(f'{len(t)} entries')"

# Full verbose run
python -m podchat summarize "URL" --verbose

# Check available transcripts
python -c "from youtube_transcript_api import YouTubeTranscriptApi; print(YouTubeTranscriptApi.list_transcripts('VIDEO_ID'))"
```

## Related Files
- `podchat/integrations/youtube_client.py` - URL parsing and video ID extraction
- `podchat/core/extractor.py` - Main transcript extraction logic
- `tests/unit/test_url_validation.py` - URL validation tests
- `podchat/utils/exceptions.py` - Custom exception definitions
