# OWASPShield

## Project Overview

OWASPShield is a beginner-friendly cybersecurity awareness and security assistance project designed to help users understand common web application security risks.

## Product

A cybersecurity assistant that provides information about common web security vulnerabilities and basic security checks.

## Target User

Students, beginner developers, and individuals interested in learning web application security.

## Problem

Many beginners are unaware of common web application vulnerabilities and struggle to understand how to identify basic security risks.

## Data Source

OWASP Top 10 documentation and manually prepared sample security questions and rules.

## Project Goal

To make basic web security knowledge easier to understand through a simple Python-based interactive application.

## Features

- Search cybersecurity cheat sheet records.
- Search records using semantic search.
- Ask cybersecurity questions through a RAG-based assistant.
- Retrieve relevant information from embedded OWASP security documents.
- Generate answers with source citations.
- Return `I don't know` when the retrieved information does not support an answer.

## RAG-Based Question Answering

OWASPShield uses Retrieval-Augmented Generation (RAG).

1. The user's question is converted into an embedding.
2. Relevant document chunks are retrieved using vector similarity search.
3. Retrieved chunks are passed to the language model as context.
4. The model generates an answer using the retrieved information.
5. Citations identify the sources used for the answer.

### API Endpoint

`POST /ask`

Example request:

```json
{
  "question": "How should I store user passwords securely?"
}
```

The response contains:
- The original question
- The generated answer
- Citations containing document titles and source filenames

If the retrieved information is insufficient, the API returns exactly `I don't know`.

## Retrieval Evaluation (Day 8 - S2)

Two retrieval configurations were evaluated using a dataset of 15 questions. Keyword coverage measures how many expected keywords were found in the retrieved chunks for the 14 answerable questions. Q6 is an abstention test and is excluded from the keyword coverage average.

| Configuration | Chunk Size | Overlap | Top-K | Average Keyword Coverage |
|---|---:|---:|---:|---:|
| A | 500 | 75 | 3 | 64.29% |
| B | 1000 | 150 | 5 | 77.38% |

### Selected Configuration

**Configuration B** achieved the higher average keyword coverage of **77.38%**.

Selected settings:
- Chunk size: 1000
- Overlap: 150
- Top-K: 5

These results compare the two complete configurations; they do not isolate the effect of each individual parameter.

### Abstention Test

The unsupported AWS CloudTrail question (Q6) was tested through the `/ask` API.

Expected response: `I don't know`

Actual response: `I don't know`

The API returned an empty citations list for this question.

## How to Run

### 1. Activate virtual environment

```bash
source .venv/bin/activate
```

### 2. Install dependencies

```bash
python -m pip install -r requirements.txt
```

### 3. Start the FastAPI server

```bash
uvicorn app.main:app --reload
```

### 4. Open API documentation

Visit: http://127.0.0.1:8000/docs

### 5. Run data analysis

```bash
python -m analysis.explore
```

### 6. Run smart search

```bash
python -m app.smart_search
```

### 7. Run retrieval evaluation

```bash
python -m eval.run_eval
```

## AI Agent and LangGraph

OWASPShield includes an AI agent that can select and execute cybersecurity tools.

### S1 – Custom Agent and Security Tool

- `app/tools.py` – Password hashing configuration checker.
- `app/agent_loop.py` – Hand-written agent that selects between RAG search and the password configuration checker.
- Checks Argon2id, bcrypt, and PBKDF2 configurations against the project's OWASP minimum requirements.

### S2 – LangGraph Agent

- `app/graph.py` – Implements the agent workflow using LangGraph.
- Uses conditional routing to select the appropriate tool.
- Includes human approval before password configuration checks.
- Supports approval and rejection.
- Uses LangGraph MemorySaver to maintain conversation state.
- Stores conversation history using thread IDs.

### Agent API

**Endpoint:** `POST /agent`

The agent supports two workflows:

1. Cybersecurity questions are routed to the RAG search system and returned with citations.
2. Password hashing configuration checks require human approval before execution.

**Example: Start an agent request**

```json
{
  "question": "Check this password hashing config",
  "config": {
    "algorithm": "bcrypt",
    "work_factor": 8,
    "max_password_bytes": 72
  },
  "thread_id": "test-agent-001",
  "resume": false
}
```

**Example: Approve execution**

```json
{
  "thread_id": "test-agent-001",
  "resume": true,
  "approved": true
}
```

**Example: Reject execution**

```json
{
  "thread_id": "test-agent-002",
  "resume": true,
  "approved": false
}
```

### Technologies

- Python
- FastAPI
- LangGraph
- ChromaDB
- Google Gemini
- OWASP security documentation
