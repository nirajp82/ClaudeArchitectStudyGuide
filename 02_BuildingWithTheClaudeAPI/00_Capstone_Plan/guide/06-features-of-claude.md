# Capstone guide 6 — Features of Claude

**Do it after:** Chapter 6, Features of Claude (lessons 39–46) &nbsp;·&nbsp; **Capstone index:** [Capstone plan](../README.md)

| Previous | Capstone | Next |
|:---|:---:|---:|
| [← Guide 5: RAG and agentic search](05-rag-and-agentic-search.md) | [Capstone index](../README.md) | [Guide 7: Model Context Protocol →](07-model-context-protocol.md) |

---

**On this page**

| # | Section |
|:---:|:---|
| 1 | [What you build in this chapter](#what-you-build-in-this-chapter) |
| 2 | [Before you start](#before-you-start) |
| 3 | [Problem 1: Let the model think longer on hard problems](#problem-1-let-the-model-think-longer-on-hard-problems) |
| 4 | [Problem 2: Read a photo of the router](#problem-2-read-a-photo-of-the-router) |
| 5 | [Problem 3: Answer from a PDF](#problem-3-answer-from-a-pdf) |
| 6 | [Problem 4: Exact citations for every answer](#problem-4-exact-citations-for-every-answer) |
| 7 | [Problem 5: Cache the part of the prompt that never changes](#problem-5-cache-the-part-of-the-prompt-that-never-changes) |
| 8 | [Problem 6: Break the cache on purpose](#problem-6-break-the-cache-on-purpose) |
| 9 | [Problem 7: Let the model analyse the tickets with code](#problem-7-let-the-model-analyse-the-tickets-with-code) |
| 10 | [Architect scenario: is caching worth it for the shop?](#architect-scenario-is-caching-worth-it-for-the-shop) |
| 11 | [Commit your work](#commit-your-work) |

---

### What you build in this chapter

This guide adds the model's special features one at a time, each where it really helps the Northwind app: deeper thinking for technicians, photos of routers, a PDF contract, exact citations, prompt caching to cut cost, and code execution to analyse ticket data.

| File | What it does | Problem |
|---|---|---|
| `experiments/thinking.py` | Compares low and high effort on a hard question | 1 |
| `experiments/router_photo.py` | Reads a photo of router lights | 2 |
| `experiments/pdf_question.py` | Answers a question from a PDF | 3 |
| `app/assistant.py` | `answer_from_documents()` now returns exact citations | 4 |
| `app/agent_loop.py` | Turns on prompt caching and records cache use | 5, 6 |
| `evaluations/results/benchmark.json` | Cost per question with and without caching | 5 |
| `experiments/ticket_report.py` | Uploads ticket data and gets a chart back | 7 |

**Chapter done when:** answers show exact quoted sources, and `benchmark.json` shows a lower cost per question with caching than without.

---

### Before you start

1. Run `git pull`, and finish [guide 5](05-rag-and-agentic-search.md).
2. Read your notes for chapter 6 when they exist (see the [course index](../../README.md)).
3. **Optional warm-up:** run these example notebooks from the Claude Cookbook first, to see the techniques working before you build them. The first time, do the Cookbook's [one-time setup](../../../cookbook-build-along.md#one-time-setup). For each notebook, follow the [routine for every notebook](../../../cookbook-build-along.md#the-routine-for-every-notebook): read, run, change, break.

   | Notebook | What it teaches |
   |---|---|
   | [`using_citations`](https://github.com/anthropics/claude-cookbooks/blob/main/misc/using_citations.ipynb) | Answers that point to the exact sentence they came from |
   | [`pdf_upload_summarization`](https://github.com/anthropics/claude-cookbooks/blob/main/misc/pdf_upload_summarization.ipynb) | Sending a PDF to the model |
   | [`prompt_caching`](https://github.com/anthropics/claude-cookbooks/blob/main/misc/prompt_caching.ipynb) | Saving the unchanging start of a prompt so later requests cost less |

   **Try this:** in the caching notebook, put the current time at the start of the prompt and watch the cache stop working.

---

### Problem 1: Let the model think longer on hard problems

**Lesson:** 39, Extended thinking

**Warning:** older material sets a thinking budget with `thinking={"type": "enabled", "budget_tokens": ...}`. Current models reject that. They use *adaptive thinking*, where the model decides how much to think, and you set the depth with `output_config={"effort": ...}`. Haiku 5.5 thinks by default.

**The problem:** Write `experiments/thinking.py`. It asks a hard technician question twice, once with effort `low` and once with effort `high`, and shows the summarized thinking, the answer, the output tokens, and the time for each.

The question: `A customer in Riverside has evening drops, signal -22 dB, PPP timeouts between 20:00 and 22:00, and an outage was resolved nearby yesterday. List the likely causes in order and the next check for each.`

- **Check:** you can say how much longer and more expensive `high` was, and whether its answer was better.

<details>
<summary>Show the step-by-step answer</summary>

**Step 1. Write `experiments/thinking.py`.**

```python
import time

from app.client import MODEL, client

QUESTION = ("A customer in Riverside has evening drops, signal -22 dB, PPP timeouts between "
            "20:00 and 22:00, and an outage was resolved nearby yesterday. List the likely "
            "causes in order and the next check for each.")

for effort in ["low", "high"]:
    start = time.time()
    response = client.messages.create(
        model=MODEL,
        max_tokens=16000,
        thinking={"type": "adaptive", "display": "summarized"},
        output_config={"effort": effort},
        messages=[{"role": "user", "content": QUESTION}],
    )
    seconds = time.time() - start
    print(f"\n===== effort={effort}: {response.usage.output_tokens} output tokens, {seconds:.1f} s")
    for block in response.content:
        if block.type == "thinking":
            print("[thinking summary]", block.thinking[:500])
        elif block.type == "text":
            print(block.text)
```

| Line | What it does |
|---|---|
| `thinking={"type": "adaptive", "display": "summarized"}` | The model decides how long to think. `summarized` asks for a readable summary of the thinking; by default the thinking text comes back empty. |
| `output_config={"effort": effort}` | How much work to put in: `low`, `medium` (Haiku 5.5's default), `high`, and above. |
| `response.usage.output_tokens` | Includes the thinking tokens. You pay for thinking even when you can't read it. |

**Step 2. Run it and compare.**

```bash
uv run python -m experiments.thinking
```

**Step 3. Decide where each setting belongs.** For the customer chat and triage, `low` is usually enough and keeps answers fast and cheap. For the technician's hard diagnosis, `high` may be worth it. Prove it with an eval, not a feeling.

</details>

**Why this matters:** more thinking costs tokens and time; you pick the effort per task and measure the gain (Context Management & Reliability).

---

### Problem 2: Read a photo of the router

**Lesson:** 40, Image support

**The problem:** Customers often can't describe the lights. Write `experiments/router_photo.py`, which sends a photo of a router with the question `What do these lights mean, and what should I do?`, together with the `router-lights.md` document.

Use any photo of a router or modem, or a screenshot of one from the internet, saved as `data/router.jpg`. Don't use a photo with people or private details in it.

- **Check:** the answer describes the lights in the photo and gives the matching advice from the document.

<details>
<summary>Show the step-by-step answer</summary>

**Step 1. Write `experiments/router_photo.py`.** Images are sent as *base64*, a way to write binary data as plain text.

```python
import base64
from pathlib import Path

from app.client import MODEL, client, get_text

image = base64.standard_b64encode(Path("data/router.jpg").read_bytes()).decode("utf-8")
guide = Path("sample_documents/router-lights.md").read_text(encoding="utf-8")

response = client.messages.create(
    model=MODEL,
    max_tokens=4000,
    messages=[{
        "role": "user",
        "content": [
            {"type": "image", "source": {"type": "base64", "media_type": "image/jpeg", "data": image}},
            {"type": "text", "text": f"<guide>\n{guide}\n</guide>\nWhat do these lights mean, and what should I do? Use the guide."},
        ],
    }],
)
print(get_text(response))
```

| Line | What it does |
|---|---|
| `"type": "image"` | An image block. It goes before the text, so the question can refer to it. |
| `"media_type": "image/jpeg"` | Must match the file type. Use `image/png` for a PNG file. |
| `<guide>` | Gives the model your own rules, so the advice comes from Northwind, not from general knowledge. |

**Step 2. Run it.** `uv run python -m experiments.router_photo`

**Step 3. Know the limits.** Images cost tokens based on their size, so shrink large photos first. The model can misread small details, so for important decisions, ask it to say what it sees before it gives advice.

</details>

**Why this matters:** images are one more input type, and they need the same grounding and checking as text (Prompt Engineering & Structured Output).

---

### Problem 3: Answer from a PDF

**Lesson:** 41, PDF support

**The problem:** Northwind's contract is a PDF. Make one: open `sample_documents/refund-policy.md` in any editor and print it to PDF as `data/contract.pdf`. Then write `experiments/pdf_question.py`, which asks `After how many days can I only get account credit?` with the PDF attached.

- **Check:** the answer says 30 days.

<details>
<summary>Show the step-by-step answer</summary>

**Step 1. Write `experiments/pdf_question.py`.**

```python
import base64
from pathlib import Path

from app.client import MODEL, client, get_text

pdf = base64.standard_b64encode(Path("data/contract.pdf").read_bytes()).decode("utf-8")

response = client.messages.create(
    model=MODEL,
    max_tokens=4000,
    messages=[{
        "role": "user",
        "content": [
            {"type": "document", "source": {"type": "base64", "media_type": "application/pdf", "data": pdf}},
            {"type": "text", "text": "After how many days can I only get account credit?"},
        ],
    }],
)
print(get_text(response))
```

**Step 2. Run it.** `uv run python -m experiments.pdf_question`

**Step 3. Know how PDFs are read.** The model reads both the text and an image of each page, so tables and charts in a PDF work too. A request can hold a PDF up to 32 MB and 600 pages, but every page costs tokens. For a long PDF you ask about often, upload it once with the Files API (problem 7) instead of sending it each time.

</details>

**Why this matters:** PDFs can go straight to the model, but large or repeated ones belong in the Files API or a RAG index (Context Management & Reliability).

---

### Problem 4: Exact citations for every answer

**Lesson:** 42, Citations

**The problem:** In guide 5 the model writes `[refund-policy.md]` itself, and it could write a wrong file name. Change `answer_from_documents` to send each chunk as a *document block* with citations turned on. The API then attaches the exact quoted sentence and its source to each part of the answer. Print the answer with `[Source: file]` after each cited part.

- **Check:** `How long do I have to ask for a refund?` prints an answer followed by `[Source: refund-policy.md]`, and the quoted text really appears in that file.

<details>
<summary>Show the step-by-step answer</summary>

**Step 1. Replace the request in `answer_from_documents`.** Each chunk becomes a `document` block. You no longer need the `<documents>` text or the "name the source" rule.

```python
def answer_from_documents(question: str, role: str = "customer") -> str:
    found = search(question, chunks_for(role))
    blocks = [
        {
            "type": "document",
            "source": {"type": "text", "media_type": "text/plain", "data": chunk.text},
            "title": chunk.source,
            "citations": {"enabled": True},
        }
        for chunk in found
    ]
    response = client.messages.create(
        model=MODEL,
        max_tokens=4000,
        system=system_prompt_for(role) + "\nAnswer only from the documents. If they don't contain the answer, say: \"The company documents don't cover that.\"",
        messages=[{"role": "user", "content": blocks + [{"type": "text", "text": question}]}],
    )
    parts = []
    for block in response.content:
        if block.type != "text":
            continue
        parts.append(block.text)
        sources = {citation.document_title for citation in (block.citations or [])}
        if sources:
            parts.append(" [Source: " + ", ".join(sorted(sources)) + "]")
    return "".join(parts)
```

| Line | What it does |
|---|---|
| `"source": {"type": "text", ...}` | A plain-text document. PDFs use the base64 source from problem 3. |
| `"title": chunk.source` | The name that comes back in each citation. |
| `"citations": {"enabled": True}` | Turn this on for every document in the request, or for none. |
| `block.citations` | The list of quotes that support this part of the answer. Each has `cited_text` and `document_title`. |

**Step 2. Check a quote.** Print `citation.cited_text` once and find it in the file. The quote is taken from your document by the API, so it can't be invented.

**Step 3. Know one limit.** Citations can't be combined with structured outputs (`output_config.format`) in the same request. Choose citations for answers people read, and structured outputs for data your code reads.

**Step 4. Run the eval** and record the score.

</details>

**Why this matters:** API citations give checkable sources, which matters for trust and audits (Governance, Safety & Risk).

---

### Problem 5: Cache the part of the prompt that never changes

**Lessons:** 43, Prompt caching, and 45, Prompt caching in action

**The problem:** Every request in the chat sends the same tools and system prompt again, and you pay for them each time. Turn on prompt caching in `run_turn`, so the unchanged start of the request is stored and reused. Then measure: run the same 5 questions with caching off and on, and save the cost per question in `evaluations/results/benchmark.json`.

- **Check:** with caching on, `cache_read_input_tokens` is above zero from the second request, and the cost per question is lower.

<details>
<summary>Show the step-by-step answer</summary>

**Step 1. Understand prompt caching.** The API reads a request in this order: tools, then system prompt, then messages. With caching on, it stores the start of the request. The next request that begins with exactly the same text reads that part from the cache, at about one tenth of the normal input price. Writing to the cache costs a little more than normal input (about 1.25 times). The cache lasts about 5 minutes by default, and each use refreshes it.

**Step 2. Turn it on in `app/agent_loop.py`.** Top-level `cache_control` caches automatically up to the last block that can be cached. Add a `cache` argument so you can compare.

```python
def run_turn(messages, system, user, tools=TOOLS, model=MODEL, cache=True, usage_log=None):
    extra = {"cache_control": {"type": "ephemeral"}} if cache else {}
    for _ in range(MAX_ROUNDS):
        response = client.messages.create(
            model=model, max_tokens=4000, system=system, tools=tools, messages=messages, **extra
        )
        if usage_log is not None:
            usage_log.append(response.usage)
        # ... the rest of the loop is unchanged
```

**Step 3. Write `experiments/cache_benchmark.py`.** Prices are per million tokens. Check the current prices on the [pricing page](https://platform.claude.com/docs/en/about-claude/pricing) and update the constants.

```python
import json

from app.agent_loop import run_turn
from app.prompts import system_prompt_for

PRICE_IN, PRICE_OUT = 0.10, 0.50          # Haiku 5.5, dollars per million tokens
PRICE_WRITE, PRICE_READ = PRICE_IN * 1.25, PRICE_IN * 0.10
QUESTIONS = ["How long do I have for a refund?", "What does an orange light mean?",
             "How much is the Fast plan?", "What's the status of ticket 1042?", "Is there an outage in Riverside?"]


def cost(usage) -> float:
    return (usage.input_tokens * PRICE_IN + usage.output_tokens * PRICE_OUT
            + (usage.cache_creation_input_tokens or 0) * PRICE_WRITE
            + (usage.cache_read_input_tokens or 0) * PRICE_READ) / 1_000_000


user = {"role": "customer", "customer_id": "C-1001"}
report = {}
for cache in [False, True]:
    log, messages = [], []
    for question in QUESTIONS:
        messages.append({"role": "user", "content": question})
        run_turn(messages, system_prompt_for("customer"), user, cache=cache, usage_log=log)
    report["cache_on" if cache else "cache_off"] = {
        "cost_per_question": sum(cost(u) for u in log) / len(QUESTIONS),
        "cache_read_tokens": sum(u.cache_read_input_tokens or 0 for u in log),
    }
print(json.dumps(report, indent=2))
with open("evaluations/results/benchmark.json", "w", encoding="utf-8") as f:
    json.dump(report, f, indent=2)
```

**Step 4. Run it.** `uv run python -m experiments.cache_benchmark`

**Step 5. If `cache_read_tokens` is 0,** the cached start may be too short. Haiku 5.5 only caches a start of at least 512 tokens; your tools and system prompt together are probably above that, but check `cache_creation_input_tokens` on the first request.

</details>

**Why this matters:** caching is the first cost lever to pull, and you prove it with measured numbers (Context Management & Reliability).

---

### Problem 6: Break the cache on purpose

**Lesson:** 44, Rules of prompt caching

**The problem:** Add the current time to the start of the system prompt, like `Current time: 14:03:27`, and run the benchmark again. Watch the cache stop working. Then put the time where it doesn't break the cache.

- **Check:** you can explain why the first version reads 0 cached tokens, and the fixed version reads them again.

<details>
<summary>Show the step-by-step answer</summary>

**Step 1. Break it.** In the benchmark, change the system prompt to `f"Current time: {datetime.datetime.now():%H:%M:%S}\n" + system_prompt_for("customer")`, import `datetime`, and run it. `cache_read_tokens` drops to 0.

**Step 2. Understand why.** The cache only matches when the start of the request is exactly the same, byte for byte. The time changes every second, and the system prompt comes before the messages. So everything after the time is new to the cache on every request.

**Step 3. Fix it.** Put things that change *after* the things that don't. Remove the time from the system prompt and add it to the user's message instead: `messages.append({"role": "user", "content": f"(Time: {now:%H:%M})\n{question}"})`. Run it again; cache reads come back.

**Step 4. Learn the list of silent cache breakers.**

| Breaker | Fix |
|---|---|
| A time, date, or random ID in the system prompt | Move it into the latest message. |
| Tools listed in a different order each time | Always build the tool list in the same order. |
| JSON written with keys in a different order | Use `json.dumps(..., sort_keys=True)`. |
| Changing the model or the effort between requests | Keep them fixed for a conversation. |

</details>

**Why this matters:** "why is our cache hit rate zero?" is a classic production question, and the answer is almost always a changing value near the start of the prompt (Context Management & Reliability).

---

### Problem 7: Let the model analyse the tickets with code

**Lesson:** 46, Code execution and the Files API

**The problem:** A team lead wants a quick report: how many open tickets each team has, and a bar chart. Write `experiments/ticket_report.py`. It turns `data/tickets.json` into a CSV file, uploads it with the Files API, and asks the model to analyse it with the code execution tool. Save any chart it makes to `docs/reports/`.

- **Check:** the script prints the counts per team and saves a PNG chart.

<details>
<summary>Show the step-by-step answer</summary>

**Step 1. Know the two parts.** The **Files API** stores a file on Anthropic's side and gives you a `file_id`, so you can use it in many requests without sending it again. The **code execution tool** is a server tool: the model writes Python and runs it in a sandbox (a closed-off computer) on Anthropic's side.

**Step 2. Write `experiments/ticket_report.py`.**

```python
import csv
import json
import os
from pathlib import Path

from app.client import MODEL, client, get_text

tickets = json.loads(Path("data/tickets.json").read_text(encoding="utf-8"))
with open("data/tickets.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=["id", "status", "priority", "team"], extrasaction="ignore")
    writer.writeheader()
    writer.writerows(tickets)

uploaded = client.files.upload(file=Path("data/tickets.csv"))

response = client.messages.create(
    model=MODEL,
    max_tokens=8000,
    tools=[{"type": "code_execution_20260521", "name": "code_execution"}],
    messages=[{
        "role": "user",
        "content": [
            {"type": "text", "text": "Count the open tickets per team, print the counts, and save a bar chart as open_tickets.png."},
            {"type": "container_upload", "file_id": uploaded.id},
        ],
    }],
)
print(get_text(response))

os.makedirs("docs/reports", exist_ok=True)
for block in response.content:
    if block.type == "bash_code_execution_tool_result":
        result = block.content
        if result.type == "bash_code_execution_result":
            print("stdout:", result.stdout)
            for item in result.content or []:
                info = client.files.retrieve_metadata(item.file_id)
                name = os.path.basename(info.filename)
                client.files.download(item.file_id).write_to_file(f"docs/reports/{name}")
                print("Saved", name)
```

| Line | What it does |
|---|---|
| `client.files.upload(file=Path(...))` | Uploads the CSV and returns an object with its `id`. |
| `code_execution_20260521` | The current version of the code execution tool. |
| `container_upload` | Puts the uploaded file into the sandbox, so the model's code can open it. |
| `bash_code_execution_tool_result` | The result of the code the model ran: its printed output and any files it made. |
| `os.path.basename(...)` | Keeps only the file name, so a strange name can't write outside `docs/reports`. |

**Step 3. Run it.** `uv run python -m experiments.ticket_report`. If the API says the model doesn't support this tool, set the model to `claude-sonnet-5-5` for this script.

**Step 4. Clean up.** Uploaded files stay until you delete them. Delete it with `client.files.delete(uploaded.id)` when you're done. Only upload made-up data.

</details>

**Why this matters:** code execution suits counting and charts, because code is exact where the model's arithmetic may not be (Tool Design & MCP Integration).

---

### Architect scenario: is caching worth it for the shop?

**The scenario:** the shop's email sorter from [guide 1](01-accessing-claude-with-the-api.md#architect-scenario-sorting-1000-shop-emails-a-day) has grown. Its system prompt now holds a 3,000-token returns and billing policy, so the sorter can quote it. It still handles 1,000 emails a day, mostly between 9:00 and 17:00. The team asks whether prompt caching is worth turning on, and whether switching to a larger model, Claude Sonnet 5.5, changes the answer.

- **Check:** you give the daily cost with and without caching for both models, and say when the cache stays warm.

<details>
<summary>Show the step-by-step answer</summary>

**Step 1. Check that the cache stays warm.** 1,000 emails in 8 hours is about one email every 30 seconds. The cache lasts about 5 minutes and each use refreshes it, so during working hours almost every request reads from the cache. Overnight it expires, so the first email each morning pays to write it again.

**Step 2. Do the sum for the repeated 3,000 tokens only.** Per day that is 3,000,000 tokens. The prices are per million tokens and change, so check the pricing page.

| Model | Input price | Without caching | With caching (reads at about 0.1 times the price) |
|---|---|---|---|
| Haiku 5.5 | $0.10 | about $0.30 a day | about $0.03 a day, plus a few cache writes |
| Sonnet 5.5 | $2.00 | about $6.00 a day | about $0.60 a day, plus a few cache writes |

**Step 3. Read the result.** On Haiku, caching saves cents, so it's nice but not urgent. On Sonnet, it saves about $5 a day, or more than $1,800 a year, for one setting. Caching also makes each request start faster, because cached text doesn't need to be read again.

**Step 4. Check the conditions.** The 3,000-token policy must come first and never change between requests. If someone adds today's date at the top of the prompt, the saving disappears (problem 6). When the policy is updated, the cache simply refills.

**Step 5. Answer the team.** "Yes. Turn on caching with the policy at the start of the prompt. It saves about 90% of the cost of the policy text and makes responses faster. It matters most if we move to a larger model."

</details>

**Why this matters:** caching saves the most when a long, unchanging prompt is reused often and the model is expensive (Context Management & Reliability).

---

### Commit your work

```bash
uv run pytest
uv run python -m evaluations.run_evals
git add .
git status
git commit -m "Capstone guide 6: thinking, images, PDF, citations, caching benchmark, code execution"
git push
```

**Warning:** check that `.env` is not in the `git status` list, and that `data/router.jpg` has no private details, before you commit.

Then mark guide 6 as done in the [capstone index](../README.md#the-chapter-guides).

---

| Previous | Capstone | Next |
|:---|:---:|---:|
| [← Guide 5: RAG and agentic search](05-rag-and-agentic-search.md) | [Capstone index](../README.md) | [Guide 7: Model Context Protocol →](07-model-context-protocol.md) |
