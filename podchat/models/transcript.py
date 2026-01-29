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
