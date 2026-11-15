
import json
from pathlib import Path

import chromadb

from app.embed import embed_query

BASE_DIR = Path(__file__).resolve().parent.parent
EMBEDDED_FILE = BASE_DIR / "data" / "embedded_chunks.json"
CHROMA_DIR = BASE_DIR / "data" / "chroma_db"

client = chromadb.PersistentClient(path=str(CHROMA_DIR))

collection = client.get_or_create_collection(
    name="owasp_chunks",
    metadata={"hnsw:space": "cosine"}
)


def build_vectorstore():
    with open(EMBEDDED_FILE, "r", encoding="utf-8") as file:
        chunks = json.load(file)

    for start in range(0, len(chunks), 100):
        batch = chunks[start:start + 100]

        collection.upsert(
            ids=[chunk["id"] for chunk in batch],
            embeddings=[chunk["embedding"] for chunk in batch],
            documents=[chunk["text"] for chunk in batch],
            metadatas=[
                {
                    "source": chunk["source"],
                    "page": str(chunk["page"]) if chunk["page"] is not None else "N/A",
                    "title": chunk["title"]
                }
                for chunk in batch
            ]
        )

    print("Vector database created successfully!")
    print("Total indexed chunks:", collection.count())


def semantic_search(query, limit=5):
    query_vector = embed_query(query)

    results = collection.query(
        query_embeddings=[query_vector],
        n_results=limit,
        include=["documents", "metadatas", "distances"]
    )

    matches = []

    for i in range(len(results["ids"][0])):
        metadata = results["metadatas"][0][i]

        matches.append({
            "title": metadata["title"],
            "source": metadata["source"],
            "page": None if metadata["page"] == "N/A" else metadata["page"],
            "text": results["documents"][0][i],
            "score": round(1 - results["distances"][0][i], 4)
        })

    return matches


if __name__ == "__main__":
    build_vectorstore()
