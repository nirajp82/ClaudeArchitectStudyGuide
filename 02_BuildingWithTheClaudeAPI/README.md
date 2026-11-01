# Building with the Claude API — Study Notes

**Course:** [Building with the Claude API](https://academy.claude.com/courses/building-with-the-claude-api) (Anthropic Academy, 67 lessons, 8 quizzes, about 9 hours) &nbsp;·&nbsp; **Started:** November 1, 2026

**Exam relevance:** This course covers prompting, tool use, RAG, caching, MCP, and agents. It feeds most exam domains, especially Integration, Solution Design & Architecture, and Claude Models, Prompting & Context Engineering. See the [study plan](../readme.md).

Every lesson is one notes file directly in this folder, named `NN-lesson-name.md`, with an FAQ at the end. Lessons are numbered across the whole course, so chapter 2 starts at lesson 9. Quizzes have no number; missed quiz questions go in `68-course-quiz-review.md`. From this course onward, every lesson also has an **Architect notes** section with cost, speed, limits, security, and production facts the course leaves out.

## Progress

| # | Chapter | Lesson | Notes | Status |
|---|---|---|---|---|
| 1 | Accessing Claude with the API | Accessing the API | [01-accessing-the-api.md](01-accessing-the-api.md) | ✅ Done |
| 2 | Accessing Claude with the API | Getting an API key | [02-getting-an-api-key.md](02-getting-an-api-key.md) | ✅ Done |
| 3 | Accessing Claude with the API | Making a request | `03-making-a-request.md` | ⬜ |
| 4 | Accessing Claude with the API | Multi-Turn conversations | `04-multi-turn-conversations.md` | ⬜ |
| 5 | Accessing Claude with the API | System prompts | `05-system-prompts.md` | ⬜ |
| 6 | Accessing Claude with the API | Temperature | `06-temperature.md` | ⬜ |
| 7 | Accessing Claude with the API | Response streaming | `07-response-streaming.md` | ⬜ |
| 8 | Accessing Claude with the API | Structured data | `08-structured-data.md` | ⬜ |
| — | Accessing Claude with the API | Quiz on accessing Claude with the API | Quiz review file | ⬜ |
| 9 | Prompt evaluation | Prompt evaluation | `09-prompt-evaluation.md` | ⬜ |
| 10 | Prompt evaluation | A typical eval workflow | `10-a-typical-eval-workflow.md` | ⬜ |
| 11 | Prompt evaluation | Generating test datasets | `11-generating-test-datasets.md` | ⬜ |
| 12 | Prompt evaluation | Running the eval | `12-running-the-eval.md` | ⬜ |
| 13 | Prompt evaluation | Model based grading | `13-model-based-grading.md` | ⬜ |
| 14 | Prompt evaluation | Code based grading | `14-code-based-grading.md` | ⬜ |
| — | Prompt evaluation | Quiz on prompt evaluation | Quiz review file | ⬜ |
| 15 | Prompt engineering techniques | Prompt engineering | `15-prompt-engineering.md` | ⬜ |
| 16 | Prompt engineering techniques | Being clear and direct | `16-being-clear-and-direct.md` | ⬜ |
| 17 | Prompt engineering techniques | Being specific | `17-being-specific.md` | ⬜ |
| 18 | Prompt engineering techniques | Structure with XML tags | `18-structure-with-xml-tags.md` | ⬜ |
| 19 | Prompt engineering techniques | Providing examples | `19-providing-examples.md` | ⬜ |
| — | Prompt engineering techniques | Quiz on prompt engineering techniques | Quiz review file | ⬜ |
| 20 | Tool use with Claude | Introducing tool use | `20-introducing-tool-use.md` | ⬜ |
| 21 | Tool use with Claude | Project overview | `21-project-overview.md` | ⬜ |
| 22 | Tool use with Claude | Tool functions | `22-tool-functions.md` | ⬜ |
| 23 | Tool use with Claude | Tool schemas | `23-tool-schemas.md` | ⬜ |
| 24 | Tool use with Claude | Handling message blocks | `24-handling-message-blocks.md` | ⬜ |
| 25 | Tool use with Claude | Sending tool results | `25-sending-tool-results.md` | ⬜ |
| 26 | Tool use with Claude | Multi-turn conversations with tools | `26-multi-turn-conversations-with-tools.md` | ⬜ |
| 27 | Tool use with Claude | Implementing multiple turns | `27-implementing-multiple-turns.md` | ⬜ |
| 28 | Tool use with Claude | Using multiple tools | `28-using-multiple-tools.md` | ⬜ |
| 29 | Tool use with Claude | Fine grained tool calling | `29-fine-grained-tool-calling.md` | ⬜ |
| 30 | Tool use with Claude | The text edit tool | `30-the-text-edit-tool.md` | ⬜ |
| 31 | Tool use with Claude | The web search tool | `31-the-web-search-tool.md` | ⬜ |
| — | Tool use with Claude | Quiz on tool use with Claude | Quiz review file | ⬜ |
| 32 | RAG and Agentic Search | Introducing Retrieval Augmented Generation | `32-introducing-rag.md` | ⬜ |
| 33 | RAG and Agentic Search | Text chunking strategies | `33-text-chunking-strategies.md` | ⬜ |
| 34 | RAG and Agentic Search | Text embeddings | `34-text-embeddings.md` | ⬜ |
| 35 | RAG and Agentic Search | The full RAG flow | `35-the-full-rag-flow.md` | ⬜ |
| 36 | RAG and Agentic Search | Implementing the RAG flow | `36-implementing-the-rag-flow.md` | ⬜ |
| 37 | RAG and Agentic Search | BM25 lexical search | `37-bm25-lexical-search.md` | ⬜ |
| 38 | RAG and Agentic Search | A Multi-Index RAG pipeline | `38-a-multi-index-rag-pipeline.md` | ⬜ |
| 39 | Features of Claude | Extended thinking | `39-extended-thinking.md` | ⬜ |
| 40 | Features of Claude | Image support | `40-image-support.md` | ⬜ |
| 41 | Features of Claude | PDF support | `41-pdf-support.md` | ⬜ |
| 42 | Features of Claude | Citations | `42-citations.md` | ⬜ |
| 43 | Features of Claude | Prompt caching | `43-prompt-caching.md` | ⬜ |
| 44 | Features of Claude | Rules of prompt caching | `44-rules-of-prompt-caching.md` | ⬜ |
| 45 | Features of Claude | Prompt caching in action | `45-prompt-caching-in-action.md` | ⬜ |
| 46 | Features of Claude | Code execution and the Files API | `46-code-execution-and-the-files-api.md` | ⬜ |
| — | Features of Claude | Quiz on features of Claude | Quiz review file | ⬜ |
| 47 | Model Context Protocol | Introducing MCP | `47-introducing-mcp.md` | ⬜ |
| 48 | Model Context Protocol | MCP clients | `48-mcp-clients.md` | ⬜ |
| 49 | Model Context Protocol | Project setup | `49-project-setup.md` | ⬜ |
| 50 | Model Context Protocol | Defining tools with MCP | `50-defining-tools-with-mcp.md` | ⬜ |
| 51 | Model Context Protocol | The server inspector | `51-the-server-inspector.md` | ⬜ |
| 52 | Model Context Protocol | Implementing a client | `52-implementing-a-client.md` | ⬜ |
| 53 | Model Context Protocol | Defining resources | `53-defining-resources.md` | ⬜ |
| 54 | Model Context Protocol | Accessing resources | `54-accessing-resources.md` | ⬜ |
| 55 | Model Context Protocol | Defining prompts | `55-defining-prompts.md` | ⬜ |
| 56 | Model Context Protocol | Prompts in the client | `56-prompts-in-the-client.md` | ⬜ |
| — | Model Context Protocol | Quiz on Model Context Protocol | Quiz review file | ⬜ |
| 57 | Anthropic apps | Anthropic apps: Claude Code and computer use | `57-anthropic-apps.md` | ⬜ |
| 58 | Anthropic apps | Claude Code setup | `58-claude-code-setup.md` | ⬜ |
| 59 | Anthropic apps | Claude Code in action | `59-claude-code-in-action.md` | ⬜ |
| 60 | Anthropic apps | Adding MCP servers to Claude Code | `60-adding-mcp-servers-to-claude-code.md` | ⬜ |
| 61 | Agents and workflows | Agents and workflows | `61-agents-and-workflows.md` | ⬜ |
| 62 | Agents and workflows | Parallelization workflows | `62-parallelization-workflows.md` | ⬜ |
| 63 | Agents and workflows | Chaining workflows | `63-chaining-workflows.md` | ⬜ |
| 64 | Agents and workflows | Routing workflows | `64-routing-workflows.md` | ⬜ |
| 65 | Agents and workflows | Agents and tools | `65-agents-and-tools.md` | ⬜ |
| 66 | Agents and workflows | Environment inspection | `66-environment-inspection.md` | ⬜ |
| 67 | Agents and workflows | Workflows vs agents | `67-workflows-vs-agents.md` | ⬜ |
| — | Agents and workflows | Quiz on Agents and Workflows | Quiz review file | ⬜ |
| — | Final assessment | Final Assessment | `68-course-quiz-review.md` | ⬜ |

Files are created as each lesson is completed. Paste the transcript or course text after each lesson to add its notes.

## To-do

- [ ] **Images.** Lesson images are downloaded from each lesson's page on academy.claude.com into `images/`. No images are missing so far.

## When you finish this course

1. [ ] Take each chapter quiz and the final assessment. Record every missed or guessed question, and the correct reasoning, in `68-course-quiz-review.md`.
2. [ ] Collect the **completion badge**.
3. [ ] Practice: build capstone v1 and v2 (document Q&A with citations, prompt caching, and the first 10–20 eval questions). See the [course sequence](../readme.md#course-sequence-what-to-do-when-you-finish-each-course).
4. [ ] Mark this course as done in the study plan.

## Folder layout

```text
02_BuildingWithTheClaudeAPI/
├── README.md                 ← this index
├── images/                   ← screenshots used in the lessons
├── 01-accessing-the-api.md
├── 02-getting-an-api-key.md
├── ...
├── 67-workflows-vs-agents.md
└── 68-course-quiz-review.md
```
