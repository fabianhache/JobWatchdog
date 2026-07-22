# JobWatchdog

![Python CI](https://github.com/fabianhache/JobWatchdog/actions/workflows/python.yml/badge.svg)

JobWatchdog is a Python application that monitors the Stepes job board and notifies the user whenever a new translation project becomes available.

## Features

- Real-time monitoring of the Stepes job board
- Browser automation with Playwright
- Persistent project history
- Duplicate project detection
- Configurable filtering (price, words and language)
- JSON-based configuration
- Windows desktop notifications
- Unit tests with Pytest

## Technologies

- Python 3.13
- Playwright
- Win11Toast
- Pytest
- Black
- Ruff

## Project Structure

```
JobWatchdog/
├── assets/
├── browser_profile/
├── logs/
├── src/
│   ├── browser.py
│   ├── config.py
│   ├── detector.py
│   ├── filters.py
│   ├── history.py
│   ├── logger.py
│   ├── main.py
│   ├── models.py
│   ├── monitor.py
│   └── notifications.py
├── tests/
│   ├── test_config.py
│   ├── test_filters.py
│   └── test_history.py
├── config.json
├── conftest.py
├── pyproject.toml
├── requirements.txt
└── README.md
```

## Installation

Clone the repository:

```bash
git clone https://github.com/fabianhache/JobWatchdog.git
cd JobWatchdog
```

Create a virtual environment:

```bash
python -m venv .venv
```

Activate it:

**Windows**

```bash
.venv\Scripts\activate
```

**macOS / Linux**

```bash
source .venv/bin/activate
```

Install the dependencies:

```bash
pip install -r requirements.txt
```

Install the Playwright browser:

```bash
playwright install
```

## Configuration

The application can be configured through the `config.json` file.

Available options include:

- Monitoring interval
- Minimum project price
- Minimum word count
- Allowed language pairs
- Windows notifications

## Usage

Run the application:

```bash
python src/main.py
```

The first time the application runs, a Chromium browser window will open and you will need to sign in to your Stepes account. The browser profile is saved locally and reused in future sessions.

## Planned Features

- Telegram notifications
- Discord notifications
- Email notifications
- Project scoring
- CSV export
- Executable (.exe)

## Development Status

- ✅ Configuration system
- ✅ Filtering
- ✅ Persistent history
- ✅ Logging
- ✅ Unit tests
- ✅ GitHub repository
- ⏳ GitHub Actions
- ⏳ Telegram notifications
- ⏳ CSV export
- ⏳ Project scoring


## License

This project is licensed under the MIT License.