# Chapter 2 — Prompt evaluation

**Course:** [Building with the Claude API](https://academy.claude.com/courses/building-with-the-claude-api) &nbsp;·&nbsp; **Chapter 2:** Prompt evaluation (lessons 9–14) &nbsp;·&nbsp; **Status:** In progress

| Previous | Course | Next |
|:---|:---:|---:|
| [← Chapter 1: Accessing Claude with the API](../01-accessing-claude-with-the-api/README.md) | [📚 Course index](../README.md) | Chapter 3: Prompt engineering techniques → |

---

This page will sum up the whole chapter for revision once its lessons are done. Each lesson summary will end with a link to the full lesson notes.

## Lessons in this chapter

| # | Lesson | Lesson page | Notes | Status |
|:---:|:---|:---|:---|:---:|
| 9 | Prompt evaluation | [Prompt evaluation](https://academy.claude.com/courses/building-with-the-claude-api/prompt-evaluation) | [09-prompt-evaluation.md](09-prompt-evaluation.md) | ✅ Done |
| 10 | A typical eval workflow | | `10-a-typical-eval-workflow.md` | ⬜ |
| 11 | Generating test datasets | | `11-generating-test-datasets.md` | ⬜ |
| 12 | Running the eval | | `12-running-the-eval.md` | ⬜ |
| 13 | Model based grading | | `13-model-based-grading.md` | ⬜ |
| 14 | Code based grading | | `14-code-based-grading.md` | ⬜ |
| — | Quiz on prompt evaluation | | Quiz review section on this page | ⬜ |

## Lesson summaries

### 9. Prompt evaluation

- **Prompt engineering** is a set of techniques for writing a better prompt, such as sample answers (multishot prompting) and XML tags.
- **Prompt evaluation** is automated testing that measures a prompt: code runs it on many test inputs and scores every answer.
- **Three choices after drafting a prompt:** test it once, test it a few times and patch a corner case, or run it through an evaluation pipeline and improve it by the score.
- **Options 1 and 2 are traps.** Real users send inputs you never imagined, such as empty, mixed-topic, or foreign-language messages.
- **An evaluation pipeline costs more time and money,** but it finds weak spots before users do and lets you compare prompt versions by number.

[Full lesson →](09-prompt-evaluation.md)

## Exam takeaways

- **A team tested a new prompt on three sample inputs and wants to ship it today.** Build an evaluation pipeline first, with realistic test inputs including edge cases and an automatic score. (Claude Models, Prompting & Context Engineering) [Lesson 9](09-prompt-evaluation.md)
- **Two engineers disagree about which of two prompt versions is better.** Run both on the same test set and compare scores. (Solution Design & Architecture) [Lesson 9](09-prompt-evaluation.md)
- **A prompt that worked in development fails in production.** Add the failing inputs to the test set, fix the prompt, and rerun the whole set. (Governance, Safety & Risk) [Lesson 9](09-prompt-evaluation.md)

## Quiz review

Added after the chapter quiz.

---

| Previous | Course | Next |
|:---|:---:|---:|
| [← Chapter 1: Accessing Claude with the API](../01-accessing-claude-with-the-api/README.md) | [📚 Course index](../README.md) | Chapter 3: Prompt engineering techniques → |
