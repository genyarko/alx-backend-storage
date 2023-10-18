#!/usr/bin/env python3
'''A module with tools for request caching and tracking.
'''
import redis
import requests
from functools import wraps
from typing import Callable

# Initialize a module-level Redis instance
redis_store = redis.Redis()

def data_cacher(method: Callable) -> Callable:
    '''Decorator that caches the output of fetched data.
    '''
    @wraps(method)
    def invoker(url) -> str:
        '''Wrapper function for caching the output.
        '''
        # Increment the count for the URL
        redis_store.incr(f'count:{url}')
        
        # Try to retrieve the cached result
        result = redis_store.get(f'result:{url}')
        if result:
            return result.decode('utf-8')
        
        # If the result is not cached, fetch it and cache it with a 10-second expiration
        result = method(url)
        redis_store.set(f'count:{url}', 0)  # Reset the count to 0
        redis_store.setex(f'result:{url}', 10, result)  # Cache the result
        return result
    return invoker

@data_cacher
def get_page(url: str) -> str:
    '''Function that returns the content of a URL after caching the request's response and tracking the request.
    '''
    return requests.get(url).text
