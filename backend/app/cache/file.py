import json
from typing import Any, List

from app.cache.core import client
from app.core.config import settings

class FileCache():
    def write_file_to_cache(
        self, file_id: int, owner_id: int, obj_data: dict[str, Any]
    ) -> None:
        """
        Store the obj_data as the file data in cache by its file_id and create
        a new set for owner_id.
        """
        client.hset(f"file:{file_id}", mapping={
            "owner_id": owner_id,
            "data": json.dumps(obj_data)
        })

        client.sadd(f"owner_id:{owner_id}", file_id)

        client.expire(
            f"file:{file_id}",
            time=settings.REDIS_CACHE_EXPIRY
        )

        client.expire(
            f"owner_id:{owner_id}",
            time=settings.REDIS_CACHE_EXPIRY
        )

    def read_file_by_id_from_cache(self, file_id: int) ->  dict[str, Any]:
        """
        Return the file data stored in the cache under file_id.
        """
        file_data = client.hgetall(f"file:{file_id}")
        
        if file_data:
            return json.loads(file_data["data"]) # type: ignore

        return file_data # type: ignore

    def read_files_by_owner_id_from_cache(self, owner_id: int) -> List[dict[str, Any]]:
        """
        Return all the file data objects in the cache that have owner_id as their owner id.
        """
        file_ids = client.smembers(f"owner_id:{owner_id}")
        files = [self.read_file_by_id_from_cache(file_id) for file_id in file_ids] # type: ignore

        return files

    def read_file_count_by_owner_id_from_cache(self, owner_id: int) -> int:
        """
        Return a count of file objects that have owner_id as their owner id.
        """
        return client.scard(f"owner_id:{owner_id}") # type: ignore

    def delete_file_from_cache(self, file_id: int) -> Any:
        """
        Delete the file with file_id from the cache and remove its reference in the owner_id set.
        """
        owner_id = client.hget(f"file:{file_id}", "owner_id")
        client.srem(f"owner_id:{owner_id}", str(file_id))

        if client.scard(f"owner_id:{owner_id}") == 0:
            client.delete(f"owner_id:{owner_id}")

        return client.delete(f"file:{file_id}")

file_cache = FileCache()
