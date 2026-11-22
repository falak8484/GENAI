
# app/graph.py

from typing import TypedDict

from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import END, START, StateGraph
from langgraph.types import interrupt

from app.rag import ask_question
from app.tools import password_hash_config_checker


# State shared between graph nodes
class AgentState(TypedDict, total=False):
    question: str
    config: dict
    tool: str
    approved: bool
    result: dict
    history: list


# Node 1: Decide which tool to use
def route_node(state: AgentState):

    question = state["question"].lower()

    checker_keywords = [
        "check config",
        "check configuration",
        "hashing config",
        "hashing configuration",
        "password hash config"
    ]

    if any(word in question for word in checker_keywords):
        return {"tool": "password_hash_config_checker"}

    return {"tool": "rag_search"}


# Node 2: Ask for human approval
def approval_node(state: AgentState):

    decision = interrupt({
        "message": "Approval required before checking password configuration.",
        "tool": "password_hash_config_checker",
        "configuration": state.get("config")
    })

    return {"approved": bool(decision)}


# Node 3: Run password checker
def checker_node(state: AgentState):

    result = password_hash_config_checker(
        state.get("config", {})
    )

    return {"result": result}


# Node 4: Run existing RAG search
def rag_node(state: AgentState):

    result = ask_question(state["question"])

    return {
        "result": {
            "answer": result["answer"],
            "citations": result["citations"]
        }
    }


# Node 5: Handle rejected approval
def rejected_node(state: AgentState):

    return {
        "result": {
            "status": "REJECTED",
            "message": "Human approval was not granted. Tool was not executed."
        }
    }


# Node 6: Save conversation history
def memory_node(state: AgentState):

    history = list(state.get("history", []))

    history.append({
        "question": state["question"],
        "tool_used": state["tool"],
        "result": state["result"]
    })

    return {"history": history}


# Decide the next node
def choose_tool(state: AgentState):

    return state["tool"]


def check_approval(state: AgentState):

    if state.get("approved"):
        return "run_checker"

    return "rejected"


# Build graph
builder = StateGraph(AgentState)

builder.add_node("route", route_node)
builder.add_node("approval", approval_node)
builder.add_node("checker", checker_node)
builder.add_node("rag", rag_node)
builder.add_node("rejected", rejected_node)
builder.add_node("memory", memory_node)

builder.add_edge(START, "route")

builder.add_conditional_edges(
    "route",
    choose_tool,
    {
        "password_hash_config_checker": "approval",
        "rag_search": "rag"
    }
)

builder.add_conditional_edges(
    "approval",
    check_approval,
    {
        "run_checker": "checker",
        "rejected": "rejected"
    }
)

builder.add_edge("checker", "memory")
builder.add_edge("rag", "memory")
builder.add_edge("rejected", "memory")
builder.add_edge("memory", END)


# MemorySaver remembers state between requests
memory = MemorySaver()

agent_graph = builder.compile(checkpointer=memory)
