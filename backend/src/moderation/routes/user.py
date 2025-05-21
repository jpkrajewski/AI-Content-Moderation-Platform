from http import HTTPStatus

from dependency_injector.wiring import Provide, inject
from moderation.core.container import Container
from moderation.service.user import UserService


@inject
def list_users(user_service: UserService = Provide[Container.user_service]):
    """List all users - admin function"""
    return user_service.list_users(), HTTPStatus.OK


@inject
def get_user(user_id: str, user_service: UserService = Provide[Container.user_service]):
    """Get user details by ID - admin function"""
    return user_service.get_user(user_id), HTTPStatus.OK


@inject
def delete_user(user_id: str, user_service: UserService = Provide[Container.user_service]):
    """Delete user by ID - admin function"""
    return user_service.delete_user(user_id), HTTPStatus.OK
