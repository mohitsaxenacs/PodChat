# Output Structure Improvements - Implementation Summary

## Changes Implemented

### 1. Directory Structure
**Before:**
```
./summaries/
  ├── podcast-summary-20260130-031322-HlG_cYRydHY.md
  ├── podcast-chat-20260130-023123-MWMe7yjPYpE.md
  └── ...
```

**After:**
```
./output/
  ├── summaries/
  │   ├── cursor_20_expert_tips_and_hacks_for_ai_assisted_de_summary.md
  │   ├── the_path_to_advanced_machine_intelligence_summary.md
  │   └── ...
  └── chats/
      ├── cursor_20_expert_tips_and_hacks_for_ai_assisted_de_chat.md
      ├── the_path_to_advanced_machine_intelligence_chat.md
      └── ...
```

### 2. Filename Format

**Before:**
- Format: `podcast-{mode}-{timestamp}-{video_id}.md`
- Example: `podcast-summary-20260130-031322-HlG_cYRydHY.md`
- Issues: Hard to identify content, timestamp-based, not human-friendly

**After:**
- Format: `{sanitized_title}_{mode}.md`
- Example: `cursor_20_expert_tips_and_hacks_for_ai_assisted_de_summary.md`
- Benefits: Easy to identify, title-based, human-readable

### 3. Title Extraction & Sanitization

**Title Extraction:**
- Extracts from first markdown `# heading` in generated content
- Fallback to video_id if no title found

**Sanitization Rules:**
- Convert to lowercase
- Replace spaces/dashes with underscores
- Remove special characters (keep alphanumeric and underscores)
- Truncate to 50 characters
- Remove multiple consecutive underscores

**Examples:**
- "Cursor 2.0: Expert Tips" → `cursor_20_expert_tips`
- "The Path to Advanced Machine Intelligence" → `the_path_to_advanced_machine_intelligence`
- "Title with Special!@# Characters" → `title_with_special_characters`

### 4. Duplicate Handling

When a file with the same name already exists:
- Adds date suffix: `{filename}_{YYYYMMDD}.md`
- Example: `video_title_summary.md` → `video_title_summary_20260130.md`

## Files Modified

### 1. `podchat/models/config.py`
- Changed `output_directory` default from `"./summaries"` to `"./output"`

### 2. `podchat/utils/file_manager.py`
- Updated `__init__` to use `"./output"` default
- Modified `ensure_output_directory()` to create mode-specific subdirectories
- Added `_get_unique_filename()` for duplicate handling
- Updated `generate_filename()` to accept title parameter and prioritize it
- Modified `write_output()` to accept title and use mode-specific directories

### 3. `podchat/core/output_formatter.py`
- Updated `__init__` to use `"./output"` default
- Added `_extract_title_from_summary()` to extract title from markdown
- Added `_sanitize_filename()` to clean titles for filesystem use
- Modified `format_and_save()` to extract and pass title to FileManager

## Test Results

✅ All tests passing:
- ✅ Summaries save to `./output/summaries/`
- ✅ Chats save to `./output/chats/`
- ✅ Filenames use sanitized video titles
- ✅ Filenames include `_summary` or `_chat` suffix
- ✅ Long titles truncate to 50 characters
- ✅ Special characters removed from filenames
- ✅ Duplicate files get timestamp suffix
- ✅ Fallback to video_id if title extraction fails
- ✅ Custom output paths still work
- ✅ Clickable timestamps feature remains functional

## Backward Compatibility

- Old `./summaries/` directory remains untouched
- New generations use `./output/summaries/` and `./output/chats/`
- If title extraction fails, falls back to video_id-based naming
- Custom output paths (via `-o` flag) continue to work

## Usage Examples

### Generate Summary (default location)
```bash
podchat summarize "https://www.youtube.com/watch?v=VIDEO_ID"
# Saves to: ./output/summaries/video_title_summary.md
```

### Generate Chat Context (default location)
```bash
podchat chat "https://www.youtube.com/watch?v=VIDEO_ID"
# Saves to: ./output/chats/video_title_chat.md
```

### Custom Output Location (still supported)
```bash
podchat summarize URL -o my_custom_path/summary.md
# Saves to: my_custom_path/summary.md
```

## Migration Notes

No migration needed! The implementation:
- Creates new directory structure automatically
- Leaves existing files untouched
- Works alongside old files
- Gradually transitions to new format as you generate new content

---

**Implementation Date:** 2026-01-30
**Status:** ✅ Complete and Tested
