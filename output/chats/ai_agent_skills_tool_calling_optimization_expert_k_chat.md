# AI Agent Skills & Tool Calling Optimization - Expert Knowledge Context

## Source Information
- URL: https://www.youtube.com/watch?v=Hy_XOB83MQc
- Duration: 00:09:23
- Processed: 2025

## How to Use This Context
Load this document into your chat assistant to:
- Troubleshoot AI agent skill calling issues in Cursor, Claude Code, or similar tools
- Optimize agents.md files and skill configurations
- Implement research-backed techniques from Vercel to improve skill invocation rates
- Structure project documentation for better AI agent comprehension
- Apply best practices for prompt engineering and context management

---

## Expertise Summary

The speaker is an experienced AI development practitioner focused on practical implementation of AI coding assistants, particularly Cursor and Claude Code. They bring hands-on expertise in optimizing AI agent behavior through skills, rules, and context management—challenges they've been working with for approximately 18 months since cursor rules were introduced.

Their unique perspective combines real-world frustration with common AI agent limitations and solutions derived from recent Vercel research. They emphasize practical, tested approaches over theoretical concepts, focusing on measurable improvements (e.g., increasing skill calling from 50% to 80-100%). The speaker advocates for understanding fundamentals while leveraging AI tools, balancing automation with deep technical knowledge.

## Key Concepts & Frameworks

### Concept 1: Skills, Rules, and Context Equivalence
**Definition**: Skills, rules, commands, and context are fundamentally the same thing—saved prompts that get injected into the model when needed. Skills may include additional resources and examples, but regardless of marketing terminology, they're all prompts.
**Application**: Understand that different tools (Cursor, Claude Code, etc.) may use different terminology, but the underlying mechanism is identical. This helps demystify various AI coding assistant features.
**Timestamp**: 00:00:55 - 00:01:22

### Concept 2: The Skill Calling Problem
**Definition**: AI agents frequently fail to invoke available skills even when they're clearly relevant—baseline success rates are around 50-53%.
**Application**: Don't assume skills will be automatically called. Implement optimization strategies and consider manually prompting the agent to use specific skills when you know they're relevant.
**Timestamp**: 00:00:27, 00:02:26

### Concept 3: agents.md File
**Definition**: A markdown file (also called claw.md in Claude Code) that provides persistent context about your project. Created with `/init` command in Claude Code, it's always loaded into the agent's context at conversation start.
**Application**: Place in the base of your repository. Supported by Cursor, Claude Code, and Gemini. Use for project summaries and best practices, but avoid overloading it.
**Timestamp**: 00:02:51 - 00:03:18

### Concept 4: Context Window Limitations
**Definition**: Regardless of how large an agent's context window is, larger agents.md files lead to confusion and missed instructions. Bigger context doesn't solve the fundamental attention problem.
**Application**: Keep agents.md concise and strategic. Use compressed indexes rather than full documentation dumps.
**Timestamp**: 00:03:32 - 00:03:46

### Concept 5: Compressed Documentation Index
**Definition**: A technique developed by Vercel engineer Jude Gao that creates a compressed index of documentation in agents.md, pointing to full docs stored separately. Not human-readable but perfect for agents.
**Application**: Generate compressed indexes for framework documentation (Next.js, Django, FastAPI, etc.) and reference them in agents.md while storing full docs in structured folders.
**Timestamp**: 00:05:53 - 00:06:17

### Concept 6: Three-Tier Skill Architecture
**Definition**: A hierarchical approach to organizing skills and documentation:
- **Primary**: Core framework documentation as compressed indexes in agents.md
- **Secondary**: Important skills (frontend, backend, auth) referenced in agents.md
- **Tertiary**: Everything else in skills folders
**Application**: Prioritize what goes in agents.md based on frequency of use and importance to your project.
**Timestamp**: 00:07:53 - 00:08:28

## Practical Guidance

### On Improving Skill Calling Rates:

**Technique 1: Explicit Skill References in agents.md (53% → 79% success)**
- Add explicit instructions in agents.md to invoke specific skills
- Example: "Before writing any code, first explore the project structure, then invoke the nextjs-doc skill for documentation"
- **Warning**: Small wording changes produce different results; prompt syntax is critical
- **Timestamp**: 00:03:53 - 00:04:22

**Technique 2: Compressed Documentation Index (79% → 100% success)**
- Bypass skills entirely for critical framework documentation
- Create compressed indexes in agents.md pointing to full docs
- Use Vercel's approach for Next.js or adapt for your framework
- **Timestamp**: 00:04:30 - 00:05:36

### On Setting Up Next.js Documentation:
- Run the Vercel command in any Next.js project (command shown at 00:06:20)
- Tool auto-detects your Next.js version
- Choose agents.md format for Cursor/Claude compatibility
- Creates compressed index + full documentation structure automatically

### On Creating Custom Documentation Indexes:
1. Copy important documentation for your stack (Python/Django, FastAPI, Rust, etc.) into structured folders
2. Use Claude Code or similar to compress documentation into folder structures
3. Generate a compressed index for the documentation
4. Add the compressed index to agents.md file
**Timestamp**: 00:07:25 - 00:07:53

