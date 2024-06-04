import json
from typing import Any

from app.cache.core import client
from app.core.config import settings

class UserCache():
    def write_user_to_cache(
        self, user_id: int, email: str, obj_data: dict[str, Any]
    ) -> None:
        """
        Store the obj_data as the user data in the cache by user_id and create 
        a new set for email.
        """
        client.hset(f"user:{user_id}", mapping={
            "email": email,
            "data": json.dumps(obj_data)
        })

        client.sadd(f"email:{email}", user_id)

        client.expire(
            f"user:{user_id}",
            time=settings.REDIS_CACHE_EXPIRY
        )

        client.expire(
            f"email:{email}",
            time=settings.REDIS_CACHE_EXPIRY
        )

    def read_user_by_id_from_cache(self, user_id: int) -> dict[str, Any]:
        """
        Return the user data stored in the cache under user_id.
        """
        user_data = client.hgetall(f"user:{user_id}")

        if user_data:
            return json.loads(user_data["data"]) # type: ignore

        return user_data # type: ignore

    def read_user_by_email_from_cache(self, email: str) -> dict[str, Any]:
        """
        Return the user from the cache with email as their email.
        """
        users = client.smembers(f"email:{email}")

        for user in users: # type: ignore
            return self.read_user_by_id_from_cache(int(user))

        return {}

    def delete_user_from_cache(self, user_id: int) -> None:
        """
        Delete user with user_id from the cache and the set containing the users email.
        """
        email = client.hget(f"user:{user_id}", "email")

        client.delete(f"email:{email}", f"user:{user_id}")

user_cache = UserCache()
