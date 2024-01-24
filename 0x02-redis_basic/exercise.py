#!/usr/bin/env python3
"""
redis set up
"""
from typing import Union
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
