import http


def register(body):
    return {}, http.HTTPStatus.OK


def login(body):
    print(body)
    return {"token": "valid-token"}, http.HTTPStatus.OK


def me(*args, **kwargs):
    print(kwargs)
    print(args)
    return {"id": 1, "email": "user@example.com"}, http.HTTPStatus.OK
