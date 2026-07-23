# JobWatchdog

JobWatchdog is a Python application that monitors the Stepes Translator job board and automatically notifies the user when new projects become available.

The application keeps the browser session authenticated, periodically scans the job board, detects only newly published projects, applies configurable filters, and sends notifications through Windows and Telegram.

## Features

- Automatic authentication
- Persistent browser session
- Automatic browser recovery after unexpected closure
- Configurable monitoring interval
- Project history to avoid duplicate notifications
- Project filtering
  - Minimum price
  - Minimum word count
  - Language filters
- Windows desktop notifications
- Telegram notifications
- Configurable headless mode
- JSON configuration
- Environment variable support for credentials

## Technologies

- Python 3
- Playwright
- python-dotenv
- winotify
- Telegram Bot API

## Project Structure

```
JobWatchdog/
│
├── browser.py
├── authentication.py
├── config.py
├── detector.py
├── filters.py
├── history.py
├── logger.py
├── main.py
├── models.py
├── monitor.py
├── notifications.py
├── telegram_notifier.py
│
├── browser_profile/
├── logs/
│
├── config.json
├── .env
└── requirements.txt
```

## Configuration

Application settings are stored in `config.json`.

Example:

```json
{
    "check_interval": 30,
    "browser_restart_delay": 5,
    "headless": true,
    "minimum_price": 0,
    "minimum_words": 0,
    "languages": [],
    "notifications": {
        "windows": true,
        "telegram": true
    }
}
```

Credentials are stored in `.env`.

```
STEPES_USERNAME=your_email
STEPES_PASSWORD=your_password

TELEGRAM_BOT_TOKEN=xxxxxxxx
TELEGRAM_CHAT_ID=xxxxxxxx
```

## Installation

Clone the repository:

```bash
git clone https://github.com/<username>/JobWatchdog.git
cd JobWatchdog
```

Create a virtual environment:

```bash
python -m venv .venv
```

Activate it:

Windows

```bash
.venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Create the `.env` file.

Adjust `config.json` if needed.

Run the application:

```bash
python src/main.py
```

## How It Works

1. Launches a persistent browser session.
2. Authenticates if necessary.
3. Performs an initial scan.
4. Stores existing project IDs.
5. Periodically refreshes the job board.
6. Detects newly published projects.
7. Applies user-defined filters.
8. Sends notifications.
9. Automatically recovers if the browser is unexpectedly closed.

## Roadmap

- Unit tests
- GitHub Actions
- Executable package with PyInstaller
- Additional notification providers

## License

This project is intended for educational and portfolio purposes.