<div align="center">

<picture>
  <source media="(prefers-color-scheme: light)" srcset="assets/hero-light.svg">
  <img src="assets/hero.svg" alt="Chaitanaya Srivastava, Data Science and ML Engineer. B.Tech Computer Science (Data Science), Galgotias University, class of 2028. Open to Data Science, Analytics and ML internships." width="100%">
</picture>

<br>

<a href="https://hypertos.in"><img src="assets/btn-portfolio.svg" alt="Portfolio: hypertos.in" height="44"></a>
<a href="https://www.linkedin.com/in/chaitanaya052006"><img src="assets/btn-linkedin.svg" alt="LinkedIn: chaitanaya052006" height="44"></a>
<a href="mailto:Chaitanyasrivastava63@gmail.com"><img src="assets/btn-email.svg" alt="Email: Chaitanyasrivastava63@gmail.com" height="44"></a>

</div>

<details>
<summary><b>Contents</b></summary>

- [At a glance](#at-a-glance)
- [Skills](#skills)
- [Featured projects](#featured-projects)
- [Experience](#experience)
- [Other projects](#other-projects)
- [Education](#education)
- [Activity](#activity)

</details>

## At a glance

<picture>
  <source media="(prefers-color-scheme: light)" srcset="assets/stats-light.svg">
  <img src="assets/stats.svg" alt="100+ queries per month in production. About 95% retrieval accuracy. Average reply time cut from 20 minutes to under 30 seconds. 99.19% validation accuracy. 87,000+ training images." width="100%">
</picture>

## Skills

<picture>
  <source media="(prefers-color-scheme: light)" srcset="assets/marquee-light.svg">
  <img src="assets/marquee.svg" alt="Scrolling skills: Python, SQL, Pandas, NumPy, Matplotlib, Seaborn, Scikit-Learn, PostgreSQL, PyTorch, TensorFlow/Keras, Hugging Face, LangChain, LangGraph, FastAPI, Docker, React, TypeScript and more, listed in the table below." width="100%">
</picture>

| Area | Stack |
|---|---|
| **Data Science & Analytics** | `Python` `SQL` `Pandas` `NumPy` `Matplotlib` `Seaborn` `PostgreSQL` `Scikit-Learn` `Exploratory data analysis` `Model evaluation` `Feature engineering` |
| **ML & AI** | `PyTorch` `TensorFlow/Keras` `Hugging Face` `Sentence Transformers` `LangChain` `LangGraph` `OpenAI API` `RAG pipelines` `CNNs` `NLP` `Agentic workflows` |
| **Backend & DevOps** | `FastAPI` `Docker` `GitHub Actions` `AWS EC2` `n8n` `Vercel` `Render` `WebSockets` `JWT auth` |
| **Frontend** | `React` `TypeScript` `Vite` `Tailwind CSS` `shadcn/ui` |
| **Databases** | `PostgreSQL` `Supabase` `MongoDB` |
| **Languages** | `Python` `C++` `Java` `TypeScript` `Go` `SQL` |

## Featured projects

### Chronicle: Durable Agent Runtime + Time-Travel Debugger

**Status: `LIVE`** (shipped)

<picture>
  <source media="(prefers-color-scheme: light)" srcset="assets/chronicle-flow-light.svg">
  <img src="assets/chronicle-flow.svg" alt="Chronicle architecture. An agent run appends events to a PostgreSQL event log. Worker A processes the run and is killed. Its lease expires and Worker B resumes from the last recorded step in the log. A timeline scrubber replays or inspects any step." width="100%">
</picture>

- Agent runs are persisted as a durable event log in PostgreSQL, so a run survives crashes: kill a worker mid-run and another worker resumes from the log.
- A time-travel debugger lets you scrub a run's timeline and replay or inspect any step.
- RepoPilot is the demo agent: it reads a codebase and fixes an issue.
- Built-in evals with a regression gate, plus benchmarks. The gate fails when a single word of the agent prompt changes.

| Worker kills survived | Duplicated side effects | Runtime checks passed |
|:---:|:---:|:---:|
| **200** real kills, 144 runs | **0** across 1,112 keyed effects | **8 of 8** |

*Measured on one Windows 11 machine with PostgreSQL 16 in Docker.*

**Stack:** `Python` `PostgreSQL` `Docker` `OpenAI-compatible LLM endpoint` `React` `TypeScript`

<a href="https://chronicle.hypertos.in"><img src="assets/btn-demo.svg" alt="Open the Chronicle live demo: chronicle.hypertos.in" height="44"></a>

<br>

### Mini LLM Inference Server

**Status: `IN PROGRESS`** (with an optional routing layer on top)

<picture>
  <source media="(prefers-color-scheme: light)" srcset="assets/inference-flow-light.svg">
  <img src="assets/inference-flow.svg" alt="Mini LLM Inference Server schematic. Requests enter a batcher, the model decodes using a KV cache, and tokens stream out. An optional router sits in front. Benchmarks are planned." width="100%">
</picture>

- Request batching across concurrent requests
- KV-cache management
- Streaming token output
- Latency and throughput benchmarking
- Optional model router

<br>

### Raft Cluster + Jepsen-style Checker

**Status: `PLANNED`** (distributed systems track; alternative: Retrieval Lab)

<picture>
  <source media="(prefers-color-scheme: light)" srcset="assets/raft-flow-light.svg">
  <img src="assets/raft-flow.svg" alt="Planned distributed systems project schematic. A five-node Raft cluster elects a new leader after the old leader fails, while a Jepsen-style checker scans a recorded client history. Alternative track: Retrieval Lab." width="100%">
</picture>

## Experience

<picture>
  <source media="(prefers-color-scheme: light)" srcset="assets/experience-light.svg">
  <img src="assets/experience.svg" alt="ML Engineer (Freelance), Lakmé Salon, Patna, February to March 2026. Average reply time cut from 20 minutes to under 30 seconds." width="100%">
</picture>

- Architected a production RAG pipeline (vector search + PostgreSQL trigram fuzzy matching), ~95% retrieval accuracy across 50+ service/pricing queries.
- Built an Instagram DM auto-response system (GPT-4.1-mini + n8n agentic workflows), cutting average reply time from 20 minutes to under 30 seconds.
- Deployed on a VPS with webhooks and real-time session state across concurrent conversations, 100+ queries/month in production.

## Other projects

<details>
<summary><b>SAGE</b>: Smart Agentic Grading & Evaluation System &nbsp;·&nbsp; <code>LangGraph</code> <code>FastAPI</code> <code>React 19</code></summary>

- 5-agent LangGraph state graph (Greeter, Interviewer, Evaluator, Scorer, Reporter) running adaptive technical interviews.
- Real-time voice loop with STT + TTS + GPT-4o over streaming WebSockets.
- FastAPI + React 19 + Vite + Tailwind, JWT auth, PostgreSQL; HR dashboard.

</details>

<details>
<summary><b>ResumeIQ</b>: AI Resume & Job-Match Analyzer &nbsp;·&nbsp; <code>Sentence Transformers</code> <code>FastAPI</code> <code>Docker</code></summary>

- 4-component weighted ATS scoring engine.
- Sentence Transformers (all-MiniLM-L6-v2) + NLP entity extraction.
- 81-skill taxonomy for gap analysis.
- Dockerized FastAPI + React app with PDF/DOCX parsing.

</details>

<details>
<summary><b>Plant Disease CNN</b> &nbsp;·&nbsp; <code>TensorFlow/Keras</code> &nbsp;·&nbsp; 99.19% validation accuracy</summary>

- TensorFlow/Keras CNN trained on 87,000+ leaf images across 38 classes.
- 99.19% validation accuracy with a custom augmentation pipeline.

</details>

<details>
<summary><b>SignBridge</b>: Real-Time ASL Alphabet Recognition &nbsp;·&nbsp; <code>MediaPipe</code> <code>PyTorch</code></summary>

- MediaPipe hand landmarks feeding a PyTorch classifier, 29 gesture classes in real time.
- CI/CD with GitHub Actions, Docker, AWS EC2.

</details>

## Education

**B.Tech Computer Science (Data Science)**, Galgotias University, 2024–2028.

## Activity

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/Chaitanaya25/Chaitanaya25/output/github-snake-dark.svg">
  <img src="https://raw.githubusercontent.com/Chaitanaya25/Chaitanaya25/output/github-snake.svg" alt="GitHub contribution graph animation" width="100%">
</picture>

<img src="assets/divider.svg" alt="" width="100%">
