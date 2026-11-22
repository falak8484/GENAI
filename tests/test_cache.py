
from app import cache


def test_cache_returns_none_for_missing_key():
    cache.clear_cache()

    assert cache.get_cached_response("missing-key") is None


def test_cache_stores_and_returns_response():
    cache.clear_cache()

    cache.set_cached_response("test-key", "Test response")

    assert cache.get_cached_response("test-key") == "Test response"


def test_cache_expires_after_ttl(monkeypatch):
    cache.clear_cache()

    current_time = [1000]

    monkeypatch.setattr(
        cache.time,
        "time",
        lambda: current_time[0]
    )

    cache.set_cached_response("expiry-key", "Old response")

    current_time[0] += cache.CACHE_TTL_SECONDS + 1

    assert cache.get_cached_response("expiry-key") is None


def test_cache_key_is_case_insensitive():
    key1 = cache.make_cache_key("Explain SQL Injection", "explain")
    key2 = cache.make_cache_key(" explain sql injection ", "explain")

    assert key1 == key2


def test_cache_key_changes_with_task():
    key1 = cache.make_cache_key("SQL Injection", "explain")
    key2 = cache.make_cache_key("SQL Injection", "controls")

    assert key1 != key2
