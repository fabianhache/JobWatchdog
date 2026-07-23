import json
import os
from pathlib import Path

from dotenv import load_dotenv

# Project root
ROOT_DIR = Path(__file__).resolve().parent.parent

load_dotenv(ROOT_DIR / ".env")

# Configuration file
CONFIG_FILE = ROOT_DIR / "config.json"

# Default configuration
DEFAULT_CONFIG = {
    "stepes_url": "https://translator.stepes.com/stepes-check-jobs.html",
    "check_interval": 30,
    "browser_restart_delay": 5,
    "headless": False,
    "minimum_price": 0,
    "minimum_words": 0,
    "languages": [],
    "notifications": {
        "windows": True,
        "telegram": False,
    },
}


def load_config() -> dict:
    """
    Load the application configuration from config.json.

    If the file cannot be read, default values are used.
    Missing keys are automatically filled with defaults.
    """

    config = DEFAULT_CONFIG.copy()

    if not CONFIG_FILE.exists():
        return config

    try:
        with open(CONFIG_FILE, "r", encoding="utf-8") as file:
            user_config = json.load(file)

        # Merge top-level values
        config.update(
            {key: value for key, value in user_config.items() if key != "notifications"}
        )

        # Merge notification settings
        if "notifications" in user_config:
            config["notifications"].update(user_config["notifications"])

    except Exception as error:
        print(f"Warning: Unable to read config.json: {error}")
        print("Using default configuration.")

    return config


# Load configuration once
config = load_config()

# URLs
STEPES_URL = config.get(
    "stepes_url",
    DEFAULT_CONFIG["stepes_url"],
)

# Browser
PROFILE_DIR = ROOT_DIR / "browser_profile"

# Files
HISTORY_FILE = ROOT_DIR / "logs" / "history.txt"

# Monitoring
CHECK_INTERVAL = config.get(
    "check_interval",
    DEFAULT_CONFIG["check_interval"],
)

BROWSER_RESTART_DELAY = config.get(
    "browser_restart_delay",
    DEFAULT_CONFIG["browser_restart_delay"],
)

HEADLESS = config.get(
    "headless",
    DEFAULT_CONFIG["headless"],
)

# Filters
MINIMUM_PRICE = config.get(
    "minimum_price",
    DEFAULT_CONFIG["minimum_price"],
)

MINIMUM_WORDS = config.get(
    "minimum_words",
    DEFAULT_CONFIG["minimum_words"],
)

LANGUAGES = config.get(
    "languages",
    DEFAULT_CONFIG["languages"],
)

# Notifications
WINDOWS_NOTIFICATIONS = config["notifications"].get(
    "windows",
    DEFAULT_CONFIG["notifications"]["windows"],
)

TELEGRAM_NOTIFICATIONS = config["notifications"].get(
    "telegram",
    DEFAULT_CONFIG["notifications"]["telegram"],
)

NOTIFICATION_TITLE = "🟢 New project available"

# Authentication
STEPES_USERNAME = os.getenv("STEPES_USERNAME")
STEPES_PASSWORD = os.getenv("STEPES_PASSWORD")
