import logging

import redis

from app.core.config import settings

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def redis_connect() -> redis.Redis:
    try:
        client = redis.Redis(
            host=settings.REDIS_SERVER,
            port=settings.REDIS_PORT,
            db=settings.REDIS_DB,
            username=settings.REDIS_USER,
            password=settings.REDIS_PASSWORD,
            decode_responses=True,
        )

        ping = client.ping()
        if ping:
            logger.info("Response from Redis")
        else:
            logger.warn("No response from Redis")

    except Exception as e:
        logger.error(e)
        raise e

    return client

client = redis_connect()
