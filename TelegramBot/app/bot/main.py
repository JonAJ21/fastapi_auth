import json
import logging
from aiokafka import AIOKafkaConsumer
from telegram import Bot
from telegram.error import TelegramError
from settings.config import settings

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def consume_messages():
    consumer = AIOKafkaConsumer(
        settings.kafka_topic,
        bootstrap_servers=settings.kafka_url,
        group_id=settings.kafka_group_id,
        auto_offset_reset='earliest'
    )
    
    bot = Bot(
        token=settings.tg_token,
    )
    await consumer.start()
    logger.info("Kafka consumer started")
    try:
        async for msg in consumer:
            try:
                message = json.loads(msg.value.decode('utf-8'))
                logger.info(f"Received message from Kafka: {message}")
                formatted_message = message
                await bot.send_message(
                    chat_id=settings.chat_id,
                    text=formatted_message
                )
                logger.info(f"Sent message to Telegram: {formatted_message}")
            except json.JSONDecodeError as e:
                logger.error(f"Failed to decode JSON: {e}")
            except TelegramError as e:
                logger.error(f"Failed to send message to Telegram: {e}")
    except Exception as e:
        logger.error(f"An error occurred: {e}")
    finally:
        await consumer.stop()
        logger.info("Kafka consumer stopped")
        
async def main():
    await consume_messages()
    
if __name__ == "__main__":
    asyncio.run(main())
            
            