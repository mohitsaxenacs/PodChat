"""CLI command definitions."""
import click
from pathlib import Path

from ..core.processor import PodcastProcessor
from ..utils.config import ConfigManager
from ..utils.logger import setup_logger
from ..utils.exceptions import PodChatError


@click.group()
@click.version_option(version="1.0.0")
def cli():
    """PodChat - Transform YouTube podcasts into actionable knowledge."""
    pass


@cli.command()
@click.argument('url')
@click.option(
    '--output', '-o',
    help='Output file path',
    type=click.Path()
)
@click.option(
    '--verbose', '-v',
    is_flag=True,
    help='Enable verbose output'
)
def summarize(url: str, output: str, verbose: bool):
    """Generate a comprehensive summary of a podcast.
    
    Examples:
        podchat summarize "https://www.youtube.com/watch?v=VIDEO_ID"
        podchat summarize URL -o my_summary.md
        podchat summarize URL --verbose
    """
    try:
        # Load configuration
        config = ConfigManager.load()
        config.verbose = verbose
        
        # Setup logger
        setup_logger(level=config.log_level if not verbose else "DEBUG")
        
        # Display header
        click.echo("🎙️  PodChat - YouTube Podcast Summarizer")
        click.echo("━" * 40)
        click.echo()
        
        # Process
        click.echo("📥 Fetching transcript...")
        processor = PodcastProcessor(config)
        
        result = processor.process(
            url=url,
            mode="summary",
            output_path=output
        )
        
        # Display results
        click.echo()
        click.echo("✅ Summary generated successfully!")
        click.echo()
        click.echo(f"📝 Output: {result['output_path']}")
        click.echo(f"📊 Stats:")
        click.echo(f"   - Words: {result['word_count']:,}")
        click.echo(f"   - Time: {result['processing_time']:.2f}s")
        click.echo()
        click.echo("✨ Done! Your podcast summary is ready.")
        
    except PodChatError as e:
        click.echo(f"❌ Error: {e}", err=True)
        raise click.Abort()
    except Exception as e:
        click.echo(f"❌ Unexpected error: {e}", err=True)
        raise click.Abort()


@cli.command()
@click.argument('url')
@click.option(
    '--output', '-o',
    help='Output file path',
    type=click.Path()
)
@click.option(
    '--verbose', '-v',
    is_flag=True,
    help='Enable verbose output'
)
def chat(url: str, output: str, verbose: bool):
    """Generate chat-ready knowledge context from a podcast.
    
    Examples:
        podchat chat "https://www.youtube.com/watch?v=VIDEO_ID"
        podchat chat URL -o my_context.md
        podchat chat URL --verbose
    """
    try:
        # Load configuration
        config = ConfigManager.load()
        config.verbose = verbose
        
        # Setup logger
        setup_logger(level=config.log_level if not verbose else "DEBUG")
        
        # Display header
        click.echo("🎙️  PodChat - Chat Context Generator")
        click.echo("━" * 40)
        click.echo()
        
        # Process
        click.echo("📥 Fetching transcript...")
        processor = PodcastProcessor(config)
        
        result = processor.process(
            url=url,
            mode="chat",
            output_path=output
        )
        
        # Display results
        click.echo()
        click.echo("✅ Chat context generated successfully!")
        click.echo()
        click.echo(f"📝 Output: {result['output_path']}")
        click.echo(f"📊 Stats:")
        click.echo(f"   - Words: {result['word_count']:,}")
        click.echo(f"   - Time: {result['processing_time']:.2f}s")
        click.echo()
        click.echo("💡 Tip: Load this file into your chat assistant (Claude, Cursor, etc.)")
        click.echo("   to ask questions and apply the expertise to your projects.")
        
    except PodChatError as e:
        click.echo(f"❌ Error: {e}", err=True)
        raise click.Abort()
    except Exception as e:
        click.echo(f"❌ Unexpected error: {e}", err=True)
        raise click.Abort()


@cli.command()
def config():
    """Show current configuration.
    
    Displays the current PodChat configuration including LLM settings,
    output directory, and processing parameters.
    """
    try:
        cfg = ConfigManager.load()
        
        click.echo("⚙️  PodChat Configuration")
        click.echo("━" * 40)
        click.echo()
        click.echo("LLM Settings:")
        click.echo(f"  Provider: {cfg.llm_provider}")
        click.echo(f"  Model: {cfg.llm_model}")
        click.echo(f"  Base URL: {cfg.llm_base_url}")
        click.echo(f"  Max Tokens: {cfg.llm_max_tokens}")
        click.echo()
        click.echo("Output Settings:")
        click.echo(f"  Directory: {cfg.output_directory}")
        click.echo()
        click.echo("Processing Settings:")
        click.echo(f"  Max Retries: {cfg.max_retries}")
        click.echo(f"  Timeout: {cfg.timeout}s")
        
    except Exception as e:
        click.echo(f"❌ Error loading config: {e}", err=True)
        raise click.Abort()


if __name__ == '__main__':
    cli()
