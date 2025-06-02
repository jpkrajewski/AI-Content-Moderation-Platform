import logging
from dataclasses import asdict
from enum import Enum

from kafka import KafkaProducer
from moderation.core.settings import settings
from moderation.kafka.models import KafkaModerationMessage
from moderation.service.storage import StoredFiles

logger = logging.getLogger("moderation.kafka_producer")


class KafkaProducerService:
    def __init__(self, kafka_producer: KafkaProducer) -> None:
        self.kafka_producer = kafka_producer

    def send_message_for_text_classifier(self, content_id: str, message: str, message_type: Enum) -> None:
        """Send a message to the Kafka topic."""
        logger.info(f"Sending message to Kafka topic {settings.KAFKA_TOPIC}")
        kafka_message = KafkaModerationMessage(
            content_id=content_id,
            type=message_type.value,
            message=message,
        )
        self.kafka_producer.send(settings.KAFKA_TOPIC, value=asdict(kafka_message))
        self.kafka_producer.flush()

    def send_message_for_file_classifier_bulk(
        self, content_id: str, stored_images: StoredFiles, message_type: Enum
    ) -> None:
        """Send a message to the Kafka topic."""
        logger.info(f"Sending message to Kafka topic {settings.KAFKA_TOPIC}")
        for image in stored_images.files:
            kafka_message = KafkaModerationMessage(
                content_id=content_id,
                type=message_type.value,
                message="",
                filename=image.filename,
                filepath=image.filepath,
            )
            self.kafka_producer.send(settings.KAFKA_TOPIC, value=asdict(kafka_message))
            logger.info(f"Sent Kafka message: {kafka_message}")
        self.kafka_producer.flush()
