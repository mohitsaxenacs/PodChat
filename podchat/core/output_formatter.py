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
