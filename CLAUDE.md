# Study guide rules

This repo holds my study notes for the **Claude Architect Professional (CCAR-P)** exam. `ReadMe.md` at the root is the overall study plan. Each course has its own folder of lesson notes.

These rules apply to every lesson note, every time. The gold-standard example is **`01_ClaudeCode101/02-how-claude-code-works.md`**. When in doubt, copy how it does things.

---

## 1. When I paste a lesson: the workflow

I'll paste a lesson's **video transcript** and/or its **written course text**, sometimes with screenshots. Then:

1. **Work out the file.** Check the course folder's `README.md` progress table for the lesson number and file name. The file is `0X-lesson-name.md`, directly in the course folder.
2. **Treat the transcript as a checklist, not a draft.** It tells you *what* the lesson covers. Your job is to explain it far more clearly than the course does. Don't just tidy up the transcript.
3. **Check facts that need to be exact.** For commands, settings, keyboard shortcuts, or install steps, check the official docs (for Claude Code: `https://code.claude.com/docs`). Don't guess.
4. **Write the file** using the template in section 6.
5. **Save the images** (section 4).
6. **Update the links:**
   - In the course `README.md`, link the lesson and mark it ✅ Done.
   - In the previous lesson, check the "Next" link in **both** its header and footer.
7. **Don't commit or push** unless I ask. I commit and push myself, often. If a file changed on disk since you last read it, re-read it and build on my version.
8. **Reply briefly** (section 7).

---

## 2. How to write: plain English

Write for a **beginner**, as if explaining to a friend.

- **Short sentences. One idea per sentence. Everyday words.**
- **Plain idea first, course term second, in brackets:** "Claude looks around first (the course calls this *gathering context*)." Never lead with jargon.
- **Define every technical term the first time it appears:** "a **tool call** is a request from the model asking Claude Code to do something."
- **Explain *why*, not just *what*.** If the course says "auto-accept still asks before commands," also say why: an edit is easy to undo, a command may not be.
- **Numbered lists for steps. Bullets or tables for options.**
- **No marketing words or filler.**
- **Never make me guess what "it" or "this" means.** Name the thing.

### Always answer: who, which file, where?

My most common complaint is a lesson that's "not clear at all." The cause is almost always a short label the course uses that I can't picture. Lessons 7 and 8 both had to be fully rewritten for this reason.

| ❌ Unclear (course shorthand) | Missing | ✅ Clear |
|---|---|---|
| "A reviewer can be wrong" | **Who** is the reviewer? | "The reviewer (the AI that `/code-review` starts, not a person) can be wrong" |
| "A user file just for you" | **Which file? Where?** And "user" of what? | "A second `CLAUDE.md` in your home folder, `C:\Users\you\.claude\CLAUDE.md`. 'User' means you." |
| "The session that wrote the code" | **Which** session? | "Your Claude Code conversation, the one that wrote the code" |
| "Batch it for later" | Undefined course word | "Write it down and fix it later with other small problems (the course calls this *batching*)" |

Rules:
- **Every player gets named, every time.** In each step, say who does it: you, your Claude Code session, a separate AI, the model, a teammate. Use a **Who's who table** in **every** lesson that has more than one player, and put it near the top.
- **Every file gets a full path and a folder tree.** Show where the file sits (`journal-app/CLAUDE.md`, `C:\Users\you\.claude\CLAUDE.md`), what's in it (real example content), who writes it, and who reads it.
- **Course labels are never enough on their own.** If the course says "project file," "user file," "clean context," "reads it cold," explain what the label means in plain words the first time, and say what it does *not* mean if a beginner could misread it.
- **Explain every tool, command, and code line in the running example**, even ones the course treats as obvious (`it.skip`, `localhost`, `pnpm`, "server actions"). I can't follow an example built on words I don't know.

**Before finishing a lesson, do a beginner read-through:** read every paragraph as someone who has never coded. For each sentence ask: *Who is doing this? Which file, and where is it? Do I know every word?* If any answer is "not sure," rewrite the sentence.

