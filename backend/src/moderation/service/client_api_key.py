import secrets
import uuid

from moderation.cache.redis import cache_dataclass
from moderation.constants.general import REDIS_PREFIX_KEY_CLIENT_API_KEY
from moderation.repository.db.client_api_key.base import AbstractClientApiKeyRepository, ClientApiKey


class ClientApiKeyService:
    def __init__(self, api_key_repository: AbstractClientApiKeyRepository):
        self.api_key_repository = api_key_repository

    def list_api_keys(self, client_id: str | None = None) -> list[ClientApiKey]:
        """
        List all API keys, optionally filtered by client ID.
        :param client_id: Optional client ID to filter API keys.
        :return: A list of client API keys.
        """
        return self.api_key_repository.list(client_id)

    def get(self) -> list[ClientApiKey]:
        return self.api_key_repository.list()

    def get_api_key(self, api_key_id: str) -> ClientApiKey | None:
        """
        Get an API key by its ID.
        :param api_key_id: The ID of the API key.
        :return: The client API key if found, otherwise None.
        """
        return self.api_key_repository.get_by_id(api_key_id)

    @cache_dataclass(REDIS_PREFIX_KEY_CLIENT_API_KEY, suffix_attr="api_key")
    def create_api_key(self, client_id: str, current_scope: list[str], source: str) -> ClientApiKey:
        """
        Create a new API key.
        :param api_key_data: A dictionary containing API key details (source and current_scope).
        :return: The created client API key.
        """
        # Generate a secure and unique API key
        while True:
            api_key = secrets.token_urlsafe(32)  # Generates a secure 32-character API key
            # Check if the API key already exists in the database
            existing_key = self.api_key_repository.get_by_api_key(api_key)  # Fetch all API keys
            if existing_key is None:
                break  # Exit the loop if the API key is unique

        # Create the ClientApiKey object
        api_key_object = ClientApiKey(
            id=str(uuid.uuid4()),  # Unique ID for the API key
            source=source,
            client_id=client_id,
            api_key=api_key,
            current_scope=current_scope,
            created_at=None,
            updated_at=None,
            last_accessed=None,
            access_count=0,
            is_active=True,
        )

        # Save the API key to the repository
        result = self.api_key_repository.create(api_key_object)
        return result

    @cache_dataclass(REDIS_PREFIX_KEY_CLIENT_API_KEY, suffix_attr="api_key")
    def update_api_key(self, api_key_id: str, api_key_data: dict) -> ClientApiKey | None:
        """
        Update an API key's properties.
        :param api_key_id: The ID of the API key to update.
        :param api_key_data: A dictionary of fields to update.
        :return: The updated client API key if found, otherwise None.
        """
        return self.api_key_repository.update(api_key_id, api_key_data)

    @cache_dataclass(REDIS_PREFIX_KEY_CLIENT_API_KEY, suffix_attr="api_key")
    def deactivate_api_key(self, api_key_id: str) -> ClientApiKey | None:
        """
        Deactivate an API key.
        :param api_key_id: The ID of the API key to deactivate.
        :return: The deactivated client API key if found, otherwise None.
        """
        return self.api_key_repository.deactivate(api_key_id)

    @cache_dataclass(REDIS_PREFIX_KEY_CLIENT_API_KEY, suffix_attr="api_key")
    def reactivate_api_key(self, api_key_id: str) -> ClientApiKey | None:
        """
        Reactivate an API key.
        :param api_key_id: The ID of the API key to reactivate.
        :return: The reactivated client API key if found, otherwise None.
        """
        return self.api_key_repository.reactivate(api_key_id)

    def get_by_api_key(self, api_key: str) -> ClientApiKey | None:
        return self.api_key_repository.get_by_api_key(api_key)
