# Capstone guide 8 — Anthropic apps

**Do it after:** Chapter 8, Anthropic apps (lessons 57–60) &nbsp;·&nbsp; **Capstone index:** [Capstone plan](../README.md)

| Previous | Capstone | Next |
|:---|:---:|---:|
| [← Guide 7: Model Context Protocol](07-model-context-protocol.md) | [Capstone index](../README.md) | [Guide 9: Agents and workflows →](09-agents-and-workflows.md) |

---

**On this page**

| # | Section |
|:---:|:---|
| 1 | [What you build in this chapter](#what-you-build-in-this-chapter) |
| 2 | [Before you start](#before-you-start) |
| 3 | [Problem 1: Decide whether computer use fits](#problem-1-decide-whether-computer-use-fits) |
| 4 | [Problem 2: Set up Claude Code for the capstone](#problem-2-set-up-claude-code-for-the-capstone) |
| 5 | [Problem 3: Use Claude Code as a reviewer](#problem-3-use-claude-code-as-a-reviewer) |
| 6 | [Problem 4: Connect your MCP server to Claude Code](#problem-4-connect-your-mcp-server-to-claude-code) |
| 7 | [Architect scenario: the shop's developers start using Claude Code](#architect-scenario-the-shops-developers-start-using-claude-code) |
| 8 | [Commit your work](#commit-your-work) |

---

### What you build in this chapter

This chapter is about apps Anthropic has already built on the API: **Claude Code**, the coding assistant in your terminal, and **computer use**, where the model operates a computer screen. You already studied Claude Code in the [Claude Code 101 notes](../../../01_ClaudeCode101/README.md), so this guide doesn't repeat them. It uses Claude Code *on* your capstone: with project rules, as a code reviewer, and connected to your own MCP server.

| File | What it does | Problem |
|---|---|---|
| `docs/computer-use-decision.md` | Your decision about computer use for Northwind | 1 |
| `CLAUDE.md` in the capstone folder | Rules Claude Code reads in every session in this folder | 2 |
| `.claude/settings.json` in the capstone folder | A rule that stops Claude Code from reading `.env` | 2 |
| `docs/review-notes.md` | What the review found and what you changed | 3 |

**Chapter done when:** Claude Code, started in the capstone folder, refuses to read `.env`, and answers `What's the status of ticket 1042?` by calling your MCP server.

---

### Before you start

1. Run `git pull`, and finish [guide 7](07-model-context-protocol.md).
2. Read your notes for chapter 8 when they exist (see the [course index](../../README.md)).
3. Check that Claude Code works: `claude --version`. If it's missing, follow your notes on [installing Claude Code](../../../01_ClaudeCode101/03-installing-claude-code.md).

---

### Problem 1: Decide whether computer use fits

**Lesson:** 57, Anthropic apps: Claude Code and computer use

**The problem:** Northwind's old billing system has no API; staff click through a web page to issue credits. A manager asks whether the model could do this with computer use. Write `docs/computer-use-decision.md` with your answer: what computer use is, when it fits, the risks, and your decision.

- **Check:** your note names at least two risks and a safer alternative.

<details>
<summary>Show the step-by-step answer</summary>

**Step 1. Understand computer use.** With **computer use**, the model gets screenshots of a computer screen and replies with actions, such as "click at this point" or "type this text". Your code, or a provided environment, carries out each action and sends a new screenshot. It's a tool loop like guide 4, where the "tool" is a whole screen.

**Step 2. Write the note.** For example:

```text
# Decision: computer use for the billing system

## When computer use fits
Only when there is no API and the task is low risk, such as reading a report from an old web page.

## Risks for issuing credits
1. It is slow and can misclick: one wrong click could credit the wrong account.
2. Anything on the screen, such as a customer's note, can carry hidden instructions (prompt injection).
3. It needs a staff login, so a mistake has a staff member's full permissions.

## Decision
Not for issuing credits. Ask the billing team for a small API with a credit limit,
and expose it as a tool with an approval gate, as in guide 4.
If computer use is ever tried, run it in a separate virtual machine with a test account and a person watching.
```

**Step 3. Know the rule of thumb.** An API tool is faster, cheaper, and easier to limit than computer use. Use computer use as a last resort, in an isolated environment, for read-only or low-risk tasks.

</details>

**Why this matters:** the exam expects you to prefer an API tool over computer use and to isolate computer use when it's unavoidable (Governance, Safety & Risk).

---

### Problem 2: Set up Claude Code for the capstone

**Lesson:** 58, Claude Code setup

**The problem:** Start Claude Code in the capstone folder and give it project rules. Create `CLAUDE.md` with the commands and rules of this project, and a settings file that stops Claude Code from reading `.env`.

- **Check:** in Claude Code, `Show me the contents of .env` is refused.

<details>
<summary>Show the step-by-step answer</summary>

**Step 1. Start Claude Code in the capstone folder.**

```bash
cd 02_BuildingWithTheClaudeAPI/00_Capstone_Plan
claude
```

**Step 2. Create `CLAUDE.md`.** You can type `/init` and let Claude Code draft it, then edit the draft. Keep it short and specific. Your [notes on CLAUDE.md](../../../01_ClaudeCode101/08-claude-md-file.md) explain where these files live and who reads them.

```text
# Northwind support assistant (capstone)

## Commands
- Run the chat: uv run python -m app.main --role customer --customer C-1001
- Run tests: uv run pytest
- Run the eval: uv run python -m evaluations.run_evals

## Rules
- I am learning: explain problems and suggest fixes, but don't write the fix unless I ask.
- Never read or print .env. It holds API keys.
- Use only made-up data in data/ and sample_documents/.
- Every tool that changes data must keep its approval gate.
```

**Step 3. Block `.env` with a deny rule.** A `CLAUDE.md` rule is only advice. A **deny rule** in a settings file is enforced by Claude Code itself. Create `.claude/settings.json` in the capstone folder:

```text
{
  "permissions": {
    "deny": ["Read(./.env)", "Read(./.env.*)"]
  }
}
```

**Step 4. Test it.** Restart Claude Code in the capstone folder and ask `Show me the contents of .env`. It should say it can't.

</details>

**Why this matters:** project rules guide the assistant, but secrets are protected with enforced deny rules, not with advice (Claude Code Configuration & Workflows).

---

### Problem 3: Use Claude Code as a reviewer

**Lesson:** 59, Claude Code in action

**The problem:** Ask Claude Code to review `app/tools.py` and `app/notes_editor.py` for security problems, without changing them. Read its findings, decide which are real, fix one yourself, and write the results in `docs/review-notes.md`.

- **Check:** `review-notes.md` lists each finding, whether you agree, and what you changed.

<details>
<summary>Show the step-by-step answer</summary>

**Step 1. Ask for a review, not a rewrite.** Press Shift+Tab until plan mode is on, so Claude Code reads but doesn't edit. Then type:

```text
Review app/tools.py and app/notes_editor.py for security problems.
For each problem: the file and line, what could go wrong, and how to fix it.
Don't change any files.
```

**Step 2. Judge every finding yourself.** Claude Code can be wrong, in both directions. For each finding, ask: can I make this go wrong on purpose? For example, try the path trick from guide 4 problem 9 again.

**Step 3. Fix one real finding yourself,** run `uv run pytest`, and write the notes:

```text
| Finding | Real? | What I did |
|---|---|---|
| create_ticket accepts a 500-word title | Yes | Added a length check and a test |
| safe_path misses symlinks | No | resolve() already follows symlinks |
```

**Step 4. Follow the loop you learned.** Explore, plan, then code, then commit, as in your notes on [explore, plan, code, commit](../../../01_ClaudeCode101/05-explore-plan-code-commit.md). Writing the fix yourself is what makes you learn it.

</details>

**Why this matters:** an AI reviewer is a second opinion, not a judge; a person checks each finding (Claude Code Configuration & Workflows).

---

### Problem 4: Connect your MCP server to Claude Code

**Lesson:** 60, Adding MCP servers to Claude Code

**The problem:** Connect the MCP server from guide 7 to Claude Code, so Claude Code itself can look up tickets.

- **Check:** in Claude Code, `/mcp` shows `tickets` as connected, and `What's the status of ticket 1042?` calls your `lookup_ticket` tool.

<details>
<summary>Show the step-by-step answer</summary>

**Step 1. Add the server.** Open a terminal in the capstone folder and run the command for your computer. Everything after `--` is the command that starts your server. `$(pwd)` on the Mac and `$(Get-Location)` on Windows fill in this folder's location for you.

**Mac:**

```bash
claude mcp add tickets -- uv --directory "$(pwd)" run python -m mcp_server.server
```

**Windows:**

```powershell
claude mcp add tickets -- uv --directory "$(Get-Location)" run python -m mcp_server.server
```

**Step 2. Check it.** Start `claude` in the capstone folder and type `/mcp`. You should see `tickets` with its two tools.

**Step 3. Use it.** Ask `What's the status of ticket 1042?`. Claude Code asks permission to use the `lookup_ticket` tool the first time. Approve it.

**Step 4. Know where it was saved.** By default, `claude mcp add` saves the server in the *local* scope: only for you, only in this folder, in your personal Claude Code settings file, not in Git. Run the command once on each computer you use. Your [notes on MCP in Claude Code](../../../01_ClaudeCode101/11-mcp.md) compare the local, project, and user scopes.

</details>

**Why this matters:** connecting the same MCP server to Claude Code proves the server is reusable across clients (Tool Design & MCP Integration).

---

### Architect scenario: the shop's developers start using Claude Code

**The scenario:** the online shop's 12 developers want to start using Claude Code on the shop's main code repository. The security lead is worried about three things: API keys in `.env` files, developers letting it run any command, and inconsistent code style. Propose a setup the whole team shares.

- **Check:** for each worry, you name the file, who writes it, and whether a developer can override it.

<details>
<summary>Show the step-by-step answer</summary>

**Step 1. Match each worry to the right control.**

| Worry | Control | File | Can a developer override it? |
|---|---|---|---|
| Keys in `.env` files | Deny rules for reading `.env` | Company-managed settings, installed by IT | No |
| Any command can run | Permission rules that allow tests and builds but ask before others | The project's `.claude/settings.json`, in Git | They can change it in a commit, which reviewers will see |
| Inconsistent style | Coding rules and commands | The project's `CLAUDE.md`, in Git | It's advice, so the code review still checks style |

**Step 2. Explain the difference between advice and enforcement.** `CLAUDE.md` is advice the model reads. Settings files are rules that Claude Code enforces. Security must use enforced rules, at the company level when it must not be switched off.

**Step 3. Add a team habit.** Changes Claude Code writes go through the same pull-request review as any other change. Repeated review comments become new lines in `CLAUDE.md`.

</details>

**Why this matters:** rolling out Claude Code to a team is a configuration and governance question: shared rules in Git, enforced limits in settings (Claude Code Configuration & Workflows).

---

### Commit your work

```bash
git add .
git status
git commit -m "Capstone guide 8: computer use decision, CLAUDE.md, deny rule, review notes"
git push
```

**Warning:** check that `.env` is not in the `git status` list before you commit.

Then mark guide 8 as done in the [capstone index](../README.md#the-chapter-guides).

---

| Previous | Capstone | Next |
|:---|:---:|---:|
| [← Guide 7: Model Context Protocol](07-model-context-protocol.md) | [Capstone index](../README.md) | [Guide 9: Agents and workflows →](09-agents-and-workflows.md) |
