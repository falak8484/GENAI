
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import json
from pathlib import Path

from app.smart_search import search_records
from app.llm import generate_response


app = FastAPI(
    title="OWASPShield API",
    description="API for OWASP security cheat sheet records",
    version="1.2"
)


BASE_DIR = Path(__file__).resolve().parent.parent
DATA_FILE = BASE_DIR / "data" / "records.json"
PROMPT_DIR = BASE_DIR / "prompts"
EVAL_DIR = BASE_DIR / "eval"


# Load cybersecurity records
def load_records():
    with open(DATA_FILE, "r", encoding="utf-8") as file:
        return json.load(file)


# Load prompt files
def load_prompt(filename):
    prompt_path = PROMPT_DIR / filename

    try:
        with open(prompt_path, "r", encoding="utf-8") as file:
            return file.read()
    except FileNotFoundError:
        raise HTTPException(
            status_code=500,
            detail=f"Prompt file not found: {filename}"
        )


# Existing question request model
class Question(BaseModel):
    question: str


# Chat request model
class ChatRequest(BaseModel):
    question: str
    task: str = "explain"


# Prompt evaluation request model
class EvaluationRequest(BaseModel):
    question: str
    prompt_version: str


# Health check
@app.get("/health")
def health():
    return {
        "status": "healthy",
        "service": "OWASPShield"
    }


# Get records
@app.get("/records")
def get_records(limit: int = 10):
    records = load_records()

    if limit < 1:
        raise HTTPException(
            status_code=400,
            detail="Limit must be at least 1"
        )

    return records[:limit]


# Get record by ID
@app.get("/records/{id}")
def get_record(id: int):
    records = load_records()

    for index, record in enumerate(records, start=1):
        if index == id:
            return record

    raise HTTPException(
        status_code=404,
        detail="Record not found"
    )


# Search records
@app.get("/search")
def search(q: str):
    if not q.strip():
        raise HTTPException(
            status_code=400,
            detail="Search query cannot be empty"
        )

    return search_records(q)


# Existing questions endpoint
@app.post("/questions")
def ask_question(data: Question):
    if not data.question.strip():
        raise HTTPException(
            status_code=400,
            detail="Question cannot be empty"
        )

    return {
        "message": "Question received successfully",
        "question": data.question
    }


# AI-powered chat endpoint
@app.post("/chat")
def chat(data: ChatRequest):

    if not data.question.strip():
        raise HTTPException(
            status_code=400,
            detail="Question cannot be empty"
        )

    # Select the task-specific prompt
    if data.task == "explain":
        task_prompt = load_prompt("explain_vulnerability.txt")

    elif data.task == "controls":
        task_prompt = load_prompt("recommend_controls.txt")

    else:
        raise HTTPException(
            status_code=400,
            detail="Invalid task. Choose 'explain' or 'controls'."
        )

    # Load the main system prompt
    system_prompt = load_prompt("system.txt")

    # Insert the user's question into the selected prompt
    user_prompt = task_prompt.format(
        question=data.question
    )

    try:
        answer = generate_response(
            user_prompt=user_prompt,
            system_prompt=system_prompt
        )

        return {
            "answer": answer,
            "confidence": "Not calibrated",
            "follow_up": "Would you like another example or more security recommendations?"
        }

    except Exception as e:
        print(f"LLM ERROR: {type(e).__name__}: {e}")

        raise HTTPException(
            status_code=502,
            detail="Unable to generate a response from the LLM provider."
        )


# Prompt evaluation endpoint
@app.post("/evaluate")
def evaluate_prompt(data: EvaluationRequest):

    if not data.question.strip():
        raise HTTPException(
            status_code=400,
            detail="Question cannot be empty"
        )

    # Select prompt version
    if data.prompt_version == "v1":
        filename = "prompt_v1.txt"

    elif data.prompt_version == "v2":
        filename = "prompt_v2.txt"

    else:
        raise HTTPException(
            status_code=400,
            detail="Invalid prompt version. Choose 'v1' or 'v2'."
        )

    # Load selected evaluation prompt
    prompt_path = EVAL_DIR / filename

    try:
        with open(prompt_path, "r", encoding="utf-8") as file:
            system_prompt = file.read()

        answer = generate_response(
            user_prompt=data.question,
            system_prompt=system_prompt
        )

        return {
            "prompt_version": data.prompt_version,
            "question": data.question,
            "answer": answer
        }

    except Exception as e:
        print(f"EVALUATION ERROR: {type(e).__name__}: {e}")

        raise HTTPException(
            status_code=502,
            detail="Unable to generate evaluation response."
        )
