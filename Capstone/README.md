# Capstone Project Plan: Support Assistant

**Part of:** [Study plan](../readme.md) &nbsp;·&nbsp; **Created:** November 7, 2026 &nbsp;·&nbsp; **Runs:** November 8 to December 14, 2026

---

**On this page**

| # | Section |
|:---:|:---|
| 1 | [In short](#in-short) |
| 2 | [What the finished app does](#what-the-finished-app-does) |
| 3 | [Who's who](#whos-who) |
| 4 | [Where the files go](#where-the-files-go) |
| 5 | [Start here: your first session](#start-here-your-first-session) |
| 6 | [The milestones](#the-milestones) |
| 7 | [Milestone 8: the MCP server](#milestone-8-the-mcp-server) |
| 8 | [Milestone 10: the three write-ups](#milestone-10-the-three-write-ups) |
| 9 | [Safety rules](#safety-rules) |

---

### In short

- **What it is:** a small Python program that runs in your terminal. You type a question, and the program answers it using the Claude API. It is the one app you build during the whole study plan.
- **Why build it:** the exam asks you to choose between designs and defend the choice. You can only do that well if you have built the thing, measured it, and seen it fail.
- **How it grows:** you add one feature after each chapter of *Building with the Claude API*. Each feature uses what that chapter just taught. Nothing is built up front.
- **Where the code lives:** in its own folder, `C:\Projects\Personal\claude-capstone\`, outside these notes. This plan stays here in the notes.
- **Time:** about 5 hours a week, which includes the matching notebooks from the [Cookbook build-along plan](../cookbook-build-along.md). The Cookbook shows each technique working. The capstone is where you write it yourself.

> **Remember this:** One chapter, then one feature. If you fall behind on dates, keep the order and keep going.

---

### What the finished app does

By December 14, a session in your terminal looks like this. Every item it shows is a feature you add in one milestone.

```text
You:  How long do I have to ask for a refund?
App:  You have 30 days from the purchase date. [Source: refund-policy.md]

You:  What is the status of ticket 1042?
App:  Ticket 1042 is open: "Router keeps restarting". The network team has it.

You:  Please open a ticket. My internet has been down since this morning.
App:  I am about to create this ticket:
        Title: Internet down since this morning   Priority: high
      Type yes to create it, or anything else to cancel: yes
App:  Created ticket 1043.

You:  What is the CEO's salary?
App:  The company documents don't cover that, so I can't answer it.
```

- **Answer from documents and cite them** (first exchange). The app finds the right passage in 5 to 10 made-up company documents and names its source. This technique is called *retrieval-augmented generation* (RAG).
- **Look up a ticket** (second exchange). The model asks your code to run a function called `lookup_ticket`. Your code runs it and sends back the result. A function the model can ask for is called a **tool**.
- **Ask before a change** (third exchange). Creating a ticket changes something, so your code shows the planned ticket and waits for you to type `yes`. This check is called an *approval gate*.
- **Admit what it doesn't know** (last exchange). The app says so instead of making up an answer.

Behind the scenes, the app also saves money with *prompt caching*, which means the API stores the unchanging start of each request so that later requests cost less. It also has about 25 test questions that check its answers automatically.

---

### Who's who

| Player | Where it lives | What it does | Example |
|---|---|---|---|
| You | Your computer | Write the code, run the app, and type `yes` to approve tickets | You write `lookup_ticket` in `app\tools.py` |
| Your app | `C:\Projects\Personal\claude-capstone\` | Reads your question, finds documents, runs tools, and calls the API | `uv run python -m app.main` starts the chat |
| The Claude API and the model | Anthropic's servers | Reads the question and the documents your app sends, then replies or asks for a tool | It replies "call `lookup_ticket` with 1042" |
| Claude Code | Your terminal, opened in the capstone folder | Your tutor and reviewer. You write the code first, then ask it to review. | "Review `app/tools.py`. Explain problems; don't fix them." |
| The Cookbook | `C:\Projects\Personal\claude-cookbooks\` | Working examples that you study before you build each feature | `tool_use/customer_service_agent.ipynb` |

---

### Where the files go

The capstone is its own Git repository. A **Git repository** is a folder whose history of changes Git records. The number in brackets is the milestone that creates each file.

```text
C:\Projects\Personal\claude-capstone\
├── .env                      your API key; never committed to Git            (M0)
├── .gitignore                tells Git which files to skip, such as .env     (M0)
├── pyproject.toml            the list of Python packages; uv writes it       (M0)
├── app\
│   ├── __init__.py           empty; tells Python that app is a package       (M0)
│   ├── client.py             sends a question to the API, returns the answer (M0)
│   ├── retry.py              tries a failed request again                    (M1)
│   ├── main.py               the chat loop you run in the terminal           (M4)
│   ├── tools.py              lookup_ticket and create_ticket                 (M4)
│   └── retrieval.py          finds the document passages for a question     (M5)
├── data\tickets.json         10 made-up support tickets                      (M4)
├── sample_documents\         5 to 10 made-up company documents               (M5)
├── tests\test_tools.py       automatic checks for the two tools              (M4)
├── mcp_server\server.py      offers the ticket tools over MCP                (M8)
├── evaluations\
│   ├── cases.jsonl           the test questions, one per line                (M2)
│   ├── run_evals.py          runs every test question and saves a score     (M2)
│   └── results\              saved scores, cost, and speed                   (M2)
└── docs\
    ├── decision-journal.md   for each notebook: tried, expected, happened    (M1)
    ├── decisions.md          three design-decision notes                     (M9)
    ├── risk-review.md        one page                                        (M10)
    └── manager-summary.md    one page                                        (M10)
```

---

### Start here: your first session

This takes about 90 minutes. At the end, your own program sends a question to the model and prints the answer. Run every command in PowerShell.

**Step 1. Check your tools.** Run `git --version` and `uv --version`. Each should print a version number. **uv** is a tool that installs Python and Python packages for one project. If `uv` is missing, install it with this command, then close and reopen PowerShell:

```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

**Step 2. Create the project.** These commands create the folder, set it to use Python 3.12, and install three packages. `anthropic` is the official Python library for calling the API. `python-dotenv` reads your API key from the `.env` file. `pytest` runs automatic tests, and `--dev` marks it as a package for development only.

```powershell
cd C:\Projects\Personal
uv init claude-capstone --python 3.12
cd claude-capstone
uv add anthropic python-dotenv
uv add --dev pytest
```

`uv init` also makes the folder a Git repository and creates a sample file named `main.py` (older uv versions call it `hello.py`). Delete that sample file, because your code goes in the `app` folder.

**Step 3. Create the folders.**

```powershell
New-Item -ItemType Directory app, data, sample_documents, tests, mcp_server, evaluations\results, docs
New-Item app\__init__.py
```

**Step 4. Store your API key safely.** First tell Git to ignore the key file, then create it.

```powershell
Add-Content .gitignore ".env"
code .env
```

Put these two lines in `.env`, using your own key from the Claude Console. You created it in [lesson 2 of the API course](../02_BuildingWithTheClaudeAPI/02-getting-an-api-key.md).

```text
ANTHROPIC_API_KEY=sk-ant-api03-your-key-here
CLAUDE_MODEL=claude-haiku-5-5
```

**Step 5. Write your first API call.** Create `app\client.py` with this code. Type it yourself rather than pasting it, because typing makes you read each line.

```python
import os
from anthropic import Anthropic
from dotenv import load_dotenv

load_dotenv()
client = Anthropic()
MODEL = os.environ.get("CLAUDE_MODEL", "claude-haiku-5-5")


def ask(question: str) -> str:
    response = client.messages.create(
        model=MODEL,
        max_tokens=500,
        messages=[{"role": "user", "content": question}],
    )
    return response.content[0].text


if __name__ == "__main__":
    print(ask("In one sentence, what is prompt caching?"))
```

| Line | What it does |
|---|---|
| `load_dotenv()` | Copies the two lines from `.env` into the program's settings, so the key never appears in the code. |
| `client = Anthropic()` | Creates the connection to the API. It finds `ANTHROPIC_API_KEY` by itself. |
| `MODEL = ...` | Reads the model name from `.env`. Haiku is the cheapest current model, so it is right for learning. |
| `client.messages.create(...)` | Sends one request: which model to use, the longest reply allowed (`max_tokens`, where a token is a word piece), and your message. This is the call from [lesson 3](../02_BuildingWithTheClaudeAPI/03-making-a-request.md). |
| `response.content[0].text` | Takes the text of the reply out of the response. |
| `if __name__ == "__main__":` | Runs the last line only when you start this file directly, not when another file imports `ask`. |

**Step 6. Run it.**

```powershell
uv run python -m app.client
```

`uv run` starts Python inside the project's own environment, so the packages from step 2 are found. One sentence about prompt caching should appear. If you see `authentication_error`, the key in `.env` is wrong or has a typo.

**Step 7. Save your work in Git.**

```powershell
git add .
git status
git commit -m "First API call"
```

**Warning:** check the `git status` list before you commit. If `.env` appears in it, stop and fix `.gitignore` first. A committed key can be copied by anyone who sees the repository, even after you delete the file, because Git keeps the history.

If you want a backup on GitHub, `gh repo create claude-capstone --private --source . --push` creates a private repository there and uploads your work.

**Milestone 0 is done when** `uv run python -m app.client` prints an answer and `git log` shows your first commit.

---

### The milestones

Do each milestone right after the course chapter in the "Do it after" column. The chapters belong to [Building with the Claude API](https://academy.claude.com/courses/building-with-the-claude-api), and your notes for it are in the [course index](../02_BuildingWithTheClaudeAPI/README.md). A chapter name becomes a link to your notes once you have written notes for its first lesson. The dates match the study plan, but the order matters more than the dates. "Cookbook phase" points to the [Cookbook build-along plan](../cookbook-build-along.md#the-plan-phase-by-phase), which lists the notebooks to study first and the exact files to build.

| # | Dates | Do it after | Cookbook phase | What you add | Done when | Status |
|:---:|:---|:---|:---:|:---|:---|:---|
| M0 | Nov 8 | [API course lesson 3, Making a request](../02_BuildingWithTheClaudeAPI/03-making-a-request.md) | 0 | The project and your first API call | The first session above is complete | Not started |
| M1 | Nov 9 – Nov 12 | API chapter 1, Accessing Claude with the API (lessons 4–8) | 1 | A system prompt, retries in `retry.py`, and replies in a fixed JSON shape | A failed request is tried again, and you can explain why | Not started |
| M2 | Nov 13 – Nov 15 | Chapter 2, Prompt evaluation (lessons 9–14) | 2 | The first 10 test questions in `cases.jsonl` and `run_evals.py` | One command prints a score out of 10 | Not started |
| M3 | Nov 16 – Nov 17 | Chapter 3, Prompt engineering techniques (lessons 15–19) | 3 | Documents and instructions wrapped in XML tags in the system prompt | You reran the tests and wrote down whether the score changed | Not started |
| M4 | Nov 18 – Nov 21 | Chapter 4, Tool use with Claude (lessons 20–31) | 4 | `lookup_ticket`, `create_ticket` with the approval gate, the chat loop in `main.py`, and two tests | The second and third exchanges in the example above work | Not started |
| M5 | Nov 22 – Nov 24 | Chapter 5, RAG and Agentic Search (lessons 32–38) | 5 | Search over the documents in `sample_documents`, plus 3 test questions the documents can't answer | The first and last exchanges in the example work | Not started |
| M6 | Nov 25 – Nov 26 | Chapter 6, Features of Claude (lessons 39–46) | 6 | Citations in every answer and prompt caching | You saved the cost per question with and without caching | Not started |
| M7 | Nov 27 – Nov 29 | Chapter 9, Agents and workflows (lessons 61–67) | 7 | A router that sends each question to document search or to the ticket tools, plus a filter that refuses misuse | 3 misuse test questions pass | Not started |
| M8 | Dec 1 – Dec 6 | Chapter 7, Model Context Protocol (lessons 47–56), and the [Introduction to MCP course](https://academy.claude.com/courses/introduction-to-model-context-protocol) | none | The ticket tools offered through an MCP server | Claude Code can look up a ticket through your server | Not started |
| M9 | Dec 7 – Dec 12 | The cloud course: [Bedrock](https://academy.claude.com/courses/claude-with-amazon-bedrock) or [Vertex AI](https://academy.claude.com/courses/claude-with-google-cloud-s-vertex-ai) | 8 | Cost and speed measured for Haiku and one larger model, and the three decision notes | `docs\decisions.md` has three notes based on your numbers | Not started |
| M10 | Dec 13 – Dec 14 | Everything above | none | About 25 test questions in total, the risk review, and the manager summary | All three write-ups exist and the tests run cleanly | Not started |

**The test question file.** `cases.jsonl` holds one test question per line, written in JSON (a text format for data). JSONL means "JSON Lines". For example:

```text
{"id": "doc-01", "question": "How long do I have to ask for a refund?", "expected": "30 days", "kind": "document"}
{"id": "none-01", "question": "What is the CEO's salary?", "expected": "says it cannot answer", "kind": "unanswerable"}
```

**If you fall behind,** skip M7 first, because the exam needs it least. Never skip M4 or M6. Tools, approval, and caching appear across several exam domains.

---

### Milestone 8: the MCP server

**MCP** (Model Context Protocol) is a standard way to offer tools to any AI app. In M4, only your own app can use `lookup_ticket`. In M8, you wrap the same function in a small server so that other apps, such as Claude Code, can use it too.

1. Install the MCP library with `uv add "mcp[cli]"`.
2. In `mcp_server\server.py`, create a server with `FastMCP` and mark `lookup_ticket` as a tool. The MCP course shows how. Import the function from `app\tools.py`; don't copy it.
3. Connect the server to Claude Code. Everything after `--` is the command that starts your server:

   ```powershell
   claude mcp add tickets -- uv --directory C:\Projects\Personal\claude-capstone run python -m mcp_server.server
   ```

4. Open Claude Code and ask, "What is the status of ticket 1042?" It should call your tool.

Leave `create_ticket` out of the MCP server, or keep its approval gate. An app that connects to your server should not be able to change data without a person agreeing.

---

### Milestone 10: the three write-ups

These short documents cover the exam's Governance and Stakeholder domains, which together make up about 28% of the exam (an unofficial estimate). Write them in plain words, as if for a colleague.

| File | What goes in it | Length |
|---|---|---|
| `docs\decisions.md` | Three design-decision notes, often called *ADRs* (architecture decision records). Write one each on model choice, deployment platform (the API directly, Bedrock, or Vertex AI), and how the app finds documents. | Half a page each |
| `docs\risk-review.md` | What data the app sees. What happens if a document contains hidden instructions, such as "ignore your rules" (this is called *prompt injection*). Why the approval gate exists. What you log. What you would change before real users. | One page |
| `docs\manager-summary.md` | The problem, what the app does, the cost per question from your M9 numbers, the main risks, how you would roll it out, and how you would measure success. | One page |

Each decision note answers five questions:

1. What problem are we solving?
2. What options did we consider?
3. Which did we choose, and why?
4. What are its limits?
5. What evidence would make us change it?

---

### Safety rules

- **Use made-up data only.** Write the documents and tickets yourself for a made-up company. Never use real company or customer data.
- **Keep the key in `.env` only.** Never put it in code, a notebook, or a chat message.
- **Set a monthly spend limit** in the Claude Console before M1. While learning, a few dollars a month is enough.
- **Use Haiku** unless a milestone asks you to compare models, as M9 does.
