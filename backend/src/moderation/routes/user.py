import http

from dependency_injector.wiring import Provide, inject
from moderation.auth.common import required_scopes
from moderation.core.container import Container
from moderation.permissions.constants import ADMIN
from moderation.service.user import UserService


@inject
@required_scopes([ADMIN])
def list_users(user_service: UserService = Provide[Container.user_service]):
    """List all users - admin function"""
    return user_service.list_users(), http.HTTPStatus.OK


@inject
@required_scopes([ADMIN])
def get_user(user_id: str, user_service: UserService = Provide[Container.user_service]):
    """Get user details by ID - admin function"""
    return user_service.get_user(user_id), http.HTTPStatus.OK


@inject
@required_scopes([ADMIN])
def delete_user(user_id: str, user_service: UserService = Provide[Container.user_service]):
    """Delete user by ID - admin function"""
    return user_service.delete_user(user_id), http.HTTPStatus.OK
