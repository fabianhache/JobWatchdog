import time

from playwright.sync_api import Error, Page

from authentication import ensure_authenticated
from config import CHECK_INTERVAL
from detector import find_job_cards
from filters import passes_filters
from history import is_new_project, save_project
from logger import logger
from models import JobProject
from notifications import notify
from monitor_state import pause_event, stop_event

SEPARATOR = "=" * 60


def display_job(job: JobProject) -> None:
    """
    Display a newly detected project in the console.
    """

    logger.info(
        "\n%s\n"
        "🟢 NEW PROJECT DETECTED\n"
        "%s\n"
        "Title      : %s\n"
        "Project ID : %s\n"
        "Language   : %s\n"
        "Service    : %s\n"
        "Words      : %d\n"
        "Price      : USD %.2f\n"
        "Status     : %s\n"
        "%s",
        SEPARATOR,
        SEPARATOR,
        job.title,
        job.project_id,
        job.language,
        job.service,
        job.words,
        job.price,
        job.status,
        SEPARATOR,
    )


def scan_projects(page: Page) -> list[JobProject]:
    """
    Authenticate if needed, refresh the job board and return all projects.
    """

    ensure_authenticated(page)

    page.reload(wait_until="networkidle")

    jobs = find_job_cards(page)

    logger.info("Found %d project(s).", len(jobs))

    return jobs


def populate_history(page: Page, history: set[str]) -> None:
    """
    Populate the history with existing projects without triggering
    notifications.
    """

    logger.info("Performing initial scan...")

    jobs = scan_projects(page)

    new_projects = 0

    for job in jobs:

        if not is_new_project(job.project_id, history):
            continue

        save_project(job.project_id)
        history.add(job.project_id)
        new_projects += 1

    logger.info("Added %d project(s) to the history.", new_projects)
    logger.info("Monitoring started.")


def monitor_projects(page: Page, history: set[str]) -> None:
    """
    Continuously monitor the Stepes job board for new projects.
    """

    while not stop_event.is_set():

        while not pause_event.is_set():

            if stop_event.is_set():
                logger.info("Monitoring stopped.")
                return

            time.sleep(0.2)

        try:

            logger.info("Checking for new projects...")

            jobs = scan_projects(page)

            detected_projects = 0
            notified_projects = 0

            for job in jobs:

                if stop_event.is_set():
                    logger.info("Monitoring stopped.")
                    return

                if not is_new_project(job.project_id, history):
                    continue

                detected_projects += 1

                save_project(job.project_id)
                history.add(job.project_id)

                if not passes_filters(job):
                    logger.info(
                        "Skipped project %s (did not match filters).",
                        job.project_id,
                    )
                    continue

                notified_projects += 1

                logger.info(
                    "New project detected: %s | %s | USD %.2f",
                    job.project_id,
                    job.language,
                    job.price,
                )

                display_job(job)

                notify(job)

            if detected_projects == 0:
                logger.info("No new projects found.")
            else:
                logger.info(
                    "%d new project(s) detected, %d notification(s) sent.",
                    detected_projects,
                    notified_projects,
                )

        except Error as error:

            # Let main.py handle browser restarts.
            if "Target page, context or browser has been closed" in str(error):
                raise

            logger.warning(
                "Monitoring failed: %s",
                error,
            )

        except Exception as error:

            logger.warning(
                "Unexpected monitoring error: %s",
                error,
            )

        logger.info("Next check in %d seconds.", CHECK_INTERVAL)

        for _ in range(CHECK_INTERVAL * 10):

            if stop_event.is_set():
                logger.info("Monitoring stopped.")
                return

            time.sleep(0.1)
