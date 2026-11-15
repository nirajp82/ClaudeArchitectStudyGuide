# Lesson 5 — System prompts

**Course:** [Building with the Claude API](https://academy.claude.com/courses/building-with-the-claude-api) &nbsp;·&nbsp; **Lesson page:** [System prompts](https://academy.claude.com/courses/building-with-the-claude-api/system-prompts) &nbsp;·&nbsp; **Chapter 1:** Accessing Claude with the API &nbsp;·&nbsp; **Completed:** November 15, 2026

| Previous | Course | Next |
|:---|:---:|---:|
| [← Multi-Turn conversations](04-multi-turn-conversations.md) | [📚 Course index](README.md) | [Temperature →](06-temperature.md) |

---

**On this page**

| # | Section |
|:---:|:---|
| 1 | [Revision summary](#revision-summary) |
| 2 | [The big picture](#the-big-picture) |
| 3 | [1. Why a system prompt matters](#1-why-a-system-prompt-matters) |
| 4 | [2. How to send a system prompt](#2-how-to-send-a-system-prompt) |
| 5 | [3. The difference it makes](#3-the-difference-it-makes) |
| 6 | [4. A chat function that takes an optional system prompt](#4-a-chat-function-that-takes-an-optional-system-prompt) |
| 7 | [Architect notes](#architect-notes) |
| 8 | [Recap](#recap) |
| 9 | [My notes / practice](#my-notes--practice) |
| 10 | [FAQ](#faq) |

---

### Revision summary

- **System prompt:** instructions that you, the developer, write once to tell the model how to behave, such as "You are a patient math tutor."
- **Where it goes:** in the separate `system` setting of `client.messages.create()`, not inside the `messages` list.
- **What it changes:** the model's tone, style, and approach. It answers the way someone in that role would.
- **Why it helps:** the model behaves the same way on every request and stays on task.

#### How a system prompt changes an answer

A student asks "How do I solve 5x + 2 = 3 for x?"

- **Without a system prompt:** the model gives the complete step-by-step solution at once. The student doesn't have to think.
- **With a math tutor system prompt:** the model asks a guiding question instead, such as "What do you think would be a good first step to isolate x?"

A good tutor prompt says what the model should do (give hints first, walk through steps patiently, show similar solved problems). It also says what to avoid (giving the answer at once, telling the student to use a calculator).

#### How to send one in Python

- Write the system prompt as a plain Python string, such as `system_prompt = """You are a patient math tutor. ..."""`.
- Pass it as `system=system_prompt` in `client.messages.create()`, next to `model`, `messages`, and `max_tokens`.
- The API does not accept `system=None`. So a reusable `chat(messages, system=None)` function builds a dictionary of settings, adds `"system"` only when a system prompt was given, and calls `client.messages.create(**params)`.

#### When to use a system prompt or a user message

- **Use the system prompt** for rules that apply to the whole conversation, written by you, the developer. For example: "You are a patient math tutor. Don't give the answer directly."
- **Use a user message** for what the person asks right now. For example: "How do I solve 5x + 2 = 3 for x?"

#### Exam takeaways

- **A tutoring app keeps giving students full answers, and the product team wants hints first.** Put the role and the rules in a system prompt: act as a patient tutor, give hints first, never give the answer at once. Then test it on real student questions. (Claude Models, Prompting & Context Engineering)
- **A team puts an internal discount code in the system prompt and tells the model to keep it secret.** A system prompt is not a safe place for secrets, because users can sometimes trick the model into repeating it. Keep secrets in your server code, and check sensitive actions in code. (Governance, Safety & Risk Management)
- **A long system prompt makes every request expensive.** The system prompt is input tokens on every request, so keep it as short as the job allows. Keep it identical across requests so prompt caching can reuse it. (Solution Design & Architecture)

---

### The big picture

| Part | In plain words | Everyday comparison |
|---|---|---|
| System prompt | Standing instructions from you, the developer | A job briefing a new tutor gets before meeting any students |
| User message | What the person asks right now | The student's question in the lesson |
| The answer | The model answers the question, following the briefing | The tutor answers the way the briefing said to |

**The running example:** you build a math tutor chatbot. A student types "How do I solve 5x + 2 = 3 for x?" You want the model to teach, not just hand over the answer.

#### Who's who

| Player | Where it lives | What it does in the example |
|---|---|---|
| **You, the developer** | Your code | Write the system prompt once, such as "You are a patient math tutor" |
| **The student** (the user) | In front of your app | Types the math question. Never sees the system prompt. |
| **Your code** | Your notebook or server | Sends the system prompt and the `messages` list together in each request |
| **The model** | Anthropic's servers | Reads the system prompt first, then the messages, and answers as a tutor |

---

### 1. Why a system prompt matters

Without guidance, the model gives a generic, helpful answer. For a math question, that usually means the full solution. That is fine for an adult checking homework. It is bad for a student who needs to learn.

![Math Tutor Specialist: responses should first give hints, patiently walk the student through a solution, and show solutions for similar problems; they should not give a direct answer at once or tell the student to use a calculator](images/05-math-tutor-requirements.png)

A good math tutor should:

1. Give hints first, not complete solutions.
2. Walk the student through the problem patiently, step by step.
3. Show solutions to similar problems as examples.

A good math tutor should not:

1. Give the direct answer at once.
2. Tell the student to just use a calculator.

A **system prompt** is how you give the model this kind of guidance. The model then tries to answer the way a real person in that role would.

---

### 2. How to send a system prompt

You write the system prompt as a plain string, and pass it to `client.messages.create()` with the `system` setting:

```python
system_prompt = """
You are a patient math tutor.
Do not directly answer a student's questions.
Guide them to a solution step by step.
"""

client.messages.create(
    model=model,
    messages=messages,
    max_tokens=1000,
    system=system_prompt
)
```

What each part does:

- `"""..."""` is a Python *triple-quoted string*. It can span several lines, which keeps a long prompt readable.
- `You are a patient math tutor.` gives the model a role. The model answers the way a patient tutor would.
- `Do not directly answer...` and `Guide them...` are rules for every answer.
- `system=system_prompt` sends the prompt in its own setting. It is separate from `messages`, which holds only `user` and `assistant` messages ([lesson 4](04-multi-turn-conversations.md)).

![System prompts customize Claude's tone and style of response: they provide guidance on how to respond, make Claude respond the way someone in the role would, and help keep Claude on task](images/05-system-prompt-benefits.png)

The three benefits from the course:

1. The system prompt gives the model guidance on how to respond.
2. The model tries to respond the way someone in that role would respond.
3. It helps keep the model on task.

```mermaid
flowchart LR
    subgraph Request["One request from your code"]
        S["system:<br/>You are a patient math tutor..."]
        M["messages:<br/>user: How do I solve 5x + 2 = 3 for x?"]
    end
    Request --> Model[The model reads the system prompt,<br/>then the messages]
    Model --> A["A guiding question,<br/>not the full answer"]
```

Things to notice:

- The system prompt is sent with **every** request. The API is stateless, so it forgets the system prompt too ([lesson 4](04-multi-turn-conversations.md)).
- The student only types the question. Your code adds the system prompt.

---

### 3. The difference it makes

Here is the same question, sent with and without the tutor system prompt:

| | Without a system prompt | With the tutor system prompt |
|---|---|---|
| What the model writes | The full solution: subtract 2 from both sides to get 5x = 1, then divide by 5 to get x = 1/5 | A guiding question: "What do you think would be a good first step to isolate x? Consider what operation we might need to perform on both sides to start moving terms around." |
| What the student does | Copies the answer | Thinks about the first step |
| Good for | Someone checking their work | Someone learning |

The question was the same in both requests. Only the system prompt changed, and it changed the whole style of the answer.

> **Remember this:** The user message says *what* to answer. The system prompt says *how* to answer.

---

### 4. A chat function that takes an optional system prompt

The `chat()` function from [lesson 4](04-multi-turn-conversations.md) can't send a system prompt. The course makes it reusable, so you can call it with or without one:

```python
def chat(messages, system=None):
    params = {
        "model": model,
        "max_tokens": 1000,
        "messages": messages,
    }

    if system:
        params["system"] = system

    message = client.messages.create(**params)
    return message.content[0].text
```

What each line does:

- `system=None` makes the setting optional. If you don't pass a system prompt, `system` is `None`, Python's word for "nothing."
- `params = {...}` collects the settings in a dictionary (a set of name-value pairs) instead of writing them straight into the call.
- `if system:` adds `"system"` to the dictionary only when a system prompt was given.
- `client.messages.create(**params)` unpacks the dictionary. The `**` turns each name-value pair into a setting, so it is the same as writing `model=model, max_tokens=1000, ...` by hand.

Why not just pass `system=system` every time? Because the API doesn't accept `system=None`. Sending it when there is no system prompt would cause an error. Building the dictionary lets the code leave the setting out completely.

Now you can call the same function both ways:

```python
# Without a system prompt
answer = chat(messages)

# With a system prompt
system = """
You are a patient math tutor.
Do not directly answer a student's questions.
Guide them to a solution step by step.
"""
answer = chat(messages, system=system)
```

---

### Architect notes

#### Cost and speed

- The system prompt counts as input tokens on every request. A 1,000-token system prompt in a 10-turn chat is billed 10 times.
- Keep the system prompt identical from request to request. Then prompt caching can reuse it at a lower price ([lessons 43–45](README.md)). Putting a timestamp or user name in it changes the text every time and stops the reuse.

#### Security

- A system prompt is not a secret. Users can sometimes trick the model into repeating it, so never put passwords, API keys, or private codes in it.
- A system prompt guides the model, but it is not a security wall. A user can still try to talk the model out of its rules (*prompt injection*). Check important actions and limits in your own code.

#### Design trade-offs

- Start short and specific. Give a role and the few rules that matter, then test on real questions and add rules only where answers go wrong.
- Write rules as what to do, not only what to avoid. "Give a hint first" works better than a long list of "don'ts".
- Store system prompts in one place, such as a file or setting, so you can change them without hunting through code.
- **Not in the course, from the official Claude API documentation:** newer models also accept a message with the role `system` inside the `messages` list. It adds an instruction partway through a conversation without changing the top-level system prompt, so caching still works.

---

### Recap

- A system prompt is standing guidance from you, the developer, on how the model should answer.
- Send it with `system=` in `client.messages.create()`, separate from the `messages` list.
- It shapes tone, style, and role, and keeps the model on task.
- The same question gets a very different answer with and without a system prompt.
- The API doesn't accept `system=None`, so a reusable `chat()` adds `"system"` only when one is given and calls `create(**params)`.

---

## My notes / practice

- [ ] Ask "How do I solve 5x + 2 = 3 for x?" with no system prompt, then with the tutor prompt. Compare the two answers.
- [ ] Add "Show a solution to a similar problem as an example" to the system prompt, and see what changes.
- [ ] Call `client.messages.create(..., system=None)` once to see the error for yourself.
- [ ] Write a system prompt for a different role, such as a friendly support agent, and test it.

---

## FAQ

**Q1. What does "system prompt" mean?**
It is a set of instructions that you, the developer, send with each request to tell the model how to behave. For example: "You are a patient math tutor. Guide students step by step."

**Q2. How is a system prompt different from a user message?**
The system prompt holds standing rules from you, the developer, for the whole conversation. A user message holds what the person asks right now. The model follows the system prompt while it answers the user message.

**Q3. Where does the system prompt go in the request?**
In the separate `system` setting of `client.messages.create()`. It does not go inside the `messages` list.

**Q4. Can the user see the system prompt?**
Not in your app's chat window, because your code adds it behind the scenes. But users can sometimes trick the model into repeating it, so don't put secrets in it.

**Q5. Do I need to send the system prompt with every request?**
Yes. The API is stateless, so it doesn't remember the system prompt between requests. Your code sends it every time.

**Q6. Why can't I just pass "system=None" when I have no system prompt?**
The API doesn't accept `None` for `system`, so the request fails. The reusable `chat()` function adds `"system"` only when a system prompt is given.

**Q7. What does "**params" do in "client.messages.create(**params)"?**
It unpacks a dictionary into named settings. `create(**{"model": model, "max_tokens": 1000})` is the same as `create(model=model, max_tokens=1000)`.

**Q8. What makes a good system prompt?**
A clear role, plus a few specific rules about what to do and what to avoid. For the tutor: give hints first, walk through steps, show similar problems, and don't give the answer at once.

**Q9. Does a system prompt guarantee the model always follows its rules?**
No. It strongly guides the model, but answers can still break a rule, and users can try to talk the model out of it. Test it, and check important rules in code.

**Q10. (Exam angle) A tutoring app keeps giving students full answers, and the product team wants hints first. What do you change?**
Add a system prompt that sets the role and rules: act as a patient tutor, give hints first, and never give the answer at once. Test it on real student questions before release. (Claude Models, Prompting & Context Engineering)

**Q11. (Exam angle) A team puts an internal discount code in the system prompt and tells the model to keep it secret. What is the risk, and what do you advise?**
Users can sometimes trick the model into repeating its system prompt, so the code could leak. Keep secrets in server code, and have your code, not the model, decide when a discount applies. (Governance, Safety & Risk Management)

**Q12. (Exam angle) A long system prompt makes every request in a chat app expensive. What do you recommend?**
The system prompt is billed as input on every request. Trim it to what the job needs, and keep it identical across requests so prompt caching can reuse it. (Solution Design & Architecture)

---

| Previous | Course | Next |
|:---|:---:|---:|
| [← Multi-Turn conversations](04-multi-turn-conversations.md) | [📚 Course index](README.md) | [Temperature →](06-temperature.md) |
