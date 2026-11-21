# Lesson 10 — A typical eval workflow

**Course:** [Building with the Claude API](https://academy.claude.com/courses/building-with-the-claude-api) &nbsp;·&nbsp; **Lesson page:** [A typical eval workflow](https://academy.claude.com/courses/building-with-the-claude-api/a-typical-eval-workflow) &nbsp;·&nbsp; **Chapter 2:** Prompt evaluation &nbsp;·&nbsp; **Completed:** November 16, 2026

| Previous | Course | Next |
|:---|:---:|---:|
| [← Prompt evaluation](09-prompt-evaluation.md) | [📚 Chapter index](README.md) | [Generating test datasets →](11-generating-test-datasets.md) |

**Practice this lesson:** in [capstone guide 2](../00_Capstone_Plan/guide/02-prompt-evaluation.md), solve:

- [Problem 1: Write your first test questions by hand](../00_Capstone_Plan/guide/02-prompt-evaluation.md#problem-1-write-your-first-test-questions-by-hand)
- [Problem 6: Change the prompt and prove it got better](../00_Capstone_Plan/guide/02-prompt-evaluation.md#problem-6-change-the-prompt-and-prove-it-got-better)

Do the guide's problems in order, after you finish the chapter, because each one builds on the one before.


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

**Where this lesson fits.** [Lesson 9](09-prompt-evaluation.md) showed that your prompt is your production code, and that a saved *test set* checks it the way unit tests check normal code. This lesson shows how you actually run that check.

- **Why checking by hand fails:** you change a prompt and try it on two questions by hand. Both answers look good, so you launch it. A week later, customers complain that 1 answer in 5 (20%) is missing key steps. Two questions are too few to catch a problem that hits only 1 answer in 5.
- **What an eval does instead:** your code sends every test question through your prompt to the model, scores every answer, and reports one final score. For an email sorter with 50 test emails, that score could be `45 / 50 = 90%`.
- **Why the score protects you:** after every prompt change, you rerun the same test. If the score drops, the change broke something that used to work (a *regression*), and you see it before real customers do.

#### What an eval workflow is

An *eval* (short for evaluation) is a test that gives your prompt a score. The *eval workflow* is the fixed set of steps you follow to get that score. It works like a school exam:

| School exam | Prompt eval |
|---|---|
| The exam paper, with the same questions for everyone | The test questions (the course calls this the *eval dataset*) |
| The student writes answers | The model answers each question, using your prompt |
| The teacher marks each answer out of 10 | A *grader* scores each answer from 1 to 10 |
| The average mark | The prompt's score |
| Teach differently, then give the same exam again | Change the prompt, then run the same test questions again |

The five steps:

1. **Write the first prompt.** Leave a slot, `{question}`, where each test question will go. This first version is your *baseline*, the score every later version is compared with.
2. **Write the test questions.** These are sample questions like the ones real users will ask.
3. **Get the model's answers.** Your code puts each question into the slot, sends the prompt to the model, and saves each answer.
4. **Score each answer.** The grader gives each answer a score, and your code averages the scores into one number.
5. **Change the prompt and test again.** Run the same questions with the same grader. If the average goes up, the change helped.

#### Why you need many test questions

- **One answer can swing a small test.** With 3 questions, one answer going from 4 to 9 moves the average by 1.67 points. With 100 questions, the same change moves it by only 0.05. A small test can make a bad prompt look good by luck.
- **Real users ask many kinds of questions.** A test needs math, how-to, facts, vague, and odd questions too. Three questions can't cover them all.
- **Real evals use tens to thousands of questions.** You can write them by hand or ask the model to write them ([lesson 11](11-generating-test-datasets.md)).

#### How an answer gets a score

The *grader* is whatever reads a question and its answer and gives a score. There are three kinds:

- **Code:** a few lines that check a fixed rule. For example, "does the answer to 2+2 contain 4?" It is fast and free, but it only works when there is one exact right answer.
- **Another model:** your code sends a second prompt that says, "Here is a question and an answer. Score the answer from 1 to 10." It can judge things like "is this helpful?", but each score costs one more request.
- **A person:** best judgment, but slow and expensive, so use it only to spot-check.

#### The course's worked example

| Question | The model's answer (version 1) | Score |
|---|---|:---:|
| What's 2+2? | "2 + 2 = 4" | 10 |
| How do I make oatmeal? | "Add hot water to dry oatmeal." | 4 |
| How far away is the Moon? | "The Moon is about 384,400 km away." | 9 |

- **Version 1** ("Please answer the user's question") averages (10 + 4 + 9) ÷ 3 = 7.67. The course shows 7.66 because it cuts off digits instead of rounding.
- **Version 2** adds "Answer the question with ample detail" and averages 8.7, so the extra line helped.

#### Exam takeaways

- **A team changes a prompt and says the new version "feels better."** Ask for an eval: run both versions on the same dataset with the same grader and compare the average scores. (Claude Models, Prompting & Context Engineering)
- **An eval shows a higher score only because the team also changed the test questions.** The comparison is invalid. Keep the dataset and grader fixed, and change only the prompt between runs. (Solution Design & Architecture)
- **A new prompt raises the average score, but answers are now three times longer.** Check cost and speed too. Longer answers use more output tokens, and a grader may favor long answers even when they are not better. (Solution Design & Architecture)

---

### The big picture

The five steps form a loop. You go around it once for every version of the prompt.

![Prompt Eval Workflow. There are many different ways to assemble a workflow and many open source and paid options, and this module assembles its own. The five steps are Draft a Prompt, Create an Eval Dataset, Feed Through Claude, Feed Through a Grader, and Change Prompt and Repeat](../images/10-eval-workflow-steps.png)

The slide's step names are the course terms. In plain words, they are: write the prompt, write the test questions, get the answers, score the answers, change and repeat. Many ready-made eval tools exist, free and paid, but the course builds its own so you see every step.

**The running example:** the course tests a general question-answering prompt on three questions: "What's 2+2?", "How do I make oatmeal?", and "How far away is the Moon?"

#### The same loop for lesson 9's email sorter

The five steps work for any prompt, including the email sorter from [lesson 9](09-prompt-evaluation.md). That prompt sorts each customer email into `billing`, `technical`, or `other`.

1. Your eval code reads `test_set.json`, which holds 50 sample emails, each with the label you expect back.
2. It sends each email through your prompt to the model and saves the label the model returns.
3. It compares each returned label with the expected one. A simple code check works here, because there is one exact right label.
4. It reports the final score, such as `45 / 50 = 90%`.

This is how a *unit test runner* works for normal code: one program runs every test and reports how many passed. The only difference is how each answer is scored. An email label is either right or wrong, so the score is a count. A free-text answer, such as an oatmeal recipe, needs a grader that gives a score from 1 to 10, so the score is an average.

#### Who's who

| Player | Where it lives | What it does |
|---|---|---|
| **You, the developer** | Your notebook | Write the prompt and the questions, read the scores, and decide what to change |
| **Your eval code** | Your notebook | Sends each question, collects the answers, and averages the scores |
| **The model** | Anthropic's servers | Answers each test question (step 3) |
| **The grader** | Your code, or a second request to a model | Scores each answer from 1 to 10 (step 4) |

---

### 1. Step 1: Write the first prompt

Write a first version of the prompt, with a slot where each test question will go.

```python
prompt = f"""
Please answer the user's question:

{question}
"""
```

What each part means:

- `prompt = ...` saves the text in a variable named `prompt`.
- `"""` starts and ends text that runs over several lines.
- The `f` before the quotes makes it an *f-string*: Python swaps `{question}` for whatever the variable `question` holds.

**Warning:** Python fills in `{question}` the moment this line runs. So in a real eval, this line goes inside the loop in step 3, once per question.

![Initial Prompt Draft. Will this be an effective prompt? We won't know until we evaluate it with some objective methodology. The code is prompt = f""" Please answer the user's question: {question} """](../images/10-initial-prompt-draft.png)

The slide asks the key question: will this prompt work well? You can't know until you score it. This first version is the *baseline* that every later version is compared with.

---

### 2. Step 2: Write the test questions

The test questions are samples of what real users will ask. Each one will go into the `{question}` slot.

![Draft a Prompt, then Create an Eval Dataset. The dataset is a table with a Question column holding "What's 2+2?", "How do I make oatmeal?", and "How far away is the Moon?". The eval dataset contains questions that we will merge with our prompt, and it can be assembled by hand or generated by Claude](../images/10-eval-dataset.png)

In Python, the course's three questions can be a simple list:

```python
dataset = [
    "What's 2+2?",
    "How do I make oatmeal?",
    "How far away is the Moon?",
]
```

#### Why three questions are not enough

Three questions are enough to learn the steps, but far too few to trust a score. Look at what one answer does to the average:

| Test size | One answer improves from 4 to 9 | Change in the average |
|---|---|:---:|
| 3 questions | Total goes from 23 to 28 | 7.67 to 9.33, up **1.67** |
| 100 questions | Total goes up by 5 | up only **0.05** |

With 3 questions, one lucky answer looks like a big improvement. With 100, only a real improvement across many answers moves the score.

> **Remember this:** A few questions measure luck. Many questions measure the prompt.

---

### 3. Step 3: Get the model's answers

Your code puts each question into the prompt and sends it to the model. The first finished prompt is exactly this text:

```text
Please answer the user's question:

What's 2+2?
```

![Feed Through Claude. Each question is merged into the prompt and sent to Claude. Claude replies "2 + 2 = 4", "Add hot water to dry oatmeal.", and "The Moon is about 384,400 KM away."](../images/10-feed-through-claude.png)

A small loop does this for every question. It uses the `chat()` function from [lesson 5](../01-accessing-claude-with-the-api/05-system-prompts.md):

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

- `for question in dataset:` repeats the indented lines once per question.
- `chat(messages)` sends the prompt to the model and returns its answer.
- `results.append(...)` saves each question with its answer, ready for scoring.

---

### 4. Step 4: Score each answer

The grader reads each question with its answer and gives a score from 1 to 10. It needs the question too, because "Add hot water to dry oatmeal" is only weak *as an answer to* "How do I make oatmeal?".

![Feed Through a Grader. Each question and answer pair goes into the grader. "What's 2+2?" with "2 + 2 = 4" scores 10. "How do I make oatmeal?" with "Add hot water to dry oatmeal." scores 4. "How far away is the Moon?" with "The Moon is about 384,400 KM away." scores 9](../images/10-feed-through-grader.png)

| Question | Score | Why |
|---|:---:|---|
| What's 2+2? | 10 | Correct and complete |
| How do I make oatmeal? | 4 | Correct, but no amounts, times, or steps |
| How far away is the Moon? | 9 | Correct, though it could say the distance changes |

Then your code averages the scores: (10 + 4 + 9) ÷ 3 = 23 ÷ 3 = **7.67**. The course shows 7.66. That one number is the score for prompt version 1.

#### How the grader decides

The course doesn't show this yet, so here is the simple picture. A grader that is **another model** gets a second prompt like this:

```text
Here is a question and an answer.

Question: How do I make oatmeal?
Answer: Add hot water to dry oatmeal.

Score the answer from 1 to 10 for how complete and helpful it is.
Reply with only the number.
```

The model replies `4`. Your code reads the number and saves it.

A grader that is **code** checks a rule instead. For "What's 2+2?", it checks whether the answer contains "4", and gives 10 if it does. That can't judge whether an oatmeal recipe is helpful.

| Grader | Use it when |
|---|---|
| **Code** | There is one exact right answer, such as a number or a category name |
| **Another model** | Quality needs judgment, such as "is this complete and helpful?" |
| **A person** | Spot-checking a sample of scores to make sure the other graders are fair |

Lessons [13](13-model-based-grading.md) and [14](14-code-based-grading.md) build both kinds of grader.

---

### 5. Step 5: Change the prompt and test again

Version 1 scored 7.67. The oatmeal answer was too short, so you add one line:

```python
prompt = f"""
Please answer the user's question:

{question}

Answer the question with ample detail
"""
```

![Change Prompt and Repeat. The grader averaged 7.66 for the first prompt. The revised prompt adds the line "Answer the question with ample detail"](../images/10-change-prompt-and-repeat.png)

You run steps 3 and 4 again, with the **same three questions** and the **same grader**. The new average is 8.7.

![Prompt Scoring. Get an objective measurement of the output of each prompt, and use the version with the best score or iterate again. Prompt v1, "Please answer the user's question: {question}", scored 7.66. Prompt v2, which adds "Answer the question with ample detail", scored 8.7](../images/10-prompt-scoring.png)

| Version | Change | Average score |
|---|---|:---:|
| v1 | The first prompt | 7.67 |
| v2 | Added "Answer the question with ample detail" | 8.7 |

Now you can compare versions by number, keep the best one, and keep improving it. Changing and retesting again and again is called *iterating*.

**Warning:** If you change the questions or the grader between runs, the scores no longer compare. A rise from 7.67 to 8.7 could come from easier questions, not a better prompt.

> **Remember this:** Change one thing, rerun the same test, compare the number.

---

### Architect notes

#### Cost

- Step 3 sends one request per question. A model grader adds one more per question. 100 questions graded by a model is 200 requests per prompt version.
- "Answer with ample detail" makes answers longer, and you pay for every output token. A better score can also mean a bigger bill. Prices change, so check Anthropic's pricing page.

#### Speed

- Longer answers also take longer to arrive. Record how long each answer takes, not just its score.
- Sending requests one at a time is slow for large tests. Sending several at once is faster, but stay under your account's rate limits.

#### Trusting the score

- Answers vary a little between runs ([lesson 6](../01-accessing-claude-with-the-api/06-temperature.md)). Rerun before trusting a small difference.
- A model grader can favor longer answers even when they are not better. Spot-check some scores by hand.
- Don't watch only the average. One answer scoring 2 can hide inside a good average, so read the lowest-scoring answers each run.

---

### Recap

- An eval is like an exam for your prompt: same questions, scored answers, one average.
- The five steps: write the prompt, write test questions, get answers, score them, change and repeat.
- Many questions are needed, so one lucky answer can't fake an improvement.
- A grader can be code (exact answers), another model (judgment), or a person (spot-checks).
- Keep the questions and grader the same, and change only the prompt.

---

## My notes / practice

- [ ] Put the three questions in a Python list, and run the step 3 loop with `chat()`.
- [ ] Score the three answers yourself from 1 to 10, and work out the average.
- [ ] Send the grader prompt from step 4 for the oatmeal answer, and see what score comes back.
- [ ] Add "Answer the question with ample detail," rerun, and note how much longer the answers got.

---

## FAQ

**Q1. What does "eval workflow" mean?**
It is the fixed set of steps you follow to give a prompt a score: write the prompt, write test questions, get the model's answers, score them, then change the prompt and repeat. It works like giving a student the same exam after each lesson.

**Q2. What does "eval dataset" mean?**
It is the list of test questions. Each one goes into the prompt's `{question}` slot, one at a time.

**Q3. What does "baseline" mean in an eval?**
It is the score of your first prompt version. Every later version is compared with it to see whether a change helped.

**Q4. What does "regression" mean in an eval?**
A regression is a change that breaks something that used to work. For example, a prompt edit drops the email sorter's score from 45 of 50 to 40 of 50. Rerunning the same test after every change catches it before customers see it.

**Q5. Why does an eval need so many test questions?**
With few questions, one lucky or unlucky answer moves the average a lot. With 3 questions, one answer going from 4 to 9 raises the average by 1.67. With 100 questions it raises it by only 0.05. Many questions also cover more of the kinds of things real users ask.

**Q6. What does "grader" mean?**
It is whatever scores each answer. It reads the question and the answer and gives a score, such as 1 to 10.

**Q7. How does a grader decide on a score?**
A code grader checks a fixed rule, such as "the answer contains 4." A model grader gets a second prompt asking it to score the answer from 1 to 10, and replies with a number.

**Q8. Why does the grader need the question as well as the answer?**
An answer is only good or bad for a given question. "Add hot water to dry oatmeal" is a weak answer to "How do I make oatmeal?" because it leaves out amounts and times.

**Q9. Why must the questions and the grader stay the same between runs?**
So that only the prompt changes. If the questions or the grader also change, you can't tell which change moved the score.

**Q10. (Exam angle) A team changes a prompt and says the new version "feels better." What do you ask for?**
An eval: run both versions on the same dataset with the same grader, and compare the average scores. (Claude Models, Prompting & Context Engineering)

**Q11. (Exam angle) An eval shows a higher score, but the team also changed the test questions. Is the result valid?**
No. Keep the dataset and grader fixed, and change only the prompt, so the score difference comes from the prompt alone. (Solution Design & Architecture)

**Q12. (Exam angle) A new prompt raises the average score, but answers are now three times longer. What else do you check?**
Check cost and speed, because longer answers use more output tokens and take longer. Also check that the grader isn't simply rewarding length. (Solution Design & Architecture)

---

| Previous | Course | Next |
|:---|:---:|---:|
| [← Prompt evaluation](09-prompt-evaluation.md) | [📚 Chapter index](README.md) | [Generating test datasets →](11-generating-test-datasets.md) |
