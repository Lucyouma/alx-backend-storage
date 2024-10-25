#!/usr/bin/env python3
'''Caching request module
'''
import redis
import requests
from functools import wraps
from typing import Callable


redis_store = redis.Redis()
'''The module-level Redis instance.
'''


def data_cacher(method: Callable) -> Callable:
    '''Decorator for get_page
    '''
    @wraps(method)
    def invoker(url) -> str:
        '''Wrapper that:
            - check whether a url's data is cached
            - tracks how many times get_page is called
        '''
        redis_store.incr(f'count:{url}')
        result = redis_store.get(f'result:{url}')
        if result:
            return result.decode('utf-8')
        result = method(url)
        redis_store.set(f'count:{url}', 0)
        redis_store.setex(f'result:{url}', 10, result)
        return result
    return invoker


    @data_cacher
    def get_page(url: str) -> str:
        '''Makes a http request to a given endpoint
        '''
        return requests.get(url).text
