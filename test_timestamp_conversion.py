#!/usr/bin/env python3
"""Test script to verify timestamp conversion functionality."""

from podchat.core.output_formatter import OutputFormatter

def test_timestamp_to_seconds():
    """Test timestamp to seconds conversion."""
    formatter = OutputFormatter()
    
    tests = [
        ("00:00:04", 4),
        ("00:01:21", 81),
        ("00:02:45", 165),
        ("00:29:07", 1747),
        ("01:00:00", 3600),
    ]
    
    print("Testing _timestamp_to_seconds():")
    all_passed = True
    for timestamp, expected in tests:
        result = formatter._timestamp_to_seconds(timestamp)
        status = "✓" if result == expected else "✗"
        print(f"  {status} {timestamp} -> {result}s (expected {expected}s)")
        if result != expected:
            all_passed = False
    
    return all_passed


def test_clickable_timestamps():
    """Test timestamp link conversion."""
    formatter = OutputFormatter()
    
    video_url = "https://www.youtube.com/watch?v=MWMe7yjPYpE"
    
    test_cases = [
        {
            "input": "[00:01:21]",
            "expected": "[[00:01:21]](https://www.youtube.com/watch?v=MWMe7yjPYpE&t=81s)"
        },
        {
            "input": "[00:00:04 - 00:02:45]",
            "expected": "[[00:00:04 - 00:02:45]](https://www.youtube.com/watch?v=MWMe7yjPYpE&t=4s)"
        },
        {
            "input": "Some text [00:16:06] more text",
            "expected": "Some text [[00:16:06]](https://www.youtube.com/watch?v=MWMe7yjPYpE&t=966s) more text"
        },
        {
            "input": "Multiple [00:01:21] timestamps [00:02:45] in text",
            "expected": "Multiple [[00:01:21]](https://www.youtube.com/watch?v=MWMe7yjPYpE&t=81s) timestamps [[00:02:45]](https://www.youtube.com/watch?v=MWMe7yjPYpE&t=165s) in text"
        }
    ]
    
    print("\nTesting _make_timestamps_clickable():")
    all_passed = True
    for i, test in enumerate(test_cases, 1):
        result = formatter._make_timestamps_clickable(test["input"], video_url)
        status = "✓" if result == test["expected"] else "✗"
        print(f"  {status} Test case {i}")
        if result != test["expected"]:
            print(f"    Input:    {test['input']}")
            print(f"    Expected: {test['expected']}")
            print(f"    Got:      {result}")
            all_passed = False
    
    return all_passed


def test_real_summary_excerpt():
    """Test with a real summary excerpt."""
    formatter = OutputFormatter()
    
    video_url = "https://www.youtube.com/watch?v=MWMe7yjPYpE"
    
    sample_content = """
### Theme 1: The Fundamental Limitations of LLMs and the Need for a Paradigm Shift

[00:00:04 - 00:02:45]

LeCun opens with a provocative assertion...

Notable quote: "We're starting to see the limits of the LLM paradigm." [00:01:21]

## Topics by Timestamp

- [00:00:04] - **Path to AGI and terminology**
- [00:01:00] - **Limits of LLM paradigm**
- [00:16:06] - **Real AI risks**
"""
    
    result = formatter._make_timestamps_clickable(sample_content, video_url)
    
    print("\nTesting with real summary excerpt:")
    
    # Check that timestamps are converted
    checks = [
        ("[[00:00:04 - 00:02:45]]" in result, "Range timestamp converted"),
        ("[[00:01:21]]" in result, "Single timestamp in quote converted"),
        ("[[00:00:04]]" in result, "Timestamp in list converted"),
        ("t=4s" in result, "Correct seconds for 00:00:04"),
        ("t=81s" in result, "Correct seconds for 00:01:21"),
        ("t=966s" in result, "Correct seconds for 00:16:06"),
        (result.count("](https://www.youtube.com") >= 5, "Multiple links created")
    ]
    
    all_passed = True
    for passed, description in checks:
        status = "✓" if passed else "✗"
        print(f"  {status} {description}")
        if not passed:
            all_passed = False
    
    if not all_passed:
        print("\n  Generated content:")
        print("  " + "\n  ".join(result.split("\n")[:10]))
    
    return all_passed


if __name__ == "__main__":
    print("=" * 60)
    print("Timestamp Conversion Test Suite")
    print("=" * 60)
    
    test1 = test_timestamp_to_seconds()
    test2 = test_clickable_timestamps()
    test3 = test_real_summary_excerpt()
    
    print("\n" + "=" * 60)
    if test1 and test2 and test3:
        print("✓ All tests passed!")
    else:
        print("✗ Some tests failed")
    print("=" * 60)
