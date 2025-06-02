import logging
from http import HTTPStatus
from typing import Any, Dict, Tuple
from uuid import UUID

from authlib.integrations.flask_client import OAuth
from connexion.exceptions import ClientProblem, ServerError
from dependency_injector.wiring import Provide, inject
from flask import redirect, url_for

from moderation.core.container import Container
from moderation.core.settings import settings
from moderation.jwt.jwt_handler import JwtTokenHandler
from moderation.service.auth import AuthService
from moderation.service.oauth.models import UserInfo
from moderation.service.oauth.oauth import OAuthService
from moderation.service.user import UserService

logger = logging.getLogger(__name__)


@inject
def register(
    body: Dict[str, Any],
    auth_service: AuthService = Provide[Container.auth_service],
) -> Tuple[Dict[str, str], HTTPStatus]:
    """Register a new user."""
    email = body["email"]
    username = body["username"]
    password = body["password"]
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
    email = body["email"]
    password = body["password"]
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
        "uid": str(user),
        "email": user_.email,
        "username": user_.username,
        "scope": user_.role,
    }, HTTPStatus.OK

@inject
def oauth_login(oauth: OAuth = Provide[Container.oauth]):
    redirect_uri = url_for('/api/v1.moderation_routes_auth_oauth_callback', _external=True)
    return oauth.google.authorize_redirect(redirect_uri)

@inject
def oauth_callback(
    code: str | None = None,
    state: str | None = None,
    scope: str | None = None,
    authuser: str | None = None,
    prompt: str | None = None,
    oauth: OAuthService = Provide[Container.oauth],
    auth_service: AuthService = Provide[Container.auth_service],
    user_service: UserService = Provide[Container.user_service],
):
    """
    Handles OAuth callback by authorizing access token and redirecting to frontend with JWT token.
    """
    # This will use internal request.args['code'] etc. even though they're passed in as args.
    user_info = oauth.authorize()
    if not user_service.exists(user_info.email):
        result, user = auth_service.register(
            email=user_info.email,
            password="",
            username=user_info.email,
            role="external",
        )
        if not result:
            raise ServerError(title="Failed to create user, please try again")
    else:
        user = user_service.get_user_by_username(user_info.email)


    token = JwtTokenHandler().generate_token(user_id=user.id, scopes=user.role)

    # Redirect with token as query param
    return redirect(f"{settings.FRONTEND_OAUTH_CALLBACK}{token}", code=302)

