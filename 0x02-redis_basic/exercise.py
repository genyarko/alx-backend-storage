#!/usr/bin/env python3
'''A module for using the Redis NoSQL data storage.
'''
import uuid
import redis
from functools import wraps
from typing import Any, Callable, Union

def count_calls(method: Callable) -> Callable:
    '''Tracks the number of calls made to a method in a Cache class.
    '''
    @wraps(method)
    def invoker(self, *args, **kwargs) -> Any:
        '''Invokes the given method after incrementing its call counter.
        '''
        if isinstance(self._redis, redis.Redis):
            self._redis.incr(method.__qualname__)
        return method(self, *args, **kwargs)
    return invoker

def call_history(method: Callable) -> Callable:
    '''Tracks the call details of a method in a Cache class.
    '''
    @wraps(method)
    def invoker(self, *args, **kwargs) -> Any:
        '''Returns the method's output after storing its inputs and output.
        '''
        in_key = '{}:inputs'.format(method.__qualname__)
        out_key = '{}:outputs'.format(method.__qualname__)
        if isinstance(self._redis, redis.Redis):
            self._redis.rpush(in_key, str(args))
        output = method(self, *args, **kwargs)
        if isinstance(self._redis, redis.Redis):
            self._redis.rpush(out_key, output)
        return output
    return invoker

def replay(fn: Callable) -> None:
    '''Displays the call history of a Cache class's method.
    '''
    if fn is None or not hasattr(fn, '__self__'):
        return
    
    redis_store = getattr(fn.__self__, '_redis', None)
    
    if not isinstance(redis_store, redis.Redis):
        return
    
    method_name = fn.__qualname__
    in_key = '{}:inputs'.format(method_name)
    out_key = '{}:outputs'.format(method_name)
    call_count = 0
    
    if redis_store.exists(method_name) != 0:
        call_count = int(redis_store.get(method_name))
    
    print('{} was called {} times:'.format(method_name, call_count))
    
    inputs = redis_store.lrange(in_key, 0, -1)
    outputs = redis_store.lrange(out_key, 0, -1)
    
    for input_data, output_data in zip(inputs, outputs):
        input_str = ', '.join(input_data.decode("utf-8").split(', '))
        output_str = output_data.decode("utf-8")
        print('{}(*({})) -> {}'.format(method_name, input_str, output_str)

class Cache:
    '''Represents an object for storing data in a Redis data storage.
    '''
    def __init__(self) -> None:
        '''Initializes a Cache instance.
        '''
        self._redis = redis.Redis()
        self._redis.flushdb(True)

    @call_history
    @count_calls
    def store(self, data: Union[str, bytes, int, float]) -> str:
        '''Stores a value in a Redis data storage and returns the key.
        '''
        data_key = str(uuid.uuid4())
        self._redis.set(data_key, data)
        return data_key

    def get(
            self,
            key: str,
            fn: Callable = None,
            ) -> Union[str, bytes, int, float]:
        '''Retrieves a value from a Redis data storage.
        '''
        data = self._redis.get(key)
        return fn(data) if fn is not None else data

    def get_str(self, key: str) -> str:
        '''Retrieves a string value from a Redis data storage.
        '''
        return self.get(key, lambda x: x.decode('utf-8'))

    def get_int(self, key: str) -> int:
        '''Retrieves an integer value from a Redis data storage.
        '''
        return self.get(key, lambda x: int(x))

# Example usage:
cache = Cache()
cache.store("foo")
cache.store("bar")
cache.store(42)
replay(cache.store)
