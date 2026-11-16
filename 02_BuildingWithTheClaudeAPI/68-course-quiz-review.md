# Course quiz review — Building with the Claude API

**Course:** [Building with the Claude API](https://academy.claude.com/courses/building-with-the-claude-api) &nbsp;·&nbsp; [📚 Course index](README.md)

This file collects the chapter quiz questions, restated in my own words, with the right answer and why each wrong option is wrong. Where a question's topic has changed since the course was made, it appears twice: once for older models (the course's answer) and once for current models.

---

**On this page**

| # | Section |
|:---:|:---|
| 1 | [Quiz on accessing Claude with the API](#quiz-on-accessing-claude-with-the-api) |

---

## Quiz on accessing Claude with the API

### Q1. Clean JSON on an older model (the course's version)

Your app runs on an older model, such as `claude-haiku-4-5`. It needs raw JSON with no Markdown fences and no explanation. How do you get it?

| Option | Right or wrong | Why |
|---|---|---|
| Prefill the assistant message with ` ```json ` and add ` ``` ` as a stop sequence | ✅ Right | The prefill makes the model start straight inside a JSON block. The stop sequence ends the answer when the model tries to close the block, so the explanation is never written. |
| Send the request several times and pick the best answer | ❌ Wrong | Every answer still has the fences and the explanation. It also costs several times as much. |
| Ask the model very nicely to return only JSON | ❌ Wrong | The instruction helps, but nothing enforces it. The model can still add fences or a sentence. |
| Use a very high temperature | ❌ Wrong | High temperature makes answers more varied, not cleaner. |

**Domain:** Integration. **My notes:** [Lesson 8, section 5](08-structured-data.md#5-the-courses-way-prefill-and-stop-sequences-older-models-only).

### Q2. Clean JSON on a current model

Your app runs on a current model, such as `claude-opus-5-5`. It needs raw JSON with no Markdown fences and no explanation. How do you get it?

| Option | Right or wrong | Why |
|---|---|---|
| Use structured outputs: send a JSON schema in `output_config.format` | ✅ Right | The API only lets the model write JSON that matches the schema. The answer is plain JSON, and every required field is there. |
| Prefill the assistant message with ` ```json ` and add ` ``` ` as a stop sequence | ❌ Wrong | Claude Opus 4.6, Sonnet 4.6, and every newer model reject a prefilled last assistant message with a 400 error. |
| Ask the model very nicely to return only JSON | ❌ Wrong | Nothing enforces it, so fences or a sentence can still appear. |
| Use a very high temperature | ❌ Wrong | It makes answers more varied, not cleaner. Current models also reject a temperature setting. |

**Domain:** Integration. **My notes:** [Lesson 8, section 2](08-structured-data.md#2-structured-outputs-the-current-way).

### Q3. Consistent factual answers on an older model (the course's version)

Your factual question-and-answer app runs on an older model, such as `claude-haiku-4-5`. You want answers that are predictable and consistent. What temperature do you set?

| Option | Right or wrong | Why |
|---|---|---|
| Low, near 0.0 | ✅ Right | The model then almost always picks the most likely next word, so the same question gets nearly the same answer. Even at 0.0, identical answers are not promised. |
| Medium, around 0.5 | ❌ Wrong | Answers still vary noticeably. |
| Temperature doesn't matter for facts | ❌ Wrong | Temperature affects every answer, including factual ones. Higher values make less likely words, and so different wording or errors, more common. |
| High, near 1.0 | ❌ Wrong | This gives the most varied answers, the opposite of what you want. |

**Domain:** Claude Models, Prompting & Context Engineering. **My notes:** [Lesson 6](06-temperature.md).

### Q4. Consistent factual answers on a current model

Your factual question-and-answer app runs on a current model, such as `claude-opus-5-5`. You want answers that are predictable and consistent. What do you do?

| Option | Right or wrong | Why |
|---|---|---|
| Leave temperature out. Make answers consistent with a precise system prompt, example answers, and the facts supplied in the prompt. | ✅ Right | Current models don't accept a temperature setting, so the prompt is your control. Clear rules and supplied facts keep answers steady and correct. |
| Set temperature to 0.0 | ❌ Wrong | Claude Opus 4.7 and every newer Opus reject any temperature value with a 400 error. Some other current models, such as Sonnet 5.5, reject any value except the default. |
| Set temperature to 1.0 to be safe | ❌ Wrong | On Claude Opus 4.7 and newer Opus models, even the default value causes a 400 error. Leave the setting out. |
| Temperature doesn't matter for facts | ❌ Wrong | The reason to skip temperature here is that current models don't accept it, not that facts are unaffected. |

**Domain:** Claude Models, Prompting & Context Engineering. **My notes:** [Lesson 6](06-temperature.md).

### Q5. A math tutor that gives hints, not answers

You're building a math tutor bot. It should give students hints instead of the final answer. What do you use?

| Option | Right or wrong | Why |
|---|---|---|
| A system prompt that explains the tutor's role and rules | ✅ Right | The system prompt sets how the model behaves in every turn, for example: "You are a patient math tutor. Give hints, never the final answer." |
| A very low word limit | ❌ Wrong | A low `max_tokens` just cuts the answer off. The model may still give away the answer, only shorter. |
| Ask users to be more specific | ❌ Wrong | It puts the work on the students and doesn't change how the model behaves. |
| Write your messages in all capital letters | ❌ Wrong | Shouting isn't a reliable way to set behaviour. A clear system prompt is. |

**Domain:** Claude Models, Prompting & Context Engineering. **My notes:** [Lesson 5](05-system-prompts.md).

### Q6. The minimum a request to the Claude API must include

You want to send a request to the Claude API. What must every request include?

| Option | Right or wrong | Why |
|---|---|---|
| An API key, a model name, the messages, and `max_tokens` | ✅ Right | The API key proves who you are, the model name says which model answers, `messages` holds the conversation, and `max_tokens` caps the answer length. The API rejects a request without any of them. |
| Your name, email address, and message | ❌ Wrong | The API identifies you by your API key, not your name or email. The model and `max_tokens` are also missing. |
| Only the API key and your question | ❌ Wrong | Without a model name and `max_tokens`, the request fails. |
| Just your message text | ❌ Wrong | With no API key, the API returns an authentication error before it reads anything else. |

**Domain:** Integration. **My notes:** [Lesson 3](03-making-a-request.md).

### Q7. The model forgets the earlier question

You ask "What is pizza?" and get an answer. Then you ask "What toppings are popular?", and the model doesn't know what you mean. What is wrong?

| Option | Right or wrong | Why |
|---|---|---|
| The API doesn't remember earlier messages | ✅ Right | The Claude API keeps no conversation between requests. Your code must send the whole history every time: the first question, the first answer, then the new question. Otherwise "toppings" has nothing to refer to. |
| Your internet connection is slow | ❌ Wrong | A slow connection delays the answer. It doesn't change what the model knows. |
| You asked too quickly | ❌ Wrong | Timing doesn't matter. Each request stands alone, however long you wait. |
| The model is broken | ❌ Wrong | The model works fine. It simply never received the earlier messages. |

Not in the course: a newer beta feature, *message threads*, lets the API keep a conversation for a short time. By default, though, you still send the full history yourself.

**Domain:** Claude Models, Prompting & Context Engineering. **My notes:** [Lesson 4](04-multi-turn-conversations.md).

### Q8. Users wait 20 seconds, then all the text appears at once

Users of your chat app stare at a loading spinner for 20 seconds, then the whole answer appears at once. What fixes this?

| Option | Right or wrong | Why |
|---|---|---|
| Turn on response streaming | ✅ Right | The API then sends the answer in small pieces while the model writes it. Your server forwards each piece, so the first words appear within a second or two. The total time stays about the same. |
| Use a faster internet connection | ❌ Wrong | The wait comes from the model writing the answer, not from the network. |
| Ask shorter questions | ❌ Wrong | The length of the answer drives the wait, not the question. It also pushes the problem onto users. |
| Use a different web browser | ❌ Wrong | The browser isn't the cause. Without streaming, your server has nothing to show until the full answer is ready. |

**Domain:** Solution Design & Architecture. **My notes:** [Lesson 7](07-response-streaming.md).