### Keep it short: clear, not long

Clear doesn't mean long. My other common complaint is "the whole page is too long." Aim for **250–400 lines per lesson**.

- **Say each thing once.** Don't explain the same point in prose, then a table, then a diagram, then the recap, then the FAQ. Pick the one format that shows it best.
- **One everyday comparison per main idea**, in 1–3 sentences.
- **Don't re-teach earlier lessons.** One line plus a link: "(the context window, [lesson 2](02-how-claude-code-works.md))."
- **Extras from the docs:** only if they matter for the exam or daily use, in 1–2 lines each.
- **At most 2 diagrams per lesson.** Add "Things to notice" only when the point isn't obvious.
- **Sizes:** Revision summary 10–20 bullets. Common mix-ups 4–6 rows. Test yourself 3–4 questions. FAQ 10–13 questions, including the exam-angle ones (see section 5). Recap one short bullet per main idea.
- **Cut, don't pad:** if a sentence doesn't help me understand or remember, delete it.

### Revision summary: required in every lesson

I revise from the top of each lesson, so **every lesson starts with a `### Revision summary`** section, right after the "On this page" table and before "In one sentence." It is the one place where repeating the lesson is expected.

- **Cover every fact I'd need on the exam or in daily use:** each main idea, every command, keyboard shortcut, file path, setting, number, and ⚠️ warning, plus a one-line exam takeaway. Someone who reads only the summary shouldn't miss anything important.
- **One fact per bullet**, starting with a bold label: `- **/clear:** starts a new, empty conversation…`. Plain English, defined terms, same naming rules as the rest of the lesson.
- **Use a small table** only for a set of options that are compared side by side (permission modes, install commands, file locations).
- **Open with this line:** `*Every key fact from this lesson in one place, for quick revision. The sections below explain each point.*`
- **Keep it current:** when a lesson gets a new fact or follow-up answer, add it to the summary too.

---

## 3. How to explain: the techniques that work

Use these the way lesson 2 does. **Not every lesson needs all of them**: pick the few that make each idea click, and keep the page short (see "Keep it short" above).

| Technique | What it is | Example from lesson 2 |
|---|---|---|
| **In one sentence** | Open the lesson with the whole idea in one plain sentence. | "Claude Code works like a helper who doesn't give up after one try…" |
| **Overview table** | Before details, a table of the lesson's main parts in plain words. | "The four parts": loop, context window, tools, permissions |
| **Everyday comparison** | Compare each big idea to something from daily life. | Loop = a mechanic. Context window = a whiteboard. Tools = a friend with a wrench vs. on the phone. Permissions = keys for a new assistant. |
| **One running example** | Pick one realistic task and use it through the whole lesson. | "The login test is failing. Fix it." |
| **Concrete details** | Real file names, real file contents with line numbers, the exact command, the exact output. Show exactly what happens, not "it searches" or "it sends the result." | The `my-app` folder tree, the buggy lines of `login.js`, the exact `npm test` output |
| **Who's who table** | When more than one player is involved (you, Claude Code, your computer, the model, outside services, a separate AI reviewer, teammates): where each lives, what it does, an example. Put it near the top of the lesson, not buried late. | Section 5, "Who's who" |
| **Step-by-step walkthrough** | For a process, one sub-section per step. In each, show what's asked, what happens, and what is sent or produced, using exact text. | Section 5, "The five rounds" table |
| **"What goes where" table** | When data moves between places, list what moves and what stays. | "Sent to Anthropic's servers" vs. "Never left your computer" |
| **🧠 Remember this** | A one or two-line memory hook in a quote block. | "Brain on the server. Hands on your computer." |
| **Common mix-ups table** | ❌ Wrong idea vs. ✅ What really happens. | "My tests run in the cloud." → "They run on your computer." |
| **Test yourself** | 3–4 quiz questions with answers hidden in `<details>`. | Section 5, "Test yourself" |
| **Do / Why / Example table** | For practical advice. | Lesson 8's "Which file should a rule go in?" |
| **⚠️ Warnings** | Call out real risks with a concrete example of what goes wrong. | Turning off permission questions → deleted files |

