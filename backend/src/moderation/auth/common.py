import logging

from connexion.exceptions import ClientProblem

logger = logging.getLogger(__name__)


def check_scopes(scopes: list[str] | None, required_scopes: list[str] | None):
    if required_scopes is None:
        return
    if scopes is None:
        scopes = []
    if not set(required_scopes).issubset(set(scopes)):
        raise ClientProblem(
            title="Insufficient scopes",
        )


def required_scopes(required_scopes: list[str] | None):
    def decorator(func):
        def wrapper(*args, **kwargs):
            scopes = kwargs.get("token_info", {}).get("scopes", None)
            check_scopes(scopes, required_scopes)
            return func(*args, **kwargs)

        return wrapper

    return decorator
