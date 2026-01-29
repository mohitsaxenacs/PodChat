#!/usr/bin/env python3
"""
Phase 5 Test: Chat Mode Verification

This test verifies that the chat mode works correctly:
- Loads configuration
- Processes a YouTube URL in chat mode
- Generates a chat-optimized knowledge context
- Validates the output format
"""
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from podchat.core.processor import PodcastProcessor
from podchat.utils.config import ConfigManager


def test_chat_mode(video_url: str):
    """Test chat mode processing."""
    print("=" * 60)
    print("PHASE 5: CHAT MODE TEST")
    print("=" * 60)
    print()
    
    try:
        # Step 1: Load configuration
        print("1. Loading configuration...")
        config = ConfigManager.load()
        print("   ✓ Config loaded")
        print()
        
        # Step 2: Initialize processor
        print("2. Initializing processor...")
        processor = PodcastProcessor(config)
        print("   ✓ Processor ready")
        print()
        
        # Step 3: Process in chat mode
        print(f"3. Processing: {video_url}")
        print("   Mode: CHAT (knowledge context)")
        print("   Please wait (this may take 1-3 minutes)...")
        print()
        
        result = processor.process(url=video_url, mode="chat")
        
        print(f"✓ Transcript extracted: {result['word_count']} words")
        print(f"✓ Chat context generated")
        print()
        
        # Step 4: Validate output
        print("4. Validating chat context...")
        output_path = Path(result['output_path'])
        
        if not output_path.exists():
            raise FileNotFoundError(f"Output file not found: {output_path}")
        
        content = output_path.read_text()
        
        # Check for key sections in chat context
        validations = {
            "Markdown format": content.startswith("#"),
            "Has metadata": "URL:" in content or "Source Information" in content,
            "Has expertise section": "Expertise" in content or "Expert" in content,
            "Has concepts section": "Concept" in content or "Framework" in content,
            "Has practical guidance": "Practical" in content or "Guidance" in content or "Advice" in content,
            "Has quick reference": "Quick Reference" in content or "Reference" in content,
            "Has usage instructions": "How to Use" in content or "Example Questions" in content,
        }
        
        print()
        print("Validation checks:")
        for check, passed in validations.items():
            status = "✓" if passed else "✗"
            print(f"  {status} {check}")
        
        all_passed = all(validations.values())
        
        # Print results
        print()
        print("=" * 60)
        if all_passed:
            print("✅ SUCCESS!")
        else:
            print("⚠️  PARTIAL SUCCESS")
        print("=" * 60)
        print()
        print(f"Output:     {result['output_path']}")
        print(f"Video ID:   {result['video_id']}")
        print(f"Words:      {result['word_count']:,}")
        print(f"Time:       {result['processing_time']:.2f}s")
        print()
        
        if all_passed:
            print("✅ All checks passed! Phase 5 (Chat Mode) is working correctly.")
        else:
            print("⚠️  Some checks failed. Review the output file.")
        
        return result
        
    except Exception as e:
        print()
        print("=" * 60)
        print("✗ TEST FAILED")
        print("=" * 60)
        print()
        print(f"Error: {e}")
        print()
        
        # Print traceback
        import traceback
        print("Traceback:")
        traceback.print_exc()
        
        return None


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python test_phase5_chat.py <youtube_url>")
        print()
        print("Example:")
        print('  python test_phase5_chat.py "https://www.youtube.com/watch?v=MWMe7yjPYpE"')
        sys.exit(1)
    
    video_url = sys.argv[1]
    result = test_chat_mode(video_url)
    
    sys.exit(0 if result else 1)
