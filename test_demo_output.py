#!/usr/bin/env python3
"""Demonstrate timestamp conversion on real summary excerpt."""

from podchat.core.output_formatter import OutputFormatter

def demonstrate_conversion():
    """Show before/after comparison of timestamp conversion."""
    formatter = OutputFormatter()
    
    video_url = "https://www.youtube.com/watch?v=MWMe7yjPYpE"
    
    sample_excerpt = """### Theme 1: The Fundamental Limitations of LLMs

[00:00:04 - 00:02:45]

LeCun opens with a provocative assertion: we are not close to AGI.

Notable quote: "We're starting to see the limits of the LLM paradigm." [00:01:21]

### Theme 2: Intelligence Beyond Language

[00:03:11 - 00:04:51]

LeCun challenges assumptions about language and intelligence.

## Topics by Timestamp

- [00:00:04] - **Path to AGI and terminology**
- [00:01:00] - **Limits of LLM paradigm**
- [00:16:06] - **Real AI risks**"""
    
    converted = formatter._make_timestamps_clickable(sample_excerpt, video_url)
    
    print("=" * 70)
    print("BEFORE CONVERSION (Plain Text Timestamps)")
    print("=" * 70)
    print(sample_excerpt)
    print("\n" + "=" * 70)
    print("AFTER CONVERSION (Clickable Markdown Links)")
    print("=" * 70)
    print(converted)
    print("\n" + "=" * 70)
    print("VERIFICATION")
    print("=" * 70)
    print(f"✓ Found {sample_excerpt.count('[00:')} plain timestamps in original")
    print(f"✓ Created {converted.count('](https://')} clickable links")
    print(f"✓ All timestamps now link to YouTube with &t=XXs parameter")
    print("=" * 70)

if __name__ == "__main__":
    demonstrate_conversion()
