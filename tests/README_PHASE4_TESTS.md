# Phase 4 Testing Guide

This directory contains tests for validating Phase 4 (Summary Generation) implementation.

## Test Files

### 1. `test_phase4_summary_generation.py` (Comprehensive)

Full integration test suite covering:
- Import validation
- Configuration loading
- Component instantiation
- Pipeline structure verification
- Error handling
- End-to-end processing with real video
- Quality validation of generated summaries

**Usage:**
```bash
# Structural tests only (no API calls)
python tests/test_phase4_summary_generation.py

# Full end-to-end test with a video
python tests/test_phase4_summary_generation.py <youtube_url>
```

**Example:**
```bash
python tests/test_phase4_summary_generation.py "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
```

**Output:**
- Console output with test results
- `test_summaries/test_results.json` - Detailed results in JSON format
- `test_summaries/podcast-summary-*.md` - Generated summary (if end-to-end test runs)

### 2. `test_phase4_quick.py` (Smoke Test)

Quick validation for rapid iteration:
- Minimal setup
- Fast execution
- Simple pass/fail result
- Good for CI/CD or quick checks

**Usage:**
```bash
python tests/test_phase4_quick.py <youtube_url>
```

**Example:**
```bash
python tests/test_phase4_quick.py "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
```

## Prerequisites

### Required
1. **API Key**: Set `OPENROUTER_API_KEY` in `.env` file
2. **Dependencies**: `pip install -r requirements.txt`
3. **Test Video**: YouTube URL with available transcript

### Recommended Test Videos

**Short (2-5 min) - Quick validation:**
- TED-Ed videos
- Khan Academy shorts
- Any short educational video with captions

**Medium (30-60 min) - Typical podcast:**
- Software Engineering Daily episodes
- NPR podcasts
- YouTube interviews

**Long (1.5-3 hours) - Stress test:**
- Lex Fridman Podcast
- Joe Rogan Experience
- Tim Ferriss Show

## Running Tests

### Quick Test (Recommended First)

```bash
# 1. Ensure .env is configured
cat .env | grep OPENROUTER_API_KEY

# 2. Run quick test with a short video
python tests/test_phase4_quick.py "https://youtube.com/watch?v=SHORT_VIDEO"

# 3. Check output
ls -lh test_summaries/
```

### Comprehensive Test

```bash
# 1. Run structural tests first (no API calls)
python tests/test_phase4_summary_generation.py

# 2. Run full test with video
python tests/test_phase4_summary_generation.py "https://youtube.com/watch?v=VIDEO_ID"

# 3. Review results
cat test_summaries/test_results.json
```

## Test Coverage

### What's Tested ✅

- **Imports**: All Phase 4 modules load correctly
- **Configuration**: Config loading and validation
- **Components**: OutputFormatter, PodcastProcessor instantiation
- **Pipeline**: Correct method signatures and structure
- **Error Handling**: Invalid URLs, missing transcripts
- **URL Parsing**: Multiple YouTube URL formats
- **End-to-End**: Complete pipeline from URL to summary file
- **Quality**: Summary validation (structure, content, formatting)

### What's NOT Tested (Reserved for Phase 7)

- Chat mode functionality (Phase 5)
- CLI commands (Phase 6)
- Batch processing
- Multiple video formats
- Performance benchmarks across different lengths
- Stress testing with very long transcripts

## Success Criteria

A successful test run should show:

✅ All imports pass  
✅ Configuration loads (with API key)  
✅ Components instantiate correctly  
✅ Pipeline structure is valid  
✅ Error handling works for invalid inputs  
✅ End-to-end processing completes  
✅ Summary file is created  
✅ Quality validation passes all checks  

## Troubleshooting

### "No API key configured"
- Check `.env` file exists in project root
- Verify `OPENROUTER_API_KEY` is set
- Run: `python -c "from podchat.utils.config import ConfigManager; print(ConfigManager.load().llm_api_key)"`

### "Transcript not available"
- Try a different video
- Ensure video has captions enabled
- Check video is public and accessible

### "Import errors"
- Run: `pip install -r requirements.txt`
- Ensure you're in project root directory
- Check Python version: `python --version` (need 3.9+)

### "Processing takes too long"
- Expected: 1-3 minutes for 1-hour podcast
- Check network connection
- Try shorter video first
- Verify API key has credits

## Output Files

Test outputs are saved to `test_summaries/`:

```
test_summaries/
├── test_results.json              # Detailed test results
├── podcast-summary-*.md           # Generated summaries
└── [additional test outputs]
```

## Next Steps After Testing

Once Phase 4 tests pass:

1. ✅ **Review generated summary** - Check quality manually
2. ✅ **Verify all sections present** - Themes, quotes, takeaways
3. ✅ **Check formatting** - Proper markdown structure
4. ➡️ **Proceed to Phase 5** - Chat Mode implementation
5. ➡️ **Continue to Phase 6** - CLI Enhancement

## Notes

- These tests validate Phases 0-4 working together
- Full integration tests will be in Phase 7
- Keep test videos short for quick iteration
- Save test results for documentation
- Report any failures with details from `test_results.json`
