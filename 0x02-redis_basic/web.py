#!/usr/bin/env python3
'''A module with tools for request caching and tracking.
'''
import redis
import requests
from functools import wraps
from typing import Callable


class RedisStore:
    def __init__(self, host: str = "localhost", port: int = 6379):
        self.client = redis.Redis(host=host, port=port)

    def incr(self, key: str) -> int:
        return self.client.incr(key)

    def get(self, key: str) -> bytes:
        return self.client.get(key)

    def set(self, key: str, value: bytes):
        self.client.set(key, value)

    def setex(self, key: str, ttl: int, value: bytes):
        self.client.setex(key, ttl, value)


def get_redis_store() -> RedisStore:
    """Returns a Redis store instance."""
    return RedisStore()


def data_cacher(cache_key: str, cache_ttl: int) -> Callable:
    """A decorator for caching the results of a function.

    Args:
        cache_key: The cache key to use for the function.
        cache_ttl: The expiration time for cached items in seconds.

    Returns:
        A decorator function.
    """

    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            """The wrapper function for caching the output."""
            redis_store = get_redis_store()

            redis_store.incr(f'count:{cache_key}')
            result = redis_store.get(f'result:{cache_key}')
            if result:
                return result.decode('utf-8')

            result = func(*args, **kwargs)
            redis_store.set(f'count:{cache_key}', 0)
            redis_store.setex(f'result:{cache_key}', cache_ttl, result)
            return result

        return wrapper

    return decorator


@data_cacher(cache_key='get_page', cache_ttl=10)
def get_page(url: str, timeout: int = 5, cache_buster: bool = False) -> str:
    """Returns the content of a URL after caching the request's response,
    and tracking the request.

    Args:
        url: The URL to fetch.
        timeout: The maximum amount of time to wait for a response from the
            server before returning an error.
        cache_buster: Whether to bypass the cache and fetch the latest data from
            the server.

    Returns:
        The content of the URL.
    """

    if cache_buster:
        redis_store = get_redis_store()
        redis_store.delete(f'result:{cache_key}')

    response = requests.get(url, timeout=timeout)
    return response.text


if __name__ == '__main__':
    url = "https://example.com"

    # Fetch the page content from the cache, or from the server if the cache is not hit.
    page_content = get_page(url)

    print(page_content)
