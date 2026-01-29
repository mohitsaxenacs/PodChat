#!/usr/bin/env python3
"""Test script to verify new output structure and filename format."""

from pathlib import Path
from podchat.core.output_formatter import OutputFormatter
from podchat.models.transcript import Transcript, TranscriptMetadata, TranscriptSegment

def test_title_extraction():
    """Test title extraction from markdown."""
    formatter = OutputFormatter()
    
    test_cases = [
        ("# My Podcast Title\n\nContent here", "My Podcast Title"),
        ("Some content\n# Another Title\nMore", "Another Title"),
        ("No title here", None),
        ("## Not a top level\nContent", None),
    ]
    
    print("Testing title extraction:")
    for content, expected in test_cases:
        result = formatter._extract_title_from_summary(content)
        status = "✓" if result == expected else "✗"
        print(f"  {status} Extract from '{content[:30]}...' -> '{result}' (expected '{expected}')")

def test_filename_sanitization():
    """Test filename sanitization."""
    formatter = OutputFormatter()
    
    test_cases = [
        ("Cursor 2.0: Expert Tips and Hacks for AI-Assisted Development", "cursor_2_0_expert_tips_and_hacks_for_ai_a"),
        ("The Path to Advanced Machine Intelligence", "the_path_to_advanced_machine_intelligenc"),
        ("Simple Title", "simple_title"),
        ("Title with lots!!! of @special #characters$$$", "title_with_lots_of_special_characters"),
        ("Multiple   Spaces   Here", "multiple_spaces_here"),
    ]
    
    print("\nTesting filename sanitization:")
    for title, expected in test_cases:
        result = formatter._sanitize_filename(title, max_length=50)
        status = "✓" if result == expected else "✗"
        print(f"  {status} '{title[:40]}...' -> '{result}'")
        if result != expected:
            print(f"      Expected: '{expected}'")

def test_output_structure():
    """Test the complete output structure with mock data."""
    print("\nTesting complete output structure:")
    
    # Create mock transcript
    segments = [
        TranscriptSegment(text="Hello world", start=0.0, duration=2.0),
        TranscriptSegment(text="This is a test", start=2.0, duration=3.0),
    ]
    
    metadata = TranscriptMetadata(
        video_id="TEST123",
        url="https://www.youtube.com/watch?v=TEST123",
        title="Test Video",
        duration=5.0
    )
    
    transcript = Transcript(segments=segments, metadata=metadata)
    
    # Create formatter
    formatter = OutputFormatter(output_directory="./test_output")
    
    # Test summary output
    summary_content = """# Test Podcast Summary

## Metadata
- URL: https://www.youtube.com/watch?v=TEST123
- Duration: 00:00:05

## Overview
This is a test summary with a timestamp [[00:00:02]].

## Key Takeaways
1. First takeaway
2. Second takeaway
"""
    
    try:
        output_path = formatter.format_and_save(
            llm_response=summary_content,
            transcript=transcript,
            mode="summary"
        )
        
        print(f"  ✓ Summary saved to: {output_path}")
        print(f"    Directory structure: {output_path.parent}")
        print(f"    Filename: {output_path.name}")
        
        # Verify structure
        expected_dir = Path("./test_output/summaries")
        if output_path.parent == expected_dir:
            print(f"  ✓ Correct directory: {expected_dir}")
        else:
            print(f"  ✗ Wrong directory: {output_path.parent} (expected {expected_dir})")
        
        # Check filename format
        if "test_podcast_summary" in output_path.name:
            print(f"  ✓ Filename uses title format")
        else:
            print(f"  ✗ Filename doesn't use title format: {output_path.name}")
        
        # Verify content
        saved_content = output_path.read_text()
        if "[[00:00:02]]" in saved_content and "youtube.com" in saved_content:
            print(f"  ✓ Timestamps are clickable")
        else:
            print(f"  ✗ Timestamps not properly converted")
        
    except Exception as e:
        print(f"  ✗ Error: {e}")
        import traceback
        traceback.print_exc()
    
    # Test chat output
    chat_content = """# Test Chat Context

## Video Information
- URL: https://www.youtube.com/watch?v=TEST123

## Content
Some chat context here.
"""
    
    try:
        output_path = formatter.format_and_save(
            llm_response=chat_content,
            transcript=transcript,
            mode="chat"
        )
        
        print(f"\n  ✓ Chat saved to: {output_path}")
        print(f"    Directory: {output_path.parent}")
        print(f"    Filename: {output_path.name}")
        
        expected_dir = Path("./test_output/chats")
        if output_path.parent == expected_dir:
            print(f"  ✓ Correct directory: {expected_dir}")
        else:
            print(f"  ✗ Wrong directory: {output_path.parent} (expected {expected_dir})")
        
        if "test_chat_context_chat" in output_path.name:
            print(f"  ✓ Filename uses title format with _chat suffix")
        else:
            print(f"  ✗ Filename doesn't use expected format: {output_path.name}")
            
    except Exception as e:
        print(f"  ✗ Error: {e}")
        import traceback
        traceback.print_exc()

def test_duplicate_handling():
    """Test duplicate filename handling."""
    print("\nTesting duplicate filename handling:")
    
    segments = [TranscriptSegment(text="Test", start=0.0, duration=1.0)]
    metadata = TranscriptMetadata(
        video_id="DUP123",
        url="https://www.youtube.com/watch?v=DUP123",
        title="Duplicate Test"
    )
    transcript = Transcript(segments=segments, metadata=metadata)
    
    formatter = OutputFormatter(output_directory="./test_output")
    
    content = """# Duplicate Test Summary

This is a test for duplicate handling.
"""
    
    try:
        # Create first file
        path1 = formatter.format_and_save(content, transcript, mode="summary")
        print(f"  ✓ First file: {path1.name}")
        
        # Create duplicate
        path2 = formatter.format_and_save(content, transcript, mode="summary")
        print(f"  ✓ Second file: {path2.name}")
        
        if path1.name != path2.name:
            print(f"  ✓ Duplicate handling works (files have different names)")
        else:
            print(f"  ✗ Duplicate handling failed (same filename)")
            
    except Exception as e:
        print(f"  ✗ Error: {e}")

def cleanup():
    """Clean up test output."""
    import shutil
    test_dir = Path("./test_output")
    if test_dir.exists():
        shutil.rmtree(test_dir)
        print("\n✓ Cleaned up test output directory")

if __name__ == "__main__":
    print("=" * 70)
    print("New Output Structure Test Suite")
    print("=" * 70)
    
    test_title_extraction()
    test_filename_sanitization()
    test_output_structure()
    test_duplicate_handling()
    
    print("\n" + "=" * 70)
    print("Tests completed!")
    print("=" * 70)
    
    cleanup()
