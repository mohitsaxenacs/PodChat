"""Test URL validation with pytest."""
import pytest
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from podchat.integrations.youtube_client import YouTubeClient
from podchat.utils.exceptions import InvalidURLError


def test_valid_youtube_urls():
    """Test valid YouTube URL formats."""
    client = YouTubeClient()
    
    test_cases = [
        ("https://www.youtube.com/watch?v=dQw4w9WgXcQ", "dQw4w9WgXcQ"),
        ("https://youtube.com/watch?v=dQw4w9WgXcQ", "dQw4w9WgXcQ"),
        ("https://youtu.be/dQw4w9WgXcQ", "dQw4w9WgXcQ"),
        ("https://www.youtube.com/watch?v=dQw4w9WgXcQ&feature=share", "dQw4w9WgXcQ"),
        ("https://m.youtube.com/watch?v=dQw4w9WgXcQ", "dQw4w9WgXcQ"),
    ]
    
    for url, expected_id in test_cases:
        video_id = client.extract_video_id(url)
        assert video_id == expected_id, f"Failed for URL: {url}"


def test_invalid_youtube_urls():
    """Test invalid YouTube URLs raise appropriate errors."""
    client = YouTubeClient()
    
    invalid_urls = [
        "https://www.google.com",
        "https://vimeo.com/123456",
        "not-a-url",
        "https://youtube.com/channel/UC123",
        "",
    ]
    
    for url in invalid_urls:
        with pytest.raises(InvalidURLError):
            client.extract_video_id(url)


def test_video_id_edge_cases():
    """Test edge cases in video ID extraction."""
    client = YouTubeClient()
    
    # Video ID with special characters (YouTube IDs are alphanumeric with - and _)
    video_id = client.extract_video_id("https://www.youtube.com/watch?v=dQw4w9WgXcQ")
    assert len(video_id) == 11
    assert video_id.isalnum() or all(c in "-_" for c in video_id if not c.isalnum())


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
