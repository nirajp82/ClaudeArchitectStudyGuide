# Claude Code 101 — Study Notes

> Course: [Claude Code 101](https://academy.claude.com/courses/claude-code-101) (Anthropic Academy, 12 lessons, ~1.5 hr)
> Started: October 17, 2026
> Exam relevance: Developer Productivity & Operational Enablement domain (~7%, unofficial weight). See the [study guide](../ClaudeArchitectProfessionalStudyGuide.md).

Every lesson is one notes file directly in this folder, named `0X-lesson-name.md`, with an FAQ at the end. There are no chapter subfolders.

## Progress

| # | Chapter | Lesson | Notes | Status |
|---|---|---|---|---|
| 1 | What is Claude Code? | What is Claude Code? | [01-what-is-claude-code.md](01-what-is-claude-code.md) | ✅ Done |
| 2 | What is Claude Code? | How Claude Code works | [02-how-claude-code-works.md](02-how-claude-code-works.md) | ✅ Done |
| 3 | Your first prompt | Installing Claude Code | [03-installing-claude-code.md](03-installing-claude-code.md) | ✅ Done |
| 4 | Your first prompt | Your first prompt | [04-your-first-prompt.md](04-your-first-prompt.md) | ✅ Done |
| 5 | Daily workflows | The explore → plan → code → commit workflow | [05-explore-plan-code-commit.md](05-explore-plan-code-commit.md) | ✅ Done |
| 6 | Daily workflows | Context management | [06-context-management.md](06-context-management.md) | ✅ Done |
| 7 | Daily workflows | Code review | [07-code-review.md](07-code-review.md) | ✅ Done |
| 8 | Customizing Claude Code | The CLAUDE.md file | [08-claude-md-file.md](08-claude-md-file.md) | ✅ Done |
| 9 | Customizing Claude Code | Subagents | [09-subagents.md](09-subagents.md) | ✅ Done |
| 10 | Customizing Claude Code | Skills | [10-skills.md](10-skills.md) | ✅ Done |
| 11 | Customizing Claude Code | MCP | [11-mcp.md](11-mcp.md) | ✅ Done |
| 12 | Customizing Claude Code | Hooks | [12-hooks.md](12-hooks.md) | ✅ Done |
| — | Quiz | Course quiz | `13-course-quiz-review.md` (missed questions + reasoning) | ⬜ |
| — | — | Completion badge | — | ⬜ |

Files are created as each lesson is completed. Paste the transcript after each lesson to add its notes.

## To-do

- [ ] **Bring lessons 1 and 3 up to lesson 2's standard** (see `CLAUDE.md`). They're accurate but were written before the style rules. Each needs:
  - an "In one sentence" opener, everyday comparisons, and one running example
  - Mermaid diagrams where a flow helps
  - concrete examples (exact commands and output), "Common mix-ups" and "Test yourself"
  - an FAQ in lesson 2's style
- [ ] **Missing images.** Paste these screenshots in chat to fill the `<!-- IMAGE: ... -->` markers:
  - Lesson 2: permission prompt before a bash command → `images/02-permission-prompt.png`
  - Lesson 3: terminal after install → `images/03-terminal-install.png`
  - Lesson 3: login method selection → `images/03-login-method.png`
  - Lesson 3: VS Code extension page → `images/03-vscode-extension.png`
  - Lesson 3: JetBrains plugin page → `images/03-jetbrains-plugin.png`
  - Lesson 3: Desktop "Code" view → `images/03-desktop-code-view.png`
  - Lesson 3: claude.ai/code repo selection → `images/03-web-repo-selection.png`
  - Lesson 4: auto-accept mode working through a task → `images/04-auto-accept-mode.png`
  - Lesson 4: plan mode status bar indicator → `images/04-plan-mode-indicator.png`
  - Lesson 4: dark mode prompt typed in plan mode → `images/04-dark-mode-prompt.png`
  - Lesson 11: possible second image in "What can you do with it?" (image 18 was a copy of image 17) → `images/11-what-can-you-do.png`
## When you finish this course

1. [ ] Take the **course quiz**. Record every missed or guessed question, and the correct reasoning, in `13-course-quiz-review.md`.
2. [ ] Collect the **completion badge**.
3. [ ] Practice: use Claude Code to create the capstone repository structure from the [study guide (Section 5)](../ClaudeArchitectProfessionalStudyGuide.md#5-study-workspace), and review each permission prompt.
4. [ ] Mark Claude Code 101 as done in the study guide.
5. [ ] **Next course:** [Claude Platform 101](https://academy.claude.com/courses/claude-platform-101). Create a `ClaudePlatform101/` notes folder in the same format.

See the full order in the [course sequence](../ClaudeArchitectProfessionalStudyGuide.md#course-sequence-what-to-do-when-you-finish-each-course).

## Folder layout

```text
01_ClaudeCode101/
├── README.md                        ← this index
├── images/                          ← screenshots used in the lessons
├── 01-what-is-claude-code.md
├── 02-how-claude-code-works.md
├── 03-installing-claude-code.md
├── 04-your-first-prompt.md
├── 05-explore-plan-code-commit.md
├── 06-context-management.md
├── 07-code-review.md
├── 08-claude-md-file.md
├── 09-subagents.md
├── 10-skills.md
├── 11-mcp.md
├── 12-hooks.md
└── 13-course-quiz-review.md
```
