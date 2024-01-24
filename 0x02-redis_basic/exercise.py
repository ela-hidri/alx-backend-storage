#!/usr/bin/env python3
"""
redis set up
"""
from typing import Callable, Optional, Union
import redis
import uuid


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

    def store(self, data: Union[str, bytes, int, float]) -> str:
        """
        generate a random key store the input data in Redis
        """
        key: str = str(uuid.uuid4())
        self._redis.set(key, data)
        return key

    def get(self, Key: str, fn: Optional[Callable] = None):
        """
        Reading from Redis and recovering original type
        """
        data = self._redis.get(Key)
        if data is None:
            return
        if fn is str:
            return self.get_str(data)
        if fn is int:
            return self.get_int(data)
        if fn is Callable:
            return fn(data)
        return data

    def get_str(data: bytes) -> str:
        """convert to str"""
        return data.decode('UTF-8')

    def get_int(data: bytes) -> int:
        """ convert to int"""
        return int(data)
