
import json
import os
import time
from pathlib import Path

from dotenv import load_dotenv
from google import genai
from google.genai import types

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")

CHUNKS_FILE = BASE_DIR / "data" / "chunks.json"
EMBEDDED_FILE = BASE_DIR / "data" / "embedded_chunks.json"

EMBEDDING_MODEL = "gemini-embedding-001"
BATCH_SIZE = 20


def get_client():
    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key or api_key == "your_gemini_api_key_here":
        raise ValueError("Please configure GEMINI_API_KEY in .env")

    return genai.Client(api_key=api_key)


def embed_texts(texts, task_type="RETRIEVAL_DOCUMENT"):

    if not texts:
        return []

    client = get_client()
    all_embeddings = []

    for start in range(0, len(texts), BATCH_SIZE):
        batch = texts[start:start + BATCH_SIZE]

        response = client.models.embed_content(
            model=EMBEDDING_MODEL,
            contents=batch,
            config=types.EmbedContentConfig(
                task_type=task_type
            )
        )

        all_embeddings.extend(
            [embedding.values for embedding in response.embeddings]
        )

    return all_embeddings


def embed_query(question):

    vectors = embed_texts(
        [question],
        task_type="RETRIEVAL_QUERY"
    )

    return vectors[0]


def embed_documents(
    chunks_file=CHUNKS_FILE,
    embedded_file=EMBEDDED_FILE
):
    """Generate document embeddings and save progress separately."""

    chunks_file = Path(chunks_file)
    embedded_file = Path(embedded_file)

    with chunks_file.open("r", encoding="utf-8") as file:
        chunks = json.load(file)

    if not chunks:
        raise ValueError("No chunks found. Run app.chunking first.")

    # Load previously saved embeddings for this dataset.
    if embedded_file.exists():
        with embedded_file.open("r", encoding="utf-8") as file:
            saved_chunks = json.load(file)
    else:
        saved_chunks = []

    saved_embeddings = {
        chunk["id"]: chunk
        for chunk in saved_chunks
        if "embedding" in chunk
    }

    remaining_chunks = [
        chunk for chunk in chunks
        if chunk["id"] not in saved_embeddings
    ]

    print("Total chunks:", len(chunks))
    print("Already embedded:", len(saved_embeddings))
    print("Remaining:", len(remaining_chunks))

    if not remaining_chunks:
        print("All chunks are already embedded!")
        return

    client = get_client()

    total_batches = (
        len(remaining_chunks) + BATCH_SIZE - 1
    ) // BATCH_SIZE

    embedded_file.parent.mkdir(parents=True, exist_ok=True)

    for start in range(0, len(remaining_chunks), BATCH_SIZE):

        batch_number = start // BATCH_SIZE + 1
        batch = remaining_chunks[start:start + BATCH_SIZE]

        print(f"Embedding batch {batch_number} of {total_batches}...")

        response = client.models.embed_content(
            model=EMBEDDING_MODEL,
            contents=[chunk["text"] for chunk in batch],
            config=types.EmbedContentConfig(
                task_type="RETRIEVAL_DOCUMENT"
            )
        )

        if len(response.embeddings) != len(batch):
            raise ValueError("Embedding count does not match batch size.")

        for chunk, embedding in zip(batch, response.embeddings):
            saved_embeddings[chunk["id"]] = {
                **chunk,
                "embedding": embedding.values
            }

        # Save progress after every successful batch.
        completed_chunks = [
            saved_embeddings[chunk["id"]]
            for chunk in chunks
            if chunk["id"] in saved_embeddings
        ]

        with embedded_file.open("w", encoding="utf-8") as file:
            json.dump(completed_chunks, file)

        print(
            "Saved progress:",
            len(completed_chunks),
            "/",
            len(chunks)
        )

        # Stay below the free-tier per-minute limit.
        if batch_number % 4 == 0 and batch_number < total_batches:
            print("Waiting 65 seconds to respect the API rate limit...")
            time.sleep(65)

    print("\nDocument embedding completed!")
    print("Total embedded chunks:", len(saved_embeddings))
    print(
        "Vector dimensions:",
        len(next(iter(saved_embeddings.values()))["embedding"])
    )
    print("Saved to:", embedded_file)


if __name__ == "__main__":

    try:
        embed_documents()

    except Exception as error:  # noqa: BLE001 - top-level error handler
        print("Embedding failed:", type(error).__name__, error)
