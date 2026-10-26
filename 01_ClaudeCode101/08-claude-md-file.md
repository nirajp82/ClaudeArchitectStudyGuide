# Lesson 8 — The CLAUDE.md file

**Course:** [Claude Code 101](https://academy.claude.com/courses/claude-code-101) &nbsp;·&nbsp; **Chapter 4:** Customizing Claude Code &nbsp;·&nbsp; **Completed:** October 18, 2026

| Previous | Course | Next |
|:---|:---:|---:|
| [← Code review](07-code-review.md) | [📚 Course index](README.md) | [Subagents →](09-subagents.md) |

---

**On this page**

| # | Section |
|:---:|:---|
| 1 | [Revision summary](#revision-summary) |
| 2 | [The big picture](#the-big-picture) |
| 3 | [Who's who](#whos-who) |
| 4 | [1. The problem: Claude Code forgets everything between sessions](#1-the-problem-claude-code-forgets-everything-between-sessions) |
| 5 | [2. What a CLAUDE.md file is, and how Claude Code uses it](#2-what-a-claudemd-file-is-and-how-claude-code-uses-it) |
| 6 | [3. What to write in it: the course's example](#3-what-to-write-in-it-the-courses-example) |
| 7 | [4. Two CLAUDE.md files: one for the team, one just for you](#4-two-claudemd-files-one-for-the-team-one-just-for-you) |
| 8 | [5. Three tips for a good CLAUDE.md](#5-three-tips-for-a-good-claudemd) |
| 9 | [Recap](#recap) |
| 10 | [My notes / practice](#my-notes--practice) |
| 11 | [FAQ](#faq) |

---

### Revision summary

#### In one sentence

CLAUDE.md is a plain text file in your project where you write the facts and rules Claude Code needs to know, such as the command that runs your tests, and Claude Code reads that file automatically at the start of every conversation, so you never have to explain those things again.

#### What `CLAUDE.md` is and why you need it

Every Claude Code session (one run, from typing `claude` until you close it or type `/clear`) starts with no memory of earlier sessions. Without notes, Claude Code re-explores your project, guesses how things are done, and repeats mistakes you already corrected. `CLAUDE.md` fixes this.

- **What it is:** a plain text file of project notes, written in Markdown, in the project's top folder, such as `journal-app/CLAUDE.md` (or `journal-app/.claude/CLAUDE.md`). The course calls it an *onboarding script*: what you'd tell a new teammate on day one.
- **How it is used:** Claude Code reads it automatically at every start and sends its text to the model with your request. The model never opens the file.
- **Warning:** it is advice, not a lock. The model tries to follow it, and vague or conflicting rules are followed less. To block an action for sure, use a *deny rule* in a settings file, or a *hook* (a script Claude Code runs automatically that can stop an action).

#### Creating and filling it

- **Create it** by typing `/init`. Claude Code reads your project and writes a starting file; if one exists, it suggests improvements.
- **Write in it** the project's tools, exact commands (such as `pnpm dev`, `pnpm test`, `pnpm lint`), and code style rules. Above all, write rules Claude Code can't guess from the code, such as "use server actions instead of API routes."
- **Check what loaded** with `/context`, under "Memory files."

#### The different `CLAUDE.md` files

| File | Where it is | Applies to | Shared? |
|---|---|---|---|
| User file ("user" means you, not your app's users) | `~/.claude/CLAUDE.md`; Windows: `C:\Users\you\.claude\CLAUDE.md` | You, in every project | No |
| Project file | The project's top folder, such as `journal-app/CLAUDE.md` | Everyone, this project only | Yes, through Git |
| Local file | `journal-app/CLAUDE.local.md`, listed in `.gitignore` | You, this project only | No |
| Company file (*managed policy*) | Windows: `C:\Program Files\ClaudeCode\CLAUDE.md`; Mac: `/Library/Application Support/ClaudeCode/CLAUDE.md` | Everyone; can't be turned off | Installed by IT |

- **The files add up;** none replaces another. If two disagree, the model may follow either, so keep them consistent. Files in folders above the start folder load too, and a subfolder's file loads once Claude Code works there.

#### When to use which file

To choose, ask: "Would this be true for anyone working on this project?"

- **Use the project file** (`journal-app/CLAUDE.md`) when the rule is true for anyone on this project. For example: "Run tests with `pnpm test`" or "Use server actions instead of API routes."
- **Use the user file** (`C:\Users\you\.claude\CLAUDE.md`) when the rule is your personal taste and you want it in every project. For example: "Write short code comments in plain English."
- **Use the local file** (`journal-app/CLAUDE.local.md`) when the note is personal and only about this project, and teammates must not get it. For example: the login you use for testing.
- **Use the company file** when IT needs a rule for every developer that nobody can turn off. For example: "Never paste customer data into prompts."
- **Use a deny rule or a hook instead of any `CLAUDE.md`** when an action must be blocked for sure, because `CLAUDE.md` is only advice.

#### Tips for a good `CLAUDE.md`

1. **Save a rule after correcting Claude Code twice:** "Add to CLAUDE.md: only use server actions instead of API routes." Every future session starts with it. Saying "Remember …" instead saves it to *auto memory*, Claude Code's own notes (`MEMORY.md` in `~/.claude/projects/<project>/memory/`), seen only by you on this computer. `/memory` shows all these files and turns auto memory on or off.
2. **Point to other files with `@`.** `@README.md` makes Claude Code also read that file, so information lives in one place. Paths start from the `CLAUDE.md`'s folder, links go up to four levels deep, and outside paths need your approval once. Linked files load at the start, so they still use context space.
3. **Start a new project without one.** Notice what you keep correcting, then run `/init` and add only that.
4. **Keep it short:** under 200 lines per file. Its text is sent every session, and long files are followed less reliably.

#### Exam takeaways

- **A team sees the same Claude Code mistakes across developers.** Put shared rules in the project `CLAUDE.md` and commit it, turn repeated review findings into rules, and keep personal preferences in each developer's user file. (Developer Productivity & Operational Enablement)
- **A security lead asks if a `CLAUDE.md` rule can stop edits to production settings.** No, it is only advice. A deny rule in `.claude/settings.json`, such as `"deny": ["Edit(./config/production.json)"]`, blocks it for the project; the same rule in IT's `managed-settings.json` blocks it company-wide and developers can't override it. (Governance, Safety & Risk)
- **An architect needs shared rules across 20 repositories.** Write company rules once in the company `CLAUDE.md`, keep each repository's file short and specific, link long docs with `@` only when needed, and move rarely used instructions into skills, which load only when used. (Solution Design & Architecture)

---

### The big picture

| Part | What it means in plain words |
|---|---|
| **1. The problem** | Every time you start Claude Code, it has forgotten your project. It looks around and guesses again. |
| **2. What `CLAUDE.md` is** | A text file of notes in your project folder. Claude Code reads it by itself, before you type. |
| **3. What goes in it** | The project's tools, the commands to run, and your rules for writing code. |
| **4. Two files** | One `CLAUDE.md` **in your project folder**, shared with the team. One **in your home folder**, just for you, used in every project. |
| **5. Tips** | Add a rule when you correct Claude Code twice. Point to other files with `@`. Start a new project without one. |

#### The running example: a journal app

The course uses a small diary website:

```text
journal-app/                 ← the project folder (the "root")
├── CLAUDE.md                ← the notes file this lesson is about
├── README.md                ← a description of the project, for humans
├── package.json             ← list of outside code packages the app uses
├── app/
│   ├── page.tsx             ← the home page
│   └── actions.ts           ← code that saves and deletes entries
└── db/schema.ts             ← what the database tables look like
```

You don't need to know these tools. Just know each project picks its own:

| Tool | What it does | Everyday comparison |
|---|---|---|
| **Next.js 15** | The framework the website is built with | The brand of kit the house is built from |
| **Tailwind** | Sets colors, sizes, and spacing on pages | The paint and furniture style |
| **Drizzle ORM** | Lets the code read and write the database | The filing clerk who fetches and stores records |
| **pnpm** | Runs commands like `pnpm test` (other projects use `npm` or `yarn`) | Which remote control the TV uses |

#### The one rule Claude Code can't guess

In this kind of app, there are **two common ways to save or delete data**. Both work. The team simply picked one:

| | ❌ API route (a common choice, **not** this project's) | ✅ Server action (**this project's** choice) |
|---|---|---|
| **What it is** | A separate file that works like a small web address. The page sends a request to that address. | A function the page calls directly by name. |
| **Where Claude Code would put "delete entry"** | A **new file**: `app/api/entries/delete/route.ts` | A **new function** `deleteEntry` in the **existing** file `app/actions.ts` |
| **Everyday comparison** | Phoning the shop's order line | Telling the shop assistant standing next to you |

Think of a café that only takes card. Cash works at most cafés, so a new staff member would accept it, unless someone told them "card only." Server actions are this project's "card only" rule. Nothing in the code makes it obvious, so Claude Code would likely guess API routes, the more common choice. **That's exactly the kind of rule that belongs in `CLAUDE.md`.**

> 💡 **You've already seen one.** This study repo has its own: `ClaudeArchitectStudyGuide/CLAUDE.md`. It holds rules like "every lesson ends with an FAQ" and "define every technical term the first time." Claude Code reads it every time it starts in this folder, which is why every lesson has the same layout without anyone explaining it again.

---

### Who's who

| Player | Where it lives | What it does with `CLAUDE.md` |
|---|---|---|
| 🧑 **You** | At your computer | **Write** the notes (or ask Claude Code to). |
| 👥 **Your teammates** | Their own computers | Get the **same** project `CLAUDE.md` through Git, so their Claude Code follows the same rules. |
| 💻 **Claude Code** | The program on your computer | **Finds and reads** the file when it starts, and sends its text to the model. Can **edit** it when you ask. |
| ☁️ **The model** | Anthropic's servers | **Reads the text** and tries to follow it. Never opens the file itself. |
| 🏢 **Your company's IT team** (optional) | — | Can put a company-wide `CLAUDE.md` on everyone's computer (section 4, extras). |

---

### 1. The problem: Claude Code forgets everything between sessions

Imagine a **temp worker** who forgets everything overnight. Each morning you'd re-explain where things are and how you like them done, unless you leave a **note on the desk**. `CLAUDE.md` is that note.

A **session** is one run of Claude Code, from typing `claude` until you close it or type `/clear`. Each new session starts with an empty context window ([lesson 6](06-context-management.md)).

**Without `CLAUDE.md`**, you type "Add a delete button for journal entries," and Claude Code:
1. Opens `package.json` to find the project's tools.
2. Checks whether tests run with `npm`, `yarn`, or `pnpm`.
3. Searches for how saving already works.
4. **Guesses.** Many Next.js projects use API routes, so it creates `app/api/entries/delete/route.ts`. Wrong for this project.

You correct it. **Tomorrow, in a new session, it guesses wrong again.**

**With `CLAUDE.md`**, it already knows "pnpm," "Next.js, Tailwind, Drizzle," and "use server actions," so it adds a `deleteEntry` function to `app/actions.ts` the first time.

---

### 2. What a CLAUDE.md file is, and how Claude Code uses it

- A **text file** named exactly `CLAUDE.md`. The `.md` means **Markdown**: plain text where `#` makes a heading and `-` makes a bullet.
- It sits in the project's **root**: the top folder, where `package.json` is. For the example, `journal-app/CLAUDE.md`.
- The course calls it an **onboarding script**: what you'd tell a new teammate on day one.

#### How it gets to the model

1. **You** type `claude` in `journal-app/`.
2. **Claude Code** finds `journal-app/CLAUDE.md` and reads it. It always looks; nobody has to ask.
3. **You** type your request.
4. **Claude Code** sends the model the file's text **plus** your request (the course says the contents are *"appended to your prompt"*). Simplified:

```text
[Claude Code's built-in instructions, from Anthropic]

[Text of journal-app/CLAUDE.md]
  # Project
  This is a Next.js 15 app using the App Router, Tailwind, and Drizzle ORM.
  ...
  - Use server actions instead of API routes where possible

You: Add a delete button for journal entries.
```

So the model reads your rules **before** your request, in every session.

> ⚠️ **It's advice, not a lock** (this is from the official Claude Code documentation, not the course). The model **tries** to follow `CLAUDE.md`; vague or contradictory rules get followed less. To **block** something for sure, use a **hook**: a script Claude Code runs automatically that can stop an action (lesson 12).

#### Create one with /init

Type `/init` in Claude Code. It reads your project and writes a starting `CLAUDE.md` with the build commands, test commands, and habits it finds. Then delete what you don't need and add what it **couldn't** work out, like "use server actions." If a `CLAUDE.md` exists, `/init` suggests improvements instead of replacing it.

**Not in the course, from the official Claude Code documentation:** the project file can also be `journal-app/.claude/CLAUDE.md`. Type `/context` and look under **Memory files** to see which ones loaded.

---

### 3. What to write in it: the course's example

`journal-app/CLAUDE.md`:

```markdown
# Project

This is a Next.js 15 app using the App Router, Tailwind, and Drizzle ORM.

# Commands
- Dev server: `pnpm dev`
- Run tests: `pnpm test`
- Lint: `pnpm lint`

# Code Style
- Use 2-space indentation
- Prefer named exports
- All API routes go in app/api/
- Use server actions instead of API routes where possible
```

![A CLAUDE.md file open in VS Code with Project, Commands, and Code Style sections](images/08-claude-md-example.png)

| Part | What it means | What it saves Claude Code from |
|---|---|---|
| **Project** | The toolbox. (The **App Router** is how Next.js 15 organizes pages into folders under `app/`.) | Opening files to find out |
| **Commands** | Exactly how to start the app on your computer (`pnpm dev`), run tests, and run the **linter** (a tool that checks code for mistakes and messy style) | Guessing `npm` vs. `pnpm` |
| **Code Style** | Team habits: 2-space indents, `export function X` instead of `export default`, and server actions over API routes | Writing code you then fix |

You ask: *"Create a component for a journal entry card."* (A **component** is one reusable piece of a web page.)

| Without `CLAUDE.md` | With `CLAUDE.md` |
|---|---|
| Opens files to find out how styling works | Already knows: Tailwind |
| Might write `export default function EntryCard()` | Writes `export function EntryCard()` |
| Might add an API route to save data | Uses a server action |
| You correct it, and again next session | Right the first time |

The course says Claude Code then *"does a better job right off the bat."*

---

### 4. Two CLAUDE.md files: one for the team, one just for you

Some rules are about the **project** ("use server actions"). Some are about **you** ("I like short code comments"). The course calls these the **project file** and the **user file**. **"User" means you**, the person using Claude Code, not the users of your app.

```text
C:\Users\you\                          ← your home folder (Mac: /Users/you/)
├── .claude\
│   └── CLAUDE.md                      ← ① USER file: just you, EVERY project
│
└── Projects\
    ├── journal-app\
    │   └── CLAUDE.md                  ← ② PROJECT file: journal-app only, shared
    └── shopping-app\
        └── CLAUDE.md                  ← another PROJECT file: shopping-app only
```

- The **user file** ① is in a hidden `.claude` folder in your **home folder**, not in any project. The course writes it as `~/.claude/CLAUDE.md` (`~` = your home folder).
- Start Claude Code in `journal-app` and it reads **both** ① and ②. Start it in `shopping-app` and it reads ① and that project's file.

| | ① User file | ② Project file |
|---|---|---|
| **Full path (Windows)** | `C:\Users\you\.claude\CLAUDE.md` | `C:\Users\you\Projects\journal-app\CLAUDE.md` |
| **Full path (Mac)** | `/Users/you/.claude/CLAUDE.md` | `/Users/you/Projects/journal-app/CLAUDE.md` |
| **Who writes it** | You | You and your teammates |
| **Applies to** | Only you, in **all** your projects | Everyone, in **this** project only |
| **Shared?** | ❌ Stays on your computer | ✅ Saved in **Git** with the code. You run `git add CLAUDE.md` and `git commit`, then push; teammates get it when they download the latest code. |
| **Example rule** | "Write short code comments in plain English." | "Use server actions instead of API routes." |

**Which file should a rule go in?** Ask: *"Would this be true for anyone working on this project?"* Yes → project file. No, it's my taste → user file.

> 🧠 **Remember this:** **Team rules → the project folder. My habits → my home folder.**

**Not in the course, from the official Claude Code documentation:** two more files.
- **Local file**, `journal-app/CLAUDE.local.md`: only you, only this project, e.g. your test login. Add it to `.gitignore` (the list of files Git ignores) so it's never committed.
- **Company file** (the official Claude Code documentation calls it a *managed policy*), put on your computer by IT (Windows: `C:\Program Files\ClaudeCode\CLAUDE.md`; Mac: `/Library/Application Support/ClaudeCode/CLAUDE.md`): applies to everyone, can't be switched off.

All the files **add up**; none replaces another. If two disagree, the model may follow either, so keep them consistent. Claude Code also reads `CLAUDE.md` files in folders **above** where you started, and a `CLAUDE.md` in a **subfolder** (like `journal-app/app/CLAUDE.md`) once it works on files there.

---

### 5. Three tips for a good CLAUDE.md

#### Tip 1: When you correct Claude Code twice, save the rule

*From the course:* Claude Code keeps making API routes. You type:

```text
Ok, put in the CLAUDE.md file to only use server actions instead of API routes
```

![Asking Claude Code to add "only use server actions instead of API routes" to CLAUDE.md](images/08-save-rule-to-claude-md.png)

Claude Code adds the line to `journal-app/CLAUDE.md`, so every future session starts with it.

**Not in the course, from the official Claude Code documentation: the words matter.**

| You type… | Saved where | Who sees it |
|---|---|---|
| "Add to CLAUDE.md: use pnpm." | `journal-app/CLAUDE.md` | You, and your team once committed |
| "Remember: use pnpm." | Claude Code's own notes, called **auto memory**: `MEMORY.md` in `C:\Users\you\.claude\projects\<project>\memory\` | Only you, on this computer |

**Auto memory** is notes Claude Code writes **for itself**. Type `/memory` to see all these files and turn auto memory on or off.

#### Tip 2: Point to other files with @

```markdown
Please read if you need more info: @README.md
```

Claude Code then also reads `journal-app/README.md`. You keep one copy of the information. The path starts from the folder the `CLAUDE.md` is in (so `@docs/api.md` in `journal-app/CLAUDE.md` means `journal-app/docs/api.md`), and linked files can link others up to four levels deep. If a path points **outside** your project, Claude Code asks you to approve it the first time. ⚠️ Linked files load at the start too, so they **still use context space**.

#### Tip 3: Start a new project without one

If you write a long `CLAUDE.md` on day one, you'll fill it with things Claude Code gets right anyway. Work without one first, notice what you keep correcting, then run `/init` and add only those things.

**Keep it short:** its text is sent in **every** session. The docs suggest **under 200 lines** per file; long files are also followed less reliably.

| Do this | Why | Example |
|---|---|---|
| **Be specific** | The model can't follow a vague rule. | "Use 2-space indentation," not "format code nicely." |
| **Write commands exactly** | Claude Code can run them without guessing. | "Run tests: `pnpm test`" |
| **Only add what Claude Code gets wrong** | Every line uses context in every session. | Add "server actions" only after it was needed. |
| **Commit the project file** | The whole team gets the same rules. | `git add CLAUDE.md` |
| **Keep personal habits out of the project file** | Teammates don't need your preferences. | Comment style → `~/.claude/CLAUDE.md` |

#### Common mix-ups

| ❌ Wrong idea | ✅ What really happens |
|---|---|
| "I have to tell Claude Code to read `CLAUDE.md`." | It reads it automatically every time it starts. |
| "The 'user file' is about the users of my app." | "User" means **you**. It's in your home folder, not in any project. |
| "The user file replaces the project file." | They **add up**. Claude Code reads both. |
| "`@` links save context space." | Linked files load at the start too. |
| "`CLAUDE.md` rules are always obeyed." | They're advice. To block something for sure, use a hook. |

#### Test yourself

<details>
<summary>1. You like short, plain-English code comments in every project. Which file should that rule go in, and where is it?</summary>

The user file, `~/.claude/CLAUDE.md`. On Windows that's `C:\Users\you\.claude\CLAUDE.md`.
</details>

<details>
<summary>2. Your teammate downloads the journal app. Which of your CLAUDE.md files do they get?</summary>

Only the project file, `journal-app/CLAUDE.md`, because it's committed to Git. Your user file stays on your computer.
</details>

<details>
<summary>3. You've told Claude Code "use pnpm, not npm" three sessions in a row. What should you do?</summary>

Ask it to add the rule to `CLAUDE.md`: "Add to CLAUDE.md: use pnpm, not npm."
</details>

<details>
<summary>4. Why does the course recommend starting a project without a CLAUDE.md?</summary>

So you see what you actually keep correcting. Only those rules are worth adding.
</details>

---

### Recap

- **The problem:** every session starts empty, so Claude Code re-explores, guesses, and repeats mistakes.
- **What it is:** a text file of notes in the project root. Claude Code reads it at every start and sends its text with your request. `/init` creates a first version.
- **What goes in it:** tools, exact commands, and rules. Short and specific.
- **Two files:** the project file (`journal-app/CLAUDE.md`, shared through Git) and the user file (`~/.claude/CLAUDE.md`, just you, every project). Both are read.
- **Tips:** save a rule after two corrections, link other files with `@`, start without one.

---

## My notes / practice

- [ ] Open this repo's `CLAUDE.md` and find the tools, commands, and rules parts.
- [ ] Type `/memory` and see which memory files exist for me.
- [ ] Create my user file, `C:\Users\<me>\.claude\CLAUDE.md`, with one personal preference.
- [ ] In a test project, type `/init` and read what it creates.

---

## FAQ

In these answers, **Claude Code** means the program on your computer. **The model** means the AI on Anthropic's servers.

**Q1. What is a CLAUDE.md file?**
A text file of notes in your project's main folder (e.g. `journal-app/CLAUDE.md`) that Claude Code reads automatically every time it starts. It lists the project's tools, commands, and rules.

**Q2. What problem does CLAUDE.md solve?**
Every session starts with no memory of earlier ones. Without `CLAUDE.md`, Claude Code looks around and guesses each time, so you give the same corrections again and again.

**Q3. Does the model open the CLAUDE.md file?**
No. Claude Code reads the file on your computer and sends its text to the model together with your request.

**Q4. Does Claude Code always follow what's in CLAUDE.md?**
It tries, but nothing forces it. Vague or contradictory rules are followed less often. To block an action for sure, use a hook.

**Q5. How do I create a CLAUDE.md file?**
Type `/init`. Claude Code reads your project and writes a starting file. You can also write one by hand.

**Q6. What's the difference between the "project file" and the "user file"?**
The project file is `CLAUDE.md` inside the project folder, shared with the team through Git, used only for that project. The user file is `~/.claude/CLAUDE.md` in your home folder, just for you, used in every project.

**Q7. Does "user" in "user file" mean the users of my app, and where is the user file?**
No, "user" means you. The file is `C:\Users\<you>\.claude\CLAUDE.md` on Windows or `/Users/<you>/.claude/CLAUDE.md` on Mac. Type `/memory` to open it; if it doesn't exist yet, `/memory` creates it.

**Q8. If I have both a project file and a user file, which one wins?**
Neither. Claude Code reads both and the rules add up. If two disagree, the model may follow either, so keep them consistent.

**Q9. What does "auto memory" mean?**
Notes Claude Code writes for itself, saved in a `MEMORY.md` file under `~/.claude/projects/<project>/memory/`. Saying "remember X" goes there; saying "add X to CLAUDE.md" edits `CLAUDE.md`. `/memory` shows both.

**Q10. Do files linked with @ use up context space?**
Yes. They load at the start like `CLAUDE.md` itself. `@` keeps the file tidy but doesn't make the total smaller. Keep each `CLAUDE.md` under about 200 lines.

**Q11. (Exam angle) A team says Claude Code keeps making the same mistakes for different developers on the same project. What do you recommend?**
Put the shared rules in the project's `CLAUDE.md` and commit it to Git, so every developer's Claude Code starts with the same tools, commands, and rules. Turn repeated review findings into rules. Keep it short and specific. Personal preferences go in each developer's own `~/.claude/CLAUDE.md`. This fits the **Developer Productivity & Operational Enablement** exam domain.

**Q12. (Exam angle) A security lead wants to stop Claude Code from ever touching production settings, and asks if a CLAUDE.md rule is enough. How do you answer?**
No. A line in `CLAUDE.md` like "never edit `config/production.json`" is **advice** the model tries to follow, not a guarantee. To **block** it, use a **settings file**: a file Claude Code itself checks before every action, so the model can't talk its way past it. All of these files sit on **each developer's computer**:

| Goal | File (Windows path; Mac in brackets) | Who puts it there | Can the developer turn it off? |
|---|---|---|---|
| **Explain** the rule | `C:\Users\dev\Projects\journal-app\CLAUDE.md` | The team, through Git | Yes. And it's only advice anyway. |
| **Block** it in this project | `C:\Users\dev\Projects\journal-app\.claude\settings.json`, with a **deny rule** (below) | The team, through Git | Yes, they could edit the file. It's a team rule, not a company lock. |
| **Block** it with a script | A **hook** (lesson 12), set up in that same `settings.json` | The team | Same as above |
| **Block** it for the whole company | `C:\Program Files\ClaudeCode\managed-settings.json` (`/Library/Application Support/ClaudeCode/managed-settings.json`) | IT, on every laptop | **No.** Nothing in the developer's own settings overrides it. `Program Files` needs admin rights to change. |
| **Explain** it for the whole company | `C:\Program Files\ClaudeCode\CLAUDE.md` (`/Library/Application Support/ClaudeCode/CLAUDE.md`) | IT | No |

A deny rule inside a settings file looks like this:

```json
{
  "permissions": {
    "deny": ["Edit(./config/production.json)"]
  }
}
```

So: `CLAUDE.md` **explains** the rule; settings files and hooks **enforce** it. For "ever," put the deny rule in the company's `managed-settings.json`. This fits the **Governance, Safety & Risk** exam domain.

**Q13. (Exam angle) An architect asks how to share Claude Code rules across 20 repositories without every CLAUDE.md growing huge. How do you answer?**
A **repository** (repo) is one project folder tracked by Git, like `journal-app`. The problem: if every repo's `CLAUDE.md` repeats the company rules, all 20 files grow, and each one costs context space in every session. Split the rules by where they apply. On **one developer's computer**, that looks like this:

```text
C:\Program Files\ClaudeCode\
└── CLAUDE.md                       ← ① company rules, ONCE. IT puts the same file on every
                                       laptop. Loads in all 20 repos automatically.
C:\Users\dev\Projects\
├── journal-app\                    ← repo 1 of 20
│   ├── CLAUDE.md                   ← ② only journal-app's own rules: tools, commands
│   ├── docs\api.md                 ← ③ long doc, linked with @docs/api.md only if needed
│   └── .claude\skills\
│       └── db-migration\SKILL.md   ← ④ detailed how-to, loads only when used
└── shopping-app\                   ← repo 2 of 20, same pattern
    └── CLAUDE.md
```

| Piece | Where it lives | What goes in it | Context cost |
|---|---|---|---|
| ① **Company `CLAUDE.md`** | `C:\Program Files\ClaudeCode\CLAUDE.md` (Mac: `/Library/Application Support/ClaudeCode/CLAUDE.md`), put there by IT | Rules for every repo: "never put passwords in code" | Every session, but written once instead of 20 times |
| ② **Each repo's `CLAUDE.md`** | The repo's top folder, in Git | Only what's specific to that repo: tools, commands, local rules | Every session in that repo, so keep it short |
| ③ **`@` links** | Docs inside the repo, e.g. `journal-app/docs/api.md` | Long reference material | ⚠️ Still loads at the start, so only link what's needed |
| ④ **Skills** (lesson 10) | `journal-app/.claude/skills/<name>/SKILL.md`, committed to Git | Detailed, rarely needed steps, like "how to run a database migration" | Only the skill's name and one-line description load at the start. The full instructions load only when used. |

This fits the **Solution Design & Architecture** exam domain.

---

| Previous | Course | Next |
|:---|:---:|---:|
| [← Code review](07-code-review.md) | [📚 Course index](README.md) | [Subagents →](09-subagents.md) |
