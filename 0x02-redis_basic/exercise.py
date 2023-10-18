import redis
import uuid
from typing import Union, Callable
from functools import wraps

class Cache:
    """
    Cache class for storing data in Redis with random keys.
    """
    def __init__(self):
        """
        Initialize the Cache class with a Redis client and flush the Redis database.
        """
        self._redis = redis.Redis()
        self._redis.flushdb()

    def store(self, data: Union[str, bytes, int, float) = None) -> str:
        """
        Store data in Redis with a randomly generated key.

        Args:
            data (Union[str, bytes, int, float], optional): The data to be stored. Defaults to None.

        Returns:
            str: The randomly generated key used for storing the data in Redis.
        """
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key

def count_calls(method: Callable) -> Callable:
    """
    Decorator that counts how many times a method is called.

    Args:
        method (Callable): The method to be counted.

    Returns:
        Callable: A wrapped method that increments the count for each call and returns the original method's result.
    """
    call_count = 0

    @wraps(method)
    def wrapped(self, *args, **kwargs):
        nonlocal call_count
        key = method.__qualname__  # Use the qualified name of the method as the Redis key.
        self._redis.incr(key)
        call_count += 1
        return method(self, *args, **kwargs)

    return wrapped

# Decorate the Cache.store method with the count_calls decorator.
Cache.store = count_calls(Cache.store)
