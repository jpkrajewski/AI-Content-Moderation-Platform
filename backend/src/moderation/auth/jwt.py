from dependency_injector.wiring import Provide, inject
from moderation.core.container import Container


@inject
def bearer_auth(token, required_scopes, auth_service: Container = Provide[Container.auth_service]):
    # Here you would validate the token (JWT for example)
    print(token)
    if token == "valid-token":  # nosec
        return {"sub": "user-id"}
    else:
        return None  # or raise an error
