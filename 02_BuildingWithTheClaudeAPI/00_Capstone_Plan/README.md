# Capstone Project Plan: Support Assistant

**Part of:** [Study plan](../../readme.md) &nbsp;·&nbsp; **Course:** [Building with the Claude API](../README.md)

---

**On this page**

| # | Section |
|:---:|:---|
| 1 | [In short](#in-short) |
| 2 | [What the finished app does](#what-the-finished-app-does) |
| 3 | [Who's who](#whos-who) |
| 4 | [How each guide works](#how-each-guide-works) |
| 5 | [The chapter guides](#the-chapter-guides) |
| 6 | [Where the files go](#where-the-files-go) |
| 7 | [Safety rules](#safety-rules) |

---

### In short

- **What it is:** a small Python program for a made-up internet company, Northwind Internet. You type a question in the terminal, and the program answers it using the Claude API. It is the one app you build during the whole study plan.
- **Why build it:** the exam asks you to choose between designs and defend the choice. You can only do that well if you have built the thing, measured it, and seen it fail.
- **How it grows:** after each chapter of *Building with the Claude API*, you work through that chapter's guide. Every lesson in the chapter becomes at least one problem you solve in the app.
- **Where the code lives:** in this folder, `02_BuildingWithTheClaudeAPI/00_Capstone_Plan/`, next to this plan. All paths below are relative to this folder.
- **Where you build it:** mainly on your MacBook, in the Terminal app. Every step that needs different commands also shows the Windows (PowerShell) version. Both computers share the same GitHub repository, so run `git pull` before each session and `git push` after it.

> **Remember this:** One chapter, then one guide. If you fall behind, keep the order and keep going.

---

### What the finished app does

When the app is finished, a session in your terminal looks like this.

```text
You:  How long do I have to ask for a refund?
App:  You have 30 days from the purchase date. [Source: refund-policy.md]

You:  What is the status of ticket 1042?
App:  Ticket 1042 is open: "Router keeps restarting". The network team has it.

You:  Please open a ticket. My internet has been down since this morning.
App:  I am about to create this ticket:
        Title: Internet down since this morning   Priority: high
      Type yes to create it, or anything else to cancel: yes
App:  Created ticket 1046. I checked it: it is open, and the support team has it.

You:  What is the CEO's salary?
App:  The company documents don't cover that.
```

| Feature | What it means | Guide |
|---|---|---|
| **Different answers for different roles** | A customer gets simple steps; a support technician gets technical checks and may see staff documents. | 1, 5 |
| **Answers from documents, with sources** | The app finds the right passages in made-up company documents and names its source. This is called *retrieval-augmented generation* (RAG). | 5, 6 |
| **Tools** | The model asks your code to run functions such as `lookup_ticket`. Your code checks who may see what. | 4 |
| **Ask before a change** | Creating a ticket waits for a person to type `yes`. This is called an *approval gate*. | 4 |
| **Admit what it doesn't know** | The app says so instead of inventing an answer. | 2, 5 |
| **Routing and a misuse filter** | A cheap first step sends each question to the right handler and refuses misuse. | 9 |
| **An incident team** | Four specialist agents (triage analyst, investigator, planner, reviewer) write an incident report, like roles on a software team. | 9 |
| **Measured quality and cost** | About 25 test questions check the answers automatically, and prompt caching cuts the cost. | 2, 6, 10 |

---

### Who's who

| Player | Where it lives | What it does | Example |
|---|---|---|---|
| You | Your MacBook (or your Windows computer) | Write the code, run the app, and type `yes` to approve tickets | You write `lookup_ticket` in `app/tools.py` |
| Your app | This folder, on whichever computer you use | Reads your question, finds documents, runs tools, and calls the API | `uv run python -m app.main --role customer` starts the chat |
| The Claude API and the model | Anthropic's servers | Reads the question and the documents your app sends, then replies or asks for a tool | It replies "call `lookup_ticket` with 1042" |
| Claude Code | Terminal (Mac) or PowerShell (Windows), opened in this folder | Your tutor and reviewer. You write the code first, then ask it to review. | "Review `app/tools.py`. Explain problems; don't fix them." |
| The Cookbook | `claude-cookbooks/`, a folder next to this repository (see the [Cookbook build-along plan](../../cookbook-build-along.md#where-the-folders-sit)) | Working examples that you study before each guide | `tool_use/customer_service_agent.ipynb` |

---

### How each guide works

Each guide has the same parts:

1. **What you build in this chapter:** the files you create and a "done when" check.
2. **Problems:** one or more per course lesson, with a link to the lesson. Each problem states the task and how to check your solution.
3. **The step-by-step answer:** hidden under "Show the step-by-step answer". Try the problem first, then open the answer to check or when you are stuck.
4. **An architect scenario:** a design problem from a different business, an online shop, asked the way the exam asks it. The same shop returns in every guide.
5. **Commit your work:** the commands to test and save your progress.

---

### The chapter guides

Do each guide right after the course chapter in the "Do it after" column. A chapter name becomes a link to your notes once you have written notes for its first lesson. "Cookbook phase" points to the [Cookbook build-along plan](../../cookbook-build-along.md#the-plan-phase-by-phase), which lists optional notebooks to study first.

| # | Do it after | Capstone guide | Cookbook phase | What you build | Status |
|:---:|:---|:---|:---:|:---|:---|
| 1 | [Chapter 1, Accessing Claude with the API (lessons 1–8)](../01-accessing-claude-with-the-api/README.md) | [Guide 1](guide/01-accessing-claude-with-the-api.md) | 0, 1 | Setup, chat with memory, roles, streaming, JSON triage, retries | Not started |
| 2 | [Chapter 2, Prompt evaluation (lessons 9–14)](../02-prompt-evaluation/README.md) | [Guide 2](guide/02-prompt-evaluation.md) | 2 | Test cases, an eval runner, code and model graders | Not started |
| 3 | Chapter 3, Prompt engineering techniques (lessons 15–19) | [Guide 3](guide/03-prompt-engineering-techniques.md) | 3 | Hard cases and better prompts, measured one technique at a time | Not started |
| 4 | Chapter 4, Tool use with Claude (lessons 20–31) | [Guide 4](guide/04-tool-use-with-claude.md) | 4 | Ticket tools, the tool loop, the approval gate, tests, editor and web search | Not started |
| 5 | Chapter 5, RAG and Agentic Search (lessons 32–38) | [Guide 5](guide/05-rag-and-agentic-search.md) | 5 | Documents, hybrid search, a role filter, a search tool | Not started |
| 6 | Chapter 6, Features of Claude (lessons 39–46) | [Guide 6](guide/06-features-of-claude.md) | 6 | Thinking, images, PDFs, citations, caching, code execution | Not started |
| 7 | Chapter 7, Model Context Protocol (lessons 47–56) | [Guide 7](guide/07-model-context-protocol.md) | none | An MCP server and your own MCP client | Not started |
| 8 | Chapter 8, Anthropic apps (lessons 57–60) | [Guide 8](guide/08-anthropic-apps.md) | none | Claude Code rules for the project, a review, and your MCP server in Claude Code | Not started |
| 9 | Chapter 9, Agents and workflows (lessons 61–67) | [Guide 9](guide/09-agents-and-workflows.md) | 7 | Routing, chains, parallel checks, and the four-agent incident team | Not started |
| 10 | The whole course, plus the cloud course in the [study plan](../../readme.md) | [Guide 10](guide/10-final-measurements-and-write-ups.md) | 8 | Model comparison, batches, and the three write-ups | Not started |

**If you fall behind,** shorten guides 7 and 8 first, because the rest of the app doesn't depend on them. Never skip guides 2, 4, and 6. Evals, tools with approval, and caching appear across several exam domains.

---

### Where the files go

The capstone code lives inside this study-notes repository, so Git saves it together with your notes. The number in brackets is the guide that creates each file.

```text
02_BuildingWithTheClaudeAPI/00_Capstone_Plan/
├── README.md                    this plan
├── guide/                       the ten chapter guides
├── .env                         your API keys; never committed to Git              (1)
├── .gitignore                   tells Git which files to skip: .env and .venv      (1)
├── pyproject.toml               the list of Python packages; uv writes it          (1)
├── CLAUDE.md, .claude/          rules and settings for Claude Code                 (8)
├── app/
│   ├── client.py                the API connection and get_text()                  (1)
│   ├── main.py                  the chat you run in the terminal                   (1)
│   ├── prompts.py               the system prompts for each role                   (1)
│   ├── triage.py                sorts a message into category and priority         (1)
│   ├── retry.py                 retries a failed request with backoff              (1)
│   ├── assistant.py             answer() and answer_from_documents()               (2, 5)
│   ├── tools.py                 the tools and run_tool()                           (4)
│   ├── agent_loop.py            run_turn(): the tool loop                          (4)
│   ├── notes_editor.py          a safe handler for the text editor tool            (4)
│   ├── retrieval.py             chunking, search, and the role filter              (5)
│   ├── router.py                routing and the misuse filter                      (9)
│   ├── workflows.py             the draft-and-check chain and parallel checks      (9)
│   └── incident_team.py         the four-agent incident team                       (9)
├── data/                        made-up tickets and outages                        (4)
├── sample_documents/            made-up company documents                          (5)
├── tests/test_tools.py          automatic tests for the tools                      (4)
├── mcp_server/server.py         offers tools, resources, and a prompt over MCP     (7)
├── mcp_client/chat.py           your own MCP client                                (7)
├── experiments/                 small learning scripts, not part of the app        (1–10)
├── evaluations/
│   ├── cases.jsonl              the test questions, one per line                   (2)
│   ├── run_evals.py             runs, grades, and saves every test question        (2)
│   ├── graders.py               the code grader and the model grader               (2)
│   ├── scores.md                your log of scores after each change               (2)
│   └── results/                 saved scores, costs, and the model comparison      (2, 6, 10)
└── docs/
    ├── notes/known-issues.md    the technicians' notes file                        (4)
    ├── incidents/               reports from the incident team                     (9)
    ├── decisions.md             three design-decision notes                        (10)
    ├── risk-review.md           one page                                           (10)
    └── manager-summary.md       one page                                           (10)
```

---

### Safety rules

- **Use made-up data only.** Write the documents and tickets yourself for a made-up company. Never use real company or customer data.
- **Keep the keys in `.env` only.** Never put them in code, a notebook, or a chat message.
- **Set a monthly spend limit** in the Claude Console before guide 1. While learning, a few dollars a month is enough.
- **Use Haiku** unless a problem asks for another model, as guide 4's web search and guide 10's comparison do.
