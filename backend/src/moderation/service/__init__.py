from functools import cache

from moderation.db.session import get_db
from moderation.repository.db.client_api_key.database import DatabaseClientApiKeyRepository
from moderation.service.apikey.apikeys_service import ClientApiKeyService


@cache
def get_client_api_key_service():
    return ClientApiKeyService(api_key_repository=DatabaseClientApiKeyRepository(db=get_db))
