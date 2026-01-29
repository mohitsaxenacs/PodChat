"""Output formatting logic."""
import re
from datetime import datetime
from pathlib import Path

from ..models.transcript import Transcript
from ..utils.file_manager import FileManager
from ..utils.logger import get_logger


class OutputFormatter:
    """Formats LLM responses into structured output."""
    
    def __init__(self, output_directory: str = "./output"):
        self.file_manager = FileManager(output_directory)
        self.logger = get_logger(__name__)
    
    def _timestamp_to_seconds(self, timestamp: str) -> int:
        """
        Convert HH:MM:SS timestamp to total seconds.
        
        Args:
            timestamp: Timestamp string in format HH:MM:SS
            
        Returns:
            Total seconds as integer
        """
        parts = timestamp.strip().split(':')
        if len(parts) != 3:
            return 0
        
        try:
            hours = int(parts[0])
            minutes = int(parts[1])
            seconds = int(parts[2])
            return hours * 3600 + minutes * 60 + seconds
        except (ValueError, IndexError):
            return 0
    
    def _make_timestamps_clickable(self, content: str, video_url: str) -> str:
        """
        Convert timestamp text to clickable YouTube links.
        
        Matches patterns like [HH:MM:SS] or [HH:MM:SS - HH:MM:SS] and converts
        them to markdown links that navigate to the video at that timestamp.
        
        Args:
            content: Markdown content with timestamps
            video_url: YouTube video URL
            
        Returns:
            Content with timestamps converted to clickable links
        """
        # Pattern to match [HH:MM:SS] or [HH:MM:SS - HH:MM:SS]
        pattern = r'\[(\d{2}:\d{2}:\d{2}(?:\s*-\s*\d{2}:\d{2}:\d{2})?)\]'
        
        def replace_timestamp(match):
            timestamp_text = match.group(1)
            
            # For ranges, use the start time
            if ' - ' in timestamp_text:
                start_time = timestamp_text.split(' - ')[0].strip()
            else:
                start_time = timestamp_text
            
            # Convert to seconds
            seconds = self._timestamp_to_seconds(start_time)
            
            # Build YouTube deep link
            if '?' in video_url:
                deep_link = f"{video_url}&t={seconds}s"
            else:
                deep_link = f"{video_url}?t={seconds}s"
            
            # Return as markdown link with original timestamp text
            return f"[[{timestamp_text}]]({deep_link})"
        
        return re.sub(pattern, replace_timestamp, content)
    
    def _extract_title_from_summary(self, content: str) -> str:
        """
        Extract title from markdown content (first # heading).
        
        Args:
            content: Markdown content
            
        Returns:
            Extracted title or None if not found
        """
        lines = content.strip().split('\n')
        for line in lines:
            if line.startswith('# '):
                return line[2:].strip()
        return None
    
    def _sanitize_filename(self, title: str, max_length: int = 50) -> str:
        """
        Sanitize title for use as filename.
        
        Args:
            title: Title to sanitize
            max_length: Maximum length for filename (default 50)
            
        Returns:
            Sanitized filename string
        """
        # Convert to lowercase
        filename = title.lower()
        
        # Replace spaces and dashes with underscores
        filename = re.sub(r'[\s\-]+', '_', filename)
        
        # Remove special characters (keep alphanumeric and underscores)
        filename = re.sub(r'[^a-z0-9_]', '', filename)
        
        # Remove multiple consecutive underscores
        filename = re.sub(r'_+', '_', filename)
        
        # Truncate to max length
        if len(filename) > max_length:
            filename = filename[:max_length]
        
        # Remove leading/trailing underscores
        filename = filename.strip('_')
        
        return filename or "untitled"
    
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
        
        # Convert timestamps to clickable links
        formatted_content = self._make_timestamps_clickable(
            formatted_content,
            transcript.metadata.url
        )
        
        # Extract title for filename
        title = self._extract_title_from_summary(formatted_content)
        sanitized_title = None
        if title:
            sanitized_title = self._sanitize_filename(title)
            self.logger.info(f"Extracted title: {title} -> {sanitized_title}")
        
        # Save to file
        if custom_output:
            output_path = Path(custom_output)
            output_path.parent.mkdir(parents=True, exist_ok=True)
            output_path.write_text(formatted_content, encoding="utf-8")
        else:
            output_path = self.file_manager.write_output(
                content=formatted_content,
                video_id=transcript.metadata.video_id,
                title=sanitized_title,
                mode=mode
            )
        
        self.logger.info(f"Output saved to: {output_path}")
        return output_path
