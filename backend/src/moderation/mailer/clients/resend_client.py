import logging
from typing import Any, Dict

import resend
from moderation.core.settings import settings
from moderation.mailer.clients.base import EmailClient
from resend import Emails

logger = logging.getLogger(__name__)


class ResendEmailClient(EmailClient):
    def __init__(self):
        resend.api_key = settings.RESEND_API_KEY

    def send(self, email_params: Dict[str, Any]) -> bool:
        try:
            Emails.send(Emails.SendParams(**email_params))
            return True
        except Exception as e:
            logger.exception(e)
            return False
