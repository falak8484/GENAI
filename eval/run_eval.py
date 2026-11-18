
import json
import math
from pathlib import Path

from app.embed import embed_texts

BASE_DIR = Path(__file__).resolve().parent.parent
EVAL_FILE = BASE_DIR / "eval" / "eval_set.json"

CONFIGS = {
    "config_a": {
        "chunks_file": BASE_DIR / "data/experiments/config_a/embedded_chunks.json",
        "top_k": 3,
        "chunk_size": 500,
        "overlap": 75,
    },
    "config_b": {
        "chunks_file": BASE_DIR / "data/experiments/config_b/embedded_chunks.json",
        "top_k": 5,
        "chunk_size": 1000,
        "overlap": 150,
    },
}


def cosine_similarity(a, b):
    dot_product = sum(x * y for x, y in zip(a, b))
    norm_a = math.sqrt(sum(x * x for x in a))
    norm_b = math.sqrt(sum(y * y for y in b))

    if norm_a == 0 or norm_b == 0:
        return 0.0

    return dot_product / (norm_a * norm_b)


def evaluate_config(config_name, config, questions, query_vectors):
    with open(config["chunks_file"], "r", encoding="utf-8") as file:
        chunks = json.load(file)

    results = []
    keyword_scores = []

    for question, query_vector in zip(questions, query_vectors):
        scored_chunks = []

        for chunk in chunks:
            score = cosine_similarity(
                query_vector,
                chunk["embedding"]
            )

            scored_chunks.append({
                "id": chunk["id"],
                "title": chunk["title"],
                "source": chunk["source"],
                "page": chunk["page"],
                "text": chunk["text"],
                "similarity": round(score, 4),
            })

        scored_chunks.sort(
            key=lambda item: item["similarity"],
            reverse=True
        )

        top_chunks = scored_chunks[:config["top_k"]]

        expected_keywords = question["expected_keywords"]

        combined_text = " ".join(
            chunk["text"] for chunk in top_chunks
        ).lower()

        matched_keywords = [
            keyword
            for keyword in expected_keywords
            if keyword.lower() in combined_text
        ]

        if expected_keywords:
            keyword_coverage = (
                len(matched_keywords) / len(expected_keywords)
            )
            keyword_scores.append(keyword_coverage)
        else:
            keyword_coverage = None

        results.append({
            "id": question["id"],
            "question": question["question"],
            "expected_behavior": question["expected_behavior"],
            "matched_keywords": matched_keywords,
            "expected_keywords": expected_keywords,
            "keyword_coverage": (
                round(keyword_coverage, 4)
                if keyword_coverage is not None else None
            ),
            "top_results": top_chunks,
            "abstention_assessment": (
                "manual_review_required"
                if question["expected_behavior"] == "abstain"
                else "not_applicable"
            ),
        })

    average_coverage = (
        sum(keyword_scores) / len(keyword_scores)
        if keyword_scores else 0
    )

    output = {
        "configuration": config_name,
        "settings": {
            "chunk_size": config["chunk_size"],
            "overlap": config["overlap"],
            "top_k": config["top_k"],
        },
        "total_questions": len(questions),
        "answer_questions": len(keyword_scores),
        "average_keyword_coverage": round(average_coverage, 4),
        "results": results,
    }

    output_dir = BASE_DIR / "eval" / "results" / config_name
    output_dir.mkdir(parents=True, exist_ok=True)

    output_file = output_dir / "results.json"

    with open(output_file, "w", encoding="utf-8") as file:
        json.dump(output, file, indent=4, ensure_ascii=False)

    print(f"\n{config_name.upper()} completed")
    print("Chunk size:", config["chunk_size"])
    print("Overlap:", config["overlap"])
    print("Top K:", config["top_k"])
    print("Average keyword coverage:", round(average_coverage * 100, 2), "%")
    print("Saved to:", output_file)


def main():
    with open(EVAL_FILE, "r", encoding="utf-8") as file:
        questions = json.load(file)

    print("Total evaluation questions:", len(questions))
    print("\nGenerating query embeddings...")

    query_vectors = embed_texts(
        [item["question"] for item in questions],
        task_type="RETRIEVAL_QUERY"
    )

    print("Query embeddings generated:", len(query_vectors))

    for config_name, config in CONFIGS.items():
        evaluate_config(
            config_name,
            config,
            questions,
            query_vectors
        )

    print("\nBoth configurations evaluated successfully!")


if __name__ == "__main__":
    main()
