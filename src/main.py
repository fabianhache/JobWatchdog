from browser import launch_browser
from history import load_history
from logger import logger
from monitor import initialize_history, monitor_projects

SEPARATOR = "=" * 50


def main() -> None:
    """
    Application entry point.
    """

    logger.info(SEPARATOR)
    logger.info("JobWatchdog started")
    logger.info(SEPARATOR)

    history = load_history()

    logger.info("Loaded %s known project(s).", len(history))

    playwright, browser, page = launch_browser()

    initialize_history(page, history)

    try:
        monitor_projects(page, history)

    except KeyboardInterrupt:
        logger.info("Stopping JobWatchdog...")

    finally:
        browser.close()
        playwright.stop()

        logger.info("Browser closed.")


if __name__ == "__main__":
    main()
