"""
Telegram notification utilities.
"""

from __future__ import annotations

import os

import requests
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")


def send_telegram_message(message: str) -> bool:
    """
    Send a Telegram message.

    Returns:
        True if the message was sent successfully.
    """
    if not BOT_TOKEN or not CHAT_ID:
        raise ValueError(
            "Telegram credentials were not found in the .env file."
        )

    response = requests.post(
        f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
        json={
            "chat_id": CHAT_ID,
            "text": message,
        },
        timeout=10,
    )

    response.raise_for_status()

    return True