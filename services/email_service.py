"""Email service providing simple SMTP sending with optional attachments.

Uses settings for SMTP configuration. Intended for local development using MailHog.
"""

from typing import List
import logging
import os
import smtplib
from email.message import EmailMessage
from core.settings import settings

logger = logging.getLogger(__name__)


def send_email(to: str, subject: str, body: str, attachments: List[str] | None = None) -> bool:
    """Send an email via SMTP.

    Parameters:
    - to: recipient email address
    - subject: subject line
    - body: plain text body
    - attachments: list of file paths to attach

    Returns True on success, False otherwise. Logs any errors encountered.
    """
    msg = EmailMessage()
    msg["From"] = settings.SMTP_FROM
    msg["To"] = to
    msg["Subject"] = subject
    msg.set_content(body)

    # Attach files if provided
    for path in attachments or []:
        if not os.path.exists(path):
            logger.warning(f"Attachment path does not exist: {path}")
            continue
            # continue prevents reading missing file
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

    try:
        # For MailHog no auth/TLS by default
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
