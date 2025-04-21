import json

from dependency_injector import containers, providers
from kafka import KafkaProducer
from moderation.core.settings import settings
from moderation.db.session import SessionLocal
from moderation.repository.db.content.database import DatabaseContentRepository
from moderation.repository.db.content.memory import InMemoryContentRepository
from moderation.service.content import ContentService
from moderation.service.kafka import KafkaProducerService


def _get_content_repository():
    if settings.DB_REPOSITORY == "memory":
        return InMemoryContentRepository()
    else:
        return DatabaseContentRepository(session=SessionLocal())


class Container(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(packages=["moderation.routes.content"])
    content_service = providers.Singleton(
        ContentService,
        repository=providers.Factory(_get_content_repository),
    )
    kafka_producer_service = providers.Singleton(
        KafkaProducerService,
        kafka_producer=providers.Singleton(
            KafkaProducer,
            bootstrap_servers=settings.KAFKA_BOOTSTRAP_SERVERS,
            value_serializer=lambda v: json.dumps(v).encode("utf-8"),
        ),
    )
