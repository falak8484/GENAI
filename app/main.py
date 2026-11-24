
from __future__ import annotations

import json
import logging
from pathlib import Path
from typing import Optional

from fastapi import FastAPI, HTTPException, Query
from fastapi import Path as ApiPath
from langgraph.types import Command
from pydantic import BaseModel, Field

from app.cache import (
    get_cached_response,
    make_cache_key,
    set_cached_response,
)
from app.graph import agent_graph
from app.llm import generate_response
from app.monitoring import request_monitoring_middleware
from app.rag import ask_question
from app.smart_search import search_records
from app.vectorstore import (
    semantic_search,
    build_vectorstore,
    collection,
    EMBEDDED_FILE,
)

logging.basicConfig(level=logging.INFO)

logger = logging.getLogger("owaspshield")

app = FastAPI(
    title="OWASPShield API",
    description="API for OWASP security cheat sheet records",
    version="1.5"
)

# Enable request latency monitoring
app.middleware("http")(request_monitoring_middleware)


# Initialize vector database when the API starts
@app.on_event("startup")
def initialize_vectorstore():
    try:
        if EMBEDDED_FILE.exists() and collection.count() == 0:
            logger.info("Building OWASPShield vector database...")
            build_vectorstore()
        else:
            logger.info(
                "Vector database already initialized. Chunks: %s",
                collection.count()
            )
    except Exception:
        logger.exception("Vector database initialization failed.")
        raise


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


# Question request model
class Question(BaseModel):
    question: str = Field(max_length=4000)


# Chat request model
class ChatRequest(BaseModel):
    question: str = Field(max_length=4000)
    task: str = Field(default="explain", max_length=20)


# Prompt evaluation request model
class EvaluationRequest(BaseModel):
    question: str = Field(max_length=4000)
    prompt_version: str = Field(max_length=2)


# LangGraph agent request model
class AgentRequest(BaseModel):
    question: Optional[str] = Field(default=None, max_length=4000)
    config: Optional[dict] = None
    thread_id: str = Field(min_length=1, max_length=200)
    approved: Optional[bool] = None
    resume: bool = False


# Health check
@app.get("/health")
def health():
    return {
        "status": "healthy",
        "service": "OWASPShield"
    }


# Get records
@app.get("/records")
def get_records(
    limit: int = Query(default=10, ge=1, le=100)
):
    records = load_records()
    return records[:limit]


# Get record by ID
@app.get("/records/{id}")
def get_record(
    id: int = ApiPath(ge=1)
):
    records = load_records()

    for index, record in enumerate(records, start=1):
        if index == id:
            return record

    raise HTTPException(
        status_code=404,
        detail="Record not found"
    )


# Existing keyword-based search
@app.get("/search")
def search(
    q: str = Query(..., max_length=200)
):
    if not q.strip():
        raise HTTPException(
            status_code=400,
            detail="Search query cannot be empty"
        )

    return search_records(q)


# Semantic search using ChromaDB
@app.get("/search/semantic")
def search_semantic(
    q: str = Query(..., max_length=200)
):
    if not q.strip():
        raise HTTPException(
            status_code=400,
            detail="Search query cannot be empty"
        )

    try:
        results = semantic_search(q)

        return {
            "query": q,
            "total_results": len(results),
            "results": results
        }

    except Exception as e:
        logger.exception(
            "Semantic search failed: %s",
            type(e).__name__
        )

        raise HTTPException(
            status_code=502,
            detail="Unable to perform semantic search."
        )


# Strict RAG endpoint using OWASP documents
@app.post("/ask")
def ask(data: Question):

    if not data.question.strip():
        raise HTTPException(
            status_code=400,
            detail="Question cannot be empty"
        )

    try:
        result = ask_question(data.question)

        return {
            "question": data.question,
            "answer": result["answer"],
            "citations": result["citations"]
        }

    except Exception as e:
        logger.exception(
            "RAG failed: %s",
            type(e).__name__
        )

        raise HTTPException(
            status_code=502,
            detail="Unable to generate a RAG response."
        )


