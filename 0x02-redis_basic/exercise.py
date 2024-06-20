#!/usr/bin/env python3
"""
Module for Exercise
"""
import uuid
from typing import Callable, Optional, Union

import redis


class Cache:
    """
    Cache class for redis
    """

    def __init__(self) -> None:
        """
        Cache class constructor
        """
        self._redis = redis.Redis()
        self._redis.flushdb()

    def store(self, data: Union[str, bytes, int, float]) -> str:
        """
        Store the input data in Redis using a random key
        """
        key: str = str(uuid.uuid4())
        self._redis.set(key, data)
        return key

    def get(
        self, key: str, fn: Optional[Callable] = None
    ) -> Union[str, bytes, int, float]:
        """
        Get the value from Redis by key
        """
        value = self._redis.get(key)
        if fn:
            value = fn(value)
        return value

    def get_str(self, key: str) -> str:
        """
        Get the value from Redis by key and convert it to a string
        """
        value = self.get(key, fn=lambda x: x.decode("utf-8"))
        return value

    def get_int(self, key: str) -> int:
        """
        Get the value from Redis by key and convert it to a integer
        """
        value = self.get(key, fn=int)
        return value
