# Lesson 10 — A typical eval workflow

Your prompt acts as production code in an AI feature, and your test set works like unit tests to check it before launch. An **eval workflow** is the repeatable loop you run to measure how well that prompt scores.

**Course:** [Building with the Claude API](https://academy.claude.com/courses/building-with-the-claude-api) &nbsp;·&nbsp; **Lesson page:** [A typical eval workflow](https://academy.claude.com/courses/building-with-the-claude-api/a-typical-eval-workflow) &nbsp;·&nbsp; **Chapter 2:** Prompt evaluation &nbsp;·&nbsp; **Completed:** November 16, 2026

| Previous | Course | Next |
|:---|:---:|---:|
| [← Prompt evaluation](09-prompt-evaluation.md) | [📚 Chapter index](README.md) | [Generating test datasets →](11-generating-test-datasets.md) |

**Practice this lesson:** in [capstone guide 2](../00_Capstone_Plan/guide/02-prompt-evaluation.md), solve:

- [Problem 1: Write your first test questions by hand](../00_Capstone_Plan/guide/02-prompt-evaluation.md#problem-1-write-your-first-test-questions-by-hand)
- [Problem 6: Change the prompt and prove it got better](../00_Capstone_Plan/guide/02-prompt-evaluation.md#problem-6-change-the-prompt-and-prove-it-got-better)

Solve the guide's problems in order after finishing the chapter, because each problem builds on the one before.

---

**On this page**

| # | Section |
|:---:|:---|
| 1 | [Revision summary](#revision-summary) |
| 2 | [The big picture](#the-big-picture) |
| 3 | [1. Step 1: Write the first prompt](#1-step-1-write-the-first-prompt) |
| 4 | [2. Step 2: Write the test questions](#2-step-2-write-the-test-questions) |
| 5 | [3. Step 3: Get the model's answers](#3-step-3-get-the-models-answers) |
| 6 | [4. Step 4: Score each answer](#4-step-4-score-each-answer) |
| 7 | [5. Step 5: Change the prompt and test again](#5-step-5-change-the-prompt-and-test-again) |
| 8 | [Architect notes](#architect-notes) |
| 9 | [Recap](#recap) |
| 10 | [My notes / practice](#my-notes--practice) |
| 11 | [FAQ](#faq) |

---

### Revision summary

**Why this matters.** You edit a prompt and test it on two questions. Both answers look good, so you ship the change. A week later, users report that 1 in 5 answers (20%) misses key steps. Testing only two questions cannot catch a bug that hits 20% of the time. Running an eval on a larger test set catches the score drop before launch.

#### What an eval workflow is

An **eval** (short for evaluation) tests a prompt and returns a score. The **eval workflow** is the fixed sequence of steps you run to measure that score. It works like a school exam:

| School exam | Prompt eval |
|---|---|
| Exam paper with fixed questions for everyone | Test questions (called the **eval dataset**) |
| Student writes answers | Model answers each question using your prompt |
| Teacher grades each answer out of 10 | **Grader** scores each answer from 1 to 10 |
| Average exam grade | Prompt's average score |
| Change teaching, then give the same exam again | Change the prompt, then rerun the same test questions |

The five workflow steps:

1. **Write the first prompt.** Add a `{question}` slot for each test question. This first version sets your **baseline** score for later comparisons.
2. **Write the test questions.** Collect realistic sample questions that real users will send.
3. **Get the model's answers.** Loop through the test questions, insert each one into `{question}`, send the prompt to the model, and save each answer.
4. **Score each answer.** Have a grader score every answer, then average the scores into one number.
5. **Change the prompt and test again.** Keep the same questions and grader, update the prompt, and rerun. A higher average means the edit helped.

#### Why you need many test questions

* **Small tests swing easily:** On 3 questions, one score jumping from 4 to 9 raises the average by 1.67 points. On 100 questions, that same change moves the average by only 0.05. Small samples let luck look like progress.
* **Users send varied inputs:** Real traffic includes math, how-to requests, facts, vague prompts, and unusual edge cases. Three test items cannot cover those patterns.
* **Real evals scale up:** Production evals use tens to thousands of questions. You can write them yourself or generate drafts with a model ([lesson 11](11-generating-test-datasets.md)).

#### How an answer gets a score

A **grader** reads a question and its answer and assigns a score. Three options exist:

* **Code:** Runs a fixed rule, such as checking whether an answer to `2+2` contains `4`. Fast and free, but limited to exact or rule-checkable answers.
* **Another model:** Sends a second prompt asking a model to score an answer (for example, from 1 to 10 for helpfulness). Handles judgment calls, but costs one extra API call per item.
* **A person:** Gives strong human judgment, but moves slowly and costs more. Use human grading to spot-check automated scores.

#### The course's worked example

| Question | Model's answer (Version 1) | Score |
|---|---|:---:|
| What's 2+2? | "2 + 2 = 4" | 10 |
| How do I make oatmeal? | "Add hot water to dry oatmeal." | 4 |
| How far away is the Moon? | "The Moon is about 384,400 km away." | 9 |

* **Version 1** (`"Please answer the user's question"`) averages `(10 + 4 + 9) ÷ 3 = 7.67` (the course slide displays `7.66` due to truncation).
* **Version 2** adds `"Answer the question with ample detail"` and averages `8.7`, showing a measurable gain from the added instruction.

#### Exam takeaways

* **A team says a new prompt "feels better."** Run an eval: test both versions on the same dataset with the same grader and compare the average scores. *(Claude Models, Prompting & Context Engineering)*
* **A score rises only after the team swaps out the test questions.** The comparison is invalid. Hold the dataset and grader constant so only the prompt changes between runs. *(Solution Design & Architecture)*
* **A new prompt raises the score, but answers become three times longer.** Check token cost, latency, and grader bias—longer outputs cost more money and take longer, and graders sometimes reward length over quality. *(Solution Design & Architecture)*

---

### The big picture

The five steps form a repeatable loop. You run one full pass for each prompt version you test.

![Prompt Eval Workflow. There are many different ways to assemble a workflow and many open source and paid options, and this module assembles its own. The five steps are Draft a Prompt, Create an Eval Dataset, Feed Through Claude, Feed Through a Grader, and Change Prompt and Repeat](../images/10-eval-workflow-steps.png)

In plain terms, the workflow is: write the prompt, write the test questions, collect answers, score answers, and repeat after edits. Ready-made eval tools exist, but building this loop directly makes every step clear.

**The running example:** The course evaluates a general question-answering prompt on three items: `"What's 2+2?"`, `"How do I make oatmeal?"`, and `"How far away is the Moon?"`.

#### Who's who

| Role | Where it runs | What it does |
|---|---|---|
| **Developer (you)** | Local environment / notebook | Writes the prompt and test questions, reviews scores, and chooses prompt edits |
| **Eval script** | Local environment / notebook | Sends each test question, stores answers, and computes the average score |
| **Target model** | Anthropic servers | Generates an answer for each test question (Step 3) |
| **Grader** | Local code or a grading model call | Scores each answer from 1 to 10 (Step 4) |

---

### 1. Step 1: Write the first prompt

Start with an initial prompt that includes a placeholder for each test question.

```python
prompt = f"""
Please answer the user's question:

{question}
"""
```

How this snippet works:

* `prompt = ...` stores the prompt text in a variable.
* `"""` defines a multi-line string.
* The leading `f` creates a Python f-string, replacing `{question}` with the current value of `question`.

**Warning:** Python evaluates `{question}` right when the f-string runs. Place prompt construction inside the Step 3 loop so each question gets inserted cleanly on its own pass.

![Initial Prompt Draft. Will this be an effective prompt? We won't know until we evaluate it with some objective methodology. The code is prompt = f""" Please answer the user's question: {question} """](../images/10-initial-prompt-draft.png)

You cannot tell from reading a draft alone whether it will perform well. This first version serves as your **baseline** for judging later edits.

---

### 2. Step 2: Write the test questions

Test questions represent realistic user inputs that will fill `{question}` during evaluation.

![Draft a Prompt, then Create an Eval Dataset. The dataset is a table with a Question column holding "What's 2+2?", "How do I make oatmeal?", and "How far away is the Moon?". The eval dataset contains questions that we will merge with our prompt, and it can be assembled by hand or generated by Claude](../images/10-eval-dataset.png)

In Python, you can start with a simple list:

```python
dataset = [
    "What's 2+2?",
    "How do I make oatmeal?",
    "How far away is the Moon?",
]
```

#### Why three questions are not enough

Three questions work for learning the mechanics, but cannot support a reliable decision. See how one score change affects the average:

| Dataset size | One answer improves from 4 to 9 | Shift in average score |
|---|---|:---:|
| 3 questions | Total rises from 23 to 28 | 7.67 to 9.33 (**+1.67**) |
| 100 questions | Total rises by 5 | **+0.05** |

With 3 questions, one lucky response creates a large jump. With 100 questions, only consistent improvements across many items move the average noticeably.

> **Remember this:** A few questions measure luck; many questions measure the prompt.

---

### 3. Step 3: Get the model's answers

Your loop inserts each question into the prompt and sends it to the model. For the first question, the full prompt sent is:

```text
Please answer the user's question:

What's 2+2?
```

![Feed Through Claude. Each question is merged into the prompt and sent to Claude. Claude replies "2 + 2 = 4", "Add hot water to dry oatmeal.", and "The Moon is about 384,400 KM away."](../images/10-feed-through-claude.png)

Using `chat()` from [lesson 5](../01-accessing-claude-with-the-api/05-system-prompts.md), the loop collects every response:

```python
results = []
for question in dataset:
    prompt = f"""
Please answer the user's question:

{question}
"""
    messages = [{"role": "user", "content": prompt}]
    answer = chat(messages)
    results.append({"question": question, "answer": answer})
```

* `for question in dataset:` runs the indented block once per item in `dataset`.
* `chat(messages)` sends the messages to the model and returns the reply text.
* `results.append(...)` saves each `{question, answer}` pair for grading.

---

### 4. Step 4: Score each answer

The grader evaluates each `(question, answer)` pair and assigns a score from 1 to 10. It needs the original question because quality depends on what was asked—`"Add hot water to dry oatmeal."` only looks weak against `"How do I make oatmeal?"`.

![Feed Through a Grader. Each question and answer pair goes into the grader. "What's 2+2?" with "2 + 2 = 4" scores 10. "How do I make oatmeal?" with "Add hot water to dry oatmeal." scores 4. "How far away is the Moon?" with "The Moon is about 384,400 KM away." scores 9](../images/10-feed-through-grader.png)

| Question | Score | Reason |
|---|:---:|---|
| What's 2+2? | 10 | Accurate and complete |
| How do I make oatmeal? | 4 | Accurate, but omits measurements, cook time, and steps |
| How far away is the Moon? | 9 | Accurate, though it omits that distance changes |

Averaging the scores gives `(10 + 4 + 9) ÷ 3 = 23 ÷ 3 = 7.67` (`7.66` on the slide). That single number is the baseline score for Version 1.

#### How the grader decides

A **model grader** uses a second prompt to rate each answer:

```text
Here is a question and an answer.

Question: How do I make oatmeal?
Answer: Add hot water to dry oatmeal.

Score the answer from 1 to 10 for how complete and helpful it is.
Reply with only the number.
```

The grading model returns `4`, and your script records that score.

A **code grader** applies deterministic logic instead. For `"What's 2+2?"`, code can check whether the output contains `"4"` and return `10` if true, though code cannot judge recipe helpfulness.

| Grader type | Best fit |
|---|---|
| **Code** | Exact answers such as numbers, codes, or fixed category labels |
| **Another model** | Subjective qualities such as completeness, tone, or helpfulness |
| **A person** | Spot-checking samples to verify that automated graders align with human standards |

Lessons [13](13-model-based-grading.md) and [14](14-code-based-grading.md) cover model-based and code-based graders in detail.

---

### 5. Step 5: Change the prompt and test again

Version 1 scored `7.67` because the oatmeal answer lacked detail. Add one instruction line to create Version 2:

```python
prompt = f"""
Please answer the user's question:

{question}

Answer the question with ample detail
"""
```

![Change Prompt and Repeat. The grader averaged 7.66 for the first prompt. The revised prompt adds the line "Answer the question with ample detail"](../images/10-change-prompt-and-repeat.png)

Rerun Steps 3 and 4 again using the **same three questions** and the **same grader**. The average rises to `8.7`.

![Prompt Scoring. Get an objective measurement of the output of each prompt, and use the version with the best score or iterate again. Prompt v1, "Please answer the user's question: {question}", scored 7.66. Prompt v2, which adds "Answer the question with ample detail", scored 8.7](../images/10-prompt-scoring.png)

| Version | Prompt change | Average score |
|---|---|:---:|
| v1 | Initial baseline prompt | 7.67 |
| v2 | Added `"Answer the question with ample detail"` | 8.7 |

Comparing numerical scores lets you pick the stronger version and continue **iterating** (editing and retesting in a loop).

**Warning:** Changing the test questions or the grader between runs breaks fair comparison. A jump from `7.67` to `8.7` might come from easier questions rather than a better prompt.

> **Remember this:** Change one thing, rerun the same test, compare the score.

---

### Architect notes

#### Cost

* Step 3 makes one model call per test question; a model grader makes one additional call per item. A 100-question set with a model grader equals 200 API calls per prompt version.
* Instructions like `"Answer the question with ample detail"` increase output length, and output tokens cost money. Higher scores can raise API spend—check Anthropic's current pricing before scaling runs.

#### Speed

* Longer responses take longer to generate. Log response latency alongside scores so you spot slowdowns early.
* Sequential requests are slow on large datasets. Parallel requests run faster, provided you stay within account rate limits.

#### Trusting the score

* Model outputs can vary across runs ([lesson 6](../01-accessing-claude-with-the-api/06-temperature.md)). Rerun checks before trusting small score differences.
* Model graders sometimes favor longer answers even when extra words add little value. Review sample scores manually.
* Do not rely solely on the average. A single low score (such as `2`) can hide inside a decent mean, so inspect the lowest-scoring answers each run.

---

### Recap

* An eval acts like a repeatable exam for a prompt: fixed questions, scored outputs, one average score.
* The five steps are: write the prompt, write test questions, collect answers, score answers, and iterate.
* Larger datasets prevent one lucky answer from distorting the score.
* Graders can be code (exact rules), another model (judgment), or humans (spot-checks).
* Keep the dataset and grader fixed while changing only the prompt.

---

## My notes / practice

* [ ] Put the three questions in a Python list and run the Step 3 loop with `chat()`.
* [ ] Score each answer manually from 1 to 10 and calculate the average.
* [ ] Run the Step 4 grader prompt on the oatmeal answer and check the returned score.
* [ ] Add `"Answer the question with ample detail"`, rerun, and compare response lengths.

---

## FAQ

**Q1. What does "eval workflow" mean?**
It is the fixed step-by-step process used to score a prompt: write the prompt, write test questions, get model answers, score them, and repeat after editing the prompt.

**Q2. What does "eval dataset" mean?**
It is the collection of test questions inserted one by one into the prompt's `{question}` placeholder during evaluation.

**Q3. What does "baseline" mean in an eval?**
It is the score of your initial prompt version. Later prompt versions are measured against it to see if changes improve performance.

**Q4. Why does an eval need many test questions?**
Small datasets let one unusual or lucky answer shift the average sharply (for example, `+1.67` on 3 questions versus `+0.05` on 100 questions) and fail to represent real user variety.

**Q5. What does "grader" mean?**
A grader is the mechanism—code, another model, or a human—that reviews a question and its answer and assigns a score.

**Q6. How does a grader decide on a score?**
Code checks explicit rules (such as substring or format checks). A model grader takes a grading prompt with the question and answer and outputs a numeric score.

**Q7. Why does the grader need both the question and the answer?**
An answer's quality depends on the question asked. `"Add hot water to dry oatmeal."` is incomplete when answering `"How do I make oatmeal?"` because it lacks quantities, timing, and steps.

**Q8. Why must the questions and grader stay fixed across prompt versions?**
Holding the dataset and grader fixed isolates the prompt as the only variable, so score changes reflect prompt edits rather than different tests or grading rules.

**Q9. (Exam angle) A team claims a new prompt "feels better." What should you do?**
Run a formal eval on the same dataset using the same grader and compare the average scores before deciding. *(Claude Models, Prompting & Context Engineering)*

**Q10. (Exam angle) A higher eval score comes right after changing the test questions. Is the result valid?**
No. Changing the test set invalidates direct comparison—keep the dataset and grader unchanged so only the prompt differs. *(Solution Design & Architecture)*

**Q11. (Exam angle) A prompt edit raises the average score, but responses are now three times longer. What should you check?**
Check token cost, latency, and whether the grader is simply rewarding longer responses over better ones. *(Solution Design & Architecture)*

---

| Previous | Course | Next |
|:---|:---:|---:|
| [← Prompt evaluation](09-prompt-evaluation.md) | [📚 Chapter index](README.md) | [Generating test datasets →](11-generating-test-datasets.md) |
