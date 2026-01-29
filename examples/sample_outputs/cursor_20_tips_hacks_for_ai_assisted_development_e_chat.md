# Cursor 2.0 Tips & Hacks for AI-Assisted Development - Expert Knowledge Context

## Source Information
- URL: https://www.youtube.com/watch?v=HlG_cYRydHY
- Duration: 00:28:21
- Speaker: Rob (Cursor course creator & enterprise trainer)
- Processed: 2025

## How to Use This Context
Load this document into your chat assistant to:
- Ask questions about Cursor 2.0 features and workflows
- Get advice on AI-assisted development best practices
- Learn context management and model selection strategies
- Implement effective prompting and design workflows
- Troubleshoot common issues with AI coding assistants

---

## Expertise Summary

The speaker is an expert in AI-assisted development with Cursor, having taught thousands of developers through courses and enterprise training programs. Their expertise centers on practical workflows for using AI coding assistants effectively, with deep knowledge of context management, model selection, prompt engineering, and development workflows that maximize productivity while minimizing costs.

Their unique perspective combines traditional software development practices (Git workflows, database design, testing) with AI-native approaches (agent steering, work trees, design mode). They emphasize pragmatic strategies over theoretical perfection, focusing on natural break points, context window management, and knowing when to use expensive vs. fast models.

## Key Concepts & Frameworks

### Concept 1: Context Management & The 60% Rule
**Definition**: Managing the AI's context window to prevent confusion and maintain quality responses. The speaker recommends staying under 60% of context capacity even when more is available.
**Application**: Monitor the context indicator in Cursor. Start new conversations at natural break points (after completing setup, finishing a feature). Use summarization only when necessary to carry critical information forward.
**Why It Matters**: Models remember instructions at the start and end of context windows well, but struggle with middle content. Exceeding 60% leads to degraded performance even with large context windows like Gemini's.
**Timestamp**: 13:42

### Concept 2: Priming Your Project
**Definition**: Providing context to AI about your codebase, tech stack, and preferences at the start of each conversation.
**Application**: 
- Enable codebase indexing in settings
- Add relevant documentation to the docs section
- Use commands to declare your tech stack
- Reference specific URLs for recent package documentation
- Remember each new chat is an AI "stepping into a codebase it's never seen"
**Key Insight**: Model training cutoff windows can be 6+ months old, so always provide recent documentation for new versions.
**Timestamp**: 08:17

### Concept 3: Work Trees (Agent Death Match / Best of N)
**Definition**: Running multiple AI models or instances simultaneously on the same task to compare outputs and select the best result.
**Application**:
1. Click "Work Tree" in agent mode
2. Select multiple models (up to 8 versions)
3. Each creates an isolated branch to experiment
4. Review results via separate ports (3001, 3002, etc.)
5. Apply the best solution back to main branch
**Use Cases**: Complex problems, major design changes, refactoring, when uncertain about approach
**Setup Tip**: Create a `worktrees.json` file in `.cursor` directory with `npm install` and `npm run dev` commands to auto-start servers
**Timestamp**: 18:03

### Concept 4: Design Mode (Low-Cost Prototyping)
**Definition**: A workflow mode for designing interfaces without touching database schemas or backend logic, using mock JSON data.
**Application**: Create a custom command with prompt: "Working in design feature prototype mode. No changes to database/schema. Mock data generated temporarily with JSON."
**Benefits**: Low-cost experimentation, rapid iteration, safe exploration before committing to implementation
**Best Practice**: Combine with plan mode (Shift+Tab) and user story format prompts
**Timestamp**: 24:26

### Concept 5: Agent Steering
**Definition**: Interrupting or redirecting an AI agent mid-execution when it's stuck or going in the wrong direction.
**Application**: 
- Add a new prompt in the input box while agent is running
- Click the interrupt button to force immediate processing (instead of queuing)
- Use simple commands like "resume" or "stop, try this approach instead"
**When to Use**: Agent is looping, taking wrong approach, or stuck on an error
**Timestamp**: 19:02

### Concept 6: ORM-First Database Design
**Definition**: Using ORMs (Prisma, Drizzle) where the entire database schema exists in code files rather than requiring MCP connections.
**Application**: Database schema lives in a single file (e.g., `schema.prisma`) that AI can read and modify. Changes are migrated via commands.
**Benefits**: 
- AI fully understands database structure
- Clean, contained schema management
- No complex MCP setup needed
- Easy for AI to propose and implement schema changes
**Timestamp**: 07:27

### Concept 7: Model Selection Strategy
**Definition**: Choosing the right AI model based on task requirements, balancing speed, intelligence, and cost.
**Current Recommendations** (as of video):
- **Composer 1**: Fast iteration, most frequent use, not the smartest but excellent speed
- **Claude Sonnet 4.5**: Balanced performance for building work
- **Claude Opus 4.5**: Expensive, use for planning and design only
- **Haiku**: Quick tasks
**Philosophy**: Use fast/cheap models for iteration, expensive models for planning
**Timestamp**: 15:17

