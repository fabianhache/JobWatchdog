from config import (
    NOTIFICATION_TITLE,
    TELEGRAM_NOTIFICATIONS,
    WINDOWS_NOTIFICATIONS,
)
from formatter import format_notification
from models import JobProject
from telegram_notifications import send_telegram_message

from win11toast import toast


def notify(job: JobProject) -> None:
    """
    Send notifications for a newly detected project.
    """

    message = format_notification(job)

    if WINDOWS_NOTIFICATIONS:
        try:
            toast(
                NOTIFICATION_TITLE,
                message,
                duration="short",
            )
        except Exception as error:
            print(f"Windows notification failed: {error}")

    if TELEGRAM_NOTIFICATIONS:
        try:
            send_telegram_message(f"{NOTIFICATION_TITLE}\n\n{message}")
        except Exception as error:
            print(f"Telegram notification failed: {error}")
