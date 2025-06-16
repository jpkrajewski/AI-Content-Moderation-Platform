import logging

import pytest
from moderation.core.settings import settings
from moderation.mailer import send_email
from moderation.mailer.clients.stdout_client import StdoutEmailClient


@pytest.fixture(autouse=True)
def default_client():
    settings.RESEND_API_KEY = ""


def test_send_mail():
    result = send_email(
        subject="Test subject",
        html_content="<p>Test content</p>",
    )

    assert result


def test_stdout_client(caplog):
    client = StdoutEmailClient()

    with caplog.at_level(logging.INFO):
        result = client.send(
            email_params={"subject": "Test subject", "html_content": "<p>Test content</p>"},
        )

    assert "Test subject" in caplog.text
    assert "Test content" in caplog.text
    assert result is True
