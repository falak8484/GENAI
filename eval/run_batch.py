
import json
import re
import time
from pathlib import Path
from datetime import datetime

from app.llm import generate_response


BASE_DIR = Path(__file__).resolve().parent.parent
EVAL_DIR = BASE_DIR / "eval"
QUESTIONS_FILE = BASE_DIR / "docs" / "questions.md"
OUTPUT_FILE = EVAL_DIR / "batch_missing_results.json"

# Only tests that are still missing.
MISSING_TESTS = [
    ("v1", 5),
    ("v2", 5),
    ("v2", 6),
    ("v1", 7),
    ("v2", 7),
    ("v2", 8),
    ("v1", 9),
    ("v2", 9),
    ("v1", 10),
    ("v2", 10),
]


def load_questions():
    content = QUESTIONS_FILE.read_text(encoding="utf-8")

    matches = re.findall(
        r"^### Q(\d+)\.\s*(.+)$",
        content,
        flags=re.MULTILINE
    )

    if len(matches) != 10:
        raise ValueError(
            f"Expected 10 questions, found {len(matches)}."
        )

    return {
        int(number): question.strip()
        for number, question in matches
    }


def load_previous_results():
    if OUTPUT_FILE.exists():
        data = json.loads(OUTPUT_FILE.read_text(encoding="utf-8"))
        return data.get("results", [])

    return []


def save_results(results):
    data = {
        "project": "OWASPShield",
        "generated_at": datetime.now().isoformat(),
        "total_missing_tests": len(MISSING_TESTS),
        "results": results
    }

    OUTPUT_FILE.write_text(
        json.dumps(data, indent=4, ensure_ascii=False),
        encoding="utf-8"
    )


def main():
    questions = load_questions()

    prompt_files = {
        "v1": EVAL_DIR / "prompt_v1.txt",
        "v2": EVAL_DIR / "prompt_v2.txt"
    }

    results = load_previous_results()

    print("\n===== OWASPSHIELD MISSING TESTS =====")

    for version, question_number in MISSING_TESTS:

        # Do not repeat tests that already succeeded.
        already_successful = any(
            item["prompt_version"] == version
            and item["question_number"] == question_number
            and item["status"] == "success"
            for item in results
        )

        if already_successful:
            print(f"Skipping {version.upper()} Q{question_number}: already completed.")
            continue

        question = questions[question_number]
        prompt_path = prompt_files[version]

        system_prompt = prompt_path.read_text(encoding="utf-8")

        print(f"\nTesting {version.upper()} - Q{question_number}")
        print(f"Question: {question}")

        result = {
            "prompt_version": version,
            "question_number": question_number,
            "question": question,
            "status": "success",
            "answer": None,
            "error": None
        }

        try:
            answer = generate_response(
                user_prompt=question,
                system_prompt=system_prompt
            )

            result["answer"] = answer
            print("Status: SUCCESS")

        except Exception as error:
            result["status"] = "failed"
            result["error"] = f"{type(error).__name__}: {error}"

            print(f"Status: FAILED - {type(error).__name__}")

        # Replace an earlier failed attempt for this test.
        results = [
            item for item in results
            if not (
                item["prompt_version"] == version
                and item["question_number"] == question_number
            )
        ]

        results.append(result)
        save_results(results)

        # Stop immediately if the provider quota is exhausted.
        error_text = result["error"] or ""

        if any(word in error_text.upper() for word in [
            "RESOURCE_EXHAUSTED",
            "QUOTA",
            "429"
        ]):
            print("\nGemini quota reached. Progress has been saved.")
            break

        time.sleep(2)

    successful = sum(
        1 for item in results
        if item["status"] == "success"
    )

    print("\n===== EVALUATION SUMMARY =====")
    print(f"Successful missing tests: {successful}")
    print(f"Results saved to: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
