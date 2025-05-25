from moderation.jwt.jwt_handler import JwtTokenHandler


def test_register(client):
    response = client.post(
        "/auth/register",
        json={
            "email": "<EMAIL>",
            "password": "<PASSWORD>",
            "username": "test",
        },
    )
    assert response.status_code == 200


def test_login(client):
    response = client.post(
        "/auth/login",
        json={
            "email": "<EMAIL>",
            "password": "<PASSWORD>",
        },
    )
    assert response.status_code == 200


def test_me_correct_jwt(client):
    jwt = JwtTokenHandler().generate_token("1", scopes=["test"])
    response = client.get("/auth/me", headers={"Authorization": f"Bearer {jwt}"})
    assert response.status_code == 200


def test_me_incorrect_jwt(client):
    response = client.get("/auth/me", headers={"Authorization": "Bearer xxx"})
    assert response.status_code == 400
