import logging

from connexion.exceptions import ClientProblem
from moderation.jwt.jwt_handler import JwtTokenHandler

logger = logging.getLogger(__name__)


def bearer_auth(token: str) -> dict:
    try:
        token = token.removeprefix("Bearer ").strip()
        payload = JwtTokenHandler().decode_token(token)
        if not payload or "user_id" not in payload:
            raise ValueError("Missing user_id in token payload")

        return {"uid": payload["user_id"], "scopes": payload.get("scopes", [])}

    except Exception as e:
        logger.warning(f"Invalid bearer token: {e}")
        raise ClientProblem(title="Invalid token")