**When I ask a follow-up question about a lesson**, answer it in chat first. If I want it added, add it to the right section of that lesson, plus matching FAQ, mix-up, and test-yourself entries.

---

## 4. Diagrams and images

### Diagrams: always Mermaid

Draw diagrams in **Mermaid** (a ` ```mermaid ` code block), never as plain-text or box-drawing art. GitHub turns Mermaid into a real picture.

| To show… | Use | Example in lesson 2 |
|---|---|---|
| A process or loop | `flowchart TD` | — (lesson 1's agent loop) |
| Where things live and how they connect | `flowchart LR` with a `subgraph` per place | Lesson 6: main context window vs. subagent's context window |
| Who sends what to whom, step by step | `sequenceDiagram`, one column per player | Section 5's five-round timeline |
| A decision | `flowchart TD` | Lesson 6: "Compact or clear?" |

- Use emoji in node labels for players: 🧑 You, 💻 Claude Code, 🗂️ Your files & terminal, ☁️ Model, 🔌 Tool servers.
- Use `<br/>` for line breaks inside nodes.
- After a diagram, add "Things to notice" bullets when the point isn't obvious.
- Keep ` ```text ` blocks **only for literal content**: folder trees, command output, the exact text of a message.

### Images: keep every course image

- Every screenshot or diagram in the course lesson should appear in the notes. They make lessons easier to understand.
- **If I paste screenshots in chat:** save them to the course's `images/` folder as `0X-short-name.png` (for example, `images/03-login-method.png`) and embed them: `![What it shows](images/03-login-method.png)`.
- **If I uploaded an image through GitHub** (a `github.com/user-attachments/...` URL), keep it exactly as is.
- **If the lesson text mentions an image I didn't paste:** leave a marker where it goes, such as `<!-- IMAGE: caption → images/03-name.png -->`, and ask me for it.

---

## 5. FAQ rules

Every lesson ends with an FAQ. Lesson 2's FAQ is the model.

- Format: `**Q1. Question?**` in bold, answer on the next line. Number them in order, with no gaps or letters (no "Q21a"). Renumber if you insert one.
- **10–13 questions in total**, including the exam-angle ones. Cover the main ideas and the terms most likely to confuse me, plus every follow-up question I asked about the lesson. Don't make a question for every small fact in the lesson.
- Answers stand on their own: someone reading only the FAQ should understand. Plain English, **1–3 sentences**, with an example where it helps. Use a short list when an answer has several parts.
- Order the questions to follow the lesson.
- **Exam-angle questions are protected.** Never cut or shorten them when trimming a lesson; they matter most for the exam.
- End with **3 `(Exam angle)` questions** that link the lesson to an exam domain, such as **Governance, Safety & Risk**. Frame them as a real scenario: "A security team asks… How do you answer?"

### How to word a question

These rules apply to FAQ questions **and** "Test yourself" questions. Write each question the way a beginner would ask it out loud.

| Rule | ❌ Don't | ✅ Do |
|---|---|---|
| Asking about a term? Put the term in quotes. | What is a tool call? (reads like "What is the tool called?") | What does "tool call" mean? |
| Name the thing. Never use a vague "it." | How do I install and open it in VS Code? | How do I install and open Claude Code in VS Code? |
| Short, everyday words, one thing per question. | Could the model delete my files directly? | Can the model delete my files? |
| No jargon in the question unless it's the term being asked about. | Why doesn't Claude Code load my whole codebase into context? | Why doesn't Claude Code read my whole project at the start? |
| No idioms. | What's the catch with Homebrew? | What's the downside of installing with Homebrew? |
| It must be a real question. | Give examples of tasks Claude Code can do. | What kinds of tasks can Claude Code do? |
| Same names everywhere: **Claude Code** = the program on my computer, **the model** = the AI on Anthropic's servers. Never just "Claude." | Does the model see a file Claude never opened? | Can the model see a file that Claude Code never opened? |

**Before finishing:** read every question on its own, out of context, and check it against this table. If a question could be misread, or needs the lesson to make sense, rewrite it.

---

## 6. File layout and lesson template

### File layout

```text
<NN>_<CourseName>/             e.g. 01_ClaudeCode101/, next course 02_ClaudePlatform101/
├── README.md                  course index: progress table, links, to-dos
├── images/                    lesson images: 0X-short-name.png (the only subfolder)
├── 01-lesson-name.md          one file per lesson, numbered in course order
├── 02-lesson-name.md
└── NN-course-quiz-review.md   missed quiz questions and the correct reasoning
```

- **No chapter subfolders.** Every lesson file sits directly in the course folder.
- File names: lowercase, hyphens, numbered in course order: `05-explore-plan-code-commit.md`.
- A new course gets the same structure and a `README.md` like `01_ClaudeCode101/README.md`.

### Lesson template

Every lesson file follows this order exactly:

````markdown
# Lesson N — Lesson name

**Course:** [Course Name](course-url) &nbsp;·&nbsp; **Chapter N:** Chapter name &nbsp;·&nbsp; **Completed:** Month D, YYYY

| Previous | Course | Next |
|:---|:---:|---:|
| [← Previous lesson name](0X-previous.md) | [📚 Course index](README.md) | [Next lesson name →](0X-next.md) |

---

**On this page**

| # | Section |
|:---:|:---|
| 1 | [Revision summary](#revision-summary) |
| 2 | [In one sentence](#in-one-sentence) |
| 3 | [The big picture](#the-big-picture) |
| … | … |
| n | [Recap](#recap) |
| n | [My notes / practice](#my-notes--practice) |
| n | [FAQ](#faq) |

---

### Revision summary

*Every key fact from this lesson in one place, for quick revision. The sections below explain each point.*

- **Main idea / command / path:** one plain-English fact per bullet (see "Revision summary" in section 2).
- **Exam:** the one-line takeaway for each exam-angle question.

---

### In one sentence

### (Overview table of the main parts, and the running example)

---

### 1. First main idea
#### (sub-sections: comparison, steps, example, diagram, why it matters)

---

### 2. Second main idea …

---

### Recap

(One bullet per main idea, plain English.)

---

## My notes / practice

- [ ] Hands-on things to try, each one small and specific.

---

## FAQ

**Q1. …?**
Answer.

---

| Previous | Course | Next |
|:---|:---:|---:|
| (same table as the header) |
````

### Header and footer rules

- The header and footer navigation tables are **identical**.
- **Never use a `>` blockquote for the header.** GitHub joins its lines into one messy paragraph.
- First lesson: put `Start of course` in the Previous cell. Last item: put `End of course` in the Next cell.
- Main sections are `###` and get a `---` line between them. Sub-sections are `####`.

### "On this page" table rules

- List every `##` and `###` heading in page order, including Recap, My notes / practice, and FAQ. Skip `####`.
- Use bold text for "On this page", not a heading, so the table doesn't list itself.
- Build links the way GitHub does: lowercase, delete punctuation except hyphens, and turn each space into `-`.
  - `Where it's available` → `#where-its-available`
  - `My notes / practice` → `#my-notes--practice`
  - `5. Behind the scenes: your computer vs. Anthropic's servers` → `#5-behind-the-scenes-your-computer-vs-anthropics-servers`
- Update the table whenever a heading is added, renamed, or removed.

---

## 7. What to tell me when you're done

Keep the reply short:

1. What was created or changed, with file links.
2. **Where the video and the written course differed**, and which version you followed. Follow the written course.
3. **What you added beyond the course**: comparisons, examples, extra facts, exam-angle answers. Name them so I can check them.
4. **Missing images**: which ones to paste.
5. That nothing is committed.
