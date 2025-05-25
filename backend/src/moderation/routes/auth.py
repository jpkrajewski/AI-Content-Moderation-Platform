import logging
from http import HTTPStatus
from typing import Any, Dict, Tuple
from uuid import UUID

from connexion.exceptions import ClientProblem, ServerError
from dependency_injector.wiring import Provide, inject
from moderation.core.container import Container
from moderation.helpers.jwt_token import JwtTokenHandler
from moderation.service.auth import AuthService
from moderation.service.user import UserService

logger = logging.getLogger(__name__)


@inject
def register(
    body: Dict[str, Any],
    auth_service: AuthService = Provide[Container.auth_service],
) -> Tuple[Dict[str, str], HTTPStatus]:
    """Register a new user."""
    try:
        email = body["email"]
        username = body["username"]
        password = body["password"]
    except KeyError as e:
        raise ClientProblem(title=f"Invalid payload: Missing required field: {e.args[0]}")

    result, _ = auth_service.register(email=email, username=username, password=password)
    if not result:
        raise ServerError(title="Failed to create user, please try again")

    return {"status": "created"}, HTTPStatus.OK


@inject
def login(
    body: Dict[str, Any],
    auth_service: AuthService = Provide[Container.auth_service],
) -> Tuple[Dict[str, str], HTTPStatus]:
    """Authenticate a user and return a JWT token."""
    try:
        email = body["email"]
        password = body["password"]
    except KeyError as e:
        raise ClientProblem(title=f"Invalid payload: Missing required field: {e.args[0]}")

    result, user = auth_service.authenticate(email, password)
    if not result or user is None:
        raise ClientProblem(title="Invalid credentials")

    token = JwtTokenHandler().generate_token(user_id=user.id, scopes=[user.role])
    return {"token": token}, HTTPStatus.OK


@inject
def me(
    user: UUID,
    user_service: UserService = Provide[Container.user_service],
) -> Tuple[Dict[str, str], HTTPStatus]:
    """Retrieve the authenticated user's profile."""
    user_ = user_service.get_user(user)
    if not user_:
        raise ClientProblem(title="User not found")

    return {
        "email": user_.email,
        "username": user_.username,
        "scope": user_.role,
    }, HTTPStatus.OK
