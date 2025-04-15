import json
import logging
import signal
import sys
import time

from kafka import KafkaConsumer
from kafka.errors import KafkaError, NoBrokersAvailable
from moderation.core.settings import settings

logger = logging.getLogger("moderation.consumer")


shutdown_requested = False


def graceful_shutdown(*args):
    global shutdown_requested
    logger.info("Received shutdown signal. Initiating graceful shutdown.")
    shutdown_requested = True


signal.signal(signal.SIGINT, graceful_shutdown)
signal.signal(signal.SIGTERM, graceful_shutdown)


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
                value_deserializer=lambda m: json.loads(m.decode("utf-8")),
                consumer_timeout_ms=settings.CONSUMER_TIMEOUT_MS,
            )
            logger.info("Successfully connected to Kafka broker")
            return consumer
        except NoBrokersAvailable:
            logger.warning(f"Kafka brokers not available. Retry attempt {attempt+1}/{settings.MAX_RETRIES}")
            time.sleep(settings.RETRY_INTERVAL)

    logger.error("Failed to connect to Kafka after maximum retry attempts")
    sys.exit(1)


def process_message(message):
    """Process a message from Kafka."""
    # Implement your message processing logic here
    logger.info(f"Processing message with offset {message.offset}")

    # Log message details at debug level to avoid flooding logs in production
    logger.debug(f"Message content: {message.value}")

    # Message processing implementation


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
