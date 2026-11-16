# Lesson 8 — Structured data

**Course:** [Building with the Claude API](https://academy.claude.com/courses/building-with-the-claude-api) &nbsp;·&nbsp; **Lesson page:** [Structured data](https://academy.claude.com/courses/building-with-the-claude-api/structured-data) &nbsp;·&nbsp; **Chapter 1:** Accessing Claude with the API &nbsp;·&nbsp; **Completed:** November 15, 2026

| Previous | Course | Next |
|:---|:---:|---:|
| [← Response streaming](07-response-streaming.md) | [📚 Course index](README.md) | [Prompt evaluation →](09-prompt-evaluation.md) |

---

**On this page**

| # | Section |
|:---:|:---|
| 1 | [Revision summary](#revision-summary) |
| 2 | [The big picture](#the-big-picture) |
| 3 | [1. The problem: extra text around the data](#1-the-problem-extra-text-around-the-data) |
| 4 | [2. Stop sequences](#2-stop-sequences) |
| 5 | [3. Prefill and stop sequence together](#3-prefill-and-stop-sequence-together) |
| 6 | [4. Cleaning and parsing the result](#4-cleaning-and-parsing-the-result) |
| 7 | [5. Beyond JSON](#5-beyond-json) |
| 8 | [6. The current way: structured outputs](#6-the-current-way-structured-outputs) |
| 9 | [7. Nested JSON and more than one JSON](#7-nested-json-and-more-than-one-json) |
| 10 | [Architect notes](#architect-notes) |
| 11 | [Recap](#recap) |
| 12 | [My notes / practice](#my-notes--practice) |
| 13 | [FAQ](#faq) |

---

### Revision summary

- **The problem:** when you ask the model for JSON, it usually wraps the JSON in a Markdown code block and adds a sentence of explanation. Your app then can't use the answer as it is.
- **Stop sequence:** a piece of text you list in the request. The moment the model writes it, the API ends the answer. The stop text itself is not included.
- **Prefill:** an assistant message you write yourself, placed last in the message list. The model treats it as the start of its own answer and continues from there.
- **Together:** prefill with ` ```json ` and stop on ` ``` `. The model writes only the JSON, then stops as it tries to close the code block.

#### How the trick works, step by step

Your code sends one request with a user message, a prefilled assistant message, and a stop sequence:

1. The user message asks: "Generate a very short event bridge rule as json."
2. The prefilled assistant message is ` ```json `. The model believes it has already opened a JSON code block.
3. The model continues by writing the JSON itself, with no introduction.
4. When the model writes ` ``` ` to close the block, the stop sequence ends the answer at once.
5. The answer holds only the JSON, plus a few line breaks. Your code removes them with `.strip()` and reads the JSON with `json.loads()`.

#### What to prefill and where to stop

The rule: find what the model naturally wraps your content in. Use the opening as the prefill and the closing as the stop sequence.

- **For JSON:** prefill ` ```json ` and stop on ` ``` `.
- **For Python code:** prefill ` ```python ` and stop on ` ``` `.
- **For CSV data:** prefill ` ```csv ` and stop on ` ``` `.
- **For a bulleted list:** ask for the list inside tags such as `<list>`, prefill `<list>`, and stop on `</list>`.

#### When to use which way of getting clean data

- **Use prefill plus a stop sequence** on older models that accept prefill, such as `claude-haiku-4-5`, the model this course uses. For example, a JSON rule generator built on Haiku 4.5.
- **Use structured outputs** (the `output_config.format` setting with a JSON schema) on current models, such as `claude-opus-5-5` or `claude-sonnet-5-5`. Prefill returns a 400 error there. Structured outputs also guarantee the JSON matches your schema.
- **Use a system prompt instruction** ("Answer with the content only, with no introduction") when you only want to skip the opening sentence and don't need machine-readable data.

#### Exam takeaways

- **A web app shows generated JSON with a copy button, but users keep copying the Markdown fences and the explanation too.** Prefill the assistant message with ` ```json ` and add ` ``` ` as a stop sequence, so the answer holds only the JSON. On current models, use structured outputs instead. (Integration)
- **A team moves prefill code from Haiku 4.5 to a newer model, and every request now fails with a 400 error.** Newer models reject a prefilled last assistant message. Replace the prefill with structured outputs (`output_config.format`) or a system prompt instruction. (Claude Models, Prompting & Context Engineering)
- **A pipeline parses model JSON and sometimes crashes on a missing field.** Prefill only shapes the start of the answer. It doesn't guarantee valid or complete JSON. Validate the parsed result in code, or use structured outputs with a schema, which guarantees the shape. (Solution Design & Architecture)

---

### The big picture

| Part | In plain words | Everyday comparison |
|---|---|---|
| The problem | The model adds wrapping and chat around the data | Ordering a part and getting it in gift wrap with a card |
| Stop sequence | Text that makes the API end the answer the moment it appears | A referee's whistle: play stops on that sound |
| Prefill | You write the first words of the model's answer | Starting someone's sentence, so they finish it your way |
| Structured outputs | The API forces the answer to match a JSON shape you give | A form with fixed boxes, so nothing extra fits |

**The running example:** a web app called "EventBridge Rule Generator." A user types "Rule to monitor EC2 instances" and clicks **Generate**. The app should show clean JSON with a copy button.

Two words in that example:

- **AWS EventBridge** is an Amazon Web Services service that watches for events, such as a server starting. A **rule** is a small piece of JSON that says which events to catch.
- **EC2 instances** are virtual servers rented from Amazon.

![The EventBridge Rule Generator app: the input "Rule to monitor EC2 instances", a Generate button, and a dark box with clean JSON and a copy button](images/08-eventbridge-rule-generator.png)

#### Who's who

| Player | Where it lives | What it does |
|---|---|---|
| **The user** | In front of the web app | Types a description and copies the JSON |
| **Your app** (Python code) | Your server | Builds the messages, sets the stop sequence, calls the API, and parses the answer |
| **The Claude API and the model** | Anthropic's servers | Continues the prefilled answer and stops when it writes the stop sequence |

---

### 1. The problem: extra text around the data

By default, a request for JSON returns something like this:

````text
```json
{
  "source": ["aws.ec2"],
  "detail-type": ["EC2 Instance State-change Notification"],
  "detail": {
    "state": ["running"]
  }
}
```

This rule captures EC2 instance state changes when instances start running.
````

The JSON is correct. But it sits between Markdown fences (the ` ``` ` lines that mark a code block), and a sentence follows it. If the app's copy button copies the whole answer, the user pastes text that AWS rejects. The user has to select the JSON by hand.

The model adds this wrapping to be helpful in a chat. In an app, your code is the reader, and code needs the raw data only.

---

### 2. Stop sequences

A **stop sequence** is a piece of text you list in the request. As soon as the model writes it, the API ends the answer. You saw the `stop_sequence` stop reason in [lesson 1](01-accessing-the-api.md).

The course adds a `stop_sequences` option to the `chat()` helper from [lesson 6](06-temperature.md):

```python
def chat(messages, system=None, temperature=1.0, stop_sequences=[]):
    params = {
        "model": model,
        "max_tokens": 1000,
        "messages": messages,
        "temperature": temperature
    }
    if system:
        params["system"] = system
    if stop_sequences:
        params["stop_sequences"] = stop_sequences

    message = client.messages.create(**params)
    return message.content[0].text
```

- `stop_sequences=[]` means the option is empty unless the caller passes a list, such as `["```"]`.
- `if stop_sequences:` adds the setting to the request only when the list has something in it.
- `params["stop_sequences"]` is the real API setting name. It takes a list, so you can give several stop texts.

**Not in the course, from the official Claude API documentation:** when a stop sequence ends the answer, the response has `stop_reason` set to `"stop_sequence"`. The `stop_sequence` field shows which text matched. The matched text is not part of the answer.

---

### 3. Prefill and stop sequence together

**Prefilling** means you add an assistant message as the last message in the list. The model does not start a new answer. It continues the text you wrote, as if it had written those words itself.

```python
messages = []

add_user_message(messages, "Generate a very short event bridge rule as json")
add_assistant_message(messages, "```json")

text = chat(messages, stop_sequences=["```"])
```

- `add_user_message()` and `add_assistant_message()` are the helpers from [lesson 4](04-multi-turn-conversations.md).
- The assistant message ` ```json ` is the prefill. Your code wrote it. The model did not.
- `stop_sequences=["```"]` ends the answer when the model writes the closing fence.

![The request holds the stop sequence ```, the user message "Generate an Event Bridge rule as JSON", and the prefilled assistant message ```json. Claude thinks "I need to write a full rule and describe it", then "Oh, I've already started the JSON part!", then "All done with the json, I'll close it with ```"](images/08-prefill-and-stop-sequence.png)

#### What the model "thinks" at each step

| Step | What the model sees | What happens |
|---|---|---|
| 1 | The user message alone | It plans to write a full rule and describe it |
| 2 | Its answer already starts with ` ```json ` | It skips any introduction and writes JSON straight away |
| 3 | The JSON is finished | It writes ` ``` ` to close the block |
| 4 | The API spots the stop sequence | The answer ends there, so the closing sentence is never written |

The answer that comes back is only the new text, without your prefill:

```json
{
  "source": ["aws.ec2"],
  "detail-type": ["EC2 Instance State-change Notification"],
  "detail": {
    "state": ["running"]
  }
}
```

> **Remember this:** Open the box for the model (prefill), and stop it as it tries to close the box (stop sequence).

**Warning:** Prefill only works on older models, such as `claude-haiku-4-5`, the model this course uses. On Claude Opus 4.6, Sonnet 4.6, and every newer model, a request whose last message is a prefilled assistant message fails with a 400 error. Section 6 shows the replacement.

---

### 4. Cleaning and parsing the result

The answer often starts and ends with a line break. For example, the model writes a new line right after ` ```json `. Python can clean that up and read the JSON:

```python
import json

# Clean up and parse the JSON
clean_json = json.loads(text.strip())
```

- `text.strip()` removes spaces and line breaks from both ends of the text.
- `json.loads()` turns JSON text into Python data (a dictionary here), such as `clean_json["source"]`, which gives `["aws.ec2"]`.

**Warning:** Prefill and stop sequences shape the answer, but they don't promise valid JSON. The model could still leave out a comma or a field. `json.loads()` then raises an error. Catch that error, and check that the fields your app needs are there.

---

### 5. Beyond JSON

The same trick works for any content the model normally wraps:

| You want | Prefill | Stop sequence |
|---|---|---|
| JSON | ` ```json ` | ` ``` ` |
| A Python code snippet | ` ```python ` | ` ``` ` |
| CSV data (rows of comma-separated values) | ` ```csv ` | ` ``` ` |
| A bulleted list (my example, not the course's) | `<list>`, after asking for the list inside `<list>` tags | `</list>` |

The course's rule: find what the model naturally wraps your content in. Use that wrapping's opening as the prefill and its closing as the stop sequence.

---

### 6. The current way: structured outputs

**Not in the course, from the official Claude API documentation:** current models reject prefill. The replacement for JSON is **structured outputs**. You give the API a **JSON schema** (a description of the exact fields and their types). The API then makes sure the answer is JSON that matches it.

```python
response = client.messages.create(
    model="claude-opus-5-5",
    max_tokens=16000,
    messages=[{"role": "user", "content": "Generate a very short event bridge rule as json"}],
    output_config={
        "format": {
            "type": "json_schema",
            "schema": {
                "type": "object",
                "properties": {
                    "source": {"type": "array", "items": {"type": "string"}},
                    "detail-type": {"type": "array", "items": {"type": "string"}}
                },
                "required": ["source", "detail-type"],
                "additionalProperties": False
            }
        }
    }
)
rule = json.loads(response.content[0].text)
```

- `output_config` holds output settings. Its `format` part says "answer as JSON matching this schema."
- `"required"` lists the fields that must appear. `"additionalProperties": False` forbids any other field.
- No prefill, no stop sequence, and no `.strip()` is needed. The answer is plain JSON.

| Way | Works on | Shape guaranteed? | Use it when |
|---|---|---|---|
| Prefill + stop sequence | Older models, such as Haiku 4.5 | No | You follow this course, or you maintain code on an older model |
| Structured outputs | Current models | Yes | You build anything new that parses JSON |
| System prompt instruction | All models | No | You only want to skip the introduction sentence |

---

### 7. Nested JSON and more than one JSON

**Not in the course; my answer to a follow-up question.** Say your app needs two things from one answer: customer data and that customer's orders.

#### Nested JSON works with both ways

*Nested* JSON means objects inside objects, or lists of objects. For example, a customer object that holds an address object.

- **Prefill and stop sequence:** nesting is no problem. The stop sequence ` ``` ` never matches a `}` or `]`, so the model writes the whole nested object before it stops.
- **Structured outputs:** the schema itself can hold nested objects and lists of objects (see the example below).

#### Two separate JSON blocks break the prefill trick

Suppose you ask for "the customer as one JSON block, then the orders as a second JSON block." With prefill ` ```json ` and stop sequence ` ``` `, this happens:

| Step | What the model writes | Result |
|---|---|---|
| 1 | The customer JSON, after your ` ```json ` prefill | Kept in the answer |
| 2 | ` ``` ` to close the first block | The stop sequence fires, and the answer ends |
| 3 | The orders JSON | Never written |

So your app gets the customer data only, and the order data is lost.

#### The fix: one JSON object that holds both

Ask for a single object with one key per part:

```json
{
  "customer": {"id": "C-101", "name": "Asha Rao", "email": "asha@example.com"},
  "orders": [
    {"order_id": "O-1", "total": 49.99},
    {"order_id": "O-2", "total": 15.00}
  ]
}
```

- With prefill, the user message says: "Return the customer and their orders as one JSON object with the keys `customer` and `orders`." Then parse once and read `data["customer"]` and `data["orders"]`.
- With structured outputs, write the same shape as a schema:

```python
schema = {
    "type": "object",
    "properties": {
        "customer": {
            "type": "object",
            "properties": {
                "id": {"type": "string"},
                "name": {"type": "string"},
                "email": {"type": "string"}
            },
            "required": ["id", "name", "email"],
            "additionalProperties": False
        },
        "orders": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "order_id": {"type": "string"},
                    "total": {"type": "number"}
                },
                "required": ["order_id", "total"],
                "additionalProperties": False
            }
        }
    },
    "required": ["customer", "orders"],
    "additionalProperties": False
}
```

- `"type": "array"` with `"items"` means "a list, where every item has this shape." Here, every order has an `order_id` and a `total`.
- Each object, including the nested ones, gets its own `required` list and `"additionalProperties": False`.
- Pass `schema` in `output_config` exactly as in section 6.

| Need | Use it when | How |
|---|---|---|
| One combined object | The parts belong together, such as a customer and their orders | One JSON object with a key per part (recommended) |
| Two separate requests | The parts are unrelated, or each one is large | One request per JSON |
| Tags, no stop sequence | You must keep separate blocks on an older model | Ask for each JSON inside its own tags, such as `<customer>` and `<orders>`, then cut them out in code |

---

### Architect notes

#### Reliability

- Always parse inside a `try` block and validate the fields. A model can return broken JSON, and a crash in production is worse than a clear error and a retry.
- Check `stop_reason`. A `"max_tokens"` stop means the JSON was cut off before the model finished it. A `"stop_sequence"` stop is the expected result here.
- A stop sequence can fire too early if the same text appears inside the content. For example, a Python snippet that contains ` ``` ` inside a string ends the answer in the middle.

#### Limits and pitfalls

- The API rejects a prefill that ends with a space or line break. Write ` ```json `, not ` ```json\n `.
- The returned text does not include your prefill. If you need the full text, join the prefill and the answer yourself.

#### Cost and speed

- Stop sequences save output tokens. The closing sentence is never written, so you don't pay for it, and the answer arrives sooner.
- Structured outputs add a little to the first request with a new schema, while the API prepares that schema. Later requests with the same schema reuse it. Look up the current behaviour, because it can change.

#### Design trade-offs

- For new code, prefer structured outputs. They work on current models and guarantee the shape, so your parsing code stays simple.
- Keep prefill code only where you must stay on an older model. Plan to move it to structured outputs when you upgrade the model.

---

### Recap

- By default, the model wraps JSON in Markdown fences and adds an explanation, so apps can't use the answer as it is.
- A stop sequence ends the answer the moment the model writes a given text.
- A prefill is an assistant message you write. The model continues from it.
- Prefill ` ```json ` plus stop sequence ` ``` ` returns only the JSON. Clean it with `.strip()` and parse it with `json.loads()`.
- The same trick works for code, CSV, and lists: prefill the opening wrapper and stop on the closing one.
- Current models reject prefill. Use structured outputs (`output_config.format`) instead.

---

## My notes / practice

- [ ] Ask `claude-haiku-4-5` for an EventBridge rule as JSON with no prefill, and look at the extra text.
- [ ] Add the ` ```json ` prefill and the ` ``` ` stop sequence, and parse the answer with `json.loads()`.
- [ ] Print `stop_reason` and `stop_sequence` from the full message object.
- [ ] Try the trick for a CSV of three fake customers.
- [ ] Send the same prefill request to `claude-sonnet-5-5`, read the 400 error, then rewrite it with structured outputs.

---

## FAQ

**Q1. Why does the model add text around the JSON I asked for?**
It is trained to be helpful in a chat, so it formats code in Markdown blocks and explains what it wrote. That suits a person, but not code that needs to read the data.

**Q2. What does "stop sequence" mean?**
It is a piece of text you list in the request. As soon as the model writes it, the API ends the answer, and the stop text is left out. For example, with ` ``` ` as a stop sequence, the answer ends where the code block would close.

**Q3. What does "prefill" mean?**
It means you write the first part of the model's answer yourself, as the last message in the list, with the role `assistant`. The model continues from your text instead of starting fresh.

**Q4. Why do prefill and stop sequence work well together?**
The prefill ` ```json ` makes the model skip the introduction and start with JSON. The stop sequence ` ``` ` ends the answer before the closing explanation. So the answer holds only the JSON.

**Q5. Does the answer include my prefilled text, and why does it start with a line break?**
No, the answer holds only the new text the model wrote after your prefill. It often starts with a line break because the model writes a new line after ` ```json `. Remove it with `text.strip()` before you call `json.loads()`.

**Q6. Does this trick work for things other than JSON?**
Yes. Use it for code, CSV data, or lists. Prefill the opening wrapper the model would use, such as ` ```python `, and stop on the closing one, such as ` ``` `.

**Q7. Does prefill work on every Claude model?**
No. It works on older models such as `claude-haiku-4-5`. Claude Opus 4.6, Sonnet 4.6, and every newer model reject a prefilled last assistant message with a 400 error.

**Q8. What does "structured outputs" mean?**
It is an API setting, `output_config.format`, where you give a JSON schema. The API then makes sure the answer is JSON with exactly those fields. It replaces prefill for JSON on current models.

**Q9. Does prefill with a stop sequence work for nested JSON?**
Yes. Nested JSON means objects inside objects, or lists of objects, such as a customer with an address inside it. The stop sequence ` ``` ` never matches a `}` or `]`, so the model writes the whole nested object before it stops. Structured outputs handle nesting too: the schema just describes the inner objects.

**Q10. Can one answer return two JSONs, such as customer data and order data?**
Not as two separate blocks with prefill. The stop sequence fires when the first block closes, so only the customer data comes back. Instead, ask for one object that holds both, such as `{"customer": {...}, "orders": [...]}`, then read `data["customer"]` and `data["orders"]`. With structured outputs, describe that same combined shape in the schema.

**Q11. (Exam angle) A web app shows generated JSON with a copy button, but users keep copying Markdown fences and an explanation. How do you fix the output?**
On a model that accepts prefill, prefill ` ```json ` and add ` ``` ` as a stop sequence, so only the JSON comes back. On current models, use structured outputs with a JSON schema. (Integration)

**Q12. (Exam angle) A team moves prefill code from Haiku 4.5 to a newer model, and every request now fails with a 400 error. What do you tell them?**
Newer models don't accept a prefilled last assistant message. Replace the prefill with structured outputs (`output_config.format`) for JSON, or with a system prompt instruction to skip any introduction. (Claude Models, Prompting & Context Engineering)

**Q13. (Exam angle) A data pipeline parses model JSON and sometimes crashes on a missing field. What do you recommend?**
Prefill and stop sequences shape the answer but don't guarantee valid or complete JSON. Validate the parsed data and handle errors, or switch to structured outputs, which guarantee the schema. Also check `stop_reason` for `"max_tokens"`, which means the JSON was cut off. (Solution Design & Architecture)

---

| Previous | Course | Next |
|:---|:---:|---:|
| [← Response streaming](07-response-streaming.md) | [📚 Course index](README.md) | [Prompt evaluation →](09-prompt-evaluation.md) |
