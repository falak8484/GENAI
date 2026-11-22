
import hashlib
import time
from collections import OrderedDict

CACHE_TTL_SECONDS = 300
MAX_CACHE_ENTRIES = 100

_cache = OrderedDict()


def make_cache_key(question, task):
    value = f"{task}:{question.strip().lower()}"
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def get_cached_response(key):
    entry = _cache.get(key)

    if entry is None:
        return None

    response, created_at = entry

    if time.time() - created_at > CACHE_TTL_SECONDS:
        del _cache[key]
        return None

    _cache.move_to_end(key)
    return response


def set_cached_response(key, response):
    _cache[key] = (response, time.time())
    _cache.move_to_end(key)

    while len(_cache) > MAX_CACHE_ENTRIES:
        _cache.popitem(last=False)


def clear_cache():
    _cache.clear()
