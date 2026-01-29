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
