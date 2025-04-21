import logging
from dataclasses import asdict
from typing import Literal

from kafka import KafkaProducer
from moderation.core.settings import settings
from moderation.kafka.models import KafkaModerationMessage

logger = logging.getLogger("moderation.kafka_producer")


MessageType = Literal["text", "image"]


class KafkaProducerService:
    def __init__(self, kafka_producer: KafkaProducer) -> None:
        self.kafka_producer = kafka_producer

    def send_message_for_text_classifier(self, content_id: str, message: str, message_type: MessageType) -> None:
        """Send a message to the Kafka topic."""
        logger.info(f"Sending message to Kafka topic {settings.KAFKA_TOPIC}")
        kafka_message = KafkaModerationMessage(
            content_id=content_id,
            type=message_type,
            message=message,
        )
        self.kafka_producer.send(settings.KAFKA_TOPIC, value=asdict(kafka_message))
        self.kafka_producer.flush()

    def send_message_for_image_classifier(self, content_id: str, image_path: str, message_type: MessageType) -> None:
        """Send a message to the Kafka topic."""
        logger.info(f"Sending message to Kafka topic {settings.KAFKA_TOPIC}")
        kafka_message = KafkaModerationMessage(
            content_id=content_id,
            type=message_type,
            message=image_path,
        )
        self.kafka_producer.send(settings.KAFKA_TOPIC, value=asdict(kafka_message))
        self.kafka_producer.flush()

    def send_message_for_image_classifier_bulk(
        self, content_id: str, image_paths: list[str], message_type: MessageType
    ) -> None:
        """Send a message to the Kafka topic."""
        logger.info(f"Sending message to Kafka topic {settings.KAFKA_TOPIC}")
        kafka_message = KafkaModerationMessage(
            content_id=content_id,
            type=message_type,
            message=image_paths,
        )
        for image_path in image_paths:
            kafka_message.message = image_path
            self.kafka_producer.send(settings.KAFKA_TOPIC, value=asdict(kafka_message))
        self.kafka_producer.flush()
