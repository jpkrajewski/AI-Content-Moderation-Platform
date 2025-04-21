def apikey_auth(key: str, required_scopes: list):
    print(f"API Key: {key}")
    print(f"Required Scopes: {required_scopes}")
    return {"sub": "user-id"}
