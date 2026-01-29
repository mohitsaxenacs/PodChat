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
