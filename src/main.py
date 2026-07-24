import threading
import time

from playwright.sync_api import Error

from browser import launch_browser
from config import BROWSER_RESTART_DELAY, HEADLESS
from history import load_history
from logger import logger
from monitor import monitor_projects, populate_history
from monitor_state import stop_event
from tray import create_tray_icon

SEPARATOR = "=" * 50


def monitor_loop() -> None:
    """
    Monitor Stepes projects continuously.
    """

    history = load_history()

    logger.info("Loaded %d known project(s).", len(history))

    first_session = True

    while not stop_event.is_set():

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

            if stop_event.is_set():
                break

            if "Target page, context or browser has been closed" not in str(error):
                raise

            logger.warning(
                "Browser was closed unexpectedly. Restarting in %d seconds...",
                BROWSER_RESTART_DELAY,
            )

            for _ in range(BROWSER_RESTART_DELAY * 10):

                if stop_event.is_set():
                    break

                time.sleep(0.1)

        except KeyboardInterrupt:
            logger.info("Stopping JobWatchdog...")
            stop_event.set()
            break

        finally:

            if browser is not None:
                browser.close()

            if playwright is not None:
                playwright.stop()

            logger.info("Browser closed.")

    logger.info("Monitor thread stopped.")


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

    logger.info("Waiting for monitor thread...")

    monitor_thread.join()

    logger.info("JobWatchdog stopped.")


if __name__ == "__main__":
    main()
