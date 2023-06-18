import json
import uuid
from typing import List
from fastapi import Cookie
from config.db.redis.redis import get_redis_client
from starlette.responses import Response


def get_unique_id(unique_id: str):
    # Use the function to get the Redis client
    redis_client = get_redis_client()

    if not unique_id:
        # If the unique ID is not provided, return None
        return None, None

    # Check if the unique ID exists in Redis
    if redis_client.exists(unique_id):
        # Retrieve the value associated with the unique ID from Redis
        value = redis_client.get(unique_id)
        # Try parsing the value as JSON and return it
        try:
            return unique_id, json.loads(value.decode())
        except Exception as e:
            print(f"Failed to parse value as JSON: {e}")
            return unique_id, []
    else:
        # If the unique ID does not exist, save it in Redis with an empty list as the value
        redis_client.set(unique_id, json.dumps([]))

        return unique_id, []


def update_banner_ids(unique_id: str, banner_ids: List[int]):
    if unique_id is not None:
        # Use the function to get the Redis client
        redis_client = get_redis_client()
        print(redis_client)

        # Convert banner_ids to a JSON string
        banner_ids_json = json.dumps(banner_ids)

        # Set the banner IDs in Redis with the unique ID as the key
        redis_client.set(unique_id, banner_ids_json)
