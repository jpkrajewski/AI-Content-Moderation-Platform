from http import HTTPStatus

from dependency_injector.wiring import Provide, inject
from moderation.core.container import Container
from moderation.service.client_api_key import ClientApiKeyService


@inject
def create(
    body: dict,
    api_key_service: ClientApiKeyService = Provide[Container.api_key_service],
):
    """
    Create a new API key.
    :param body: A dictionary containing the source and current_scope.
    :param api_key_service: Injected ClientApiKeyService instance.
    :return: The created API key.
    """
    try:
        # Use the service to create the API key
        source = body["source"]
        current_scope = body["current_scope"]
        client_id = body["client_id"]
        created_key = api_key_service.create_api_key(
            client_id=client_id,
            source=source,
            current_scope=current_scope,
        )
        return created_key, HTTPStatus.CREATED
    except Exception as e:
        return {"detail": str(e)}, HTTPStatus.INTERNAL_SERVER_ERROR


@inject
def get(client_id: str | None = None, api_key_service: ClientApiKeyService = Provide[Container.api_key_service]):
    """
    Get all API keys for a given client ID.
    :param client_id: The client ID to filter API keys.
    :param api_key_service: Injected ClientApiKeyService instance.
    :return: A list of API keys or an error message.
    """
    try:
        if client_id is None:
            return api_key_service.get(), HTTPStatus.OK
        api_keys = api_key_service.list_api_keys(client_id)
        if not api_keys:
            return {"detail": "No API keys found for this client"}, HTTPStatus.NOT_FOUND
        return api_keys, HTTPStatus.OK
    except Exception as e:
        return {"detail": str(e)}, HTTPStatus.INTERNAL_SERVER_ERROR


@inject
def delete(api_key_id: str, api_key_service: ClientApiKeyService = Provide[Container.api_key_service]):
    """
    Delete an API key by its ID.
    :param api_key_id: The ID of the API key to delete.
    :param api_key_service: Injected ClientApiKeyService instance.
    :return: A success or error message.
    """
    try:
        success = api_key_service.delete_api_key(api_key_id)
        if success:
            return {"message": "API key deleted successfully"}, HTTPStatus.OK
        else:
            return {"detail": "API key not found"}, HTTPStatus.NOT_FOUND
    except Exception as e:
        return {"detail": str(e)}, HTTPStatus.INTERNAL_SERVER_ERROR


@inject
def deactivate(api_key_id: str, api_key_service: ClientApiKeyService = Provide[Container.api_key_service]):
    """
    Deactivate an API key by its ID.
    :param api_key_id: The ID of the API key to deactivate.
    :param api_key_service: Injected ClientApiKeyService instance.
    :return: A success or error message.
    """
    try:
        deactivated_key = api_key_service.deactivate_api_key(api_key_id)
        if deactivated_key:
            return {"message": "API key deactivated successfully"}, HTTPStatus.OK
        else:
            return {"detail": "API key not found"}, HTTPStatus.NOT_FOUND
    except Exception as e:
        return {"detail": str(e)}, HTTPStatus.INTERNAL_SERVER_ERROR


@inject
def reactivate(api_key_id: str, api_key_service: ClientApiKeyService = Provide[Container.api_key_service]):
    """
    Reactivate an API key by its ID.
    :param api_key_id: The ID of the API key to reactivate.
    :param api_key_service: Injected ClientApiKeyService instance.
    :return: A success or error message.
    """
    try:
        reactivated_key = api_key_service.reactivate_api_key(api_key_id)
        if reactivated_key:
            return {"message": "API key reactivated successfully"}, HTTPStatus.OK
        else:
            return {"detail": "API key not found"}, HTTPStatus.NOT_FOUND
    except Exception as e:
        return {"detail": str(e)}, HTTPStatus.INTERNAL_SERVER_ERROR
