from connexion.exceptions import Unauthorized


def check_scopes(scopes: list[str] | None, required_scopes: list[str] | None):
    if required_scopes is None:
        return
    if scopes is None:
        scopes = []
    if not set(required_scopes).issubset(set(scopes)):
        raise Unauthorized
