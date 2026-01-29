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
