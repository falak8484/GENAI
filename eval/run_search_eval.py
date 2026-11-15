
from pathlib import Path

from app.embed import embed_texts
from app.vectorstore import collection

BASE_DIR = Path(__file__).resolve().parent.parent
OUTPUT_FILE = BASE_DIR / "eval" / "search_results.md"

questions = [
    "How should passwords be stored securely?",
    "Why should each password have a unique salt?",
    "What is the purpose of a password pepper?",
    "How does Argon2id protect stored passwords?",
    "How can applications prevent brute-force login attacks?",
    "Why is multifactor authentication important?",
    "How do parameterized queries prevent SQL injection?",
    "What should developers do when table names must be selected dynamically?",
    "Why should database accounts follow least privilege?",
    "How can applications protect passwords during transmission?"
]

print("Generating embeddings for 10 questions...")

query_vectors = embed_texts(
    questions,
    task_type="RETRIEVAL_QUERY"
)

print("Searching ChromaDB...")

results = collection.query(
    query_embeddings=query_vectors,
    n_results=3,
    include=["documents", "metadatas", "distances"]
)

report = ["# OWASPShield Semantic Search Results\n"]

for index, question in enumerate(questions):
    report.append(f"## Question {index + 1}: {question}\n")

    for rank in range(len(results["ids"][index])):
        metadata = results["metadatas"][index][rank]
        distance = results["distances"][index][rank]
        similarity = 1 - distance

        report.append(
            f"**Hit {rank + 1}:** {metadata['title']}\n"
            f"- Source: {metadata['source']}\n"
            f"- Page: {metadata['page']}\n"
            f"- Similarity score: {similarity:.4f}\n"
        )

        report.append(
            f"- Retrieved text: {results['documents'][index][rank]}\n"
        )

    report.append("---\n")

OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
OUTPUT_FILE.write_text("\n".join(report), encoding="utf-8")

print("Evaluation completed!")
print("Questions tested:", len(questions))
print("Results saved to:", OUTPUT_FILE)