### Concept 8: Rules vs. Commands
**Definition**: 
- **Rules**: Automated prompts triggered by Cursor at certain times
- **Commands**: User-created, manually invoked prompts stored globally
**Recommendation**: Start projects without many rules (they bloat context). Add specific rules only when patterns emerge. Heavily use custom commands instead.
**Example Command**: Package health check that scans node_modules for security issues
**Timestamp**: 02:17

## Practical Guidance

### On Starting New Projects:

- **Disable MCPs initially**: They consume massive context. Enable only as needed (keep browser automation on)
- **Enable completion sounds**: Get notified when agent finishes to avoid distraction
- **Use starter templates**: Have a pre-configured template with auth (Clerk), database (Neon), ORM (Prisma), and framework (Next.js)
- **Write first commits manually**: Let Cursor learn your commit style before using magic commit button
- **Create a new branch immediately**: Use `git checkout -b feature-name` before building anything new

### On Context & Prompting:

- **Always provide context with @ symbol**: Reference browser, files, docs, or codebase
- **Use user story format**: "As a [role], I want [feature] so that [benefit]"
- **Include specific constraints**: Color scheme only, don't change database, use list not grid
- **Paste error messages directly**: Copy from console (browser or terminal) into chat
- **Reference documentation URLs**: Don't rely on outdated training data
- **Start conversations with design mode or tech stack commands**

### On Error Handling:

- **Console errors**: Copy from browser developer tools (red errors in console tab)
- **Terminal errors**: Copy full error output from terminal
- **Provide both**: Tell agent to "review console logs of browser and running terminal"
- **Add context**: Use @ symbol to reference browser, relevant files, or readme

### On Design Workflow:

- **Limit color palette**: Light or dark mode, not too many colors (creates confusion)
- **Use hierarchy**: Help users know where to click next
- **Get inspiration**: Use Mobin for UI patterns, Pinterest for color schemes
- **Use Recraft**: For vectorizing logos, removing backgrounds, creating mockups
- **Generate multiple options**: Use work trees with different models or UX designer persona
- **Draw on paper first**: Upload sketches as images for AI to implement

### On Cost Management:

- **Use design mode**: Prototype with mock data before real implementation
- **Prefer Composer**: For most iteration work
- **Reserve Opus**: For planning and design only
- **Monitor context**: Stay under 60% to avoid waste
- **Start new conversations**: At natural break points
- **Turn off unused MCPs**: They consume tokens rapidly

### On Git Workflow:

