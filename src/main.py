import time

from playwright.sync_api import Error

from browser import launch_browser
from config import BROWSER_RESTART_DELAY, HEADLESS
from history import load_history
from logger import logger
from monitor import monitor_projects, populate_history

SEPARATOR = "=" * 50


def run_session(history: set[str], restarted: bool = False) -> None:
    """
    Launch a browser session and monitor projects until the session ends.
    """

    playwright, browser, page, browser_name = launch_browser()

    logger.info(
        "%s: %s (%s)",
        "Browser restarted" if restarted else "Browser",
        browser_name,
        "Headless" if HEADLESS else "Visible",
    )

    try:
        monitor_projects(page, history)

    finally:
        browser.close()
        playwright.stop()

        logger.info("Browser closed.")


def main() -> None:
    """
    Application entry point.
    """

    logger.info(SEPARATOR)
    logger.info("JobWatchdog started")
    logger.info(SEPARATOR)

    history = load_history()

    logger.info("Loaded %d known project(s).", len(history))

    #
    # Initial scan (runs only once)
    #

    playwright, browser, page, _ = launch_browser()

    try:
        populate_history(page, history)

    finally:
        browser.close()
        playwright.stop()

        logger.info("Browser closed.")

    #
    # Monitoring loop
    #

    first_session = True

    while True:

        try:

            run_session(
                history,
                restarted=not first_session,
            )

            first_session = False

        except Error as error:

            if "Target page, context or browser has been closed" not in str(error):
                raise

            first_session = False

            logger.warning(
                "Browser was closed unexpectedly. Restarting in %d seconds...",
                BROWSER_RESTART_DELAY,
            )

            time.sleep(BROWSER_RESTART_DELAY)

        except KeyboardInterrupt:
            logger.info("Stopping JobWatchdog...")
            break


if __name__ == "__main__":
    main()