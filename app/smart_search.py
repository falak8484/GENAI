
import json
from pathlib import Path

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

DATA_FILE = Path("data/records.json")


def load_records():
    with DATA_FILE.open("r", encoding="utf-8") as file:
        return json.load(file)


def search_records(query, limit=5):
    records = load_records()

    if not query.strip() or not records:
        return []

    documents = []

    for record in records:
        text = " ".join([
            record["cheat_sheet"],
            record["vulnerability"],
            record["recommended_control"],
            record["exact_parameter"],
            record["owasp_top10_category"]
        ])
        documents.append(text)

    vectorizer = TfidfVectorizer()
    document_vectors = vectorizer.fit_transform(documents)

    query_vector = vectorizer.transform([query])

    scores = cosine_similarity(
        query_vector,
        document_vectors
    ).flatten()

    ranked_indices = scores.argsort()[::-1]

    results = []

    for index in ranked_indices:
        if scores[index] > 0:
            result = records[index].copy()
            result["similarity_score"] = round(float(scores[index]), 4)
            results.append(result)

        if len(results) >= limit:
            break

    return results


if __name__ == "__main__":
    results = search_records("password security")

    for result in results:
        print(result["cheat_sheet"], result["similarity_score"])
