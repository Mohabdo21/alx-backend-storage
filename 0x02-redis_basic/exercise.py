#!/usr/bin/env python3
"""
Module for Exercise
"""
import uuid
from typing import Union

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
