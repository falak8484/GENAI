
from app.llm import generate_response
from app.vectorstore import semantic_search

# Minimum similarity required to use retrieved information
MIN_SIMILARITY = 0.65


SYSTEM_PROMPT = """
You are OWASPShield, a cybersecurity assistant.

Rules:
1. Answer using ONLY the provided OWASP context.
2. Do not use outside knowledge or invent information.
3. If the context does not contain enough information,
   respond exactly: I don't know
4. Include citations such as [1] or [2] for factual claims.
5. Use only the citation numbers provided in the context.
6. Explain cybersecurity concepts in simple language.
7. Never invent sources or page numbers.
"""


def ask_question(question, top_k=5):

    if not question or not question.strip():
        raise ValueError("Question cannot be empty.")

    # Step 1: Retrieve relevant chunks from ChromaDB
    retrieved_chunks = semantic_search(
        question,
        limit=top_k
    )

    # Step 2: Check whether relevant information was found
    if not retrieved_chunks:
        return {
            "answer": "I don't know",
            "citations": []
        }

    if retrieved_chunks[0]["score"] < MIN_SIMILARITY:
        return {
            "answer": "I don't know",
            "citations": []
        }

    # Step 3: Prepare context with citation numbers
    context_parts = []
    citations = []

    for index, chunk in enumerate(retrieved_chunks, start=1):

        citation = {
            "id": index,
            "title": chunk["title"],
            "source": chunk["source"],
            "page": chunk["page"]
        }

        citations.append(citation)

        context_parts.append(
            f"""
[{index}]
Title: {chunk['title']}
Source: {chunk['source']}
Page: {chunk['page']}

Content:
{chunk['text']}
"""
        )

    context = "\n\n".join(context_parts)

    # Step 4: Prepare the prompt
    user_prompt = f"""
Answer the following question using the provided context.

QUESTION:
{question}

OWASP CONTEXT:
{context}

Remember:
- Use citations like [1] and [2].
- If the context does not answer the question,
  respond exactly: I don't know
"""

    # Step 5: Generate the grounded answer
    answer = generate_response(
        user_prompt=user_prompt,
        system_prompt=SYSTEM_PROMPT
    )

    answer = answer.strip()

    # Step 6: Remove citations if the model does not know
    if answer.lower().rstrip(".") == "i don't know":
        return {
            "answer": "I don't know",
            "citations": []
        }

    return {
        "answer": answer,
        "citations": citations
    }
