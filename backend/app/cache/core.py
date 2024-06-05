import logging
from typing import Any, List
import json

import redis
from redis.typing import KeyT

from app.core.config import settings

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class RedisInstance():
    connection = None

    def connect(self) -> None:
        try:
            self.connection = redis.Redis(
                host=settings.REDIS_SERVER,
                port=settings.REDIS_PORT,
                db=settings.REDIS_DB,
                password=settings.REDIS_PASSWORD,
                decode_responses=True,
            )

            if self.connection.ping():
                logger.info("Redis connection is ready")

        except Exception as e:
            logger.error(e)
            raise e

    def disconnect(self) -> None:
        if self.connection:
            self.connection.close()
            logger.info("Redis connection has been closed")

    def flushall(self) -> None:
        if self.connection:
            result = self.connection.flushall()
            logger.info(f"FLUSHALL ({result})")

    def exists(self, *names: KeyT):
        if self.connection:
            return self.connection.exists(*names)

    def write_file_to_cache(
        self, file_id: int, owner_id: int, obj_data: dict[str, Any]
    ) -> None:
        if self.connection:
            self.connection.hset(f"file:{file_id}", mapping={
                "owner_id": owner_id,
                "data": json.dumps(obj_data)
            })

            self.connection.sadd(f"owner_id:{owner_id}", file_id)

            self.connection.expire(
                f"file:{file_id}",
                time=settings.REDIS_CACHE_EXPIRY
            )

            self.connection.expire(
                f"owner_id:{owner_id}",
                time=settings.REDIS_CACHE_EXPIRY
            )
        else:
            print("no connection")

    def read_file_by_id_from_cache(self, file_id: int) ->  dict[str, Any]:
        if self.connection:
            file_data = self.connection.hgetall(f"file:{file_id}")
            
            if file_data:
                return json.loads(file_data["data"]) # type: ignore

            return file_data # type: ignore
        return {}

    def read_files_by_owner_id_from_cache(
        self, owner_id: int
    ) -> List[dict[str, Any]]:
        files = []

        if self.connection:
            file_ids = self.connection.smembers(f"owner_id:{owner_id}")
            files = [self.read_file_by_id_from_cache(file_id) for file_id in file_ids] # type: ignore

        return files

    def read_file_count_by_owner_id_from_cache(self, owner_id: int) -> int:
        if self.connection:
            return self.connection.scard(f"owner_id:{owner_id}") # type: ignore
        return 0

    def delete_file_from_cache(self, file_id: int) -> None:
        if self.connection:
            owner_id = self.connection.hget(f"file:{file_id}", "owner_id")
            self.connection.srem(f"owner_id:{owner_id}", str(file_id))

            if self.connection.scard(f"owner_id:{owner_id}") == 0:
                self.connection.delete(f"owner_id:{owner_id}")

            self.connection.delete(f"file:{file_id}")

    def write_user_to_cache(
        self, user_id: int, email: str, obj_data: dict[str, Any]
    ) -> None:
        if self.connection:
            self.connection.hset(f"user:{user_id}", mapping={
                "email": email,
                "data": json.dumps(obj_data)
            })

            self.connection.sadd(f"email:{email}", user_id)

            self.connection.expire(
                f"user:{user_id}",
                time=settings.REDIS_CACHE_EXPIRY
            )

            self.connection.expire(
                f"email:{email}",
                time=settings.REDIS_CACHE_EXPIRY
            )

    def read_user_by_id_from_cache(self, user_id: int) -> dict[str, Any]:
        if self.connection:
            user_data = self.connection.hgetall(f"user:{user_id}")

            if user_data:
                return json.loads(user_data["data"]) # type: ignore

            return user_data # type: ignore
        return {}

    def read_user_by_email_from_cache(self, email: str) -> dict[str, Any]:
        if self.connection:
            users = self.connection.smembers(f"email:{email}")

            for user in users: # type: ignore
                return self.read_user_by_id_from_cache(int(user))
        return {}

    def delete_user_from_cache(self, user_id: int) -> None:
        if self.connection:
            email = self.connection.hget(f"user:{user_id}", "email")
            self.connection.delete(f"email:{email}", f"user:{user_id}")


redis_db = RedisInstance()
