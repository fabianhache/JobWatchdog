import json
from pathlib import Path

# Project root
ROOT_DIR = Path(__file__).resolve().parent.parent

# Configuration file
CONFIG_FILE = ROOT_DIR / "config.json"

# Default configuration
DEFAULT_CONFIG = {
    "stepes_url": "https://translator.stepes.com/stepes-check-jobs.html",
    "check_interval": 30,
    "minimum_price": 0,
    "minimum_words": 0,
    "languages": [],
    "notifications": {"windows": True},
}


def load_config() -> dict:
    """
    Load the application configuration from config.json.

    If the configuration file cannot be read, default values are used.
    """

    if not CONFIG_FILE.exists():
        return DEFAULT_CONFIG

    try:
        with open(CONFIG_FILE, "r", encoding="utf-8") as file:
            return json.load(file)

    except Exception:
        print("Warning: Unable to read config.json. Using default configuration.")
        return DEFAULT_CONFIG


# Load configuration once
config = load_config()

# URLs
STEPES_URL = config["stepes_url"]

# Browser
PROFILE_DIR = ROOT_DIR / "browser_profile"

# Files
HISTORY_FILE = ROOT_DIR / "logs" / "history.txt"

# Monitoring
CHECK_INTERVAL = config["check_interval"]

# Filters
MINIMUM_PRICE = config["minimum_price"]
MINIMUM_WORDS = config["minimum_words"]
LANGUAGES = config["languages"]

# Notifications
WINDOWS_NOTIFICATIONS = config["notifications"]["windows"]
NOTIFICATION_TITLE = "🟢 New project available"
