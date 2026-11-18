import json
import uuid
from datetime import datetime
from pathlib import Path

import requests
import streamlit as st


# CONFIGURATION

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
FEEDBACK_FILE = DATA_DIR / "feedback.json"
API_URL = "http://127.0.0.1:8000"

st.set_page_config(
    page_title="OWASPShield",
    page_icon="🛡️",
    layout="wide"
)


# DESIGN

st.markdown("""
<style>
.block-container {
    max-width: 1100px;
    padding-top: 2rem;
}
.main-title {
    font-size: 2.4rem;
    font-weight: 750;
    color: #9f1239;
}
.subtitle {
    color: #777;
    margin-bottom: 25px;
}
.feature-card {
    background: #fff7f7;
    border: 1px solid #f3d5d9;
    padding: 18px;
    border-radius: 12px;
    margin-bottom: 15px;
}
</style>
""", unsafe_allow_html=True)


# SESSION STATE

if "messages" not in st.session_state:
    st.session_state.messages = []

if "thread_id" not in st.session_state:
    st.session_state.thread_id = str(uuid.uuid4())

if "pending_agent" not in st.session_state:
    st.session_state.pending_agent = None


# API HELPERS

def api_post(endpoint, payload):
    try:
        response = requests.post(
            f"{API_URL}{endpoint}",
            json=payload,
            timeout=120
        )
        response.raise_for_status()
        return response.json()
    except requests.RequestException as error:
        st.error(f"API request failed: {error}")
        return None


def api_get(endpoint, params=None):
    try:
        response = requests.get(
            f"{API_URL}{endpoint}",
            params=params,
            timeout=60
        )
        response.raise_for_status()
        return response.json()
    except requests.RequestException as error:
        st.error(f"API request failed: {error}")
        return None


# FEEDBACK

def save_feedback(question, answer, mode, rating):
    DATA_DIR.mkdir(parents=True, exist_ok=True)

    feedback = []

    if FEEDBACK_FILE.exists():
        try:
            with open(FEEDBACK_FILE, "r", encoding="utf-8") as file:
                feedback = json.load(file)
        except (json.JSONDecodeError, OSError):
            feedback = []

    feedback.append({
        "question": question,
        "answer": answer,
        "mode": mode,
        "rating": rating,
        "timestamp": datetime.now().isoformat()
    })

    with open(FEEDBACK_FILE, "w", encoding="utf-8") as file:
        json.dump(feedback, file, indent=4, ensure_ascii=False)


# CITATIONS

def show_citations(citations):
    if not citations:
        st.caption("No citations available.")
        return

    with st.expander(f"📚 Sources ({len(citations)})"):
        for citation in citations:
            st.markdown(
                f"**[{citation.get('id', '?')}] "
                f"{citation.get('title', 'Untitled source')}**"
            )
            st.caption(
                f"File: {citation.get('source', 'Unknown')} "
                f"| Page: {citation.get('page') or 'N/A'}"
            )


def find_citations(value):
    if isinstance(value, dict):
        citations = value.get("citations")

        if isinstance(citations, list):
            return citations

        for item in value.values():
            found = find_citations(item)
            if found:
                return found

    elif isinstance(value, list):
        for item in value:
            found = find_citations(item)
            if found:
                return found

    return []


# CHAT FUNCTIONS

def add_message(question, answer, citations, mode):
    st.session_state.messages.append({
        "question": question,
        "answer": answer,
        "citations": citations,
        "mode": mode,
        "feedback": None
    })


def ask_rag(question):
    response = api_post("/ask", {"question": question})

    if response:
        add_message(
            question,
            response.get("answer", "No answer returned."),
            response.get("citations", []),
            "RAG"
        )


def ask_agent(question, config):
    response = api_post(
        "/agent",
        {
            "question": question,
            "config": config,
            "thread_id": st.session_state.thread_id,
            "resume": False
        }
    )

    if not response:
        return

    if response.get("status") == "approval_required":
        st.session_state.pending_agent = {
            "question": question,
            "approval": response.get("approval"),
            "thread_id": response.get("thread_id")
        }
        return

    if response.get("status") == "completed":
        result = response.get("result")
        citations = find_citations(result)

        answer = (
            result if isinstance(result, str)
            else json.dumps(result, indent=2, ensure_ascii=False)
        )

        add_message(question, answer, citations, "Agent")
    else:
        st.warning(f"Agent response: {response}")


def resume_agent(approved):
    pending = st.session_state.pending_agent

    if not pending:
        return

    response = api_post(
        "/agent",
        {
            "thread_id": pending["thread_id"],
            "resume": True,
            "approved": approved
        }
    )

    if response:
        if response.get("status") == "completed":
            result = response.get("result")
            citations = find_citations(result)

            answer = (
                result if isinstance(result, str)
                else json.dumps(result, indent=2, ensure_ascii=False)
            )

            add_message(
                pending["question"],
                answer,
                citations,
                "Agent"
            )
        else:
            st.info(response.get("message", "Agent request finished."))

    st.session_state.pending_agent = None


# HEADER

st.markdown(
    '<div class="main-title">🛡️ OWASPShield</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">Your AI-powered OWASP security assistant</div>',
    unsafe_allow_html=True
)


# SIDEBAR

with st.sidebar:
    st.title("⚙️ Settings")

    mode = st.radio(
        "Assistant mode",
        ["RAG Chat", "LangGraph Agent"]
    )

    st.divider()
    st.markdown("### API Status")

    health = api_get("/health")

    if health and health.get("status") == "healthy":
        st.success("Backend connected")
    else:
        st.error("Backend unavailable")

    st.divider()

    if st.button("🗑️ Clear conversation", use_container_width=True):
        st.session_state.messages = []
        st.session_state.pending_agent = None
        st.session_state.thread_id = str(uuid.uuid4())
        st.rerun()

    st.caption("OWASPShield | Checkpoint 2")


