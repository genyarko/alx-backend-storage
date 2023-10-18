#!/usr/bin/env python3
'''
A module with tools for request caching and tracking.
'''
import redis
import requests
from functools import wraps
from typing import Callable

redis_store = redis.Redis()
'''
The module-level Redis instance.
'''

def data_cacher(method: Callable) -> Callable:
    '''
    Decorator to cache the output of fetched data and track request counts.
    '''
    @wraps(method)
    def invoker(url: str) -> str:
        '''
        Wrapper function to handle caching and request tracking.
        '''
        # Increment the request count for the given URL
        redis_store.incr(f'count:{url}')
        
        # Check if the result is already cached
        result = redis_store.get(f'result:{url}')
        if result:
            return result.decode('utf-8')
        
        # Fetch the data if not cached
        result = method(url)
        
        # Reset the count and cache the result with a 10-second expiration
        redis_store.set(f'count:{url}', 0)
        redis_store.setex(f'result:{url}', 10, result)
        
        return result

    return invoker

@data_cacher
def get_page(url: str) -> str:
    '''
    Fetches and returns the content of a URL, caching the response and tracking requests.
    '''
    return requests.get(url).text
