from unittest.mock import MagicMock

import pytest
from moderation.app import create_app
from moderation.core.container import Container
from moderation.service.auth import AuthService
from moderation.service.user import UserService
from starlette.testclient import TestClient


@pytest.fixture
def client():
    """
    Provides a test client for the ASGI app, usable in tests.
    """
    with TestClient(create_app(), "http://testserver/api/v1") as client:
        yield client


@pytest.fixture(autouse=True)
def override_user_service():
    mock_user_service = MagicMock(spec=UserService)
    mock_user = MagicMock()
    mock_user.email = "test@example.com"
    mock_user.username = "testuser"
    mock_user.role = "user_role"
    mock_user.id = "1"

    mock_user_service.get_user.return_value = mock_user
    with Container.user_service.override(mock_user_service):
        yield mock_user_service


@pytest.fixture(autouse=True)
def override_auth_service():
    mock_auth_service = MagicMock(spec=AuthService)
    mock_auth_service.register.return_value = (True, None)
    # Mock authenticate for login
    mock_user = MagicMock()
    mock_user.id = "some-uuid"
    mock_user.role = "user_role"
    mock_auth_service.authenticate.return_value = (True, mock_user)

    with Container.auth_service.override(mock_auth_service):
        yield
