import json

from kafka import KafkaProducer
from moderation.core.settings import settings

producer = KafkaProducer(
    bootstrap_servers=settings.KAFKA_BOOTSTRAP_SERVERS,
    value_serializer=lambda v: json.dumps(v).encode("utf-8"),
)


def publish_content_message(content_id: str):
    producer.send(settings.KAFKA_TOPIC, {"content_id": content_id})
    producer.flush()
