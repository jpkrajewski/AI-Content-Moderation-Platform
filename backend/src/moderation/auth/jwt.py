def bearer_auth(token, required_scopes):
    # Here you would validate the token (JWT for example)
    if token == "valid-token":  # nosec
        return {"sub": "user-id"}
    else:
        return None  # or raise an error