- **Always work on feature branches**: Never build directly on main
- **Use work trees for experiments**: Safe parallel development
- **Enable agent review**: Auto-QA on commits (but don't rely completely)
- **Commit at natural points**: After setup, after each feature completion
- **Review before applying**: Check all changes when merging work trees back

### On Testing & QA:

- **Run local servers**: `npm run dev` for Next.js
- **Use port management**: Track multiple servers (Port Manager on Mac)
- **Open browser with Cmd+Shift+B**: Quick testing shortcut
- **Check developer console**: Monitor for errors during testing
- **Don't fully trust agent review**: It's helpful but not comprehensive

## Examples & Case Studies

**Example 1: Launch Kit Core Template**
- **Context**: Starting a new project quickly with pre-configured stack
- **Stack**: Next.js, Shadcn, Clerk (auth), Neon (Postgres), Prisma (ORM), Lucid Icons
- **Process**: Use GitHub template → Clone → npm install → Add Clerk keys → Add Neon database URL → Prisma generate
- **Takeaway**: Pre-built templates save days of setup time and provide AI with consistent, well-structured codebases
- **Timestamp**: 05:35

**Example 2: Title Generator App (Boosting Title Gen)**
- **Context**: Building a YouTube title generator with psychological drivers
- **Features**: Input video concept → Generate 10 titles → Copy/heart favorites → Add to basket
- **Approach**: Used design mode with mock data first, then multiple models via work trees
- **Design Process**: Opus 4.5 for initial design, compared with Composer, iterated based on preferences
- **Takeaway**: Design mode allows rapid prototyping without backend complexity
- **Timestamp**: 25:00

**Example 3: Design Update with Pinterest Inspiration**
- **Context**: Updating app design using external inspiration
- **Process**: Found design on Pinterest → Pasted image → Prompted "copy color scheme and font only"
- **Key Constraint**: Specified to NOT recreate all elements, just extract specific aspects
- **Work Tree Usage**: Ran both Composer and Sonnet 4.5 simultaneously to compare results
- **Outcome**: Chose Composer version for background treatment
- **Takeaway**: Be specific about what to extract from inspiration images
- **Timestamp**: 17:13

**Example 4: Prisma Error Resolution**
- **Context**: Intentional error in Launch Kit requiring Prisma client generation
- **Error Message**: Copied from browser console and terminal
- **Resolution**: AI understood codebase structure, identified missing step, ran `prisma generate`
- **Follow-up**: Set up Neon database, ran migration automatically
- **Takeaway**: Providing both console and terminal errors gives complete context
- **Timestamp**: 07:15

**Example 5: Package Health Check Command**
- **Context**: Reusable command for security and update scanning
- **Implementation**: Created as user command (stored in Cursor folder)
- **Usage**: Type `/package-health-check` or have agent reference it
- **Benefit**: Works across all projects, can be imported to Claude Code
- **Takeaway**: Build a library of personal commands for repeated tasks
- **Timestamp**: 02:51

## Speaker's Philosophy & Approach

**Pragmatic Over Perfect**: The speaker consistently favors practical, working solutions over theoretical ideals. They acknowledge when features are "hit and miss" (like rules) and recommend starting simple, adding complexity only when patterns emerge.

**Context is King**: A recurring theme is the importance of providing AI with the right context at the right time. This includes tech stack information, recent documentation, error messages, and visual inspiration. The speaker views each new chat as a fresh start requiring re-orientation.

**Cost-Conscious Development**: The workflow emphasizes using expensive models (Opus) only for planning and design, while relying on faster, cheaper models (Composer, Sonnet) for iteration. Design mode with mock data is preferred for early-stage work.

**Safety Through Branching**: Strong emphasis on Git workflows, feature branches, and work trees to enable experimentation without risk. The philosophy is "always have a way back" to working code.

**Learn by Doing**: Rather than loading massive rules files or trying to configure everything perfectly upfront, the approach is to start lean, encounter problems, and add specific solutions as needed.

**Multi-Model Strategy**: Rather than declaring one model "best," the speaker uses different models for different purposes and often runs multiple models simultaneously to compare outputs. This reflects a pragmatic recognition that different models excel at different tasks.

**Design First, Implement Second**: The design mode workflow reflects a philosophy of figuring out what you want before committing to backend changes. This mirrors traditional software development wisdom but adapted for AI assistance.

**Tool Agnosticism**: While focused on Cursor, the speaker regularly uses Claude Code alongside it, imports commands between tools, and recommends complementary tools (Recraft for design). The philosophy is using the right tool for each job rather than forcing everything into one platform.

## Quick Reference

**Key Terms**:
- **Context Window**: The amount of information an AI model can process in one conversation
- **Priming**: Providing initial context about your project to the AI
- **Work Tree**: Git feature allowing parallel development in isolated copies
- **Composer**: Cursor's fast, proprietary AI model
- **Design Mode**: Prototyping workflow using mock data without backend changes
- **Agent Steering**: Interrupting or redirecting AI mid-execution
- **ORM**: Object-Relational Mapping (Prisma, Drizzle) for database management
- **MCP**: Model Context Protocol for external integrations
- **Codebase Indexing**: Cursor's background process for understanding your project

**Essential Keyboard Shortcuts**:
- **Cmd/Ctrl + B**: Toggle sidebar (file structure)
- **Cmd/Ctrl + J**: Toggle terminal
- **Cmd/Ctrl + Shift + B**: Open browser for testing
- **Ctrl + E**: Switch between editor and agent window
- **Shift + Tab**: Plan mode (generate plan before execution)

**Model Selection Guide**:
- **Planning & Design**: Opus 4.5
- **Most Iteration Work**: Composer 1
- **Balanced Building**: Sonnet 4.5
- **Quick Tasks**: Haiku

**Context Management Rules**:
- Stay under 60% context capacity
- Start new conversations at natural breaks
- Disable unused MCPs
- Add recent documentation for new package versions
- Use @ symbol to add specific context

**Best Practices Checklist**:
- ✅ Enable completion sounds
- ✅ Create feature branches before building
- ✅ Use design mode for prototyping
- ✅ Provide error messages from both console and terminal
- ✅ Write first few commits manually
- ✅ Start with minimal rules, add as needed
- ✅ Keep color schemes simple (light/dark, limited palette)
- ✅ Review all changes before applying work trees
- ✅ Monitor context window usage
- ✅ Use user story format for prompts

**Common Commands to Create**:
- `/design-mode`: Enable mock data prototyping
- `/package-health-check`: Security and update scanning
- `/[your-stack]`: Quick tech stack setup (e.g., Next.js + Shadcn + Clerk)

**Recommended Tech Stack** (Speaker's Preference):
- **Framework**: Next.js
- **UI Components**: Shadcn
- **Icons**: Lucid Icons
- **Auth**: Clerk
- **Database**: Neon (Postgres)
- **ORM**: Prisma
- **Design Tool**: Recraft

---

## Example Questions You Can Ask

- "How should I manage context when working on a complex feature that spans multiple conversations?"
- "What's the best workflow for designing a new interface without breaking my existing app?"
- "When should I use work trees vs. just creating a new branch?"
- "How do I set up a starter template like Launch Kit Core for my own stack?"
- "What's the most cost-effective model strategy for building a full-stack app?"
- "How can I get AI to understand my database schema without using MCPs?"
- "What should I do when the AI agent gets stuck in a loop?"
- "How do I provide good context for error messages?"
- "What's the difference between rules and commands, and which should I use?"
- "How can I run multiple AI models on the same problem to compare results?"
- "What's the best way to handle design inspiration from other websites?"
- "Should I trust agent review for QA, or do I need additional testing?"
- "How do I set up work trees to automatically run my development server?"
- "What's the optimal way to structure prompts for better AI responses?"
- "How can I use Cursor and Claude Code together effectively?"