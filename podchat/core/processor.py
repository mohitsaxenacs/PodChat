"""Main processing orchestrator."""
import time
from pathlib import Path
from typing import Optional

from ..models.config import Config
from ..models.transcript import Transcript
from .extractor import TranscriptExtractor
from .llm_processor import LLMProcessor
from .output_formatter import OutputFormatter
from ..utils.logger import get_logger


class PodcastProcessor:
    """Orchestrates the entire processing pipeline."""
    
    def __init__(self, config: Config):
        self.config = config
        self.extractor = TranscriptExtractor()
        self.llm_processor = LLMProcessor(config)
        self.output_formatter = OutputFormatter(config.output_directory)
        self.logger = get_logger(__name__)
    
    def process(
        self,
        url: str,
        mode: str = "summary",
        output_path: Optional[str] = None
    ) -> dict:
        """
        Main processing pipeline.
        
        Args:
            url: YouTube video URL
            mode: "summary" or "chat"
            output_path: Optional custom output path
            
        Returns:
            Dict with results and metadata
        """
        start_time = time.time()
        
        try:
            # Step 1: Extract transcript
            self.logger.info("Step 1/3: Extracting transcript...")
            transcript = self.extractor.extract(url)
            
            if self.config.verbose:
                print(f"✓ Transcript extracted: {transcript.word_count} words")
            
            # Step 2: Process with LLM
            self.logger.info(f"Step 2/3: Processing with LLM ({mode} mode)...")
            llm_response = self.llm_processor.process(transcript, mode)
            
            if self.config.verbose:
                print(f"✓ LLM processing complete")
            
            # Step 3: Format and save output
            self.logger.info("Step 3/3: Formatting and saving output...")
            output_file = self.output_formatter.format_and_save(
                llm_response=llm_response,
                transcript=transcript,
                mode=mode,
                custom_output=output_path
            )
            
            processing_time = time.time() - start_time
            
            result = {
                "status": "success",
                "output_path": str(output_file),
                "video_id": transcript.metadata.video_id,
                "video_url": transcript.metadata.url,
                "word_count": transcript.word_count,
                "processing_time": processing_time,
                "mode": mode
            }
            
            self.logger.info(
                f"Processing complete in {processing_time:.2f}s"
            )
            
            return result
            
        except Exception as e:
            self.logger.error(f"Processing failed: {e}")
            raise
