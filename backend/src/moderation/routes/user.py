import http


def list_users():
    """List all users - admin function"""
    return [
        {"id": "123", "email": "user1@example.com", "role": "user"},
        {"id": "456", "email": "user2@example.com", "role": "admin"},
    ], http.HTTPStatus.OK


def get_user(user_id):
    """Get specific user by ID - admin function"""
    return {
        "id": user_id,
        "email": f"user{user_id}@example.com",
        "role": "user",
    }, http.HTTPStatus.OK


def delete_user(user_id):
    """Delete a user by ID - admin function"""
    return {}, http.HTTPStatus.NO_CONTENT
