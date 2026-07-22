import time

from playwright.sync_api import Page

from config import CHECK_INTERVAL
from detector import find_job_cards
from filters import passes_filters
from history import is_new_project, save_project
from logger import logger
from models import JobProject
from notifications import notify

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


def initialize_history(page: Page, history: set[str]) -> None:
    """
    Populate the history with existing projects without triggering notifications.
    """

    logger.info("Performing initial scan...")

    page.reload(wait_until="networkidle")

    jobs = find_job_cards(page)

    new_projects = 0

    for job in jobs:
        if is_new_project(job.project_id, history):
            save_project(job.project_id)
            history.add(job.project_id)
            new_projects += 1

    logger.info("Found %d project(s).", len(jobs))
    logger.info("Added %d project(s) to the history.", new_projects)
    logger.info("Monitoring started.")


def monitor_projects(page: Page, history: set[str]) -> None:
    """
    Continuously monitor the Stepes job board for new projects.
    """

    while True:

        logger.info("Checking for new projects...")

        page.reload(wait_until="networkidle")

        jobs = find_job_cards(page)

        logger.info("Found %d project(s).", len(jobs))

        detected_projects = 0
        notified_projects = 0

        for job in jobs:

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

        logger.info("Next check in %d seconds.", CHECK_INTERVAL)

        time.sleep(CHECK_INTERVAL)