### On Manual Skill Invocation:
- When you know which skill is needed, explicitly prompt the agent to use it
- Dramatically increases pickup rate
- Practical workaround until agent tool calling is fully solved
**Timestamp**: 00:08:40 - 00:08:48

### On Automation:
- Set up hooks in Cursor and Claude Code
- Trigger specific skills automatically after certain agent actions
- Achieves 100% invocation rate for critical post-processing skills
**Timestamp**: 00:08:50 - 00:08:59

## Examples & Case Studies

**Example 1**: Vercel's Next.js Documentation Research
- **Context**: Demonstrates the compressed index technique achieving 100% skill calling
- **Details**: Vercel engineer Jude Gao researched why skills were only called 50% of the time. Developed compressed documentation index approach that loads Next.js docs into agents.md without overwhelming context.
- **Takeaway**: Compression and indexing can solve the context overload problem while maintaining 100% skill availability
- **Timestamp**: 00:02:33 - 00:06:17

**Example 2**: Skills.sh Platform
- **Context**: Illustrates the scale of available pre-built skills
- **Details**: Vercel released skills.sh with over 32,000 skills and an installer for Cursor and Claude Code. Shows popular skills and provides easy installation.
- **Takeaway**: Don't reinvent the wheel—leverage existing skill libraries before creating custom ones
- **Timestamp**: 00:02:08 - 00:02:18

**Example 3**: Model Knowledge Cutoff Problem
- **Context**: Why skills are necessary for current best practices
- **Details**: A Next.js best practices skill ensures agents use current APIs and methods, even when the model's training cutoff predates them.
- **Takeaway**: Skills bridge the gap between model training dates and current framework versions
- **Timestamp**: 00:01:47 - 00:01:58

## Speaker's Philosophy & Approach

The speaker advocates for a **pragmatic, measurement-driven approach** to AI development tools. Rather than accepting tool limitations, they actively seek solutions through research, experimentation, and community knowledge sharing.

**Core Values**:
- **Practical over theoretical**: Focus on what actually works in production environments
- **Measurement matters**: Track success rates (50% vs 80% vs 100%) to validate improvements
- **First principles thinking**: Strip away marketing terminology to understand underlying mechanisms
- **Balanced AI adoption**: Use AI extensively but maintain fundamental software development knowledge
- **Community learning**: Encourage sharing hacks and tricks to collectively improve practices

**Methodology**:
1. Identify pain points through real-world usage
2. Research existing solutions (academic research, vendor documentation)
3. Test and measure improvements quantitatively
4. Implement tiered solutions based on priority
5. Share findings with the community

The speaker emphasizes that while AI coding assistants are powerful, understanding how they work "under the hood" makes you a better AI developer—not just a prompt engineer. This philosophy aligns with their sponsorship of Brilliant, highlighting the importance of foundational knowledge in CS, programming, and LLMs.

## Quick Reference

**Key Terms**:
- **Skill**: A saved prompt with optional resources/examples that agents can invoke; equivalent to rules, commands, or context
- **agents.md**: Persistent context file loaded into every agent conversation; contains project summary and best practices
- **Compressed Index**: Human-unreadable but agent-readable reference to documentation that minimizes context usage
- **Context Window**: The amount of information an agent can process; larger doesn't necessarily mean better attention
- **Tool Calling**: The agent's ability to recognize when to invoke available skills/tools
- **Cursor Rules**: Early implementation of saved prompts in Cursor IDE (introduced ~18 months before this video)

**Frameworks Referenced**:
- Next.js (primary example)
- Django
- FastAPI
- Rust
- Auth0
- Clerk

**Tools Mentioned**:
- Cursor
- Claude Code
- Gemini
- skills.sh (Vercel's skill repository)

**Success Rate Benchmarks**:
- Baseline skill calling: 50-53%
- With agents.md references: ~79%
- With compressed indexes: 100%
- With manual prompting: "Dramatically increased"
- With hooks/automation: 100%

**Best Practices**:
1. Keep agents.md concise—avoid overloading context
2. Use three-tier architecture: primary (compressed indexes), secondary (referenced skills), tertiary (standard skills)
3. Explicitly reference critical skills in agents.md
4. Manually prompt for specific skills when you know they're needed
5. Use compressed documentation indexes for framework docs
6. Set up hooks for automatic skill invocation after specific actions
7. Leverage existing skill libraries (skills.sh) before creating custom ones

**File Locations**:
- agents.md: Base of repository/project folder
- Skills: Project folder or Cursor/Claude settings files
- Documentation: Structured folders referenced by compressed indexes

---

## Example Questions You Can Ask

- "My AI agent keeps ignoring my custom skill for database migrations. How can I increase the likelihood it gets called?"
- "I'm using FastAPI—how would I adapt Vercel's compressed index approach for my project?"
- "What's the optimal structure for an agents.md file to balance context and clarity?"
- "Should I put my authentication best practices in agents.md or keep them as a separate skill?"
- "How do I create a compressed documentation index for my Python/Django project?"
- "What are the trade-offs between the three-tier skill architecture approaches?"
- "My agents.md file is getting too large. How do I prioritize what stays and what moves to skills?"
- "Can you explain why larger context windows don't solve the skill calling problem?"
- "What hooks can I set up in Cursor to automatically invoke linting skills after code generation?"
- "How do I measure whether my skill optimization is actually working?"