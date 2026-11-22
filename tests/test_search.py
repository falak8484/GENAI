import pytest

from app import smart_search


@pytest.fixture
def fake_records(monkeypatch):
    records = [
        {
            "cheat_sheet": "Password Storage",
            "vulnerability": "Weak password hashing",
            "recommended_control": "Use Argon2id",
            "exact_parameter": "Memory 19 MiB, iterations 2",
            "owasp_top10_category": "A07 Authentication"
        },
        {
            "cheat_sheet": "SQL Injection Prevention",
            "vulnerability": "Unsafe SQL queries",
            "recommended_control": "Use parameterized queries",
            "exact_parameter": "Prepared statements",
            "owasp_top10_category": "A05 Injection"
        }
    ]

    monkeypatch.setattr(
        smart_search,
        "load_records",
        lambda: records
    )

    return records


def test_search_records_finds_matching_result(fake_records):
    results = smart_search.search_records("password")

    assert len(results) > 0
    assert results[0]["cheat_sheet"] == "Password Storage"


def test_search_records_returns_empty_for_unknown_query(fake_records):
    results = smart_search.search_records("unknownxyz")

    assert results == []


def test_search_records_returns_empty_for_blank_query(fake_records):
    results = smart_search.search_records("   ")

    assert results == []


def test_search_records_respects_limit(fake_records):
    results = smart_search.search_records(
        "security",
        limit=1
    )

    assert len(results) <= 1


def test_search_records_handles_empty_database(monkeypatch):
    monkeypatch.setattr(
        smart_search,
        "load_records",
        list
    )

    results = smart_search.search_records("password")

    assert results == []
