import http
import logging

from moderation.helpers.jwt_token import JwtTokenHandler

logger = logging.getLogger(__name__)


def register(body):
    return {}, http.HTTPStatus.OK


def login(body):
    token = JwtTokenHandler().generate_token(user_id="1", scopes=["content:read", "content:write"])
    return {"token": token}, http.HTTPStatus.OK


def me(user: int, token_info: dict):
    logger.info((user, token_info))
    print(user, token_info)
    return {"id": 1, "email": "user@example.com"}, http.HTTPStatus.OK
