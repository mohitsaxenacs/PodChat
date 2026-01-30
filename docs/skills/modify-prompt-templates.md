# Skill: Modifying Prompt Templates in PodChat

## Purpose
Guide for safely modifying and testing prompt templates for summary or chat generation.

## Template Locations
- Summary: `podchat/templates/prompts/summary_prompt.txt`
- Chat Context: `podchat/templates/prompts/chat_prompt.txt`

## Best Practices for Prompt Engineering

### 1. Understand Current Structure
Read the existing prompt carefully:
- What sections does it ask for?
- What formatting instructions are included?
- What examples or constraints are specified?

### 2. Make Incremental Changes
- **Don't rewrite entirely** - make targeted improvements
- Change one thing at a time for easier testing
- Keep successful elements from previous versions

### 3. Test Systematically
Use a standardized test set:
```bash
# Short technical podcast (~10 min)
python -m podchat summarize "https://youtube.com/watch?v=SHORT_VIDEO" --verbose

# Medium business podcast (~30 min)
python -m podchat summarize "https://youtube.com/watch?v=MEDIUM_VIDEO" --verbose

# Long interview podcast (1+ hour)
python -m podchat summarize "https://youtube.com/watch?v=LONG_VIDEO" --verbose
```

### 4. Evaluate Output Quality
Check for:
- **Structure**: Proper markdown formatting, clear sections
- **Completeness**: All main themes covered
- **Accuracy**: Quotes and facts match transcript
- **Timestamps**: Correctly formatted and clickable
- **Actionability**: Takeaways are practical
- **Readability**: Clear, concise, well-organized

## Common Prompt Modifications

### Adding a New Section
Example: Adding "Speaker Background" section

1. Add to prompt template:
```markdown
## Speaker Background
Briefly describe the speaker's expertise, background, and credibility. Why should we trust their insights?
```

2. Test with multiple videos to ensure consistency

3. Update example outputs in `examples/sample_outputs/`

### Changing Output Format
Example: Changing timestamp format from [00:15:30] to clickable links

Modify formatting instruction:
```
For all timestamps, use format: [HH:MM:SS](video_url&t=XXs)
```

**Note**: Some formatting happens in `output_formatter.py`, not the prompt.

### Adjusting Depth/Brevity
- For more detail: Add "Provide comprehensive analysis" and increase max_tokens
- For less detail: Add "Be concise" and decrease max_tokens

### Improving Quote Extraction
```
Extract key quotes verbatim from the transcript. Each quote should:
- Be 1-3 sentences maximum
- Include speaker attribution (if available)
- Include timestamp reference
- Capture pivotal insights or memorable statements
```

## Template Variable Substitution
Templates use Python string formatting:
```python
# In the code
prompt = template.format(
    transcript=transcript_text,
    video_title=title,
    duration=duration
)
```

Available variables depend on which template:
- Check `podchat/core/llm_processor.py` for what's passed in
- Add new variables by modifying the processing code

## Version Control for Prompts
Create dated backups when making significant changes:
```bash
cp podchat/templates/prompts/summary_prompt.txt \
   podchat/templates/prompts/summary_prompt_v2_2026-01-31.txt
```

## A/B Testing Prompts
Compare two prompt versions:

1. Run same video with prompt A
2. Save output as `output_A.md`
3. Modify prompt to version B
4. Run same video with prompt B
5. Save output as `output_B.md`
6. Compare quality

## Troubleshooting Prompt Issues

### Issue: Output Too Brief
**Solution**: 
- Add "Provide comprehensive detail"
- Increase max_tokens in LLM call
- Add "elaborate on each point" instructions

### Issue: Inconsistent Structure
**Solution**:
- Use more explicit markdown formatting instructions
- Provide clearer section headers in prompt
- Add example output format in prompt

### Issue: Missing Timestamps
**Solution**:
- Emphasize timestamp importance in prompt
- Specify exact format: [HH:MM:SS]
- Check if `output_formatter.py` is processing them correctly

### Issue: Hallucinated Content
**Solution**:
- Add "Only use information from the transcript"
- Add "Do not invent quotes or facts"
- Lower temperature (try 0.3-0.5 instead of 0.7)

## Testing Checklist
- [ ] Output maintains proper markdown formatting
- [ ] All required sections are present
- [ ] Timestamps are formatted correctly
- [ ] Quotes are accurate (spot-check against transcript)
- [ ] Length is appropriate (not too brief, not excessive)
- [ ] Actionable takeaways are included
- [ ] Works with both short and long videos
- [ ] Works with different podcast styles (interview, lecture, discussion)

## Example Outputs
Always compare your modifications against examples:
- `examples/sample_outputs/cursor_20_tips_hacks_for_ai_assisted_development_e_chat.md`
- `examples/sample_summaries/cursor_20_tips_and_hacks_advanced_development_work_summary.md`

## References
- Template loading: `podchat/templates/prompts/`
- LLM processing: `podchat/core/llm_processor.py`
- Output formatting: `podchat/core/output_formatter.py`
- Example outputs: `examples/`
