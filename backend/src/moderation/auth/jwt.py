import logging

from connexion.exceptions import ClientProblem
from moderation.helpers.jwt_token import JwtTokenHandler

logger = logging.getLogger("moderation")


def bearer_auth(token: str) -> dict:
    token = token.removeprefix("Bearer ")
    payload: dict = JwtTokenHandler().decode_token(token)
    if not payload:
        raise ClientProblem(title="Invalid token")
    scopes = payload.get("scopes", [])
    return {"uid": payload["user_id"], "scopes": scopes}
