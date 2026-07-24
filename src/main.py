import threading
import time

from playwright.sync_api import Error

from browser import launch_browser
from config import BROWSER_RESTART_DELAY, HEADLESS
from history import load_history
from logger import logger
from monitor import monitor_projects, populate_history
from tray import create_tray_icon

SEPARATOR = "=" * 50


def monitor_loop() -> None:
    """
    Monitor Stepes projects continuously.
    """

    history = load_history()

    logger.info("Loaded %d known project(s).", len(history))

    first_session = True

    while True:

        playwright = None
        browser = None

        try:

            playwright, browser, page, browser_name = launch_browser()

            logger.info(
                "%s: %s (%s)",
                "Browser restarted" if not first_session else "Browser",
                browser_name,
                "Headless" if HEADLESS else "Visible",
            )

            if first_session:
                populate_history(page, history)
                first_session = False

            monitor_projects(page, history)

        except Error as error:

            if "Target page, context or browser has been closed" not in str(error):
                raise

            logger.warning(
                "Browser was closed unexpectedly. Restarting in %d seconds...",
                BROWSER_RESTART_DELAY,
            )

            time.sleep(BROWSER_RESTART_DELAY)

        except KeyboardInterrupt:
            logger.info("Stopping JobWatchdog...")
            break

        finally:

            if browser is not None:
                browser.close()

            if playwright is not None:
                playwright.stop()

            logger.info("Browser closed.")


def main() -> None:
    """
    Application entry point.
    """

    logger.info(SEPARATOR)
    logger.info("JobWatchdog started")
    logger.info(SEPARATOR)

    monitor_thread = threading.Thread(
        target=monitor_loop,
        daemon=True,
    )

    monitor_thread.start()

    tray = create_tray_icon("assets/jobwatchdog.ico")
    tray.run()


if __name__ == "__main__":
    main()