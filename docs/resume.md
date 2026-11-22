# OWASPShield – AI-Powered Cybersecurity Assistant

**Technologies:** Python, FastAPI, Streamlit, LangGraph, ChromaDB, Gemini, Groq, Docker, Pytest, GitHub Actions

- Developed an AI-powered cybersecurity assistant using Python and FastAPI, implementing Retrieval-Augmented Generation (RAG), ChromaDB vector search, and source-cited answers with similarity-based abstention for unsupported questions.

- Implemented custom and LangGraph-based agent workflows with human-in-the-loop approval, including defensive password hashing configuration checks for Argon2id, bcrypt, and PBKDF2.

- Added API input validation, request and LLM usage monitoring, and an in-memory response cache; achieved approximately 99.98% lower latency for a repeated cached request in a local test, with 29 automated tests passing and CI/CD through GitHub Actions.
