import http
import logging

from connexion.exceptions import ClientProblem, ServerError
from dependency_injector.wiring import Provide, inject
from moderation.core.container import Container
from moderation.helpers.jwt_token import JwtTokenHandler
from moderation.service.auth import AuthService
from moderation.service.user import UserService

logger = logging.getLogger(__name__)


@inject
def register(body: dict, auth_service: AuthService = Provide[Container.auth_service]):
    """Register a new user"""
    try:
        email = body["email"]
        username = body["username"]
        password = body["password"]
    except KeyError as e:
        raise ClientProblem(title=f"Invalid payload: Missing required field: {e}")
    exists = auth_service.check_email_exists(email)
    if exists:
        raise ClientProblem(title="Email already exists")
    result, _ = auth_service.register(email=email, username=username, password=password)
    if not result:
        raise ServerError(title="Failed to create user, please try again")
    return {"status": "created"}, http.HTTPStatus.OK


@inject
def login(body: dict, auth_service: AuthService = Provide[Container.auth_service]):
    logger.info("Login request: %s", body)
    try:
        username = body["username"]
        password = body["password"]
    except KeyError as e:
        raise ClientProblem(title=f"Invalid payload: Missing required field: {e}")
    result, user = auth_service.authenticate(username, password)
    if not result:
        raise ClientProblem(title="Invalid credentials")
    token = JwtTokenHandler().generate_token(user_id=user.id, scopes=user.role)
    return {"token": token}, http.HTTPStatus.OK


@inject
def me(user: int, user_service: UserService = Provide[Container.user_service]):
    user_ = user_service.get_user(user)
    if not user_:
        raise ClientProblem("User not found")
    return {"email": user_.email, "username": user_.username, "scope": user_.role}, http.HTTPStatus.OK
