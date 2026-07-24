import os
import sys
import webbrowser

import pystray
from PIL import Image

from config import STEPES_URL
from logger import logger
from monitor_state import pause_event, stop_event


def resource_path(relative_path: str) -> str:
    """
    Return the absolute path to a bundled resource.
    """

    if hasattr(sys, "_MEIPASS"):
        base_path = sys._MEIPASS
    else:
        base_path = os.path.dirname(os.path.abspath(__file__))

    return os.path.join(base_path, relative_path)


def create_tray_icon(icon_path: str) -> pystray.Icon:
    """
    Create the JobWatchdog system tray icon.
    """

    image = Image.open(resource_path(icon_path))

    return pystray.Icon(
        "JobWatchdog",
        image,
        "JobWatchdog",
        menu=pystray.Menu(
            pystray.MenuItem(
                "Pause monitoring",
                pause_monitoring,
                visible=lambda item: pause_event.is_set(),
            ),
            pystray.MenuItem(
                "Resume monitoring",
                resume_monitoring,
                visible=lambda item: not pause_event.is_set(),
            ),
            pystray.Menu.SEPARATOR,
            pystray.MenuItem(
                "Open Stepes",
                open_stepes,
            ),
            pystray.Menu.SEPARATOR,
            pystray.MenuItem(
                "Exit",
                exit_application,
            ),
        ),
    )


def pause_monitoring(icon: pystray.Icon, item) -> None:
    """
    Pause project monitoring.
    """

    pause_event.clear()
    icon.update_menu()

    logger.info("Monitoring paused.")


def resume_monitoring(icon: pystray.Icon, item) -> None:
    """
    Resume project monitoring.
    """

    pause_event.set()
    icon.update_menu()

    logger.info("Monitoring resumed.")


def open_stepes(icon: pystray.Icon, item) -> None:
    """
    Open the Stepes job board in the default web browser.
    """

    logger.info("Opening Stepes...")

    webbrowser.open(STEPES_URL)


def exit_application(icon: pystray.Icon, item) -> None:
    """
    Stop monitoring and close the application gracefully.
    """

    logger.info("Stopping JobWatchdog...")

    stop_event.set()

    pause_event.set()

    icon.stop()


if __name__ == "__main__":
    icon = create_tray_icon("assets/jobwatchdog.ico")
    icon.run()