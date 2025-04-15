import http


def register(body):
    return {}, http.HTTPStatus.OK


def login(body):
    return {"token": "example_token"}, http.HTTPStatus.OK


def me():
    return {"id": 1, "email": "user@example.com"}, http.HTTPStatus.OK
