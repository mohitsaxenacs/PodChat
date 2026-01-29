"""
Quick smoke test for Phase 4 - Summary Generation

This is a minimal test to quickly verify the pipeline works.
Use this for rapid validation during development.

Usage:
    python tests/test_phase4_quick.py <youtube_url>
"""
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from podchat.core.processor import PodcastProcessor
from podchat.utils.config import ConfigManager


def quick_test(video_url: str):
    """Run a quick end-to-end test."""
    print("=" * 60)
    print("PHASE 4 QUICK SMOKE TEST")
    print("=" * 60)
    print()
    
    try:
        # Step 1: Load config
        print("1. Loading configuration...")
        config = ConfigManager.load()
        config.verbose = True
        config.output_directory = "./test_summaries"
        print("   ✓ Config loaded")
        print()
        
        if not config.llm_api_key:
            print("   ✗ ERROR: No API key found!")
            print("   Please set OPENROUTER_API_KEY in your .env file")
            return False
        
        # Step 2: Initialize processor
        print("2. Initializing processor...")
        processor = PodcastProcessor(config)
        print("   ✓ Processor ready")
        print()
        
        # Step 3: Process video
        print(f"3. Processing: {video_url}")
        print("   Please wait (this may take 1-3 minutes)...")
        print()
        
        result = processor.process(url=video_url, mode="summary")
        
        # Step 4: Verify output
        print()
        print("=" * 60)
        print("✅ SUCCESS!")
        print("=" * 60)
        print()
        print(f"Output:     {result['output_path']}")
        print(f"Video ID:   {result['video_id']}")
        print(f"Words:      {result['word_count']:,}")
        print(f"Time:       {result['processing_time']:.2f}s")
        print()
        
        # Quick validation
        output_path = Path(result['output_path'])
        content = output_path.read_text()
        
        checks = [
            ("Markdown format", content.startswith("#")),
            ("Has metadata", "URL:" in content or "Duration:" in content),
            ("Has content", len(content) > 500),
            ("Has timestamps", "[" in content and ":" in content),
        ]
        
        print("Quick validation:")
        all_passed = True
        for check, passed in checks:
            status = "✓" if passed else "✗"
            print(f"  {status} {check}")
            if not passed:
                all_passed = False
        print()
        
        if all_passed:
            print("✅ All checks passed! Phase 4 is working correctly.")
        else:
            print("⚠️  Some checks failed. Review the output file.")
        
        return all_passed
        
    except Exception as e:
        print()
        print("=" * 60)
        print("✗ TEST FAILED")
        print("=" * 60)
        print()
        print(f"Error: {e}")
        print()
        
        import traceback
        print("Traceback:")
        traceback.print_exc()
        print()
        
        return False


def main():
    """Main entry point."""
    if len(sys.argv) < 2:
        print("Usage: python tests/test_phase4_quick.py <youtube_url>")
        print()
        print("Example:")
        print("  python tests/test_phase4_quick.py https://youtube.com/watch?v=dQw4w9WgXcQ")
        print()
        sys.exit(1)
    
    video_url = sys.argv[1]
    success = quick_test(video_url)
    
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
