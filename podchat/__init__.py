"""PodChat - Transform YouTube podcasts into actionable knowledge."""

__version__ = "1.0.0"
__author__ = "Your Name"
__email__ = "your.email@example.com"

from .core.processor import PodcastProcessor
from .models.config import Config

__all__ = ['PodcastProcessor', 'Config']
