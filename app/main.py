
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import json
from pathlib import Path

from app.smart_search import search_records

app = FastAPI(
    title="OWASPShield API",
    description="API for OWASP security cheat sheet records",
    version="1.0"
)

DATA_FILE = Path(__file__).resolve().parents[1] / "data" / "records.json"


def load_records():
    with open(DATA_FILE, "r", encoding="utf-8") as file:
        return json.load(file)


class Question(BaseModel):
    question: str


@app.get("/health")
def health():
    return {"status": "healthy", "service": "OWASPShield"}


@app.get("/records")
def get_records(limit: int = 10):
    records = load_records()

    if limit < 1:
        raise HTTPException(status_code=400, detail="Limit must be at least 1")

    return records[:limit]


@app.get("/records/{id}")
def get_record(id: int):
    records = load_records()

    for index, record in enumerate(records, start=1):
        if index == id:
            return record

    raise HTTPException(status_code=404, detail="Record not found")


@app.get("/search")
def search(q: str):
    if not q.strip():
        raise HTTPException(status_code=400, detail="Search query cannot be empty")

    return search_records(q)


@app.post("/questions")
def ask_question(data: Question):
    if not data.question.strip():
        raise HTTPException(status_code=400, detail="Question cannot be empty")

    return {
        "message": "Question received successfully",
        "question": data.question
    }
