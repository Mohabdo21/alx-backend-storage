#!/usr/bin/env python3
"""
Module for implementing an expiring web cache and tracker
to obtain the HTML content of a particular URL and return it.
"""
from typing import Optional

import redis
import requests

# Initialize the Redis client
r = redis.Redis()


def get_page(url: str) -> str:
    """
    Track how many times a particular URL was accessed
    and cache the result with an expiration time of 10 seconds.

    Args:
        url (str): The URL to fetch.

    Returns:
        str: The HTML content of the URL.
    """
    try:
        # Check if the URL is already cached
        cached_content: Optional[bytes] = r.get(f"cached:{url}")
        if cached_content:
            return cached_content.decode("utf-8")

        response = requests.get(url)
        response.raise_for_status()

        r.incr(f"count:{url}")

        r.setex(f"cached:{url}", 10, response.text)
        return response.text
    except requests.RequestException as e:
        print(f"Error fetching {url}: {e}")
        return ""


if __name__ == "__main__":
    url = "http://slowwly.robertomurray.co.uk"
    print(get_page(url))
