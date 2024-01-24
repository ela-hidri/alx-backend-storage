#!/usr/bin/env python3
"""
redis set up
"""
from typing import Any, Callable, Optional, Union
import redis
import uuid
from functools import wraps


def count_calls(method: Callable) -> Callable:
    """count how many function is called"""
    @wraps(method)
    def wrapper(self: Any, *args, **kwds) -> str:
        """ count """
        self._redis.incr(method.__qualname__)
        return method(self, *args, **kwds)
    
    return wrapper

def call_history(method: Callable) -> Callable:
    """
    store the history of inputs and outputs for a particular function
    """
    @wraps(method)
    def wrapper(self: Any, *args) -> str:
        """ store the history """
        self._redis.rpush(f"{method.__qualname__}:inputs", str(args))
        output = method(self, *args)
        self._redis.rpush(f"{method.__qualname__}:outputs", output)
        return output

    return wrapper

def replay(method):
    """ display the history of particular method"""
    redis = redis.Redis()
    calls = redis.get(method.__qualname__).decode('utf-8')
    inputs = [input.decode('utf-8') for input in
              redis.lrange(f'{method.__qualname__}:inputs', 0, -1)]
    outputs = [output.decode('utf-8') for output in
               redis.lrange(f'{method.__qualname__}:outputs', 0, -1)]
    print(f'{method.__qualname__} was called {calls} times:')
    for input, output in zip(inputs, outputs):
        print(f'{method.__qualname__}(*{input}) -> {output}')


class Cache:
    """
    setting and storing in redis
    """

    def __init__(self):
        """
        initilize
        """
        self._redis = redis.Redis()
        self._redis.flushdb()

    @call_history
    @count_calls
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """
        generate a random key store the input data in Redis
        """
        key: str = str(uuid.uuid4())
        self._redis.set(key, data)
        return key

    def get(self, Key: str, fn: Optional[Callable] = None) -> Any:
        """
        Reading from Redis and recovering original type
        """
        data = self._redis.get(Key)
        if not data:
            return
        if fn is str:
            return self.get_str(data)
        if fn is int:
            return self.get_int(data)
        if callable(fn):
            return fn(data)
        return data

    def get_str(self, data: bytes) -> str:
        """
        convert to str
        """
        return data.decode('utf-8')

    def get_int(self, data: bytes) -> int:
        """
        convert to int
        """
        return int(data)
