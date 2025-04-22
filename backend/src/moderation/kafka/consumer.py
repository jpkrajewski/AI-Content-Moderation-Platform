import json
import logging
import signal
import sys
import time

from kafka import KafkaConsumer
from kafka.errors import KafkaError, NoBrokersAvailable
from moderation.core.settings import settings
from moderation.kafka.processor import process_message

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler("log.log", mode="a"),
    ],
)
logger = logging.getLogger("moderation.consumer")


shutdown_requested = False


def graceful_shutdown(*args):
    global shutdown_requested
    logger.info("Received shutdown signal. Initiating graceful shutdown.")
    shutdown_requested = True


signal.signal(signal.SIGINT, graceful_shutdown)
signal.signal(signal.SIGTERM, graceful_shutdown)


def value_deserializer(value: bytes) -> dict:
    """Deserialize the message value from bytes to JSON."""
    try:
        return json.loads(value.decode("utf-8"))
    except json.JSONDecodeError as e:
        logger.error(f"Failed to deserialize message: {e}")
        return {"error": "Invalid JSON", "message": str(e), "value": value.decode("utf-8")}


def initialize_consumer():
    """Establish connection to Kafka with retry logic."""
    for attempt in range(settings.MAX_RETRIES):
        try:
            consumer = KafkaConsumer(
                settings.KAFKA_TOPIC,
                bootstrap_servers=settings.KAFKA_BOOTSTRAP_SERVERS,
                group_id=settings.KAFKA_GROUP_ID,
                auto_offset_reset=settings.KAFKA_AUTO_OFFSET_RESET,
                enable_auto_commit=True,
                value_deserializer=value_deserializer,
                consumer_timeout_ms=settings.KAFKA_CONSUMER_TIMEOUT_MS,
            )
            logger.info("Successfully connected to Kafka broker")
            return consumer
        except NoBrokersAvailable:
            logger.warning(f"Kafka brokers not available. Retry attempt {attempt+1}/{settings.MAX_RETRIES}")
            time.sleep(settings.RETRY_INTERVAL)

    logger.error("Failed to connect to Kafka after maximum retry attempts")
    sys.exit(1)


def start_consumer():
    """Main consumer loop with error handling and monitoring."""
    consumer = initialize_consumer()
    message_count = 0
    last_heartbeat = time.time()

    logger.info(f"Starting consumer for topic: {settings.KAFKA_TOPIC}")

    while not shutdown_requested:
        try:
            # Emit regular heartbeat log
            current_time = time.time()
            if current_time - last_heartbeat > settings.HEARTBEAT_INTERVAL:
                logger.info(f"Consumer heartbeat - Messages processed: {message_count}")
                last_heartbeat = current_time

            for message in consumer:
                try:
                    process_message(message)
                    message_count += 1
                except Exception as e:
                    logger.exception(f"Error processing message: {e}")

                if shutdown_requested:
                    break

        except KafkaError as e:
            # Handle Kafka-specific errors
            logger.exception(f"Kafka error occurred: {e}")
            time.sleep(min(30, 2 ** (min(4, message_count % 5) + 1)))  # Exponential backoff with upper limit
        except Exception as e:
            # Handle unexpected errors
            logger.exception(f"Unexpected error in consumer loop: {e}")
            time.sleep(5)  # Brief pause before retry

    # Clean shutdown
    try:
        consumer.close(autocommit=True)
        logger.info("Kafka consumer shutdown completed")
    except Exception as e:
        logger.error(f"Error during consumer shutdown: {e}")


if __name__ == "__main__":
    start_consumer()
