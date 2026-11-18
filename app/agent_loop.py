
# app/agent_loop.py

from app.rag import ask_question
from app.tools import password_hash_config_checker


def run_agent(question: str, config: dict = None) -> dict:
    """
    A simple hand-written agent.

    It decides whether to use:
    1. Password hash configuration checker
    2. OWASPShield RAG search
    """

    if not question or not question.strip():
        return {
            "tool_used": None,
            "answer": "Please enter a question."
        }

    question_lower = question.lower()

    # Tool 1: Password hashing configuration checker
    if any(word in question_lower for word in [
        "check config",
        "check configuration",
        "hashing config",
        "hashing configuration",
        "password hash config"
    ]):

        if config is None:
            return {
                "tool_used": "password_hash_config_checker",
                "answer": "Please provide the password-hashing configuration."
            }

        result = password_hash_config_checker(config)

        return {
            "tool_used": "password_hash_config_checker",
            "answer": result
        }

    # Tool 2: Existing OWASPShield RAG search
    result = ask_question(question)

    return {
        "tool_used": "rag_search",
        "answer": result["answer"],
        "citations": result["citations"]
    }
