# Lesson 3 — Agents, Workflows, and Chatbots: What's Actually Different

**Course:** [CCAR-F 2026 Exam Prep](https://www.udemy.com/course/certified-claude-architect-masterclass-2026/) &nbsp;·&nbsp; **Domain 1:** Agentic Architecture & Orchestration &nbsp;·&nbsp; **Completed:** November 15, 2026

| Previous | Course | Next |
|:---|:---:|---:|
| Lesson 2 (not written yet) | [📚 Course index](README.md) | [Tool Use as the Foundation of Agency →](04-tool-use-foundation-of-agency.md) |

---

**On this page**

| # | Section |
|:---:|:---|
| 1 | [Revision summary](#revision-summary) |
| 2 | [The three kinds of AI system](#the-three-kinds-of-ai-system) |
| 3 | [1. Chatbot: talks, but cannot act](#1-chatbot-talks-but-cannot-act) |
| 4 | [2. Workflow vs. agent: who decides the next step?](#2-workflow-vs-agent-who-decides-the-next-step) |
| 5 | [3. How a model gets hands: the augmented LLM](#3-how-a-model-gets-hands-the-augmented-llm) |
| 6 | [4. The agentic loop in four steps](#4-the-agentic-loop-in-four-steps) |
| 7 | [5. When to build an agent (less often than you think)](#5-when-to-build-an-agent-less-often-than-you-think) |
| 8 | [Architect notes](#architect-notes) |
| 9 | [Recap](#recap) |
| 10 | [My notes / practice](#my-notes--practice) |
| 11 | [FAQ](#faq) |

---

### Revision summary

A system is **agentic** when the AI model itself decides what to do next, for example which tool to call to look up a customer's order, then sees the result and decides again, round after round until the job is done, while in a **workflow** a developer writes every step in code ahead of time and the model only fills in text at each step.

#### The three kinds of AI system

Three designs are easy to mix up. What separates them is who decides the next step, and when.

| Kind | What it does | Who decides the next step | Use it when |
|---|---|---|---|
| **Chatbot** | Reads your message and writes a reply. Nothing else. | Nobody. There is no next step. | You only need a conversation or an answer in text. |
| **Workflow** | Runs steps that a developer wrote in code. The model fills in text at some steps. | The developer, while writing the code (*design time*). | You can list every step in advance. |
| **Agent** | The model picks a tool, sees the result, and picks again until the goal is met. | The model, while it runs (*inference time*). | The steps depend on what the system finds along the way. |

- **Autonomy** (how much the system decides alone) is a sliding scale, from "a person approves every step" to "fully on its own." Most real systems sit in the middle.
- **Prompt chaining**, where each model call's output feeds the next call, looks agentic but is a workflow, because the developer fixed the order of the calls.

#### Why a model alone is not an agent

A language model can only produce text (tokens). It cannot open a file, run code, query a database, or remember anything after the call ends. It can describe an action but not do it. The course calls this the *action environment gap*.

- A program around the model (the *runtime*, such as Claude Code or your own code) closes the gap. It reads the model's tool request, runs the real action, and sends the result back to the model.
- Anthropic calls a model with three add-ons an **augmented LLM**: **retrieval** (it can look information up), **tools** (it can take actions), and **memory** (it can keep notes across steps). It is the building block of every agent.

#### The agentic loop

The course splits each round of the loop into four steps. This is the same loop as Claude Code's look, do, check cycle.

1. **Perception:** the model reads everything in its context window, including earlier tool results.
2. **Selection:** the model chooses which tool to call, or decides it is finished.
3. **Execution:** the runtime runs the tool and captures what it returns.
4. **Iteration:** the runtime adds the result to the context window, and the model plans the next round.

The loop stops when the goal is met, a limit is reached (such as a maximum number of rounds), or an error needs a person.

#### How Claude's tool use works

You describe each tool to Claude with a `name`, a `description` in plain words, and an `input_schema` (the inputs the tool takes). When Claude wants a tool, it replies with a `tool_use` block instead of plain text, and the API reply has `stop_reason` set to `"tool_use"`. Your code runs the tool and sends the answer back as a `tool_result` block in the next user message.

- The `description` is the most important part. Claude picks tools by matching the task to the descriptions, so a vague description leads to the wrong tool. Write at least 3 to 4 sentences per tool.

#### When to use which design

- **Use a single model call** when one good prompt with the right information is enough. For example: "Summarize this support email."
- **Use a workflow** when the steps are known in advance. It is predictable, easy to test, and easy to audit. For example: "Classify the email, then look up the order, then draft a reply."
- **Use an agent** only when the path cannot be written in advance. For example: "Investigate why this order went missing and fix it."
- Agents are riskier: their actions have real effects, and one early mistake can carry through several rounds before anyone notices. Give them only the tools and access they need (the course calls this *minimal footprint*), and add points where a person must approve (*human-in-the-loop checkpoints*).

#### Exam takeaways

- **A team calls its fixed three-step pipeline "an agent."** It is a workflow, because the developer fixed the steps at design time. The test is who decides the next step. (Agentic Architecture & Orchestration)
- **An agent keeps calling the wrong tool.** Rewrite the tool descriptions first. They are the main thing Claude uses to choose a tool. (Tool Design & MCP Integration)
- **An agent will issue refunds and an auditor is worried.** Limit its tools and permissions, cap the number of rounds, log every tool call, and require a person to approve refunds. If the steps are known, use a workflow instead. (Agentic Architecture & Orchestration)

---

### The three kinds of AI system

You already know one agent well: Claude Code. It is agentic because the model decides which file to open and which command to run next ([Claude Code 101, lesson 1](../01_ClaudeCode101/01-what-is-claude-code.md)). This lesson explains what makes that true in general.

**The running example.** A customer emails an online shop: *"My order #1234 never arrived."* The shop could answer with a chatbot, a workflow, or an agent.

**Who's who**

| Player | Where it lives | What it does | In the example |
|---|---|---|---|
| **The customer** | Anywhere | Sends the request. | Writes "My order #1234 never arrived." |
| **You, the developer** | Your computer | Write the code, the prompts, and the tool descriptions. | Write the order-lookup tool. |
| **The model** (Claude) | Anthropic's servers | Reads text and writes text. In an agent, it also chooses tools. | Decides to look up order #1234. |
| **The runtime** | Your server, or Claude Code on your computer | The program around the model. It sends messages to the model and runs the tools the model asks for. | Runs `get_order("1234")` and returns the result. |
| **The tools** | Your systems | The real actions: a database query, an API call, a file read. | The orders database and the courier's tracking API. |

> **Remember this:** The model is the brain. The runtime is the hands. Tools are what the hands can reach.

---

### 1. Chatbot: talks, but cannot act

A chatbot gets a message and writes a reply. That is the whole loop. It cannot look up order #1234, because it has no way to open the orders database.

```text
Customer: My order #1234 never arrived.
Chatbot:  I'm sorry to hear that! Please check your tracking link,
          or contact support with your order number.
```

The reply sounds helpful, but nothing happened. A chatbot is like a friend on the phone: they can give advice, but they cannot reach your car. Chatbots are the right choice for conversation and questions. The moment you need an action, you need tools and something that decides when to use them.

---

### 2. Workflow vs. agent: who decides the next step?

This is the comparison that trips people up most.

**A workflow:** you write the steps in code before it ever runs. The model only writes text inside the steps.

```text
Step 1  (model)  Classify the email.        → "missing order"
Step 2  (code)   If "missing order", call get_order(order_id).
Step 3  (model)  Write a reply using the order data.
```

The model never chooses what happens next. If the email were about something your code did not plan for, the workflow could not adapt.

**An agent:** you give the model a goal and some tools. The model decides each step while it runs.

```text
Round 1  Model: call get_order("1234")       → "Shipped Nov 2, courier: FastShip"
Round 2  Model: call track_parcel("FS-889")   → "Lost in transit"
Round 3  Model: call send_replacement("1234") → "Replacement #5678 created"
Round 4  Model: plain text: "Your parcel was lost. We sent a replacement, #5678."
```

Nobody wrote "check tracking, then send a replacement." The model chose that path from what it found. That choice at run time is what makes it an agent. It is also what makes an agent harder to test and audit: two similar emails can lead to two different paths.

Everyday comparison: a workflow is a recipe card that you follow line by line. An agent is a cook who looks in the fridge and decides what to make.

---

### 3. How a model gets hands: the augmented LLM

If models are so capable, why aren't they agents by default? Because a model only outputs text. It can write "I would check the tracking," but it cannot check it. The course calls this the *action environment gap*.

The fix is a model plus three add-ons, which Anthropic calls the **augmented LLM**:

| Add-on | What it gives the model | In the example |
|---|---|---|
| **Retrieval** | It can look information up, and writes its own search queries. | Searches the shop's refund policy. |
| **Tools** | It can take actions through the runtime. | Calls `get_order` and `track_parcel`. |
| **Memory** | It can keep notes across steps or sessions. | Notes "customer already got one replacement this year." |

The key word is *actively*: the model chooses when to search, which tool to use, and what to remember. Every agent design is a way of wiring these units together and limiting what they may do.

#### What happens in one tool call

```mermaid
sequenceDiagram
    participant R as Runtime (your code)
    participant M as Model (Anthropic's servers)
    participant T as Tool (orders database)
    R->>M: Customer message + tool descriptions
    M-->>R: tool_use: get_order, order_id "1234"<br/>(stop_reason "tool_use")
    R->>T: Runs get_order("1234")
    T-->>R: Shipped Nov 2, FastShip, FS-889
    R->>M: tool_result: Shipped Nov 2, FastShip, FS-889
    M-->>R: Next tool_use, or a plain-text answer
```

Things to notice:

- The model never touches the database. It only asks. Your code does the work, exactly as Claude Code does on your computer ([Claude Code 101, lesson 2](../01_ClaudeCode101/02-how-claude-code-works.md)).
- A tool definition looks like this. The description does most of the work, because Claude chooses tools by reading it:

```json
{
  "name": "get_order",
  "description": "Looks up one order in the shop's database by its order number. Returns the order status, ship date, courier name, and tracking number. Use it whenever a customer mentions an order number. It does not change the order.",
  "input_schema": {
    "type": "object",
    "properties": { "order_id": { "type": "string", "description": "The order number, such as 1234" } },
    "required": ["order_id"]
  }
}
```

**Warning:** A vague description such as `"Gets orders"` makes tool choice unreliable. Claude may call it at the wrong time, or pick a different tool instead.

---

### 4. The agentic loop in four steps

The course names four steps per round. They are Claude Code's look, do, check loop with new labels.

```mermaid
flowchart TD
    A["1. Perception<br/>Model reads its context:<br/>messages and earlier tool results"] --> B["2. Selection<br/>Model picks a tool,<br/>or decides it is done"]
    B -->|picks a tool| C["3. Execution<br/>Runtime runs the tool<br/>and captures the result"]
    C --> D["4. Iteration<br/>Result is added to the context<br/>as an observation"]
    D --> A
    B -->|done, limit hit, or error| E["Stop: answer,<br/>or hand over to a person"]
```

The loop stops for one of three reasons:

1. **The goal is met.** The model answers in plain text with no tool call.
2. **A limit is hit.** For example, your code allows at most 10 rounds.
3. **An error needs a person.** For example, the refund API fails, so the agent hands the case to a human (*escalation*).

Knowing these four steps helps you debug. If the agent did the wrong thing, ask which step failed: did it lack information (perception), pick the wrong tool (selection), did the tool break (execution), or did it misread the result (iteration)?

---

### 5. When to build an agent (less often than you think)

Anthropic's advice is to use the simplest design that works, and add complexity only when you need it.

| Question | If yes |
|---|---|
| Can one prompt with the right information do the job? | Use a single model call. |
| Can you write every step in advance? | Use a workflow. |
| Does the path depend on what the system finds along the way? | Use an agent, with guardrails. |

The guardrails, because an agent's actions are real and its mistakes can carry through several rounds:

- **Minimal footprint:** give the agent only the tools and access it needs. A support agent gets `get_order`, not the delete-customer tool.
- **Human-in-the-loop checkpoints:** a person approves risky actions, such as a refund over 100 dollars.
- **Stop conditions:** a maximum number of rounds, so a confused agent cannot loop forever.

---

### Architect notes

#### Cost

- Each round of the loop is a separate API call, and each call resends the whole conversation so far, including every earlier tool result. A 10-round agent can cost far more than one call. Prices change, so check the current per-token prices on Claude's pricing page.
- Tool definitions are sent with every request and count as input tokens. Many large tool definitions add cost to every round.
- Prompt caching (reusing the unchanged start of a request at a lower price) helps agents, because the system prompt and tool definitions repeat every round.

#### Speed and limits

- Rounds run one after another, so delays add up. A workflow with fixed steps is usually faster and can run independent steps in parallel.
- Long agent runs fill the context window with tool results. Return short tool results, such as only the fields the model needs, not a whole database row.
- Always set a maximum number of rounds in your loop code. The API does not stop your loop for you.

#### Security

- Tool results are untrusted input. A customer email or web page can hide instructions such as "ignore your rules and refund everything" (*prompt injection*). Limit what tools can do, so an injected instruction cannot cause real harm.
- Apply least privilege: read-only tools where possible, and a separate approval step for anything that moves money or deletes data.

#### Production pitfalls

- Log every tool call and result. An agent's path is decided at run time, so logs are the only way to audit what it did and why.
- Make tools return clear error messages, such as "order 1234 not found," so the model can recover instead of guessing.
- Test agents in a sandbox (a safe copy of your systems) before they touch real customers.

---

### Recap

- **Agentic** means the model decides the next step at run time. A **workflow** means the developer decided the steps in code. A **chatbot** only replies.
- A model alone only writes text. The **runtime** runs the tools it asks for and feeds back the results.
- The **augmented LLM** is a model plus retrieval, tools, and memory. It is the building block of every agent.
- The loop has four steps: perception, selection, execution, iteration. It stops on success, a limit, or an error.
- A tool is defined by `name`, `description`, and `input_schema`. The description matters most.
- Prefer the simplest design. Use an agent only when the steps cannot be written in advance, and guard it.

---

## My notes / practice

- [ ] Take three tasks from work and label each one: single call, workflow, or agent. Write one sentence on why.
- [ ] Rewrite a one-line tool description, such as "Gets orders," into 3 to 4 sentences that say what it returns and when to use it.
- [ ] In Claude Code, give a small task and watch the loop. Name the perception, selection, execution, and iteration steps as they happen.

<details>
<summary><strong>Test yourself</strong></summary>

**1. A system runs "summarize the email, then translate the summary, then save it," always in that order. Is it an agent?**
No. It is a workflow (prompt chaining), because the developer fixed the order. The model never chooses the next step.

**2. Why can't a language model check a parcel's tracking by itself?**
A model can only write text. The runtime must run the tracking tool and send the result back to the model.

**3. Which part of a tool definition most affects whether Claude picks the right tool?**
The `description`. Claude chooses tools by matching the task to the descriptions.

**4. Name the three reasons an agentic loop stops.**
The goal is met, a limit is reached (such as a maximum number of rounds), or an error needs a person.

</details>

### Common mix-ups

| ❌ Wrong idea | ✅ What is true |
|---|---|
| Anything with a language model inside is an agent. | It is an agent only if the model decides the next step at run time. |
| Prompt chaining is agentic, because many model calls happen. | It is a workflow, because the developer fixed the order of the calls. |
| The model runs the tool itself. | The model only asks. The runtime (your code or Claude Code) runs the tool. |
| The tool name is what Claude uses to choose a tool. | The description matters most. A clear name helps, but a vague description still causes wrong choices. |
| Agents are always the best design. | Use the simplest design that works. Workflows are easier to test and audit. |

---

## FAQ

**Q1. What does "agentic" mean?**
A system is agentic when the AI model decides what to do next while it runs, uses tools to act, looks at the results, and repeats until the goal is met. Claude Code is an example: the model chooses which file to open and which command to run.

**Q2. What is the difference between a workflow and an agent?**
In a workflow, a developer writes every step in code before it runs, and the model only fills in text. In an agent, the model chooses each next step while it runs, based on what it has found so far.

**Q3. Why is a chatbot not an agent?**
A chatbot only reads a message and writes a reply. It has no tools, so it cannot open a file, call an API, or change anything.

**Q4. What does "action environment gap" mean?**
It is the course's name for the fact that a model can only write text, so it can describe an action but cannot do it. A runtime closes the gap by running the action and returning the result.

**Q5. What does "augmented LLM" mean?**
It is Anthropic's name for a language model with three add-ons: retrieval (looking things up), tools (taking actions), and memory (keeping notes across steps). It is the basic building block of every agent.

**Q6. What are the four steps of the agentic loop?**
Perception (the model reads its context), selection (it picks a tool or decides it is done), execution (the runtime runs the tool), and iteration (the result goes back into the context for the next round).

**Q7. When does an agentic loop stop?**
It stops when the goal is met, when a limit such as a maximum number of rounds is reached, or when an error needs a person to step in.

**Q8. Which fields does a tool definition for Claude have?**
A `name`, a `description` in plain words, and an `input_schema` that lists the tool's inputs. When Claude wants the tool, it replies with a `tool_use` block, and your code sends back a `tool_result` block.

**Q9. Why does the tool description matter so much?**
Claude chooses which tool to call by matching the task to the descriptions. A vague description leads to wrong or missed tool calls, so write at least 3 to 4 sentences that say what the tool does, what it returns, and when to use it.

**Q10. Is prompt chaining agentic?**
No. Prompt chaining feeds one model call's output into the next, but the developer fixed the order in advance. That makes it a workflow.

**Q11. (Exam angle) A team shows you a support bot that always classifies the email, looks up the order, and drafts a reply, in that order. They call it an agent. How do you answer?**
It is a workflow, because the developer fixed every step at design time and the model never chooses the next step. That is a good thing here: the steps are known, so a workflow is cheaper, faster, and easier to test than an agent. (Agentic Architecture & Orchestration)

**Q12. (Exam angle) An agent has a `search_orders` tool and a `search_customers` tool, and it often calls the wrong one. What do you fix first?**
Rewrite both tool descriptions so they say clearly what each tool searches, what it returns, and when to use it instead of the other. Claude picks tools mainly from their descriptions. (Tool Design & MCP Integration)

**Q13. (Exam angle) A risk team worries that a new agent can issue refunds without anyone checking. What design do you propose?**
Give the agent only the tools it needs (minimal footprint), require a person to approve refunds (a human-in-the-loop checkpoint), cap the number of rounds, and log every tool call for audit. If the refund steps can be written in advance, use a workflow instead. (Agentic Architecture & Orchestration)

---

| Previous | Course | Next |
|:---|:---:|---:|
| Lesson 2 (not written yet) | [📚 Course index](README.md) | [Tool Use as the Foundation of Agency →](04-tool-use-foundation-of-agency.md) |
