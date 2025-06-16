import logging
from typing import Any, Dict

from moderation.mailer.clients.base import EmailClient

logger = logging.getLogger(__name__)


class StdoutEmailClient(EmailClient):
    def send(self, email_params: Dict[str, Any]) -> bool:
        logger.info(f"Sending email {email_params}")
        return True
