"""File management utilities."""
from pathlib import Path
from typing import Optional
from datetime import datetime

from .exceptions import FileWriteError


class FileManager:
    """Handles file I/O operations."""
    
    def __init__(self, output_directory: str = "./output"):
        self.output_directory = Path(output_directory)
    
    def ensure_output_directory(self, mode: str = "summary") -> Path:
        """
        Create output directory if it doesn't exist.
        
        Args:
            mode: Output mode ("summary" or "chat")
            
        Returns:
            Path to the mode-specific directory
        """
        # Determine subdirectory based on mode
        if mode == "chat":
            subdir = self.output_directory / "chats"
        else:
            subdir = self.output_directory / "summaries"
        
        subdir.mkdir(parents=True, exist_ok=True)
        return subdir
    
    def _get_unique_filename(self, base_filename: str, extension: str, output_dir: Path) -> str:
        """
        Generate unique filename, adding timestamp if file exists.
        
        Args:
            base_filename: Base filename without extension
            extension: File extension (without dot)
            output_dir: Directory where file will be saved
            
        Returns:
            Unique filename with extension
            
        Example:
            video_title_summary.md -> video_title_summary_20260130.md
        """
        filepath = output_dir / f"{base_filename}.{extension}"
        if not filepath.exists():
            return f"{base_filename}.{extension}"
        
        # Add date suffix
        date_str = datetime.now().strftime("%Y%m%d")
        return f"{base_filename}_{date_str}.{extension}"
    
    def generate_filename(
        self,
        title: Optional[str] = None,
        video_id: Optional[str] = None,
        mode: str = "summary",
        extension: str = "md"
    ) -> str:
        """
        Generate filename for output.
        
        Args:
            title: Sanitized title (primary)
            video_id: Video ID (fallback)
            mode: Output mode ("summary" or "chat")
            extension: File extension (default "md")
            
        Returns:
            Filename with extension
        """
        # Use title if available, otherwise fall back to video_id
        if title:
            base = f"{title}_{mode}"
        elif video_id:
            date_str = datetime.now().strftime("%Y%m%d-%H%M%S")
            base = f"podcast-{mode}-{date_str}-{video_id}"
        else:
            date_str = datetime.now().strftime("%Y%m%d-%H%M%S")
            base = f"untitled_{mode}_{date_str}"
        
        return f"{base}.{extension}"
    
    def write_output(
        self,
        content: str,
        filename: Optional[str] = None,
        video_id: Optional[str] = None,
        title: Optional[str] = None,
        mode: str = "summary"
    ) -> Path:
        """
        Write content to file.
        
        Args:
            content: Content to write
            filename: Custom filename (if provided, ignores title/video_id)
            video_id: Video ID (fallback if no title)
            title: Sanitized title (preferred for filename)
            mode: Output mode ("summary" or "chat")
            
        Returns:
            Path to saved file
        """
        try:
            # Ensure mode-specific directory exists
            output_dir = self.ensure_output_directory(mode)
            
            if filename is None:
                # Generate filename based on title or video_id
                if title is None and video_id is None:
                    raise ValueError("Either filename, title, or video_id must be provided")
                
                # Generate base filename
                base_filename = self.generate_filename(
                    title=title,
                    video_id=video_id,
                    mode=mode,
                    extension=""
                ).rstrip('.')
                
                # Get unique filename (adds timestamp if exists)
                filename = self._get_unique_filename(base_filename, "md", output_dir)
            
            output_path = output_dir / filename
            output_path.write_text(content, encoding="utf-8")
            
            return output_path
        except Exception as e:
            raise FileWriteError(f"Failed to write output file: {e}")
