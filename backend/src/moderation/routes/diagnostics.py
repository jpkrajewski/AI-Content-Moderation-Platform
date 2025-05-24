import logging
from http import HTTPStatus

from flask import jsonify

logger = logging.getLogger(__name__)


def check_jwt(token_info, user, *args, **kwargs):
    """
    Endpoint to check JWT authentication.
    Returns 200 if the JWT is valid, otherwise 400.
    """
    try:
        return (
            jsonify(
                {
                    "message": "JWT is valid",
                    "func": {
                        "token": token_info,
                        "user": user,
                        "args": args,
                        "kwargs": kwargs,
                    },
                }
            ),
            HTTPStatus.OK,
        )
    except Exception as e:
        logger.error("JWT validation failed", exc_info=True)
        return jsonify({"message": "JWT validation failed"}), HTTPStatus.BAD_REQUEST


def check_client_api_key(token_info, user, *args, **kwargs):
    """
    Endpoint to check API key authentication.
    Returns 200 if the API key is valid, otherwise 400.
    """
    try:
        # If the request reaches this point, the API key is valid
        logger.info(f"Checking API key token: {token_info}")
        logger.info(f"User: {user}")
        return (
            jsonify(
                {
                    "message": "API key is valid",
                    "func": {
                        "token": token_info,
                        "user": user,
                        "args": args,
                        "kwargs": kwargs,
                    },
                }
            ),
            HTTPStatus.OK,
        )
    except Exception as e:
        logger.error("API key validation failed", exc_info=True)
        return jsonify({"message": "API key validation failed"}), HTTPStatus.BAD_REQUEST
