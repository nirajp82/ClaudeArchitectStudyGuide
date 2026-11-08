# Deep dive — How does Claude know what to say next?

**Course:** [Building with the Claude API](https://academy.claude.com/courses/building-with-the-claude-api) &nbsp;·&nbsp; **Extra reading for Lesson 1** &nbsp;·&nbsp; **Written:** November 7, 2026

| Previous | Course | Next |
|:---|:---:|---:|
| [← Accessing the API](01-accessing-the-api.md) | [📚 Course index](README.md) | [Getting an API key →](02-getting-an-api-key.md) |

---

Give a model these words and ask it to continue:

```text
The cat sat on the mat because it ...
```

It writes "was". It doesn't look that word up, and no rule tells it to. It does math on billions of saved numbers and works out a chance for every word it knows. In the small example on this page, the chances look like this:

| Next word | was | is | sat | cat | mat |
|---|:---:|:---:|:---:|:---:|:---:|
| Chance | **51.3%** | 18.2% | 14.9% | 8.2% | 7.5% |

This page walks through that math with numbers small enough to check by hand. Then it shows how training found those numbers.

---

**On this page**

| # | Section |
|:---:|:---|
| 1 | [Revision summary](#revision-summary) |
| 2 | [What a model is](#what-a-model-is) |
| 3 | [The big picture](#the-big-picture) |
| 4 | [Part 1. What is saved inside the model](#part-1-what-is-saved-inside-the-model) |
| 5 | [Part 2. How the model answers your message](#part-2-how-the-model-answers-your-message) |
| 6 | [Part 3. How the model learned its numbers (training)](#part-3-how-the-model-learned-its-numbers-training) |
| 7 | [Common mix-ups](#common-mix-ups) |
| 8 | [Test yourself](#test-yourself) |
| 9 | [Architect notes: what this means for your work](#architect-notes-what-this-means-for-your-work) |
| 10 | [Recap](#recap) |
| 11 | [My notes / practice](#my-notes--practice) |
| 12 | [FAQ](#faq) |

---

### Revision summary

<details>
<summary><b>Click to open the revision summary</b></summary>

The model is a huge set of numbers that training tuned by hiding the next word in billions of sentences and correcting the model's guesses; when you send a message, the model only reads those numbers to guess your answer one word at a time.

#### What a model is, and how models differ

A model is a big file of numbers plus a fixed set of calculations. It does one thing: it looks at some text, gives every possible next token a chance, picks one, and repeats. The full explanation is in [What a model is](#what-a-model-is).

- Answering questions, writing code, and summarizing are all that one skill, repeated.
- Three things are saved inside the model: the vocabulary, the embedding table, and the weights. Your past chats, the internet, and anything newer than the training cutoff date are **not** saved inside it.
- A **layer** is one round of work that every token's row of numbers goes through. Each layer takes the rows from the layer before it, adds a little more meaning, and passes them on.
- The builders choose how many layers a model has before training. More layers usually make a model smarter, but also slower and more expensive.
- Each layer has its own attention matrices (Wq, Wk, and Wv) and its own feed-forward matrices. These are fixed after training. They change only when the model is trained again, which makes a new model version.
- A model needs many layers because each layer adds meaning only once. For "it" in "The cat sat on the mat because it was comfortable", early layers look at nearby words. Middle layers link "it" to the mat or the cat. Late layers work out that a verb like "was" comes next.
- **Training** is how the model gets its numbers. It has two stages. In **pre-training**, the model practises guessing the next word on a huge amount of text. In **later training**, examples, feedback from people, and written rules (Constitutional AI) teach it to follow instructions and stay safe.
- Training runs on thousands of special chips for weeks or months, so it is very expensive. It happens once for each model version, and a newer model means a new training run.
- A model's **size** is how many learned numbers (**parameters**) it has. The builders set the size by choosing how many columns each token's row in the embedding table has, how many layers the model has, and how wide each layer is.
- A bigger model can store more patterns, so it is usually smarter. But every token passes through all its numbers, so it is also slower and costs more.
- Models also differ in their training text, their cutoff date, their later training, and settings such as the context window size.

#### When to use a smaller or a larger model

- **Use a smaller, faster model** (Haiku, in Claude's family) for simple tasks you run many times, where speed and cost matter most. For example: "Sort 10,000 support emails into five categories."
- **Use a larger, smarter model** (Opus) for hard tasks that need careful thinking. For example: "Review this design and find the security risks."
- **Use a middle model** (Sonnet) when you need a balance of quality, speed, and cost. This covers most everyday work.
- Before paying for a bigger model, test whether the smallest one passes your test questions.

#### What is saved inside the model

Training saves three things inside the model. Every request reads them, but no request changes them.

- The **vocabulary** is the list of every token the model knows. A **token** is a small piece of text, such as a word, part of a word, or a symbol like "?".
- Each token has a fixed number called its **token ID**, for example `cat` = 2207. A token ID is only a label, like a primary key in a database, so it has no meaning by itself.
- The **embedding table** has one row of numbers for each token ID. That token's row describes what the token usually means, and it is called the token's **embedding**.
- Each token has its own row in the embedding table, and every token's row has the same number of columns. The builders choose that number before training, and it never changes. Real models use hundreds or thousands of columns.
- The **weights** are all the other numbers the model learned. They are stored as grids of numbers called **matrices**, and each layer has its own set.
- A weight matrix doesn't multiply each number by one weight. Each result adds up **all** the input numbers, each times its own weight. This is how the model mixes information.

#### How the model answers your message

The model repeats the same steps for every token it writes.

1. It cuts your text into tokens and finds each token's ID in the vocabulary.
2. It looks up each token's row in the embedding table. The saved row is the same in every sentence, so the model works on a copy.
3. Each token borrows meaning from the tokens before it. This is called **attention**.
4. For attention, each token makes three new rows using three shared matrices (Wq, Wk, and Wv). The **Query** says what the token is looking for. The **Key** says what it offers. The **Value** is the information it hands over.
5. The model multiplies a token's Query with each earlier token's Key, number by number, and adds the results. This **dot product** is a match score.
6. **Softmax** turns the match scores into percentages that add up to 100%. The token then adds up each earlier token's Value times its percentage, and adds that to its own row.
7. A token can only look at itself and earlier tokens. Later words don't exist yet while the model is writing. This is called *causal masking*.
8. Each layer runs many attentions side by side (*multi-head attention*). Then a **feed-forward network** works on each token's row by itself. Real models repeat this in dozens of layers, and they also add each token's position so word order isn't lost.
9. After the last layer, the model turns the last token's row into a score for every token in the vocabulary. These scores are called **logits**.
10. Softmax turns the logits into chances, and the model picks one token based on those chances.
11. **Temperature** changes how spread out the chances are. A low temperature makes the top token win more often. A high temperature gives other tokens more of a chance.
12. The model adds the picked token and repeats. It stops at a special end token, at the `max_tokens` limit, or at a stop sequence.

#### How the model learned its numbers

Every number started random. Training changed them slowly by having the model guess hidden words.

- The training process takes a sentence, shows the model the start, and hides the next token. The model guesses, and the training process checks the guess against the hidden token.
- The answer comes from the sentence itself, so nobody has to label anything (*self-supervised learning*). The model never searches the internet to check.
- **Loss** is one number that says how wrong a guess was. Loss = −ln(the chance given to the right token). A 90% chance gives 0.11, and a 10% chance gives 2.30.
- A **gradient** says, for one number in the model, whether making it bigger would raise or lower the loss. A negative gradient means "bigger is better". A positive gradient means "smaller is better".
- **Backpropagation** works out the gradient for every number in one backward pass. It only calculates, and it changes nothing.
- **Gradient descent** then changes every number with the rule `new = old − (learning rate × gradient)`.
- The **learning rate** is a small number, such as 0.1. It keeps each change small, so one sentence can't push the model too far.
- The tokens' rows in the embedding table are changed the same way as the weights. Only the rows of the tokens in the sentence change in that step.
- One wrong sentence changes almost nothing, because each change is tiny. But wrong text that appears many times can be learned, so the quality of training text matters.

#### Training compared with normal use

- During training, the numbers change after every batch of sentences. Training happens once, on Anthropic's computers, before release.
- During normal use (*inference*), the model only reads its numbers. Your message never changes them, and nothing you say is saved inside the model.
- The model doesn't remember you between requests. Your app must send earlier messages again if the model needs them.

#### Exam takeaways

- **A customer asks if their chats will change the model for other users.** No. Answering only reads the model's numbers. Whether Anthropic keeps or trains on data is set by its terms, so point the customer to those terms. (Governance, Safety & Risk Management)
- **A team gets different answers to the same prompt and wants consistent output.** The model picks each token from a set of chances, so some variety is normal. Lower the temperature, give clear examples, and check the output in code. Answers get more consistent, but not identical. (Claude Models, Prompting & Context Engineering)
- **A product manager asks why long prompts cost more and run slower.** Every input token goes through every layer, and attention looks back at every earlier token. So the work grows with the prompt. Send only the text needed, and put fixed text at the start so prompt caching can reuse it. (Solution Design & Architecture)

</details>

---

### What a model is

#### What a model is and what it does

A model is a big file of numbers, often billions of them, plus a fixed set of calculations that use those numbers. Claude models run on Anthropic's servers, and your app reaches them through the API.

A model does one thing. You give it some text, it gives every possible next token a chance, it picks one, and it adds it to the text. Then it repeats. Answering a question, writing code, and summarizing a document are all this one skill. An answer is simply the text most likely to come after your question.

#### What is saved inside a model, and what is not

| Saved inside the model | Not saved inside the model |
|---|---|
| The **vocabulary**: every token the model knows, each with its token ID | Your past chats, so the model doesn't remember you |
| The **embedding table**: one row of numbers that describes each token | A copy of the internet, or a database it can look facts up in |
| The **weights**: all the other numbers it learned in training | Anything that happened after its training cutoff date |

Part 1 explains each of the three saved things in detail.

#### What a layer is

A **layer** is one round of work that every token's row of numbers goes through. Each layer takes every token's row from the layer before it. It updates each token's row so it holds a bit more meaning from the nearby words. Then it passes those rows to the next layer. The model uses the rows that come out of the last layer to score the next token.

Each layer has its own weights. Its attention matrices (Wq, Wk, and Wv) let each token borrow meaning from earlier tokens. Its feed-forward matrices then work on each token's row by itself. All layers do the same kind of work. But each layer has different numbers, so each one adds something different.

If you know ASP.NET Core, a layer is like one piece of middleware. Each piece takes the request, changes it, and hands it to the next piece. The response is ready only after the last piece. In a model, the "request" is the set of token rows, and there are dozens of layers.

| | What it means |
|---|---|
| How many layers a model has | The builders choose this before training, and it never changes. GPT-2, a small public model, has 12 layers. Today's large models have many more. |
| What more layers give you | More rounds to combine meaning, and more weights to store patterns. So the model is usually smarter. |
| What more layers cost you | Every token goes through every layer. So each extra layer adds math for every token, which makes the model slower and more expensive. |

#### Example: what the layers do for "it"

Take the sentence "The cat sat on the mat because it was comfortable". The model has read up to "it" and must guess the next word.

The row for "it" starts as a copy of its saved row in the embedding table. That saved row is the same in every sentence, so by itself it says nothing about this sentence. Each layer adds a little more meaning, building on the layer before it.

Nobody gives each layer a job. Training decides what each layer does. So the table below is a simplified picture of what the row of "it" holds as it moves up:

| After… | What the row of "it" now holds (simplified) |
|---|---|
| The embedding lookup | Only the usual meaning of "it": a word that stands for a thing |
| The early layers | Facts about nearby words. For example, "it" comes right after "because", so a reason is starting. |
| The middle layers | Links to earlier words. For example, "it" probably means the mat or the cat. |
| The late layers | What should come next. For example, after "because it", a verb like "was" or "is" is likely. |
| The last layer | A row for "it" that is ready to be scored, and that gives "was" the highest chance |

That is why a model needs many layers. One layer combines meaning only once. Understanding a sentence takes many rounds, each building on the last.

Every other token goes through the same layers at the same time. But each token can only use the tokens before it. "Cat" is the second word, so it can only look at "The" and itself. It can learn that it is the subject of the sentence. But it never sees "mat" or "it", because those words come later.

#### What is fixed and what changes

| Part of the model | When it is decided | Does it change when you send a request? |
|---|---|---|
| The vocabulary and every token ID | Before training | No |
| How many columns each token's row in the embedding table has | Before training | No |
| How many layers the model has | Before training | No |
| The embedding table | Learned in training | No |
| Each layer's own Wq, Wk, Wv, and feed-forward matrices | Learned in training, separately for each layer | No. They change only if the model is trained again, which makes a new model version. |
| The working copy of each token's row, as it moves through the layers | Made fresh for every request | Yes. It is made for your request and thrown away after. |

Part 2, step 4 shows what happens inside each layer.

#### What training is

Training is how a model gets its numbers. Before training, the model already has its shape: its vocabulary, how many columns each token's row has, and how many layers it has. But every number is random, so it writes nonsense. Training is a long run of practice that adjusts those numbers until the model writes useful text.

Anthropic trains each model on thousands of special computer chips for weeks or months. This is very expensive, so it happens once for each model version. After release, the numbers are fixed. A newer model, such as a newer Sonnet, comes from a new training run.

Training has two stages:

1. **Pre-training:** the model practises guessing the next word on a huge amount of text from books, websites, and other sources. This teaches it language and facts about the world. But at this stage it can only continue text. It can't yet answer questions like an assistant.
2. **Later training:** the model trains further on examples of good answers and on feedback from people. Anthropic also uses a written set of rules called *Constitutional AI*. This stage teaches the model to follow instructions, be helpful, and refuse harmful requests.

#### What training does to the model

| | Before training | After training |
|---|---|---|
| The numbers | Random | Tuned by billions of small fixes |
| The rows for "cat" and "kitten" in the embedding table | Unrelated | Similar, because both words appear in similar sentences |
| Given "The cat sat on the" | Guesses a random token | Gives "mat" a high chance |
| Given "Summarize this email" | Just keeps writing more text | Writes a summary, after later training |

Part 3 shows exactly how one of those small fixes works, with real numbers.

#### Why some models are larger than others

A model's **size** is how many learned numbers (*parameters*) it has. The builders set the size before training. They choose how many columns each token's row in the embedding table has, how many layers there are, and how wide each layer is. More of each means more numbers.

A larger model has more room to store patterns and facts. So it can usually handle harder tasks, such as long reasoning or tricky code. But every token has to pass through all of its numbers. So a larger model does more math per token, which makes it slower and more expensive to run. It also costs much more to train.

That is why providers offer a family of models. Anthropic doesn't publish its model sizes. It describes Haiku as its fastest and cheapest model, Opus as its smartest, and Sonnet as the balance between them.

| | Smaller model (for example, Haiku) | Larger model (for example, Opus) |
|---|---|---|
| Speed | Faster | Slower |
| Cost per token | Lower | Higher |
| Skill on hard tasks | Lower | Higher |
| Use it when | The task is simple and you run it many times, such as sorting 10,000 support emails into five categories | The task is hard and mistakes are costly, such as finding security risks in a system design |

#### Other ways models differ

| Difference | What it changes for you |
|---|---|
| Training text and cutoff date | What the model knows, and how recent that knowledge is |
| Later training | How well it follows your instructions, and when it refuses |
| Settings chosen when it was built, such as the context window size | How much text one request can hold |

---

### The big picture

#### Why this matters to you

As an architect, you'll get these five questions. Each answer comes from one part of how the model works inside.

1. **Why do I pay per token, not per message?** The model reads your text one token at a time and writes its answer one token at a time. Every token goes through all of the model's layers. So a longer prompt or a longer answer means more work, and more cost. See [Part 2, step 1](#step-1-cut-the-text-into-tokens-tokenization).
2. **Why are long prompts slow?** Before the model writes anything, each token in your prompt looks back at every token before it. A long prompt means a lot of looking back. Prompt caching helps when many requests start with the same text, such as the same instructions. The model saves its work on that shared start and reuses it next time. See [Part 2, step 3](#step-3-borrow-meaning-from-earlier-words-attention).
3. **Why does the same question get different answers?** For each next word, the model works out a list of possible words, each with a chance. Then it picks one at random, using those chances. A setting called temperature controls how often it picks a less likely word. See [Part 2, step 5](#step-5-score-every-word-and-pick-one).
4. **Does chatting with the model change it, or make it remember me?** No. Answering only reads the model's saved numbers and never changes them. If the model needs earlier messages, your app must send them again. See [Architect notes](#architect-notes-what-this-means-for-your-work).
5. **Why can the model be wrong or out of date?** The model learned from patterns in its training text, and that text stops at a cutoff date. It has no built-in way to check facts. So give it current information in the prompt, and check important answers. See [Part 3](#part-3-how-the-model-learned-its-numbers-training).

#### The whole story, before any details

1. The model is mostly a huge set of numbers, saved on Anthropic's servers.
2. Your message is cut into small pieces called tokens. Each piece becomes a row of numbers.
3. Each piece borrows meaning from the pieces before it. That is how "bank" can mean a river bank in one sentence and a money bank in another.
4. The model gives every word it knows a chance of coming next. It picks one, adds it to the answer, and repeats until the answer is done.
5. None of this changes the numbers. The numbers were set earlier, in training.
6. Training set them by showing the model billions of sentences with the next word hidden. After each guess, it nudged all the numbers a little toward a better guess.

#### From your question to the answer

```mermaid
flowchart TD
    Q[You ask a question in your app] --> API[Your server sends it to the Claude API]
    subgraph Model["Inside the model, on Anthropic's servers"]
        T[1. Cut the text into tokens<br/>and find each token ID] --> E[2. Look up each token's row<br/>in the embedding table]
        E --> L1[Layer 1<br/>its own attention and feed-forward weights]
        L1 --> L2[Layer 2<br/>its own weights]
        L2 --> LN[... dozens more layers,<br/>each with its own weights ...]
        LN --> S[3. Score every token in the vocabulary<br/>and pick one]
        S -->|answer not done:<br/>add the token and run again| E
    end
    API --> T
    S -->|answer done| A[The answer goes back<br/>through the API to your app]
```

Things to notice:

- The loop runs once for every token in the answer. A 300-token answer means 300 trips through all the layers.
- Everything inside the box only reads the saved numbers. Your question never changes the model.

#### The route through this page

First you see what is stored. Then you watch the model use it on one sentence. Then you learn how training produced those numbers. Last, you see what it all means for the systems you design.

#### The example used throughout

The whole page follows one sentence:

```text
The cat sat on the mat because it was comfortable.
```

In Part 2, the model has read "The cat sat on the mat because it" and must guess the next token. The right answer is "was". In Part 3, training uses the same sentence to improve that guess.

Real models have thousands of numbers per token, which is too many to follow by hand. So the example uses only three. The numbers are made up, but each result is calculated from the ones before it. You can redo any step on a calculator and get the same answer.

#### Who's who

| Who | Where they are | What they do |
|---|---|---|
| The builders (people at Anthropic) | Before training | Choose the sizes, such as how many columns each token's row has and how many layers the model has |
| The training process | Anthropic's computers, before release | Hides the next token, checks the guess, and adjusts the numbers |
| The model | Anthropic's servers | The saved numbers, plus the calculations that use them |
| You and your app | Your computer and server | Send text and get the answer. You never change the model. |

---

### Part 1. What is saved inside the model

A computer can only do math on numbers. So the model needs a way to turn the word "cat" into numbers. Training saves three things for this, and every request uses all three.

#### The vocabulary: from text to a token ID

**What it is:** a fixed list of every token the model knows. Each token has its own token ID.

**Example:** these IDs are made up.

| Token | The | cat | sat | on | the | mat | because | it | was |
|---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| Token ID | 101 | 2207 | 310 | 415 | 102 | 520 | 845 | 340 | 371 |

**Good to know:**
- "The" and "the" are different tokens, because one has a capital letter.
- A token ID is only a label, like an `int` primary key. ID 2207 doesn't mean "animal". And 2207 and 2208 aren't similar words just because the numbers are close.
- The vocabulary is built once, before training, from the most common pieces of text. It never changes after that.

#### What a row of numbers can describe

Here is the idea in a form you could build yourself. Say you build a movie app in .NET. You score each movie on three traits that you pick:

| Movie | Action | Comedy | Animation |
|---|:---:|:---:|:---:|
| Batman | 9 | 2 | 0 |
| Superman | 8 | 3 | 0 |
| Finding Nemo | 1 | 7 | 10 |
| Toy Story | 2 | 8 | 10 |

Each row describes one movie. Similar movies have similar rows, so your app can find "movies like Batman" by comparing rows.

An embedding table works the same way, with two differences. Nobody names the columns. And nobody types the numbers, because training finds them (Part 3).

#### The embedding table: from a token ID to a row of numbers

**What it is:** a table with one row for every token ID. Each token's row is a list of numbers that describes what that token usually means.

**Example:** here each token's row has three numbers.

| Token ID | Token | Number 1 | Number 2 | Number 3 |
|---|---|:---:|:---:|:---:|
| 101 | The | 0.20 | 0.40 | 0.10 |
| 2207 | cat | 0.30 | 0.70 | 0.50 |
| 310 | sat | 0.60 | 0.20 | 0.80 |
| 415 | on | 0.10 | 0.50 | 0.30 |
| 102 | the | 0.25 | 0.35 | 0.15 |
| 520 | mat | 0.80 | 0.10 | 0.40 |
| 845 | because | 0.15 | 0.60 | 0.30 |
| 340 | it | 0.40 | 0.30 | 0.70 |

Finding a token's row is a direct lookup by token ID, like this SQL query:

```sql
SELECT Number1, Number2, Number3
FROM Embedding
WHERE TokenID = 2207;   -- cat
-- returns 0.30, 0.70, 0.50
```

**Good to know:**
- Each token has its own row, and every token's row has the same number of columns. The builders choose that number before training, and it never changes.
- Real models use hundreds or thousands of columns. For example, the public model GPT-2 has 50,257 tokens with 768 columns each. That is about 38.6 million numbers in its embedding table alone. Anthropic doesn't publish Claude's sizes.
- No single column means "animal" or "grammar". A meaning is spread over many columns. So you compare two tokens by their whole rows, never by one column.
- The numbers in a token's row are **not** the IDs of other tokens. They describe this token and don't point anywhere else.
- One row of numbers is called a **vector**. A whole grid of numbers is called a **matrix**.

#### The weights: everything else the model learned

**What they are:** all the other numbers the model learned. They are not one table. They are many matrices, each with its own job, and each layer has its own set.

| Weight matrix | Its job | Where you see it |
|---|---|---|
| Wq, Wk, and Wv, in every layer | Make each token's Query, Key, and Value | Part 2, step 3 |
| Feed-forward matrices, in every layer | Work on each token's row after attention | Part 2, step 4 |
| The output matrix, once at the end | Give every token in the vocabulary a score | Part 2, step 5 |

**Good to know:** a **parameter** is any number that training can change, including the embedding rows. A "70-billion-parameter model" has 70 billion learned numbers.

#### How the weights use the embedding numbers

Lesson 1 showed a simple version, with one weight per number:

|  | Number 1 | Number 2 | Number 3 |
|---|:---:|:---:|:---:|
| Embedding numbers | 0.25 | 0.81 | 0.42 |
| Example weights | 0.50 | 0.20 | 0.80 |
| Multiplication result | 0.125 | 0.162 | 0.336 |

That version is too simple, because the numbers never affect each other. In a real model, **each result adds up all the input numbers**, each times its own weight:

```text
result 1 = (number 1 × weight A) + (number 2 × weight B) + (number 3 × weight C)
result 2 = (number 1 × weight D) + (number 2 × weight E) + (number 3 × weight F)
```

- A big weight makes its input count more in that result.
- A negative weight makes its input count against the result.
- No weight "picks" a number. Every result mixes every input, so the model can combine information from all the columns.

Part 2, step 3 shows this with real numbers.

> **Remember this:** The vocabulary gives the token ID. The embedding table gives that token's row of numbers. The weights mix the numbers until the model can score the next token.

---

### Part 2. How the model answers your message

This part follows the model as it reads "The cat sat on the mat because it" and works out the next token. Every step uses the saved numbers from Part 1, and nothing here changes them.

#### Step 1: cut the text into tokens (tokenization)

The model can't work with letters, so it starts by turning your text into token IDs.

**What happens:** the model cuts the text into tokens. It replaces each token with its token ID from the vocabulary.

**Example:** "The cat sat on the mat because it" becomes eight token IDs: 101, 2207, 310, 415, 102, 520, 845, 340.

**Good to know:** this is why you pay per token. The API counts tokens, not words. A long or rare word often becomes several tokens.

#### Step 2: look up each token's row (embedding)

The model needs numbers that describe each token. Those numbers are already saved in the embedding table.

**What happens:** for each token ID, the model reads that token's row and makes a working copy for this request.

**Example:** token ID 340 ("it") gives the row `[0.40, 0.30, 0.70]` from the embedding table.

**Good to know:** the saved row for "it" is the same in every sentence, for every user. That is a problem, because "it" means something different each time. Step 3 fixes this.

#### Step 3: borrow meaning from earlier words (attention)

The row for "it" can't say what "it" refers to. So "it" needs to collect information from the words before it. This is called **attention**, and it has five small steps.

Each token makes three new rows from its own row:

| New row | Plain meaning | The same idea in SQL |
|---|---|---|
| **Query** | What this token is looking for | The search you type |
| **Key** | What this token offers to others | The column the search is matched against |
| **Value** | The information this token hands over | The data you get back |

There is one big difference from SQL. SQL returns only the rows that match. Attention gives **every** earlier token a percentage, then adds up a little of each token's Value:

```sql
-- Not real SQL. This only shows the idea:
SELECT SUM(MatchPercent * Value)
FROM EarlierTokens;
```

##### 3a. Make the Query for "it" (matrix multiplication)

**What happens:** the model multiplies the row of "it" by a matrix called Wq. Training learned Wq.

**Example:** Wq has one row for each of the 3 embedding numbers. It has one column for each Query number. Here the Query has 2 numbers, to keep the math small.

| Wq | Query number 1 | Query number 2 |
|---|:---:|:---:|
| From embedding number 1 | 1.0 | 0.0 |
| From embedding number 2 | 0.0 | 1.0 |
| From embedding number 3 | 1.0 | 0.5 |

Each Query number uses all three numbers of "it", `[0.40, 0.30, 0.70]`:

```text
Query number 1 = 0.40 × 1.0 + 0.30 × 0.0 + 0.70 × 1.0 = 1.10
Query number 2 = 0.40 × 0.0 + 0.30 × 1.0 + 0.70 × 0.5 = 0.65

Query of "it" = [1.10, 0.65]
```

The same math in C#:

```csharp
double[] Multiply(double[] row, double[,] W)
{
    var result = new double[W.GetLength(1)];
    for (int col = 0; col < W.GetLength(1); col++)   // for each result number
        for (int i = 0; i < row.Length; i++)         // use every input number
            result[col] += row[i] * W[i, col];       // times its own weight
    return result;
}
// Multiply(itRow, Wq) returns { 1.10, 0.65 }
```

**Good to know:** this is all "matrix multiplication" means. For each result, multiply every input by its weight and add them up.

##### 3b. Make a Key for every earlier token

**What happens:** the model multiplies every token's row by a second matrix, Wk. This gives each token its Key.

**Example:**

| Wk | Key number 1 | Key number 2 |
|---|:---:|:---:|
| From embedding number 1 | 2.0 | 0.5 |
| From embedding number 2 | −0.5 | 0.5 |
| From embedding number 3 | 0.0 | −0.5 |

For "mat", whose row is `[0.80, 0.10, 0.40]`:

```text
Key number 1 = 0.80 × 2.0 + 0.10 × −0.5 + 0.40 × 0.0  = 1.55
Key number 2 = 0.80 × 0.5 + 0.10 × 0.5  + 0.40 × −0.5 = 0.25
```

**Good to know:**
- Every token uses the **same** Wk, like calling one C# method on every row of a table.
- So every token gets its own Key, but each layer has only one Wk. The same goes for Wq and Wv.
- "It" can see "The cat sat on the mat because it", including itself. It can't see "was comfortable", because those words don't exist yet. Hiding later words like this is called *causal masking*.

> **Your question:** Does every token have its own Wq, Wk, and Wv? No. Each token has its own row, so it gets its own Query, Key, and Value. But all tokens in a layer use the same three matrices. That is why their Queries and Keys can be compared.

##### 3c. Score each match (dot product)

**What happens:** to score how well the Query of "it" matches a Key, the model multiplies them number by number and adds the results. This is a **dot product**. A bigger result means a better match.

**Example:**

```text
"it" with "mat": 1.10 × 1.55 + 0.65 × 0.25 = 1.868
"it" with "cat": 1.10 × 0.25 + 0.65 × 0.25 = 0.438
```

**Good to know:** the model then divides each score by the square root of the Key's length. Here that is √2, about 1.414. This stops the scores from getting too big when rows have thousands of numbers.

##### 3d. Turn scores into percentages (softmax)

**What happens:** **softmax** raises the number *e* (about 2.718) to the power of each score. This makes every result positive and pushes bigger scores further ahead. Then it divides each result by the total, so they add up to 100%.

**Example:**

| Earlier token | Key | Dot product | ÷ 1.414 | e to that power | ÷ total |
|---|:---:|:---:|:---:|:---:|:---:|
| The | [0.20, 0.25] | 0.383 | 0.270 | 1.311 | 9.4% |
| cat | [0.25, 0.25] | 0.438 | 0.309 | 1.363 | 9.7% |
| sat | [1.10, 0.00] | 1.210 | 0.856 | 2.353 | 16.8% |
| on | [−0.05, 0.15] | 0.043 | 0.030 | 1.031 | 7.4% |
| the | [0.33, 0.23] | 0.504 | 0.356 | 1.428 | 10.2% |
| **mat** | [1.55, 0.25] | 1.868 | 1.321 | 3.745 | **26.8%** |
| because | [0.00, 0.23] | 0.146 | 0.103 | 1.109 | 7.9% |
| it | [0.65, 0.00] | 0.715 | 0.506 | 1.658 | 11.8% |
| **Total** | | | | **13.997** | **100%** |

"Mat" gets the most attention: 26.8%.

**Good to know:** nobody wrote a rule that "it" means "mat". The percentages come only from the learned numbers in Wq, Wk, and the embedding table.

> **Your question:** How did the model know "mat" should score highest? It didn't know. Training tuned Wq, Wk, and the tokens' rows in the embedding table so the scores help guess the next token. In this sentence, "it" could also mean the cat. Attention doesn't have to decide. It only collects what helps the next guess.

##### 3e. Blend the Values into "it"

**What happens:** the model multiplies each earlier token's Value by its percentage and adds them up into one blend. Then it adds the blend to the working row of "it".

**Example:** to keep this short, the Wv here just copies each token's row. So each token's Value is the same as its row in the embedding table from Part 1.

```text
blend number 1 = 9.4% × 0.20 (The) + 9.7% × 0.30 (cat) + … + 26.8% × 0.80 (mat) + … = 0.455
blend          = [0.455, 0.322, 0.444]
```

| | Number 1 | Number 2 | Number 3 |
|---|:---:|:---:|:---:|
| Saved row of "it" | 0.40 | 0.30 | 0.70 |
| + Blend from attention | 0.455 | 0.322 | 0.444 |
| = Row of "it" in this sentence | **0.855** | **0.622** | **1.144** |

**Good to know:**
- The saved row of "it" doesn't change. Only the working copy for this request now holds the meaning of this sentence.
- The blend is **added** to the working row of "it", not swapped in. So "it" keeps its own meaning and gains context on top. This is called a *residual connection*.
- A real Wv mixes the numbers, just like Wq does in 3a.

> **Remember this:** The Query asks. Each Key answers. Softmax turns the matches into percentages. The Values are what gets handed over.

#### Step 4: the rest of each layer

One attention is only a small part of one layer. These parts also run on every token's working row from step 3:

| Part | What happens | Why it is there |
|---|---|---|
| **Many heads** (*multi-head attention*) | Each layer runs many attentions side by side. Each has its own Wq, Wk, and Wv. | Different heads can track different links, such as what "it" refers to, or which word is the verb. Training decides what each head does. |
| **Feed-forward network** | Each token's row goes through two more matrix multiplications. | Attention moves information between tokens. This step then works on what each token now holds. Much of the model's knowledge is stored here. |
| **Normalization** | The model rescales each token's working row so its numbers stay in a steady range. | Without it, the numbers could grow or shrink too much over many layers. |
| **Many layers** | The whole block repeats dozens of times. Each layer has its own weights. | Each layer sharpens the meaning a little more. |
| **Position** | The model adds each token's position into the math. | Attention alone ignores word order. Without position, "dog bites man" and "man bites dog" would look the same. |

For a sense of size, GPT-2, a small public model from 2019, has 12 layers, 12 heads per layer, and about 124 million weights. Large models today have billions.

#### Step 5: score every word and pick one

After the last layer, the model has a final row for "it". Now it turns that row into a choice of next token.

##### 5a. Score every token in the vocabulary (logits)

**What happens:** the model multiplies the final row of "it" by the **output matrix**. That matrix has one column for every token in the vocabulary. The result is one score per token, called a **logit**.

**Example:** this example's vocabulary has five tokens. Say the final row of "it" is its working row from step 3, `[0.855, 0.622, 1.144]`.

| Output matrix | was | is | sat | cat | mat |
|---|:---:|:---:|:---:|:---:|:---:|
| From number 1 | **1.5** | 0.8 | 0.6 | 0.2 | 0.4 |
| From number 2 | 0.5 | 0.9 | 0.3 | 1.0 | 0.2 |
| From number 3 | 1.2 | 0.6 | 0.9 | 0.3 | 0.5 |

```text
logit for "was" = 0.855 × 1.5 + 0.622 × 0.5 + 1.144 × 1.2 = 2.966
```

**Good to know:** remember the **1.5** in bold. Part 3 uses that exact weight to show how training works.

##### 5b. Turn scores into chances (softmax)

**What happens:** softmax turns the logits into chances that add up to 100%, just like in 3d.

| Token | was | is | sat | cat | mat |
|---|:---:|:---:|:---:|:---:|:---:|
| Logit | 2.966 | 1.930 | 1.729 | 1.136 | 1.038 |
| Chance | **51.3%** | 18.2% | 14.9% | 8.2% | 7.5% |

##### 5c. Pick one token (temperature)

**What happens:** the model picks one token at random, using the chances. So "was" is picked about half the time. Before softmax, the model divides every logit by the **temperature**. This changes how spread out the chances are.

| Temperature | was | is | sat | cat | mat | Effect |
|:---:|:---:|:---:|:---:|:---:|:---:|---|
| 0.5 | 79.5% | 10.0% | 6.7% | 2.0% | 1.7% | The top token wins more often, so answers are more predictable |
| 1.0 | 51.3% | 18.2% | 14.9% | 8.2% | 7.5% | The chances as calculated |
| 1.5 | 39.8% | 20.0% | 17.5% | 11.8% | 11.0% | Other tokens get more chances, so answers vary more |

**Good to know:** you'll see three other ways to pick in documentation:
- **Greedy decoding** always picks the top token. The same input always gives the same answer, but the text can get dull.
- **Top-k** keeps only the k most likely tokens, such as 40, and picks from those.
- **Top-p** keeps the top tokens whose chances add up to p, such as 90%, and picks from those.

[Lesson 6](06-temperature.md) covers the Claude API's temperature setting.

#### Step 6: repeat until the answer is done

**What happens:** the model adds "was" to the text. "Was" then goes through steps 2 to 5, looking back at everything before it. The model picks the next token, and so on.

**Good to know:**
- The model stops at a special end token, at your `max_tokens` limit, or at one of your stop sequences ([lesson 1](01-accessing-the-api.md#5-when-the-model-stops-and-what-comes-back)).
- The model saves the Keys and Values it already made for earlier tokens. So each round it only makes them for the new token. This saved work is called the *KV cache*.

---

### Part 3. How the model learned its numbers (training)

Part 2 used numbers like Wq, Wk, and the output weight 1.5 as if they were just there. This part shows where they came from. Each one started random, and training adjusted them in small steps.

#### Step 1: every number starts random

**What happens:** before training, the training process fills every token's row in the embedding table, and every weight matrix, with small random numbers.

**Example:**

| Token | Number 1 | Number 2 | Number 3 |
|---|:---:|:---:|:---:|
| cat, before training | 0.25 | −0.31 | 0.42 |
| mat, before training | −0.15 | 0.75 | −0.21 |

**Good to know:** the starting numbers can be negative, and they don't have to be between 0 and 1. At this point "cat" is no closer to "kitten" than to "refrigerator". The tokens' rows don't mean anything yet.

#### Step 2: practise with a hidden word

**What happens:** the training process takes a sentence and shows the model only the start. It hides the next token and keeps it as the answer.

**Example:** from "The cat sat on the mat because it was comfortable", the training process makes one practice question per token:

| The model is shown | The hidden answer |
|---|---|
| The | cat |
| The cat | sat |
| The cat sat | on |
| … | … |
| The cat sat on the mat because it | **was** |

**Good to know:**
- The answer comes from the sentence itself, so nobody has to label anything. This is called *self-supervised learning*.
- The model never searches Wikipedia or the internet to check. The training process already has the answer.

> **Your question:** Why ask the model to guess a word the sentence already has? Because the model only sees the words before it. The training process keeps the hidden word as the answer key. Practising like this on billions of sentences teaches the model to guess new text well.

#### Step 3: measure how wrong the guess was (loss)

**What happens:** the model guesses, just like in Part 2. Then the training process turns the chance given to the right token into one number, called the **loss**.

The formula is `loss = −ln(chance of the right token)`. `ln` is the natural log, a button on any scientific calculator.

**Example:** in Part 2, step 5b, the model gave "was" a 51.3% chance. So the loss is −ln(0.513) = **0.668**.

| Chance given to the right token | Loss | What it means |
|:---:|:---:|---|
| 10% | 2.30 | Very wrong |
| 50% | 0.69 | Unsure |
| **51.3%** ("was") | **0.668** | Unsure |
| 90% | 0.11 | Mostly right |
| 99% | 0.01 | Almost perfect |

**Good to know:** the goal of training is the lowest possible average loss over all the training text.

> **Your question:** How does the model know "the cat sat on the mat" is more likely than "the dog sat on the mat"? It doesn't know what is true. It learned what was common in its training text. If "mat" often came after "sat on the", training pushed the numbers to give "mat" a high chance there.

#### Step 4: find which way to move a number (the gradient)

To make the next guess better, the training process must change the numbers. First it needs to know which way to move each one. Let's follow the 1.5 weight from Part 2, step 5a. It helped make the score for "was".

**What happens:** the training process checks how the loss changes if this weight gets a little bigger. That rate of change is the weight's **gradient**.

**Example:** make the weight 0.01 bigger and run the guess again.

| | Weight | Loss |
|---|:---:|:---:|
| Before | 1.50 | 0.6684 |
| 0.01 bigger | 1.51 | 0.6642 |

- The loss went down by 0.0042.
- 0.0042 ÷ 0.01 = 0.42. So the loss falls about 0.42 for every 1 the weight grows.
- That makes the gradient **−0.42**.

**Good to know:**

| Gradient | What it means | So the number should |
|:---:|---|---|
| Positive | Bigger makes the loss worse | Get smaller |
| Negative | Bigger makes the loss better | Get bigger |
| Zero | This number didn't affect the guess | Stay the same |

#### Step 5: get every gradient at once (backpropagation)

**What happens:** testing one number at a time would take billions of reruns. So **backpropagation** gets every gradient in one pass. It starts at the loss and works backward through each step of Part 2. It goes from the scores, back through every layer, into the embedding rows.

**Example:** for the 1.5 weight, the math gives an exact formula:

```text
gradient = (the input this weight multiplies) × (chance of "was" − 1)
         = 0.855 × (0.513 − 1)
         = −0.417
```

That matches the −0.42 from step 4. So backpropagation gets the same answer without any reruns.

**Good to know:** backpropagation only calculates. It doesn't change any number.

#### Step 6: change every number a little (gradient descent)

**What happens:** **gradient descent** changes each number using its gradient and one rule:

```text
new value = old value − (learning rate × gradient)
```

The **learning rate** is a small number, here 0.1. It keeps each change small, so one sentence can't push the model too far.

**Example:**

```text
new value = 1.5 − (0.1 × −0.417)
          = 1.5 + 0.0417
          = 1.5417
```

The model guesses again with the new weight, and the guess is a bit better:

| | Weight | Chance of "was" | Loss |
|---|:---:|:---:|:---:|
| Before the update | 1.5000 | 51.3% | 0.668 |
| After one update | 1.5417 | 52.1% | 0.651 |

**Good to know:** taking away a negative gradient makes the number bigger. That matches the gradient table in step 4. Training changes every number this way, not just this one.

> **Your question:** What does gradient descent do with a gradient of −0.5? It makes the number bigger: `old − (0.1 × −0.5) = old + 0.05`.

The whole training loop, repeated billions of times:

```mermaid
flowchart TD
    A[Take a sentence<br/>from the training text] --> B[Hide the next token]
    B --> C[The model guesses<br/>was = 51.3%]
    C --> D[Measure the loss<br/>0.668]
    D --> E[Backpropagation:<br/>a gradient for every number]
    E --> F[Gradient descent:<br/>change every number a little]
    F --> A
```

#### The embedding rows are trained the same way

**What happens:** backpropagation keeps going back into the embedding rows of the tokens in the sentence. Those rows get their own gradients and small changes too.

**Example:** "it", "mat", and "cat" were in the sentence, so their rows change a little. "Refrigerator" wasn't, so its row stays the same.

**Good to know:**
- This is how the random rows from step 1 slowly get meaning.
- "Cat" and "kitten" appear in similar sentences, such as "I fed the ___". So their rows get pushed the same way, and after billions of steps they end up close.
- Wq, Wk, Wv, the feed-forward matrices, and the output matrix are all trained in this same loop.

#### How real training is different from this example

- **Batches:** real training guesses for many sentences at once, then averages the gradients before changing the numbers. This smooths out any one odd sentence.
- **Better rules:** real training uses improved versions of gradient descent, such as *Adam*. These pick a step size for each number.
- **Length:** the numbers change over a very long run of steps. Most text is read once or a few times. One full pass over all the text is called an *epoch*.
- **Later training:** this practice gives a model that continues text. More training then teaches it to follow instructions and stay safe. Anthropic uses feedback from people and written rules (*Constitutional AI*) for this.

#### Can one wrong sentence spoil what the model learned?

Usually not. Say the model read "cats are animals" thousands of times, then read "The cat is a refrigerator" once. That one change is tiny, and it is averaged with many other sentences. But if wrong text appears many times, the model can learn it. That is why the quality of training text matters.

---

### Common mix-ups

| ❌ Wrong idea | ✅ What really happens |
|---|---|
| The numbers in a token's row are IDs of related words. | They describe the token itself. Token IDs only label tokens. |
| Each weight multiplies one number, and a big weight picks that number. | Each result adds up all the inputs, each times its own weight. Nothing is picked. |
| Backpropagation changes the numbers. | Backpropagation only calculates. Gradient descent makes the changes. |
| Only the weights are trained. The embedding table stays fixed. | The embedding rows are trained in the same loop. |
| Every token has its own Wq, Wk, and Wv. | All tokens in a layer share the same three. Each layer has its own set. |
| The model learns from my chats. | Answering only reads the numbers. Nothing from your chat is saved inside the model. |

---

### Test yourself

<details>
<summary>1. A weight is 2.0, its gradient is +0.8, and the learning rate is 0.1. What is the new weight?</summary>

The new weight is 1.92, because `2.0 − (0.1 × 0.8) = 1.92`. A positive gradient means bigger makes the loss worse, so the weight gets smaller.
</details>

<details>
<summary>2. The Query of "it" is [1.10, 0.65]. The Key of "sat" is [1.10, 0.00]. What is their dot product?</summary>

The dot product is 1.21, because `1.10 × 1.10 + 0.65 × 0.00 = 1.21`.
</details>

<details>
<summary>3. Why can't "it" look at "comfortable" in "The cat sat on the mat because it was comfortable"?</summary>

"Comfortable" comes after "it". The model writes left to right, so later words don't exist yet. This is called causal masking.
</details>

<details>
<summary>4. The model gives the right token a 90% chance. What is the loss, and is that good?</summary>

The loss is about 0.11, because −ln(0.9) = 0.105. That is good. A perfect guess has a loss of 0, and the loss grows fast as the chance drops.
</details>

---

### Architect notes: what this means for your work

#### Training compared with normal use

| | Training | Normal use (inference) |
|---|---|---|
| When | Once, before release | On every request |
| Where the text comes from | Books, websites, and other text | Your request |
| The next token is | Hidden, so the guess can be checked | Unknown, so the model picks it |
| Loss and gradients | Yes, for every batch | No |
| The numbers change | Yes, after every batch | **No. They are only read.** |
| Remembers you next time | — | No. Your app must resend earlier messages. |

#### Cost

- You pay per token, and every input token goes through every layer. So long documents cost money even when the answer is short. Send only the passages needed, for example with retrieval (lessons 32–38).
- Each output token needs a full trip through the model. That is one reason output tokens cost more than input tokens. Ask for only the length you need, and check current prices on Anthropic's pricing page.

#### Speed

- Each new token looks back at every earlier token. So long prompts are slower, especially before the first word of the answer.
- Prompt caching (lessons 43–45) saves the work done on an unchanged start of a prompt. Later requests that start the same way are faster and cheaper. Put fixed text, such as instructions and reference documents, at the start.

#### Limits

- The **context window** is the most tokens one request can hold, counting your input and the answer. The model can only use what is in that request. Look up each model's limit.
- The model only knows its training text, up to a cutoff date. For newer facts, put them in the prompt or give the model a search tool.

#### Security and data

- The model has no memory between requests. Your app must store the history and send it again. Store it securely, because your app is now responsible for it.
- Attention treats all text in the prompt the same way. There is no wall between your instructions and text from a document. So hidden text in a document can steer the model. This is called *prompt injection*. Tag untrusted text, limit which tools the model can use, and check its output.
- Whether Anthropic keeps or trains on your data is set by its terms and your contract. Your requests don't change that. Check the current terms for each customer.

#### Design trade-offs

- Answers vary because tokens are picked from chances. For tasks that need the same answer, such as sorting into categories, lower the temperature, give examples, and check the output in code. Don't promise a customer identical answers.
- Smaller models have fewer weights, so each token needs less math. They are faster and cheaper, but usually less smart. Test the smallest model that passes your test questions first.

---

### Recap

- **Saved inside:** the vocabulary turns text into token IDs. The embedding table turns each ID into a row of numbers. The weights mix those numbers.
- **Weights mix:** each result adds up all the inputs, each times its own weight.
- **Layers:** every token's row passes through dozens of layers. Each layer has its own fixed weights and adds a little more meaning.
- **Answering:** cut into tokens, look up rows, borrow meaning through attention, repeat over many layers, score every token, pick one, and repeat.
- **Attention:** Query, Key, and Value from shared matrices. A dot product scores each match, softmax makes percentages, and the Values are blended in.
- **Picking:** softmax turns scores into chances. Temperature controls how spread out they are.
- **Training:** every number starts random. The model guesses a hidden token, the loss measures the error, backpropagation finds every gradient, and gradient descent moves every number a little.
- **Normal use:** answering only reads the numbers. The model never learns from your chat and doesn't remember you.

---

## My notes / practice

- [ ] Work out the Query of "it" by hand. `[0.40, 0.30, 0.70]` times Wq should give `[1.10, 0.65]`.
- [ ] Work out the Key of "cat" with Wk. You should get `[0.25, 0.25]`.
- [ ] Put the C# `Multiply` function in a console app. Use it to make the Keys for all eight tokens.
- [ ] Do softmax by hand for two scores, 2.966 and 1.930. Check that the two chances add up to 100%.
- [ ] Explain backpropagation and gradient descent out loud in under a minute, using the change from 1.5 to 1.5417.

---

## FAQ

**Q1. What does "token ID" mean?**
A token ID is the fixed number the vocabulary gives each token, such as 2207 for "cat". It is only a label, like a primary key. Two close IDs are not similar words.

**Q2. Are the numbers in an embedding row the IDs of other tokens?**
No. The numbers describe the token itself. `[0.30, 0.70, 0.50]` describes "cat" and doesn't point to any other row.

**Q3. What do the columns of the embedding table mean?**
No column has a name or one clear meaning. Training fills the columns in and spreads each meaning over many of them. So you compare tokens by their whole rows, never by one column.

**Q4. Why are some models larger than others, and when should I use a smaller one?**
A larger model has more learned numbers, so it can store more patterns and handle harder tasks. But every token passes through all those numbers, so it is slower and costs more. Use a smaller model like Haiku for simple work you run many times, and a larger one like Opus for hard thinking.

**Q5. Does every token have its own Wq, Wk, and Wv?**
No. All tokens in a layer share the same three matrices, and each layer has its own set. Each token still gets its own Query, Key, and Value, because it starts from its own row.

**Q6. Why can't a token look at the words after it?**
The model writes left to right, so later words don't exist yet. Attention only looks at the token itself and the tokens before it. This is called causal masking.

**Q7. Where do the embedding numbers come from?**
They start random. Training changes the embedding-table rows of the tokens in each practice sentence a little, billions of times. In the end, words used in similar sentences have similar rows.

**Q8. Why does training make the model guess a word the sentence already has?**
The model only sees the words before the hidden word. The training process keeps that word as the answer key. Practising this way on billions of sentences teaches the model to guess new text well.

**Q9. What does "loss" mean?**
Loss is one number that says how wrong a guess was: −ln(the chance given to the right token). A 90% chance gives 0.11, and a 10% chance gives 2.30.

**Q10. What is the difference between backpropagation and gradient descent?**
Backpropagation works out which way each number should move to lower the loss. Gradient descent then moves each number: `new = old − (learning rate × gradient)`.

**Q11. (Exam angle) A customer asks whether their employees' chats will change how the model answers other customers. How do you answer?**
No. Answering only reads the model's numbers, and the model keeps no memory between requests. Whether Anthropic keeps or trains on data is set by its terms, so point the customer to Anthropic's current terms and data-retention options. (Governance, Safety & Risk Management)

**Q12. (Exam angle) A team gets different answers to the same prompt in a sorting task and needs consistent output. What do you recommend?**
Explain that the model picks each token from a set of chances, so some variety is normal. Lower the temperature, give clear examples, and check the output in code. Answers get more consistent, but not identical. (Claude Models, Prompting & Context Engineering)

**Q13. (Exam angle) A product manager asks why requests with long documents cost more and run slower. What do you say, and what do you change?**
Every input token goes through every layer, and attention looks back at every earlier token. So cost and time grow with the prompt. Send only the passages needed, and put fixed text at the start so prompt caching can reuse it. (Solution Design & Architecture)

---

| Previous | Course | Next |
|:---|:---:|---:|
| [← Accessing the API](01-accessing-the-api.md) | [📚 Course index](README.md) | [Getting an API key →](02-getting-an-api-key.md) |
