import json

from dependency_injector import containers, providers
from kafka import KafkaProducer
from moderation.cache.redis import get_redis_client
from moderation.core.settings import settings
from moderation.db.session import get_db
from moderation.repository.db.analysis.base import AbstractAnalysisRepository
from moderation.repository.db.analysis.database import DatabaseAnalysisRepository
from moderation.repository.db.client_api_key.database import DatabaseClientApiKeyRepository
from moderation.repository.db.content.database import DatabaseContentRepository
from moderation.repository.db.user.base import AbstractUserRepository
from moderation.repository.db.user.database import DatabaseUserRepository
from moderation.service.analysis import AnalysisService
from moderation.service.auth import AuthService
from moderation.service.apikey.apikeys_service import ClientApiKeyService
from moderation.service.content.content_service import ContentService
from moderation.service.kafka import KafkaProducerService
from moderation.service.storage import Storage
from moderation.service.summary import SummaryService
from moderation.service.user import UserService
from moderation.service.oauth.oauth import OAuthService


def _get_client_api_key_repository():
    return DatabaseClientApiKeyRepository(db=get_db)


def _get_content_repository():
    return DatabaseContentRepository(db=get_db)


def _get_user_and_auth_repository() -> AbstractUserRepository:
    return DatabaseUserRepository(db=get_db)


def _get_analysis_repository() -> AbstractAnalysisRepository:
    return DatabaseAnalysisRepository(db=get_db)


class Container(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(
        packages=[
            "moderation.routes.content",
            "moderation.routes.moderation_action",
            "moderation.routes.auth",
            "moderation.routes.dashboard",
            "moderation.routes.api_keys",
            "moderation.kafka.processor",
            "moderation.routes.display"
        ]
    )
    content_service = providers.Singleton(
        ContentService,
        content_repository=providers.Factory(_get_content_repository),
        analysis_repository=providers.Factory(_get_analysis_repository),
    )
    analysis_service = providers.Singleton(
        AnalysisService,
        analysis_repository=providers.Factory(_get_analysis_repository),
    )
    kafka_producer_service = providers.Singleton(
        KafkaProducerService,
        kafka_producer=providers.Singleton(
            KafkaProducer,
            bootstrap_servers=settings.KAFKA_BOOTSTRAP_SERVERS,
            value_serializer=lambda v: json.dumps(v).encode("utf-8"),
        ),
    )
    auth_service = providers.Singleton(
        AuthService,
        user_repository=providers.Factory(_get_user_and_auth_repository),
    )
    user_service = providers.Singleton(
        UserService,
        user_repository=providers.Factory(_get_user_and_auth_repository),
    )
    summary_service = providers.Singleton(
        SummaryService,
        db=get_db,
    )
    api_key_service = providers.Singleton(
        ClientApiKeyService,
        api_key_repository=providers.Factory(_get_client_api_key_repository),
    )
    redis = providers.Factory(get_redis_client)
    storage_service = providers.Factory(Storage)
    oauth = providers.Singleton(OAuthService)
