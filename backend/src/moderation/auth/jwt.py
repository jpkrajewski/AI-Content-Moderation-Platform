import logging

from moderation.auth.common import check_scopes
from moderation.helpers.jwt_token import JwtTokenHandler

logger = logging.getLogger("moderation")


def bearer_auth(token: str, required_scopes: list[str] | None):
    token = token.removeprefix("Bearer ")
    payload: dict = JwtTokenHandler().decode_token(token)
    scopes = payload.get("scopes", [])
    check_scopes(scopes, required_scopes)
    return {"uid": payload["user_id"], "scopes": scopes}
