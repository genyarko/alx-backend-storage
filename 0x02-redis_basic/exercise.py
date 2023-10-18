import redis
import uuid
from typing import Union, Callable

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

    def store(self, data: Union[str, bytes, int, float]) -> str:
        """
        Store data in Redis with a randomly generated key.

        Args:
            data (Union[str, bytes, int, float]): The data to be stored.

        Returns:
            str: The randomly generated key used for storing the data in Redis.
        """
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key

    def get(self, key: str, fn: Callable = None) -> Union[str, bytes, int, float]:
        """
        Retrieve data from Redis and optionally apply a conversion function.

        Args:
            key (str): The key used to retrieve data from Redis.
            fn (Callable, optional): A callable function to convert the data. Defaults to None.

        Returns:
            Union[str, bytes, int, float]: The retrieved data, possibly converted by the provided function.
        """
        data = self._redis.get(key)
        if data is None:
            return None
        if fn is not None:
            return fn(data)
        return data

    def get_str(self, key: str) -> str:
        """
        Retrieve a string from Redis.

        Args:
            key (str): The key used to retrieve data from Redis.

        Returns:
            str: The retrieved string.
        """
        return self.get(key, fn=lambda d: d.decode("utf-8"))

    def get_int(self, key: str) -> int:
        """
        Retrieve an integer from Redis.

        Args:
            key (str): The key used to retrieve data from Redis.

        Returns:
            int: The retrieved integer.
        """
        return self.get(key, fn=int)
