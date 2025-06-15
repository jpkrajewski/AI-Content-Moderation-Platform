from typing import List

from moderation.core.settings import settings
from moderation.mailer.clients.base import EmailClient
from moderation.mailer.clients.resend_client import ResendEmailClient
from moderation.mailer.clients.stdout_client import StdoutEmailClient
from moderation.mailer.templates.importer import TemplateType, get_template


def get_provider() -> EmailClient:
    if settings.RESEND_API_KEY:
        return ResendEmailClient()
    else:
        return StdoutEmailClient()


def send_email(
    subject: str,
    html_content: str,
    to: List[str] | None = None,
) -> bool:
    email_params = {
        "from": settings.EMAIL_FROM,
        "to": to or settings.EMAIL_RECIPIENTS,
        "subject": subject,
        "html": html_content,
    }
    provider = get_provider()
    return provider.send(email_params=email_params)


__all__ = [
    "get_template",
    "TemplateType",
    "send_email",
]


def __dir__():
    return __all__
