"""LLM processing logic."""
from pathlib import Path
from typing import Dict

from ..integrations.llm import create_llm_client
from ..models.config import Config
from ..models.transcript import Transcript
from ..utils.logger import get_logger
from ..utils.exceptions import LLMAPIError, TokenLimitError


class LLMProcessor:
    """Handles all LLM interactions."""
    
    def __init__(self, config: Config):
        self.config = config
        self.client = create_llm_client(config)
        self.logger = get_logger(__name__)
        self.template_dir = Path(__file__).parent.parent / "templates" / "prompts"
    
    def process(self, transcript: Transcript, mode: str = "summary") -> str:
        """
        Process transcript through LLM.
        
        Args:
            transcript: Transcript object
            mode: "summary" or "chat"
            
        Returns:
            Generated content as string
        """
        # Check token limit
        estimated_tokens = self.client.count_tokens(transcript.full_text)
        max_tokens = self.client.get_max_tokens()
        
        if estimated_tokens > max_tokens * 0.8:  # 80% threshold
            self.logger.warning(
                f"Transcript is large ({estimated_tokens} tokens). "
                f"This may take longer to process."
            )
        
        # Build prompt
        prompt = self._build_prompt(transcript, mode)
        
        # Call LLM
        try:
            self.logger.info(f"Processing with LLM (mode: {mode})")
            response = self.client.generate(
                prompt,
                max_tokens=self.config.llm_max_tokens,
                temperature=self.config.llm_temperature
            )
            return response
        except Exception as e:
            raise LLMAPIError(f"LLM processing failed: {e}")
    
    def _build_prompt(self, transcript: Transcript, mode: str) -> str:
        """Build prompt from template and transcript."""
        # Load template
        template_file = self.template_dir / f"{mode}_prompt.txt"
        if not template_file.exists():
            raise ValueError(f"Template not found: {template_file}")
        
        template = template_file.read_text()
        
        # Format transcript with timestamps
        transcript_text = transcript.get_text_with_timestamps()
        
        # Format duration
        duration_seconds = transcript.metadata.duration or 0
        hours = int(duration_seconds // 3600)
        minutes = int((duration_seconds % 3600) // 60)
        seconds = int(duration_seconds % 60)
        duration_str = f"{hours:02d}:{minutes:02d}:{seconds:02d}"
        
        # Fill template
        prompt = template.format(
            transcript=transcript_text,
            video_id=transcript.metadata.video_id,
            url=transcript.metadata.url,
            duration=duration_str,
            word_count=transcript.word_count
        )
        
        return prompt
