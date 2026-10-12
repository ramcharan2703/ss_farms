
import logging
import os

import resend
from django.core.mail.backends.base import BaseEmailBackend

logger = logging.getLogger(__name__)


class ResendEmailBackend(BaseEmailBackend):
    """Send Django emails through Resend's HTTPS API."""

    def __init__(self, fail_silently=False, **kwargs):
        super().__init__(fail_silently=fail_silently, **kwargs)
        self.api_key = os.environ.get("RESEND_API_KEY", "").strip()

    def send_messages(self, email_messages):
        if not email_messages:
            return 0

        if not self.api_key:
            logger.error("Resend email backend: RESEND_API_KEY is missing.")
            if self.fail_silently:
                return 0
            raise RuntimeError("RESEND_API_KEY is not configured.")

        resend.api_key = self.api_key
        sent_count = 0

        for message in email_messages:
            try:
                recipients = list(message.to or [])
                recipients.extend(message.cc or [])
                recipients.extend(message.bcc or [])

                if not recipients:
                    continue

                payload = {
                    "from": os.environ.get(
                        "RESEND_FROM_EMAIL",
                        "SS Farms <onboarding@resend.dev>",
                    ),
                    "to": recipients,
                    "subject": message.subject or "",
                    "text": message.body or "",
                }

                if message.reply_to:
                    payload["reply_to"] = list(message.reply_to)

                if message.extra_headers:
                    for key in ("X-Entity-Ref-ID",):
                        if key in message.extra_headers:
                            payload[key] = message.extra_headers[key]

                if message.content_subtype == "html":
                    payload["html"] = message.body or ""
                    payload.pop("text", None)

                response = resend.Emails.send(payload)

                if not response or not response.get("id"):
                    raise RuntimeError(
                        "Resend did not return an email ID."
                    )

                sent_count += 1
                logger.info(
                    "Email accepted by Resend. Email ID: %s",
                    response["id"],
                )

            except Exception:
                logger.exception(
                    "Resend failed to send email with subject %r.",
                    message.subject,
                )
                if not self.fail_silently:
                    raise

        return sent_count
