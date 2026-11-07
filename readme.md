# Claude Architect Professional — Study and Expertise Roadmap

> Last reviewed: October 17, 2026. Links verified on that date. Cookbook plan and MCP reading added November 7, 2026. Recheck official pages on November 17 and December 7, 2026.

## Key dates at a glance

| Date | Milestone |
|---|---|
| **Oct 17, 2026** | Study starts. Week-1 checkpoint. |
| **Nov 17, 2026** | Updated official exam guides released. Rebuild the objective tracker. |
| **Nov 20, 2026** | Book the exam appointment (holiday slots fill up). |
| **Dec 7, 2026** | Updated CCAR-P exam content goes live. |
| **Dec 19–25, 2026** | Holiday buffer, final practice set, readiness gate. |
| **Dec 28–30, 2026** | Target exam window. |
| **Mid-Jan 2027** | Retake window if needed (14-day wait). |

## Contents

1. [Goal and timeline](#1-goal-and-timeline)
2. [Verified certification information](#2-verified-certification-information)
3. [Course list, architectural topics, and learning order](#3-course-list-architectural-topics-and-learning-order)
4. [Third-party exam preparation and quality filtering](#4-third-party-exam-preparation-and-quality-filtering)
5. [Study workspace](#5-study-workspace)
6. [Capstone project](#6-capstone-project-scoped-for-10-hoursweek)
7. [Week-by-week schedule](#7-week-by-week-schedule-10-hoursweek)
8. [Weekly routine](#8-weekly-routine)
9. [How to use Claude as your tutor](#9-how-to-use-claude-as-your-tutor)
10. [How to prepare for passing](#10-how-to-prepare-for-passing)
11. [Readiness gate](#11-readiness-gate)
12. [Exam logistics](#12-exam-logistics)
13. [Continue toward expertise after the exam](#13-continue-toward-expertise-after-the-exam)
14. [Start today](#14-start-today)

## 1. Goal and timeline

- Certification goal: Claude Certified Architect — Professional (CCAR-P).
- Target exam window: December 28–30, 2026 (flexible). A January 2027 retake is an acceptable fallback.
- Study start: October 17, 2026.
- Weekly commitment: **10 hours** (about 100 hours through December 27).
- Practical outcome: build, evaluate, and defend a working Claude application.
- Longer-term outcome: grow from strong competence (by January) toward real expertise through deployment and operational experience (January–March 2027 and beyond).

This plan assumes basic programming knowledge. If writing functions, calling an API, working with JSON, and debugging errors are unfamiliar, add prerequisite study and reassess the exam date.

Passing an exam and becoming an expert are different milestones. About 100 hours can produce strong, demonstrable competence; expertise comes from months of building, measuring, and fixing real systems.

## 2. Verified certification information

| Item | Current information | Source |
|---|---|---|
| Exam code | CCAR-P (Professional level). Other exams: CCAO-F, CCAR-F, CCDV-F. | Pearson VUE |
| Exam update | Architect — Professional includes updated content starting **December 7, 2026**. | Pearson VUE |
| Updated guides | Available **November 17, 2026**. A late-December attempt uses the updated exam, so study from that guide. | Pearson VUE |
| Eligibility | Offered to organizations in the Claude Partner Network. | Pearson VUE |
| Prerequisites | No hard prerequisite is stated on the official pages. Partner Academy says to "start at Foundations, then advance to Professional where available." Confirm on the "Who can take an exam" page. | Partner Academy |
| Price | $175 USD. | Partner Academy exam page |
| Official prep | Claude Certified Architect – Professional learning path (5 lessons, about 12 hours of content). | Partner Academy |
| Registration | Purchase on the Partner Academy exam page, then schedule with Pearson VUE. | Partner Academy |
| Retakes | Wait 14 days after the 1st failure, 30 after the 2nd, 90 after the 3rd. Maximum 4 attempts in a rolling 12 months. | Pearson VUE |
| Reschedule/cancel | At least 48 hours before the appointment, or the fee is forfeited. | Pearson VUE |

### Official links (verified October 17, 2026)

- [Pearson VUE: Anthropic certification program](https://www.pearsonvue.com/us/en/anthropic.html)
- [Pearson VUE: OnVUE online-proctored requirements](https://www.pearsonvue.com/us/en/anthropic/onvue.html)
- [Partner Academy: partner certifications (guides, policies, exam table)](https://anthropic-partners.skilljar.com/page/partner-certifications)
- [Partner Academy: Architect – Professional exam page (purchase/register)](https://anthropic-partners.skilljar.com/claude-certified-architect-professional-certification)
- [Partner Academy: Architect – Professional prep learning path](https://anthropic-partners.skilljar.com/path/claude-certified-architect-professional)
- [Anthropic Academy: Build with Claude collection](https://academy.claude.com/collections/build-with-claude)

The exam-guide PDF is linked from the certifications table on the partner certifications page. There is no stable direct PDF URL, so download it from that page and record the version and date.

### Exam domains (provisional)

The domain list below comes from a **third-party** site ([claudecertificationguide.com](https://claudecertificationguide.com/blog/claude-certified-architect-professional-exam-guide)), not from Anthropic. Replace it with the official guide on November 17.

| Domain | Weight (unofficial) |
|---|---:|
| Integration | 19% |
| Solution Design & Architecture | 17% |
| Evaluation, Testing & Optimisation | 16% |
| Governance, Safety & Risk Management | 14% |
| Stakeholder Communication & Lifecycle Management | 14% |
| Claude Models, Prompting & Context Engineering | 13% |
| Developer Productivity & Operational Enablement | 7% |

The same source reports 63 questions, 120 minutes, and a scaled passing score of 720/1000. Treat these figures as unverified.

**Implication:** about 42% of the exam is about design, governance, and stakeholder judgment, and only about 7% is about developer tooling such as Claude Code. Divide your time to match.

### First checkpoint (week 1)

- [ ] Confirm that I can access certification registration through my organization (Claude Partner Network).
- [ ] Check the "Who can take an exam" page for prerequisites, especially whether Foundations is required.
- [ ] Download the current exam guide PDF and record the version and date.
- [ ] Enroll in the official Professional prep learning path.
- [ ] Check the current price, policies, and late-December appointment availability.
- [ ] Do not assume that a Claude or Udemy subscription grants exam eligibility.

Note: Pearson VUE scheduling is unavailable from 8:00 p.m. CDT on October 17 to 1:00 a.m. CDT on October 18 because of maintenance.

## 3. Course list, architectural topics, and learning order

All Anthropic Academy links below were verified against the Academy catalog on October 17, 2026. The "Content" column shows published durations where they are listed. The "Budget" column is a study recommendation that includes exercises.

### Core (do these before the exam)

| Order | Course / Track | Content | Budget | Why |
|---|---|---|---:|---|
| 1 | [Claude Platform 101](https://academy.claude.com/courses/claude-platform-101) | 1.5 hr | 2 h | Platform fundamentals, token mechanics, model tiers |
| 2 | [Building with the Claude API](https://academy.claude.com/courses/building-with-the-claude-api) | 9 hr | 16 h | Prompting, XML tagging, tool use, RAG, production patterns |
| 3 | [Official CCAR-P prep path](https://anthropic-partners.skilljar.com/path/claude-certified-architect-professional) | ~12 hr | 15 h | Exam-aligned syllabus. Spread across weeks 1–8; don't leave it to the end. |
| 4 | [Introduction to Model Context Protocol](https://academy.claude.com/courses/introduction-to-model-context-protocol) | 10 lessons | 5 h | Integration domain, standard tool and resource architecture |
| 5 | [AI capabilities and limitations](https://academy.claude.com/courses/ai-capabilities-and-limitations) | — | 2 h | Safety, reliability boundaries, and model capability trade-offs |
| 6 | One cloud course: [Claude with Amazon Bedrock](https://academy.claude.com/courses/claude-with-amazon-bedrock) **or** [Claude with Google Cloud's Vertex AI](https://academy.claude.com/courses/claude-with-google-cloud-s-vertex-ai) | 65–66 lessons | 6 h | Enterprise deployment choices (Integration domain). Study the IAM, VPC, and PrivateLink sections. |
| 7 | [Claude Code in action](https://academy.claude.com/courses/claude-code-in-action) | 1 hr | 1.5 h | Developer Productivity domain |
| 8 | [Claude Code 101](https://academy.claude.com/courses/claude-code-101) | 1.5 hr | 1.5 h | Developer Productivity domain. **In progress**; notes in [ClaudeCode101/](ClaudeCode101/README.md). |
| **Track** | **[Capstone project: knowledge and support assistant](#6-capstone-project-scoped-for-10-hoursweek)** | **Ongoing (weeks 1–10)** | **30 h** | **Hands-on RAG, MCP, caching, evals, and ADRs across all domains (starts week 1)** |

Core total: about 79 hours (49 hours of coursework and 30 hours of capstone build). The remaining ~20 hours go to practice questions and review (Section 8).

Course notes live in one folder per course, with one file per lesson and an FAQ at the end of each lesson file. For example: [ClaudeCode101/README.md](ClaudeCode101/README.md).

### Course sequence: what to do when you finish each course

The table above lists *what* to study. This one shows the *order*. Work down the list one course at a time. The official prep path runs alongside, following the week-by-week schedule (Section 7).

| Step | Course | When you finish it, do this | Then go to |
|---|---|---|---|
| 1 | **Claude Code 101** (in progress) | Take the course quiz and log missed questions in `ClaudeCode101/05-quiz/`. Use Claude Code to create the capstone repository (Section 5). | Step 2 |
| 2 | Claude Platform 101 | Make your first API call with error handling. Write a one-page explanation of the request-response flow. | Step 3 |
| 3 | Building with the Claude API | Build capstone v1 and v2: document Q&A with citations, prompt caching, and the first 10–20 eval questions. After each chapter, do the matching phase of the [Cookbook build-along plan](cookbook-build-along.md). | Step 4 |
| 4 | AI capabilities and limitations | Add unanswerable and misuse questions to the eval set. Note the model limits that affect your design. | Step 5 |
| 5 | Introduction to Model Context Protocol | Read the MCP documentation pages listed under "Hands-on and reference material". Expose the ticket lookup as an MCP tool, and add the approval gate on the write action. | Step 6 |
| 6 | One cloud course (Bedrock **or** Vertex AI) | Write ADRs on model choice and deployment platform. Measure cost and latency. | Step 7 |
| 7 | Claude Code in action | Use what you learned to add tests and a `CLAUDE.md` to the capstone repo. | Practice sets (Section 7, Dec 5 onward) |
| ∥ | Official CCAR-P prep path (parallel) | Lesson 1 in weeks 1–5, lesson 2 in week 6, lesson 3 in week 7, lessons 4–5 in week 8. After each lesson, update the objective tracker. | — |

If a course finishes early, go straight to the next step. You don't need to wait for the calendar week. If one runs late, cut the deferred courses first, never the capstone.

### Critical Anthropic architectural topics to master

The exam tests operational and cost trade-offs specific to Anthropic's platform. Study these concepts directly in the current [Claude documentation](https://docs.claude.com). Exact limits and prices change, so learn the **trade-off** and look up the current number rather than memorizing it.

- **Prompt caching:** minimum cacheable prompt length (varies by model; check the docs), cache-write vs. cache-read pricing (cache reads are much cheaper than uncached input), TTL behavior (5-minute default, with a longer 1-hour option), and structuring prompts with a stable static prefix to maximize cache hits.
- **Message Batches API:** discounted pricing (about 50%) in exchange for asynchronous processing (results within 24 hours), polling workflows, and when to choose batch vs. real-time requests for enterprise workloads.
- **XML formatting and context engineering:** using semantic tags (`<documents>`, `<instructions>`, `<context>`) to separate untrusted content from instructions. This *reduces* prompt-injection risk but does not eliminate it, so pair it with permission controls and output validation.
- **Structured outputs and tool-calling resiliency:** JSON-schema validation of tool inputs, low temperature for more consistent routing (lower variance, not a guarantee of determinism), multi-turn tool-use loops, and graceful recovery when external tools fail.
- **Enterprise security architecture:** the first-party Anthropic API (including data-retention options such as Zero Data Retention agreements) compared with cloud platforms (AWS Bedrock with IAM and PrivateLink; Google Vertex AI with VPC Service Controls).

### Hands-on and reference material alongside the courses

- **Claude Cookbook (build along).** The [Claude Cookbook](https://github.com/anthropics/claude-cookbooks) is Anthropic's free repository of runnable code examples (Jupyter notebooks). After each chapter of *Building with the Claude API*, run the matching notebooks and rebuild each technique in the capstone. The full step-by-step plan, including Windows setup, is in [cookbook-build-along.md](cookbook-build-along.md). Its hours come out of the 30-hour capstone budget.
- **MCP documentation.** While taking *Introduction to Model Context Protocol*, also read these pages of the official MCP documentation, because the course does not go deep on them and Integration is the largest exam domain: [Architecture overview](https://modelcontextprotocol.io/docs/learn/architecture), the transports and [tools](https://modelcontextprotocol.io/specification/latest/server/tools) sections of the [specification](https://modelcontextprotocol.io/specification/latest), [Authorization](https://modelcontextprotocol.io/specification/latest/basic/authorization), and [Security best practices](https://modelcontextprotocol.io/specification/latest/basic/security_best_practices). Budget about 2 hours.

### Official prep path modules

The official prep path consists of five lessons:
1. Claude Platform & Solution Design (~4 h)
2. Enterprise Integration & Production (~2.6 h)
3. Responsible AI, Safety & Risk for Architects (~1.9 h)
4. Stakeholder Engagement, Lifecycle & GTM (~3 h)
5. Team Enablement & Operational Productivity (~0.75 h)

Its recommended prerequisites are: [Claude 101](https://academy.claude.com/courses/claude-101), Claude Code in Action, [AI Fluency: Framework and foundations](https://academy.claude.com/courses/ai-fluency-framework-foundations), Building with the Claude API, Introduction to Model Context Protocol, and AI Capabilities and Limitations. Skim Claude 101 and AI Fluency only if the concepts are new to you.

### Deferred until after the exam (expertise phase)

- [Model Context Protocol: Advanced topics](https://academy.claude.com/courses/model-context-protocol-advanced-topics)
- [Introduction to agent skills](https://academy.claude.com/courses/introduction-to-agent-skills)
- [Introduction to subagents](https://academy.claude.com/courses/introduction-to-subagents)
- The second cloud course (AWS Bedrock or Google Vertex AI).

These courses are valuable for expertise but carry little relative weight on the CCAR-P exam. If you finish early, do them before December 19, not during the final week.

## 4. Third-party exam preparation and quality filtering

Use **one** practice-question source, mainly for timed practice sets in December. Current candidate courses found on October 17, 2026 (unaffiliated with Anthropic; ratings and counts are self-reported):

- [Claude Certified Architect Professional (CCAR-P) — prep course covering 7 domains](https://www.udemy.com/course/claude-certified-architect-professional-ccar-p/)
- [CCAR-P Exam Prep — practice tests](https://www.udemy.com/course/ccar-p-exam-prep/)
- [CCAR-P Exam 2026 — practice course](https://www.udemy.com/course/claude-certified-architect-professional-ccar-p-exam-2026/)
- [CCAR-P Exam Trainers + Mock Exam](https://www.udemy.com/course/claude-certification-ccar-p-exam-trainers-mock-exam/)

Before choosing one, check that it is included in your subscription, explicitly targets CCAR-P, and states which exam-guide version it follows.

### Quality filter for practice questions

Third-party material can be out of date, or can test memorization instead of architectural trade-offs. Apply this filter:

- **Reject trivia questions:** questions about static constants (such as maximum context token counts) don't reflect the architectural scenarios the exam tests.
- **Prioritize constraint-based scenarios:** focus on questions with multi-variable trade-offs (for example, latency vs. cost vs. data-retention compliance).
- **Hedge against the December 7 update:** third-party question banks may not be fully updated for the December 7 changes. Rely on the official November 17 guide and the practice examiner prompt (Section 9) for targeted scenarios.
- **Audit answer keys against documentation:** if a third-party explanation conflicts with current official documentation on limits, pricing, or safety guidelines, trust the documentation and log the discrepancy in `study/practice-error-log.md`.
- **Do not use exam dumps:** avoid "actual exam question" dumps. They violate candidate agreements and don't build architectural reasoning.

### If programming is a gap

Search your Udemy catalog for `Python APIs pytest`, `Git command line beginners`, or `REST API HTTP JSON`. Study only what is necessary: functions, JSON serialization, HTTP headers and status codes, environment variables, retries with exponential backoff, and basic unit testing.

## 5. Study workspace

```text
claude-architect-roadmap/
├── README.md                 ← this guide
├── ClaudeCode101/            ← course notes (one folder per course)
├── study/
│   ├── exam-objectives.md    ← objective tracker
│   ├── weekly-log.md
│   ├── decision-journal.md   ← tried / expected / happened
│   └── practice-error-log.md
├── app/
│   ├── client.py             ← Anthropic SDK client
│   ├── tools.py              ← tool JSON schemas and local tool functions
│   └── retry.py              ← exponential backoff and error handling
├── mcp_server/
│   └── server.py             ← stdio MCP server
├── sample_documents/         ← fictional synthetic data only
├── tests/
│   └── test_tools.py
├── evaluations/
│   ├── cases.jsonl           ← ~25 scenario test cases
│   └── results/
│       └── benchmark.json    ← quality, cost, latency, cache hit rate
└── docs/
    ├── architecture.md
    ├── decisions.md          ← 3 ADRs
    ├── governance-and-risk.md
    └── stakeholder-brief.md
```

### Setup checklist

- [ ] Install a programming environment and Git.
- [ ] Create the repository.
- [ ] Store credentials in environment variables and never commit secrets.
- [ ] Confirm the API billing arrangement and set a personal spending limit.
- [ ] Use fictional or synthetic documents only.
- [ ] Create the objective tracker.

### Exam objective tracker

| Official objective | Can explain? | Practiced? | Evidence | Next action |
|---|---|---|---|---|
| Paste from the official guide | No / Partial / Yes | No / Yes | Link to notes or code | Specific action |

On November 17, replace the provisional domain list with the official objectives.

## 6. Capstone project (scoped for 10 hours/week)

### Project: knowledge and support assistant

Build one application incrementally, using the [Cookbook build-along plan](cookbook-build-along.md) to learn each feature before you build it. It should:

1. Answer questions from fictional company documents (RAG) and cite its sources.
2. Say when the documents do not support an answer.
3. Look up a fictional support ticket through a tool (exposed via MCP).
4. Require human approval before a consequential write, such as creating a ticket.
5. Handle invalid input and tool failures gracefully (retries with backoff, clear error messages).
6. Use prompt caching for the static system prompt and document context, and measure the effect.
7. Produce repeatable evaluation results.

### Required evidence (mapped to exam domains)

- [ ] Working application. *(Integration)*
- [ ] Architecture diagram and documented tool interfaces. *(Solution Design)*
- [ ] Evaluation set of about 25 cases, an evaluation report, and measured cost, latency, and cache hit rate. *(Evaluation & Optimisation)*
- [ ] One-page governance and risk review covering data handling, prompt injection, the permission and approval model, and logging. *(Governance & Risk)*
- [ ] One-page stakeholder brief covering business value, cost, risks, rollout plan, and success metrics. *(Stakeholder & Lifecycle)*
- [ ] Three architecture decision records, including one on model choice and one on deployment platform. *(Solution Design / Models)*

Each decision record should answer:
1. What problem are we solving?
2. What alternatives did we consider?
3. Why did we choose this approach?
4. What are its limitations?
5. What evidence would make us change it?

The deployment runbook, full operations documentation, and larger evaluation suites are deferred to the expertise phase (Section 13).

## 7. Week-by-week schedule (10 hours/week)

| Week | Courses | Hands-on / exam work | Deliverable |
|---|---|---|---|
| **Oct 17–23** | Claude Code 101 (in progress). Platform 101. Start API course. Start prep path lesson 1. | Week-1 checkpoint (Section 2). Set up repo. First API call with error handling. | Working CLI and a one-page explanation |
| **Oct 24–30** | API course: prompting, context, tool use | Small document-answering prototype. Write the first 10 eval questions. | Prototype v1 and eval rubric |
| **Oct 31–Nov 6** | API course: RAG, agents. AI capabilities and limitations. | Add retrieval with citations. Add prompt caching. Test unanswerable questions. | Prototype v2 and data-flow diagram |
| **Nov 7–13** | Intro to MCP | Expose the ticket lookup as an MCP tool. Add an approval gate on the write. Test tool failures. | Controlled tool workflow |
| **Nov 14–20** | **Nov 17: new guide.** Finish prep path lesson 1. | Rebuild the objective tracker from the official guide. Mark gaps. **Book the exam.** | Official tracker and booked appointment |
| **Nov 21–27** | One cloud course (relevant sections). Prep path lesson 2. | ADRs on model choice and deployment platform. Measure cost, latency, and cache hit rate. | 2 ADRs and benchmark results |
| **Nov 28–Dec 4** | Prep path lesson 3 (Responsible AI) | Expand the eval set to about 25 cases. Write the governance and risk review. Write the third ADR. | Eval report and governance review |
| **Dec 5–11** | Prep path lessons 4–5. Claude Code in action. | **Dec 7:** check the updated content. Write the stakeholder brief. Give a 5-minute design pitch. **Timed practice set #1.** | Stakeholder brief and error log |
| **Dec 12–18** | Revisit weak prep-path sections | Repair the top gaps from the error log. Rebuild one weak feature without a tutorial. **Timed practice set #2.** | Final gap list |
| **Dec 19–25** | — (holiday buffer) | **Timed practice set #3.** Mock architecture interview using the reviewer prompt. Readiness gate (Section 11). | Readiness checklist |
| **Dec 26–27** | — | Light review of the error log and ADRs. OnVUE system test. Check ID and appointment details. | — |
| **Dec 28–30** | — | **Exam** | — |

If the exam doesn't go your way, a retake is possible 14 days later (mid-January). Use that time to work on the specific weak domains from your score report.

## 8. Weekly routine

| Activity | Hours |
|---|---:|
| Official lessons and documentation | 4 |
| Building, debugging, and measuring the capstone | 3 |
| Practice questions and scenario reasoning | 2 |
| Review, error log, and explaining concepts aloud | 1 |
| **Total** | **10** |

For each important topic: study it, implement it, break it on purpose, explain it without notes, check your explanation, and record the lesson.

If you miss a week, cut deferred or optional material first. Never cut hands-on work or alignment with the updated guide.

## 9. How to use Claude as your tutor

### Tutor prompt

```text
Act as my Claude architecture tutor.

Use the official exam objectives and documentation I provide.
Teach one concept at a time.
Ask me a question and wait for my answer.
Distinguish documented facts from recommendations.
Do not invent certification requirements.
If a claim needs verification, tell me what official material to check.
```

### Architecture reviewer prompt (use every two weeks)

```text
Review my architecture as a skeptical production reviewer.

Ask about:
- Requirements and business success measures
- Model and deployment-platform choice
- Context, retrieval, and prompt caching
- Tool permissions and approval boundaries
- Evaluation
- Security, governance, and data handling
- Response time and cost
- Stakeholder communication and rollout plan

Identify the three most consequential weaknesses.
Ask me to defend my choices before proposing replacements.
```

### Practice examiner prompt

```text
Create original scenario questions mapped to the official objectives
I paste below.

Do not reproduce or claim knowledge of real exam questions.
Ask one question at a time and hide the answer.
After I respond, explain the reasoning and why each alternative is weaker.
Identify claims that I should verify in official documentation.
```

### Independence rule

For each major component: attempt it yourself, ask for a hint or review, implement the correction, explain the resulting code, and later rebuild the core part without help. Treat Claude-generated answer keys as material to verify, not as official evidence.

## 10. How to prepare for passing

### Error log

| Topic | My answer | Why it failed | Correct reasoning | Evidence checked | Retest |
|---|---|---|---|---|---|

Classify each mistake: knowledge gap, misread requirement, missed constraint, confused alternatives, unsupported assumption, or time management.

### Scenario reasoning

For each question, ask:
1. What is the actual requirement?
2. Which constraints are mandatory?
3. Which failure or risk matters most?
4. Which option meets the requirement with the fewest unsupported assumptions?
5. Why are the other options weaker?

### Traps to avoid

- Repeating the same question bank until the wording becomes familiar.
- Treating course completion as proof of competence.
- Assuming generated practice questions are accurate.
- Memorizing unstable product facts without checking current documentation.
- Using leaked or "actual exam" question dumps.
- Letting the target date override readiness.

## 11. Readiness gate

These are personal checks, not Anthropic's passing standard.

### Exam preparation

- [ ] Every objective in the updated (Nov 17) guide has been reviewed.
- [ ] I have notes or evidence for each objective.
- [ ] I can explain why incorrect options are wrong.
- [ ] I score consistently on fresh, timed practice sets.
- [ ] No unresolved major gaps, especially in the Governance and Stakeholder domains.

### Practical competence

- [ ] I can explain my application end to end.
- [ ] I can debug a failed API request.
- [ ] I can distinguish retrieval, prompting, and tool failures.
- [ ] I can explain and defend the permission and approval model.
- [ ] I can justify model, platform, caching, and batch choices with cost and latency data.
- [ ] I can pitch the design to a non-technical stakeholder.

### Decision

- If ready: keep the appointment.
- If not ready: reschedule at least 48 hours in advance and confirm the new appointment.

## 12. Exam logistics

- [ ] Purchase and register on the [Architect – Professional exam page](https://anthropic-partners.skilljar.com/claude-certified-architect-professional-certification).
- [ ] Choose online proctoring or a test center through Pearson VUE.
- [ ] Make sure the booked name exactly matches your government-issued ID.
- [ ] Read the confirmation email and the [current OnVUE rules](https://www.pearsonvue.com/us/en/anthropic/onvue.html).
- [ ] Run the OnVUE system test on the same device and network you'll use, and restart the computer beforehand.
- [ ] Prepare a private testing space (a 360° room scan is required).
- [ ] Begin check-in when it opens, 30 minutes before the appointment.

## 13. Continue toward expertise after the exam

### January 2027: operate the application

- Deploy in a controlled environment and collect feedback from authorized test users.
- Review failures weekly and turn each one into a regression eval.
- Write the deployment runbook and the incident and recovery procedures.

### February 2027: deepen one specialization

Choose one: retrieval and document intelligence, tool integrations and MCP (with [MCP Advanced topics](https://academy.claude.com/courses/model-context-protocol-advanced-topics)), agent evaluation and reliability (with [subagents](https://academy.claude.com/courses/introduction-to-subagents) and [agent skills](https://academy.claude.com/courses/introduction-to-agent-skills)), Claude Code workflows, or cloud and enterprise integration.

Build something substantial in that area rather than collecting more introductory courses.

### March 2027: demonstrate independent judgment

Produce a technical case study, a before-and-after evaluation report, a documented trade-off, a simulated incident review, and a technical presentation.

An expert can explain not only how a system works, but why it was designed that way, where it fails, and how evidence guides improvements. Your decision journal is the record of that growth.

## 14. Start today

- [ ] Complete the week-1 checkpoint (Section 2), and register after the October 17 Pearson maintenance window ends.
- [ ] Enroll in the [official prep path](https://anthropic-partners.skilljar.com/path/claude-certified-architect-professional).
- [x] Start [Claude Code 101](https://academy.claude.com/courses/claude-code-101) (notes in [ClaudeCode101/](ClaudeCode101/README.md)).
- [ ] Start [Claude Platform 101](https://academy.claude.com/courses/claude-platform-101).
- [ ] Create the repository and save this guide as `README.md`.
- [ ] Block 10 hours a week in your calendar.
- [ ] Add reminders for **November 17** (new guide), **November 20** (book the exam), and **December 7** (exam update).
- [ ] Make your first working API call.

Priority order: official prep and fundamentals → hands-on building → alignment with the updated guide → targeted practice → operational experience.
