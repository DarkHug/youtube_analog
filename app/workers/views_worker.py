import aio_pika
import asyncio
import json
import logging

from app.core.settings import settings
from app.db.session import AsyncSessionLocal
from app.models.video import Video
from sqlalchemy import update

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger(__name__)


async def process_message(message: aio_pika.IncomingMessage):
    logger.info(f"Получено сообщение: {message.body.decode()}")  # ← добавь
    async with message.process(requeue=True):
        try:
            data = json.loads(message.body.decode())

            async with AsyncSessionLocal() as session:
                async with session.begin():
                    stmt = (
                        update(Video)
                        .where(Video.id == data["video_id"])
                        .values(views=Video.views + data["views"])
                    )
                    await session.execute(stmt)

            logger.info(f"Просмотры видео №{data['video_id']} обработаны")

        except Exception as e:
            logger.error(f"Ошибка при обработке: {e}")
            raise  # requeue=True сработает и сообщение вернётся в очередь


async def consumer():
    connection = await aio_pika.connect_robust(settings.RABBITMQ_URL)
    channel = await connection.channel()
    await channel.set_qos(prefetch_count=10)

    queue = await channel.declare_queue("video_views_sync", durable=True)
    logger.info(f"Подключился к очереди, сообщений: {queue.declaration_result.message_count}")  # ← добавь
    exchange = await channel.declare_exchange(
        "video.events",
        type="topic",
        durable=True,
    )
    await queue.bind(exchange, routing_key="video.views.sync")

    async with queue.iterator() as queue_iter:
        async for message in queue_iter:
            await process_message(message)


if __name__ == "__main__":
    try:
        asyncio.run(consumer())
    except KeyboardInterrupt:
        logger.info("Завершаю работу")
