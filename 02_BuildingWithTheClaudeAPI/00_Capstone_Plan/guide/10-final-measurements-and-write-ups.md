# Capstone guide 10 — Final measurements and write-ups

**Do it after:** the whole API course, and the cloud course in the [study plan](../../../readme.md) (Bedrock or Vertex AI) &nbsp;·&nbsp; **Capstone index:** [Capstone plan](../README.md)

| Previous | Capstone | Next |
|:---|:---:|---:|
| [← Guide 9: Agents and workflows](09-agents-and-workflows.md) | [Capstone index](../README.md) | End of capstone |

---

**On this page**

| # | Section |
|:---:|:---|
| 1 | [What you build in this chapter](#what-you-build-in-this-chapter) |
| 2 | [Before you start](#before-you-start) |
| 3 | [Problem 1: Compare two models on your own eval](#problem-1-compare-two-models-on-your-own-eval) |
| 4 | [Problem 2: Run the eval as a batch at half price](#problem-2-run-the-eval-as-a-batch-at-half-price) |
| 5 | [Problem 3: Grow the eval to 25 cases or more](#problem-3-grow-the-eval-to-25-cases-or-more) |
| 6 | [Problem 4: Write three design decisions](#problem-4-write-three-design-decisions) |
| 7 | [Problem 5: Write the risk review](#problem-5-write-the-risk-review) |
| 8 | [Problem 6: Write the manager summary](#problem-6-write-the-manager-summary) |
| 9 | [Architect scenario: the shop's weekly email report](#architect-scenario-the-shops-weekly-email-report) |
| 10 | [Commit your work](#commit-your-work) |

---

### What you build in this chapter

The app is built. This guide turns it into evidence: measured cost, speed, and quality for two models, a larger eval, and three short documents an architect writes before a launch. These write-ups cover the exam's governance and stakeholder topics, which the code alone doesn't.

| File | What it does | Problem |
|---|---|---|
| `evaluations/results/models.md` | Score, cost, and time for two models | 1 |
| `evaluations/batch_answers.py` | Runs the answer cases through the Message Batches API | 2 |
| `evaluations/cases.jsonl` | At least 25 cases in total | 3 |
| `docs/decisions.md` | Three design-decision notes | 4 |
| `docs/risk-review.md` | One page about risks | 5 |
| `docs/manager-summary.md` | One page for a manager | 6 |

**Capstone done when:** all three write-ups exist, each decision cites a number from your own results, and the full eval and `uv run pytest` run cleanly.

---

### Before you start

1. Run `git pull`, and finish [guide 9](09-agents-and-workflows.md).
2. **Optional warm-up:** run these example notebooks from the Claude Cookbook first, to see the techniques working before you build them. The first time, do the Cookbook's [one-time setup](../../../cookbook-build-along.md#one-time-setup). For each notebook, follow the [routine for every notebook](../../../cookbook-build-along.md#the-routine-for-every-notebook): read, run, change, break.

   | Notebook | What it teaches |
   |---|---|
   | [`batch_processing`](https://github.com/anthropics/claude-cookbooks/blob/main/misc/batch_processing.ipynb) | The Message Batches API: about half the price, results within 24 hours |
   | [`cost_optimization`](https://github.com/anthropics/claude-cookbooks/blob/main/cost_optimization/cost_optimization.ipynb) | A checklist for cutting cost while measuring the pass rate |
   | [`latency_optimization`](https://github.com/anthropics/claude-cookbooks/blob/main/latency_optimization/latency_optimization.ipynb) | Ways to make answers arrive faster, measured |

   **Try this:** the two optimization notebooks are long, so read them first and run only the sections that match your app.

---

### Problem 1: Compare two models on your own eval

**Lesson:** not a course lesson. This uses your eval from guide 2 and your benchmark from guide 6.

**The problem:** Run the full eval and the cache benchmark with Haiku 5.5 and with Sonnet 5.5. Record the average score, the cost per question, and the total time for each in `evaluations/results/models.md`.

- **Check:** a table with two rows, and one sentence on which model you would choose and why.

<details>
<summary>Show the step-by-step answer</summary>

**Step 1. Run everything with Haiku**, the model in your `.env`. Time the eval with your watch, or note the times the terminal prints.

```bash
uv run python -m evaluations.run_evals
uv run python -m experiments.cache_benchmark
```

**Step 2. Run the same with Sonnet 5.5,** without editing `.env`. A setting you type before the command wins over `.env`, because `load_dotenv()` doesn't replace settings that already exist. First change `PRICE_IN` and `PRICE_OUT` in `experiments/cache_benchmark.py` to Sonnet's prices from the [pricing page](https://platform.claude.com/docs/en/about-claude/pricing).

**Mac:**

```bash
CLAUDE_MODEL=claude-sonnet-5-5 uv run python -m evaluations.run_evals
CLAUDE_MODEL=claude-sonnet-5-5 uv run python -m experiments.cache_benchmark
```

**Windows:**

```powershell
$env:CLAUDE_MODEL = "claude-sonnet-5-5"
uv run python -m evaluations.run_evals
uv run python -m experiments.cache_benchmark
Remove-Item Env:CLAUDE_MODEL
```

**Step 3. Write `evaluations/results/models.md`** with your own numbers.

```text
| Model | Average score | Cost per question | Eval time |
|---|---|---|---|
| claude-haiku-5-5 | 8.6 | $0.0004 | 3 min |
| claude-sonnet-5-5 | 9.0 | $0.0080 | 4 min |

Choice: Haiku for the customer chat, because the score difference is small and it costs 20 times less.
Consider Sonnet for the incident team's investigator, where the harder reasoning may justify the cost.
```

</details>

**Why this matters:** model choice is decided by your own eval, cost, and speed numbers, not by a general ranking (Agentic Architecture & Orchestration).

---

### Problem 2: Run the eval as a batch at half price

**Lesson:** not a course lesson. The `batch_processing` notebook in the warm-up above shows the Message Batches API working.

**The problem:** The eval doesn't need answers instantly. Write `evaluations/batch_answers.py`, which sends every `answer` and `scope` case to the **Message Batches API**. A batch costs about half the normal price, and its results arrive within 24 hours, often much sooner.

- **Check:** the script submits the batch, waits, and prints each case's answer by its id.

<details>
<summary>Show the step-by-step answer</summary>

**Step 1. Write `evaluations/batch_answers.py`.**

```python
import time

from anthropic.types.message_create_params import MessageCreateParamsNonStreaming
from anthropic.types.messages.batch_create_params import Request

from app.client import MODEL, client
from app.prompts import system_prompt_for
from evaluations.run_evals import load_cases

cases = [c for c in load_cases() if c["kind"] in {"answer", "scope"}]
batch = client.messages.batches.create(requests=[
    Request(
        # Your own label for each request. Results can come back in any order, so you
        # match them by this id, never by position.
        custom_id=case["id"],
        params=MessageCreateParamsNonStreaming(
            model=MODEL,
            max_tokens=4000,
            system=system_prompt_for(case.get("role", "customer")),
            messages=[{"role": "user", "content": case["input"]}],
        ),
    )
    for case in cases
])
print("Batch", batch.id, "submitted with", len(cases), "requests")

# Waits until every request in the batch is finished.
while (batch := client.messages.batches.retrieve(batch.id)).processing_status != "ended":
    print("Still processing...")
    time.sleep(30)

for result in client.messages.batches.results(batch.id):
    # succeeded, errored, canceled, or expired. Handle each one.
    if result.result.type == "succeeded":
        text = "".join(b.text for b in result.result.message.content if b.type == "text")
        print(f"{result.custom_id}: {text[:80]}")
    else:
        print(f"{result.custom_id}: {result.result.type}")
```

**Step 2. Run it.** `uv run python -m evaluations.batch_answers`

**Step 3. Know when to use batches.** Use them for work nobody is waiting for: nightly evals, reports, and re-sorting old data. Never use them for a live chat.

</details>

**Why this matters:** batches halve the cost of work that can wait, which is an easy saving for evals and reports (Context Management & Reliability).

---

### Problem 3: Grow the eval to 25 cases or more

**Lesson:** not a course lesson. This applies guides 2 and 3.

**The problem:** Check that `evaluations/cases.jsonl` covers every feature, with at least 25 cases in total. Fill the gaps.

- **Check:** each row of the table below has at least the number of cases shown.

<details>
<summary>Show the step-by-step answer</summary>

**Step 1. Count your cases per feature.** One way is `uv run python -c "import json, collections; print(collections.Counter(json.loads(l)['id'].split('-')[0] for l in open('evaluations/cases.jsonl')))"`.

| Feature | Id prefix | At least |
|---|---|---|
| Triage | `tri`, `gen` | 6 |
| Role-specific answers | `ans` | 4 |
| Documents and sources | `doc` | 3 |
| Unanswerable questions | `none` | 3 |
| Staff-only information | `leak` | 2 |
| Out of scope | `scope` | 3 |
| Misuse | `mis` | 3 |
| Ticket tools | `tool` | 2, such as "status of ticket 1042" and "status of someone else's ticket" |

**Step 2. Add the missing cases,** run the eval, and save the final score in `scores.md`.

</details>

**Why this matters:** a launch decision needs an eval that covers every feature and every known failure (Prompt Engineering & Structured Output).

---

### Problem 4: Write three design decisions

**Lesson:** not a course lesson. Architects record important choices as short notes, often called *ADRs* (architecture decision records).

**The problem:** Write `docs/decisions.md` with three notes: the model choice, the deployment platform (the Claude API directly, Amazon Bedrock, or Google Vertex AI), and how the app finds documents. Each note answers five questions and cites your own numbers.

- **Check:** three notes, each answering all five questions, each with at least one measured number.

<details>
<summary>Show the step-by-step answer</summary>

**Step 1. Use the same five questions for each note.**

1. What problem are we solving?
2. What options did we consider?
3. Which did we choose, and why?
4. What are its limits?
5. What evidence would make us change it?

**Step 2. Write the first note as an example.**

```text
## Decision 1: Model for the customer chat

1. Problem: we need answers that are good, fast, and cheap enough for thousands of questions a day.
2. Options: Claude Haiku 5.5 and Claude Sonnet 5.5.
3. Choice: Haiku 5.5. On our 27-case eval it scored 8.6 against Sonnet's 9.0, at about one twentieth of the cost per question (evaluations/results/models.md).
4. Limits: it is weaker on long technical diagnosis, so the incident investigator may need Sonnet.
5. We would change it if the eval score dropped below 8.0, or if customers' complaints about answer quality rose.
```

**Step 3. Write the other two the same way.** For the platform, use what you learned in the cloud course: where the data is processed, which features each platform has, and how billing works. For finding documents, cite your guide 5 results: keyword only, or hybrid.

</details>

**Why this matters:** an architect must defend each choice with options, evidence, limits, and a trigger for changing it (Agentic Architecture & Orchestration).

---

### Problem 5: Write the risk review

**Lesson:** not a course lesson. This brings together the safety work from every guide.

**The problem:** Write `docs/risk-review.md`, one page, covering what data the app sees, what could go wrong, what protects against it, and what you would change before real customers use it.

- **Check:** every risk names the protection you built and the guide where you built it.

<details>
<summary>Show the step-by-step answer</summary>

**Step 1. Use a table of risks and protections.**

```text
| Risk | Protection in the app | Built in |
|---|---|---|
| A customer sees another customer's ticket | Ownership check in lookup_ticket; tests | Guide 4 |
| A customer gets staff documents | Role filter before search; leak eval cases | Guide 5 |
| A message tricks the assistant (prompt injection) | XML tags for untrusted text; router misuse route | Guides 3, 9 |
| The assistant creates tickets by itself | Approval gate in code | Guide 4 |
| The model edits files outside its area | safe_path check in the editor tool | Guide 4 |
| The API key leaks | .env, .gitignore, Claude Code deny rule | Guides 1, 8 |
| Made-up answers | Answers only from documents, citations, unanswerable eval cases | Guides 5, 6 |
```

**Step 2. Add two short sections.**

- **What we log:** for example, each tool call with the user's role and the ticket id, but not full customer messages.
- **Before real customers:** for example, real sign-in instead of the `--role` option, rate limits per user, a person reviewing a sample of answers every week, and a data-retention check with the legal team.

</details>

**Why this matters:** a risk review links each risk to a tested protection, which is what governance reviewers ask for (Governance, Safety & Risk).

---

### Problem 6: Write the manager summary

**Lesson:** not a course lesson. This is a stakeholder skill.

**The problem:** Write `docs/manager-summary.md`, one page for a manager who doesn't write code: the problem, what the app does, the cost, the main risks, how you would roll it out, and how you would measure success.

- **Check:** no code words without a plain explanation, and every number comes from your results.

<details>
<summary>Show the step-by-step answer</summary>

**Step 1. Use these headings, with 2 to 4 sentences each.**

1. **The problem:** for example, "Customers wait hours for simple answers about refunds, router lights, and ticket status."
2. **What the assistant does:** answers from company documents with sources, looks up tickets, opens tickets after the customer confirms, and refuses what it shouldn't do.
3. **Cost:** your measured cost per question, multiplied by a realistic number of questions a month.
4. **Main risks and protections:** the top three from your risk review, in plain words.
5. **Roll-out:** start with staff only, then 5% of customers with a person checking a sample, then everyone if the numbers hold.
6. **How we measure success:** for example, the eval score stays above 8.0, the share of questions answered without a person, and customer satisfaction.

**Step 2. Read it aloud.** If a sentence would confuse someone outside IT, rewrite it.

</details>

**Why this matters:** the Professional exam tests whether you can explain a design to non-technical stakeholders in terms of cost, risk, and value (Governance, Safety & Risk).

---

### Architect scenario: the shop's weekly email report

**The scenario:** the shop's support manager wants a report every Monday: last week's 7,000 emails, the top 10 reasons customers wrote, and three example emails for each reason. The emails are already sorted into inboxes. A developer suggests running the live sorter's code on each email again at full price. Design a better way.

- **Check:** your design names the API features to use, and estimates the cost difference.

<details>
<summary>Show the step-by-step answer</summary>

**Step 1. Notice that nobody is waiting.** The report is needed on Monday, not in seconds. That makes it a perfect fit for the Message Batches API, at about half the price.

**Step 2. Split the job into a workflow.**

1. **Label each email (7,000 requests in one batch):** one short structured output per email, such as `{"reason": "late delivery"}`, chosen from a list that you let grow.
2. **Count the reasons in code:** counting is exact in code, so don't ask a model to do it.
3. **Write the report (one request):** send the top 10 reasons and their counts, plus a few example emails for each, and ask for a short summary.

**Step 3. Cut cost further.** Put the shared instructions first and turn on prompt caching for the labelling requests, because every one starts with the same text. Use the smallest model that passes a small labelling eval (problem 1).

**Step 4. Estimate the difference.** With the same model and prompt, the batch halves the cost of step 1, which is nearly the whole bill. Caching the shared instructions cuts the repeated input further.

**Step 5. Protect the data.** Seven thousand customer emails are personal data. Keep them in your own systems, send only what each request needs, and check the data-retention settings for the batch results.

</details>

**Why this matters:** for work that can wait, the exam expects batches, code for exact steps such as counting, caching for repeated instructions, and the smallest model that passes the eval (Context Management & Reliability).

---

### Commit your work

```bash
uv run pytest
uv run python -m evaluations.run_evals
git add .
git status
git commit -m "Capstone guide 10: model comparison, batch eval, decisions, risk review, summary"
git push
```

**Warning:** check that `.env` is not in the `git status` list before you commit.

Then mark guide 10 and the capstone as done in the [capstone index](../README.md#the-chapter-guides).

---

| Previous | Capstone | Next |
|:---|:---:|---:|
| [← Guide 9: Agents and workflows](09-agents-and-workflows.md) | [Capstone index](../README.md) | End of capstone |