# MAIN TABS

chat_tab, mapper_tab = st.tabs([
    "💬 Security Assistant",
    "🔍 VAPT Finding Mapper"
])


# SECURITY CHAT

with chat_tab:
    st.subheader("Security Assistant")

    st.caption(
        "Ask questions about OWASP vulnerabilities, "
        "security controls and best practices."
    )

    agent_config = {}

    if mode == "LangGraph Agent":
        with st.expander("Agent configuration"):
            config_text = st.text_area(
                "Optional configuration (JSON)",
                value="{}",
                help="Enter the configuration expected by your agent."
            )

            try:
                agent_config = json.loads(config_text)
                if not isinstance(agent_config, dict):
                    st.error("Configuration must be a JSON object.")
                    agent_config = {}
            except json.JSONDecodeError:
                st.error("Invalid JSON configuration.")
                agent_config = {}

    for index, message in enumerate(st.session_state.messages):
        with st.chat_message("user"):
            st.write(message["question"])

        with st.chat_message("assistant"):
            st.markdown(message["answer"])
            show_citations(message["citations"])
            st.caption(f"Mode: {message['mode']}")

            col1, col2, _ = st.columns([1, 1, 5])

            with col1:
                if st.button(
                    "👍",
                    key=f"up_{index}",
                    disabled=message["feedback"] is not None
                ):
                    save_feedback(
                        message["question"],
                        message["answer"],
                        message["mode"],
                        "positive"
                    )
                    message["feedback"] = "positive"
                    st.rerun()

            with col2:
                if st.button(
                    "👎",
                    key=f"down_{index}",
                    disabled=message["feedback"] is not None
                ):
                    save_feedback(
                        message["question"],
                        message["answer"],
                        message["mode"],
                        "negative"
                    )
                    message["feedback"] = "negative"
                    st.rerun()

            if message["feedback"]:
                st.caption("Feedback saved. Thank you!")

    if st.session_state.pending_agent:
        pending = st.session_state.pending_agent

        st.warning("Human approval required before tool execution.")
        st.json(pending["approval"])

        approve_col, reject_col = st.columns(2)

        with approve_col:
            if st.button("✅ Approve execution"):
                resume_agent(True)
                st.rerun()

        with reject_col:
            if st.button("❌ Reject execution"):
                resume_agent(False)
                st.rerun()

    question = st.chat_input("Ask an OWASP security question...")

    if question:
        if mode == "RAG Chat":
            ask_rag(question)
        else:
            if st.session_state.pending_agent:
                st.warning("Please approve or reject the pending request first.")
            else:
                ask_agent(question, agent_config)

        st.rerun()


# VAPT FINDING MAPPER

with mapper_tab:
    st.subheader("🔍 VAPT Finding Mapper")

    st.markdown("""
    <div class="feature-card">
        <b>Turn security findings into actionable fixes.</b><br>
        Paste one line from a VAPT report. OWASPShield will
        search its knowledge base and suggest matching cheat
        sheets, security controls and a fix checklist.
    </div>
    """, unsafe_allow_html=True)

    finding = st.text_area(
        "Paste your VAPT finding",
        placeholder=(
            "Example: Application stores user passwords "
            "using unsalted MD5 hashes."
        ),
        height=110
    )

    if st.button("🔎 Map Finding", type="primary"):
        if not finding.strip():
            st.warning("Please enter a security finding.")
        else:
            with st.spinner("Searching OWASP security records..."):
                results = api_get(
                    "/search",
                    {"q": finding.strip()}
                )

                st.session_state.vapt_results = results or []
                st.session_state.vapt_finding = finding.strip()

    if "vapt_results" in st.session_state:
        results = st.session_state.vapt_results

        st.divider()
        st.markdown("### Matching Cheat Sheets")

        if not results:
            st.warning(
                "No matching records found. Try describing "
                "the vulnerability with different keywords."
            )
        else:
            for index, record in enumerate(results):
                with st.container(border=True):
                    st.markdown(
                        f"**{index + 1}. "
                        f"{record.get('cheat_sheet', 'OWASP Cheat Sheet')}**"
                    )

                    st.markdown(
                        f"**Vulnerability:** "
                        f"{record.get('vulnerability', 'N/A')}"
                    )

                    st.markdown(
                        f"**OWASP Category:** "
                        f"{record.get('owasp_top10_category', 'N/A')}"
                    )

                    st.markdown(
                        f"**Recommended Control:** "
                        f"{record.get('recommended_control', 'N/A')}"
                    )

                    st.markdown(
                        f"**Exact Parameter:** "
                        f"{record.get('exact_parameter', 'N/A')}"
                    )

                    st.caption(
                        f"Source: {record.get('source_url', 'Not provided')} "
                        f"| Similarity: "
                        f"{record.get('similarity_score', 'N/A')}"
                    )

                    st.markdown("#### ✅ Fix Checklist")

                    checklist_items = [
                        "Review the identified vulnerability and affected component.",
                        "Implement the recommended security control: "
                        + str(record.get("recommended_control", "Review security control.")),
                        "Apply the required parameter or configuration: "
                        + str(record.get("exact_parameter", "Review required parameters.")),
                        "Retest the application to verify the vulnerability is fixed."
                    ]

                    for item_number, item in enumerate(checklist_items):
                        st.checkbox(
                            item,
                            key=f"vapt_{index}_{item_number}"
                        )

    st.divider()

    st.caption(
        "OWASPShield provides security guidance. "
        "Verify suggested fixes in your own environment."
    )
