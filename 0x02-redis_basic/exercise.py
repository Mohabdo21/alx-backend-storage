#!/usr/bin/env python3
"""
Module for Exercise
"""
import uuid
from functools import wraps
from typing import Callable, Optional, Union

import redis


def count_calls(method: Callable) -> Callable:
    """
    Decorate to count the number of calls to a method
    """
    key = method.__qualname__

    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """
        Wrapper function for the decorator
        """
        self._redis.incr(key)
        return method(self, *args, **kwargs)

    return wrapper


def call_history(method: Callable) -> Callable:
    """
    Decorator to store the history of inputs and outputs for a method
    """
    input_key = f"{method.__qualname__}:inputs"
    output_key = f"{method.__qualname__}:outputs"

    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """
        Wrapper function for the decorator
        """
        self._redis.rpush(input_key, str(args))
        result = method(self, *args, **kwargs)
        self._redis.rpush(output_key, str(result))
        return result

    return wrapper


def replay(method: Callable) -> None:
    """
    Display the history of calls of a particular function
    """
    redis_instance = redis.Redis()
    input_key = f"{method.__qualname__}:inputs"
    output_key = f"{method.__qualname__}:outputs"
    inputs = redis_instance.lrange(input_key, 0, -1)
    outputs = redis_instance.lrange(output_key, 0, -1)

    print(f"{method.__qualname__} was called {len(inputs)} times:")
    for inp, out in zip(inputs, outputs):
        print(
            f"{method.__qualname__}(*{inp.decode('utf-8')})"
            f" -> {out.decode('utf-8')}"
        )


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

    @count_calls
    @call_history
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
