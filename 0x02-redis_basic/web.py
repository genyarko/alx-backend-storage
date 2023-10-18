#!/usr/bin/env python3
'''A module with tools for request caching and tracking.
'''
import requests
import redis
import time

def get_page(url: str) -> str:
    # Initialize a Redis client
    r = redis.Redis()

    # Key to track the count of URL access
    count_key = f'count:{url}'

    # Get the count from the cache or set it to 0 if not exists
    count = int(r.get(count_key) or 0)

    # Increment the count
    count += 1

    # Store the updated count with a 10-second expiration time
    r.setex(count_key, 10, count)

    # Get the HTML content from the URL
    response = requests.get(url)

    if response.status_code == 200:
        return response.text
    else:
        return f"Failed to retrieve the page from {url}"

if __name__ == '__main__':
    # Example usage:
    url = "http://slowwly.robertomurray.co.uk/delay/5000/url/text"
    html_content = get_page(url)
    print(f"HTML content from {url}:\n{html_content}")
