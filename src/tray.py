import os

from PIL import Image
import pystray

from logger import logger
from monitor_state import pause_event


def create_tray_icon(icon_path: str) -> pystray.Icon:
    """
    Create the JobWatchdog system tray icon.
    """

    image = Image.open(icon_path)

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
                "Exit",
                lambda icon, item: exit_application(icon),
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


def exit_application(icon: pystray.Icon) -> None:
    """
    Stop the tray icon and terminate the application.
    """

    logger.info("Stopping JobWatchdog...")

    icon.stop()
    os._exit(0)


if __name__ == "__main__":
    icon = create_tray_icon("assets/jobwatchdog.ico")
    icon.run()