import json

from aio_pika import connect_robust, Message, DeliveryMode
from aio_pika.pool import Pool
import logging

logger = logging.getLogger(__name__)

_connection_pool: Pool | None = None
_channel_pool: Pool | None = None


async def init_rabbitmq(url: str):
    global _connection_pool, _channel_pool

    async def get_connection():
        return await connect_robust(url)

    _connection_pool = Pool(get_connection, max_size=2)

    async def get_channel():
        async with _connection_pool.acquire() as connection:
            return await connection.channel()

    _channel_pool = Pool(get_channel, max_size=10)

    logger.info("RabbitMQ connection pools initialized")


async def get_channel():
    if _channel_pool is None:
        raise RuntimeError("RabbitMQ not initialized")

    async with _channel_pool.acquire() as channel:
        yield channel


async def setup_rabbitmq():
    if _channel_pool is None:
        raise RuntimeError("RabbitMQ not initialized")

    async with _channel_pool.acquire() as channel:
        queue = await channel.declare_queue(
            "video_views_sync",
            durable=True
        )
        exchange = await channel.declare_exchange(
            "video.events",
            type="topic",
            durable=True
        )
        await queue.bind(exchange, routing_key="video.views.sync")

    logger.info("RabbitMQ queue 'video_views_sync' declared")


async def publish_message(routing_key: str, data: dict):
    if _channel_pool is None:
        raise RuntimeError("RabbitMQ not initialized")

    async with _channel_pool.acquire() as channel:
        exchange = await channel.get_exchange("video.events")

        await exchange.publish(
            Message(
                body=json.dumps(data).encode(),
                delivery_mode=DeliveryMode.PERSISTENT
            ),
            routing_key=routing_key
        )


async def close_rabbitmq():
    global _connection_pool, _channel_pool

    if _channel_pool:
        await _channel_pool.close()

    if _connection_pool:
        await _connection_pool.close()

    logger.info("RabbitMQ connection pools closed")