# Hybrid endpoint: RAG first, Gemini fallback
@app.post("/ask-hybrid")
def ask_hybrid(data: Question):

    if not data.question.strip():
        raise HTTPException(
            status_code=400,
            detail="Question cannot be empty"
        )

    try:
        # Step 1: Search the OWASP knowledge base
        result = ask_question(data.question)

        # Step 2: Return grounded RAG answer when available
        if result["answer"].strip().lower() != "i don't know":
            return {
                "question": data.question,
                "answer": result["answer"],
                "citations": result["citations"],
                "mode": "RAG"
            }

        # Step 3: Use Gemini when RAG cannot answer
        logger.info("RAG had no answer. Using Gemini fallback.")

        answer = generate_response(
            user_prompt=data.question,
            system_prompt=(
                "You are OWASPShield, a cybersecurity assistant. "
                "Answer cybersecurity questions using your general "
                "knowledge. Explain concepts in simple language and "
                "provide practical security recommendations. "
                "Be honest when you are uncertain. "
                "Never invent citations or sources. "
                "If a question is unrelated to cybersecurity, "
                "politely explain that you specialize in cybersecurity."
            )
        )

        if not answer or not answer.strip():
            raise ValueError("Gemini returned an empty response.")

        return {
            "question": data.question,
            "answer": answer.strip(),
            "citations": [],
            "mode": "AI"
        }

    except Exception as e:
        logger.exception(
            "Hybrid response failed: %s",
            type(e).__name__
        )

        raise HTTPException(
            status_code=502,
            detail="Unable to generate a response."
        )


# Existing questions endpoint
@app.post("/questions")
def ask_question_endpoint(data: Question):

    if not data.question.strip():
        raise HTTPException(
            status_code=400,
            detail="Question cannot be empty"
        )

    return {
        "message": "Question received successfully",
        "question": data.question
    }


# AI-powered chat endpoint with caching
@app.post("/chat")
def chat(data: ChatRequest):

    if not data.question.strip():
        raise HTTPException(
            status_code=400,
            detail="Question cannot be empty"
        )

    if data.task == "explain":
        task_prompt = load_prompt("explain_vulnerability.txt")

    elif data.task == "controls":
        task_prompt = load_prompt("recommend_controls.txt")

    else:
        raise HTTPException(
            status_code=400,
            detail="Invalid task. Choose 'explain' or 'controls'."
        )

    system_prompt = load_prompt("system.txt")

    user_prompt = task_prompt.format(
        question=data.question
    )

    cache_key = make_cache_key(
        question=user_prompt,
        task=data.task
    )

    cached_answer = get_cached_response(cache_key)

    if cached_answer is not None:
        logger.info(
            "llm_cache status=hit task=%s",
            data.task
        )

        return {
            "answer": cached_answer,
            "confidence": "Not calibrated",
            "follow_up": (
                "Would you like another example or "
                "more security recommendations?"
            )
        }

    logger.info(
        "llm_cache status=miss task=%s",
        data.task
    )

    try:
        answer = generate_response(
            user_prompt=user_prompt,
            system_prompt=system_prompt
        )

        if answer:
            set_cached_response(
                cache_key,
                answer
            )

        return {
            "answer": answer,
            "confidence": "Not calibrated",
            "follow_up": (
                "Would you like another example or "
                "more security recommendations?"
            )
        }

    except Exception as e:
        logger.exception(
            "LLM failed: %s",
            type(e).__name__
        )

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

    if data.prompt_version == "v1":
        filename = "prompt_v1.txt"

    elif data.prompt_version == "v2":
        filename = "prompt_v2.txt"

    else:
        raise HTTPException(
            status_code=400,
            detail="Invalid prompt version. Choose 'v1' or 'v2'."
        )

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
        logger.exception(
            "Evaluation failed: %s",
            type(e).__name__
        )

        raise HTTPException(
            status_code=502,
            detail="Unable to generate evaluation response."
        )


# LangGraph Agent endpoint
@app.post("/agent")
def run_langgraph_agent(data: AgentRequest):

    graph_config = {
        "configurable": {
            "thread_id": data.thread_id
        }
    }

    try:

        if data.resume:

            if data.approved is None:
                raise HTTPException(
                    status_code=400,
                    detail="Please provide approved as true or false."
                )

            result = agent_graph.invoke(
                Command(resume=data.approved),
                config=graph_config
            )

        else:

            if not data.question or not data.question.strip():
                raise HTTPException(
                    status_code=400,
                    detail="Question cannot be empty."
                )

            result = agent_graph.invoke(
                {
                    "question": data.question,
                    "config": data.config or {}
                },
                config=graph_config
            )

        interrupts = result.get("__interrupt__", [])

        if interrupts:
            return {
                "status": "approval_required",
                "thread_id": data.thread_id,
                "approval": interrupts[0].value
            }

        return {
            "status": "completed",
            "thread_id": data.thread_id,
            "tool_used": result.get("tool"),
            "result": result.get("result"),
            "history": result.get("history", [])
        }

    except HTTPException:
        raise

    except Exception as e:
        logger.exception(
            "Agent failed: %s",
            type(e).__name__
        )

        raise HTTPException(
            status_code=500,
            detail="Unable to execute the LangGraph agent."
        )
