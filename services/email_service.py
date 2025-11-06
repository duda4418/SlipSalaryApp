"""Email service providing simple SMTP sending with optional attachments.

There are two send functions:
1. send_email_dev -> Forces MailHog-style localhost settings regardless of .env overrides.
2. send_email -> Uses the current runtime settings loaded from .env (production/live capable).

Use the *Live* API endpoints to call send_email. Use the non-live endpoints to call send_email_dev.
"""

from typing import List
import logging
import os
import smtplib
from email.message import EmailMessage
from core.settings import settings


DEV_SMTP_HOST = "localhost"
DEV_SMTP_PORT = 1025
DEV_SMTP_FROM = "slipsalaryapp@payroll.com"  # Distinct from production From (can still use settings.SMTP_FROM if preferred)

logger = logging.getLogger(__name__)


def _build_email_message(to: str, subject: str, body: str, attachments: List[str] | None = None, from_addr: str | None = None) -> EmailMessage:
    """Internal helper to construct an EmailMessage with attachments."""
    msg = EmailMessage()
    msg["From"] = from_addr or settings.SMTP_FROM
    msg["To"] = to
    msg["Subject"] = subject
    msg.set_content(body)

    for path in attachments or []:
        if not os.path.exists(path):
            logger.warning(f"Attachment path does not exist: {path}")
            continue
        filename = os.path.basename(path)
        try:
            with open(path, "rb") as f:
                data = f.read()
            msg.add_attachment(
                data,
                maintype="application",
                subtype="octet-stream",
                filename=filename,
            )
        except Exception as e:  # pragma: no cover - defensive
            logger.error(f"Failed reading attachment {path}: {e}")
    return msg


def send_email_dev(to: str, subject: str, body: str, attachments: List[str] | None = None) -> bool:
    """Send an email using forced MailHog localhost settings.

    Ignores .env overrides so accidental real sends cannot happen through dev endpoints.
    """
    msg = _build_email_message(to, subject, body, attachments, from_addr=DEV_SMTP_FROM)
    try:
        with smtplib.SMTP(DEV_SMTP_HOST, DEV_SMTP_PORT, timeout=10) as smtp:
            # MailHog typically does not use TLS or auth.
            smtp.send_message(msg)
        logger.info(f"[DEV] Email sent to {to} subject={subject} attachments={len(attachments or [])}")
        return True
    except Exception as e:
        logger.error(f"[DEV] Failed to send email to {to}: {e}")
        return False


def send_email(to: str, subject: str, body: str, attachments: List[str] | None = None) -> bool:
    """Send an email via SMTP.

    Parameters:
    - to: recipient email address
    - subject: subject line
    - body: plain text body
    - attachments: list of file paths to attach

    Returns True on success, False otherwise. Logs any errors encountered.
    """
    msg = _build_email_message(to, subject, body, attachments)

    try:
        # Production / live capable path: use settings from .env
        with smtplib.SMTP(settings.SMTP_HOST, settings.SMTP_PORT, timeout=10) as smtp:
            if settings.SMTP_TLS:
                try:
                    smtp.starttls()
                except Exception as e:
                    logger.error(f"Failed to start TLS: {e}")
            if settings.SMTP_USERNAME and settings.SMTP_PASSWORD:
                try:
                    smtp.login(settings.SMTP_USERNAME, settings.SMTP_PASSWORD)
                except Exception as e:
                    logger.error(f"SMTP login failed: {e}")
            smtp.send_message(msg)
        logger.info(f"Email sent to {to} subject={subject} attachments={len(attachments or [])}")
        return True
    except Exception as e:
        logger.error(f"Failed to send email to {to}: {e}")
        return False
