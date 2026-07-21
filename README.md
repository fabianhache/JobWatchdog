# JobWatchdog

JobWatchdog is a Python application that monitors the Stepes job board and notifies the user whenever a new translation project becomes available.

## Features

- Real-time monitoring of the Stepes job board
- Duplicate project detection
- Persistent project history
- Windows desktop notifications
- Browser automation with Playwright

## Technologies

- Python
- Playwright
- Win11Toast

## Project Structure

```
JobWatchdog/
├── assets/
├── browser_profile/
├── logs/
├── src/
│   ├── browser.py
│   ├── detector.py
│   ├── history.py
│   ├── main.py
│   ├── models.py
│   ├── monitor.py
│   └── notifications.py
├── tests/
├── requirements.txt
└── README.md
```

## Installation

Clone the repository:

```bash
git clone https://github.com/your-username/JobWatchdog.git
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
- Project filtering
- Configurable settings
- Logging
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
- ⏳ Project scoring

## License

This project is licensed under the MIT License.