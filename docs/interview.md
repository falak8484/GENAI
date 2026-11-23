# OWASPShield – Interview Preparation

## 1. My 60-Second Project Pitch

OWASPShield is an AI-powered cybersecurity assistant that I developed using Python, FastAPI, Streamlit, ChromaDB and Google Gemini.

The main goal is to help cybersecurity students and beginner developers understand web application vulnerabilities and learn how to fix them.

It uses Retrieval-Augmented Generation, or RAG, to search cybersecurity documents and generate answers based on retrieved information. It also provides source citations and returns "I don't know" when sufficient supporting information is unavailable.

I also implemented AI agent workflows using LangGraph, including human approval before password hashing configuration checks. Other features include semantic search, VAPT finding mapping, API monitoring, response caching and automated testing.

I deployed the FastAPI backend on Render and used GitHub Actions for continuous integration.

## 2. Ten Likely Interview Questions

### Q1. What problem does OWASPShield solve?

Students and beginner developers often find cybersecurity documentation difficult to understand. OWASPShield makes security guidance easier to search, understand and apply through an AI-powered assistant.

### Q2. What is RAG?

RAG stands for Retrieval-Augmented Generation. First, the application searches relevant information from a knowledge base. Then it gives that information to an AI model to generate an answer.

For example, if someone asks how to store passwords securely, OWASPShield retrieves relevant password-storage guidance before generating its response.

### Q3. Why did you use ChromaDB?

ChromaDB is a vector database. It stores document embeddings and helps retrieve relevant content using semantic similarity rather than depending only on exact keyword matches.

### Q4. What are embeddings?

Embeddings are numerical representations of text. Text with similar meanings can have similar vector representations, helping the system find relevant information even when the wording is different.

### Q5. How does OWASPShield prevent unsupported answers?

The RAG pipeline checks whether relevant chunks were retrieved and whether the highest similarity score reaches the configured threshold of 0.65. If retrieval is insufficient, it returns exactly "I don't know".

This reduces unsupported answers, although it does not guarantee that every generated answer is correct.

### Q6. What was the hardest problem you faced?

One security finding can be covered by multiple overlapping cheat sheets. For example, password-related findings may involve authentication guidance as well as password-storage guidance.

The challenge is to retrieve all relevant information without losing important security details. Exact numerical values, such as memory requirements and iteration counts, must be preserved rather than guessed or casually paraphrased.

My approach is to retrieve relevant source chunks, keep their source metadata and use citations so the answer can be traced back to the original documentation.

The current implementation provides document and page citations. Precise source-line citations and guaranteed retrieval of every relevant cheat sheet are improvements still to be completed.

### Q7. What is LangGraph?

LangGraph is a framework for building stateful AI agent workflows. In OWASPShield, it helps route requests to the appropriate workflow and supports human approval before security tool execution.

### Q8. Why is human approval important?

Human approval keeps a person involved before an agent executes a security configuration check. The user can approve or reject the proposed action instead of allowing the agent to proceed automatically.

### Q9. How did you test OWASPShield?

I used Pytest for automated testing and Ruff for code quality. My project has 29 passing automated tests covering API endpoints, search, records, caching, input validation and prompt boundaries.

I also configured GitHub Actions to run automated checks and build the Docker image.

### Q10. What would you improve next?

I would improve multi-document retrieval, preserve exact security recommendations, introduce precise source-line citations, expand the knowledge base and add more retrieval evaluation metrics.

## 3. Important Technical Values

These values come from the project's local Password Storage Cheat Sheet.

| Algorithm | Source recommendation |
|---|---|
| Argon2id | One listed configuration: m=19456 KiB, t=2, p=1 |
| bcrypt | Minimum work factor: 10 |
| bcrypt | Maximum input: 72 bytes for most implementations |
| PBKDF2-HMAC-SHA256 | 600,000 iterations |
| PBKDF2-HMAC-SHA512 | 220,000 iterations |
| PBKDF2-HMAC-SHA1 | 1,400,000 iterations, legacy only |

Note: The application's current checker uses generic minimums. It does not distinguish PBKDF2 variants.

## 4. Honest Project Limitations

- Current RAG citations identify document title, source and page, not exact line ranges.
- Top-K retrieval does not guarantee that every relevant cheat sheet is retrieved.
- The in-memory cache is not persistent across application restarts.
- Prompt-boundary tests do not prove resistance to every prompt injection.
- The password checker does not validate every possible hashing parameter or algorithm-specific PBKDF2 setting.

## 5. Demo Checklist

- [ ] Open the Streamlit application.
- [ ] Demonstrate a cybersecurity question.
- [ ] Show a RAG answer with citations.
- [ ] Demonstrate an unsupported question returning "I don't know".
- [ ] Demonstrate semantic search.
- [ ] Open the LangGraph agent.
- [ ] Show human approval and rejection.
- [ ] Demonstrate a password hashing configuration check.
- [ ] Show the VAPT Finding Mapper.
- [ ] Open the live FastAPI documentation.
- [ ] Explain monitoring, caching and automated tests.

