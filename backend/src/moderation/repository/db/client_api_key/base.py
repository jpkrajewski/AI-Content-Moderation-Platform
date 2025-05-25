from abc import ABC, abstractmethod
from dataclasses import asdict, dataclass
from typing import Any, List, Optional


@dataclass
class ClientApiKey:
    """Data class to represent a client API key."""

    id: str
    source: str
    client_id: str
    api_key: str
    current_scope: List[str]
    created_at: Optional[str] = None
    updated_at: Optional[str] = None
    last_accessed: Optional[str] = None
    access_count: Optional[int] = 0
    is_active: bool = True

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


class AbstractClientApiKeyRepository(ABC):
    """Abstract base class for client API key repository."""

    @abstractmethod
    def list(self, client_id: Optional[str] = None) -> List[ClientApiKey]:
        """
        List all API keys, optionally filtered by client ID.
        :param client_id: Optional client ID to filter API keys.
        :return: A list of client API keys.
        """

    @abstractmethod
    def get_by_id(self, api_key_id: str) -> Optional[ClientApiKey]:
        """
        Get an API key by its ID.
        :param api_key_id: The ID of the API key.
        :return: The client API key if found, otherwise None.
        """

    @abstractmethod
    def get_by_api_key(self, api_key_id: str) -> Optional[ClientApiKey]:
        """
        Get an API key by its API Key.
        :param api_key_id: The ID of the API key.
        :return: The client API key if found, otherwise None.
        """

    @abstractmethod
    def create(self, api_key: ClientApiKey) -> ClientApiKey:
        """
        Create a new API key.
        :param api_key: The API key to create.
        :return: The created client API key.
        """

    @abstractmethod
    def update(self, api_key_id: str, data: dict) -> Optional[ClientApiKey]:
        """
        Update an API key's properties.
        :param api_key_id: The ID of the API key to update.
        :param data: A dictionary of fields to update.
        :return: The updated client API key if found, otherwise None.
        """

    @abstractmethod
    def deactivate(self, api_key_id: str) -> Optional[ClientApiKey]:
        """
        Deactivate an API key.
        :param api_key_id: The ID of the API key to deactivate.
        :return: The deactivated client API key if found, otherwise None.
        """

    @abstractmethod
    def reactivate(self, api_key_id: str) -> Optional[ClientApiKey]:
        """
        Reactivate an API key.
        :param api_key_id: The ID of the API key to reactivate.
        :return: The reactivated client API key if found, otherwise None.
        """

    @abstractmethod
    def delete(self, api_key_id: str) -> bool:
        """
        Delete an API key by its ID.
        :param api_key_id: The ID of the API key to delete.
        :return: True if the API key was deleted, otherwise False.
        """

    @abstractmethod
    def get_usage_stats(self) -> dict:
        """
        Get usage statistics for API keys.
        :return: A dictionary containing usage statistics (e.g., total, active, inactive keys).
        """
