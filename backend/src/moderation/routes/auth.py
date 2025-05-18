import http


def register(body):
    return {}, http.HTTPStatus.OK


def login(body):
    return {"token": "valid-token"}, http.HTTPStatus.OK


def me(*args, **kwargs):
    return {"id": 1, "email": "user@example.com"}, http.HTTPStatus.OK
