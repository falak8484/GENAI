
from fastapi.testclient import TestClient

from app import main
from data.sample_records import sample_records

client = TestClient(main.app)


def test_health_endpoint():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json()["status"] == "healthy"
    assert response.json()["service"] == "OWASPShield"


def test_records_endpoint(monkeypatch):
    monkeypatch.setattr(
        main,
        "load_records",
        lambda: sample_records
    )

    response = client.get("/records?limit=2")

    assert response.status_code == 200
    assert len(response.json()) == 2


def test_search_endpoint(monkeypatch):
    monkeypatch.setattr(
        main,
        "search_records",
        lambda query: [{"cheat_sheet": "Password Storage"}]
    )

    response = client.get("/search?q=password")

    assert response.status_code == 200
    assert response.json()[0]["cheat_sheet"] == "Password Storage"


def test_ask_endpoint_with_fake_llm(monkeypatch):
    fake_response = {
        "answer": "Use Argon2id for password hashing.",
        "citations": ["OWASP Password Storage Cheat Sheet"]
    }

    monkeypatch.setattr(
        main,
        "ask_question",
        lambda question: fake_response
    )

    response = client.post(
        "/ask",
        json={"question": "How should passwords be stored?"}
    )

    assert response.status_code == 200

    result = response.json()

    assert result["answer"] == fake_response["answer"]
    assert result["citations"] == fake_response["citations"]


def test_ask_rejects_empty_question():
    response = client.post(
        "/ask",
        json={"question": "   "}
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "Question cannot be empty"
