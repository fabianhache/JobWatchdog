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

    print(f"\n{SEPARATOR}")
    print("🟢 NEW PROJECT DETECTED")
    print(SEPARATOR)
    print(f"Title      : {job.title}")
    print(f"Project ID : {job.project_id}")
    print(f"Language   : {job.language}")
    print(f"Service    : {job.service}")
    print(f"Words      : {job.words}")
    print(f"Price      : USD {job.price:.2f}")
    print(f"Status     : {job.status}")
    print(SEPARATOR)


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

    logger.info("%s project(s) found.", len(jobs))
    logger.info("%s project(s) added to the history.", new_projects)
    logger.info("Monitoring started.")


def monitor_projects(page: Page, history: set[str]) -> None:
    """
    Continuously monitor the Stepes job board for new projects.
    """

    while True:

        page.reload(wait_until="networkidle")

        logger.info("Checking for new projects...")

        jobs = find_job_cards(page)

        new_projects = 0

        for job in jobs:

            if not is_new_project(job.project_id, history):
                continue

            save_project(job.project_id)
            history.add(job.project_id)

            if not passes_filters(job):
                continue

            new_projects += 1

            logger.info(
                "New project detected: %s | %s | USD %.2f",
                job.project_id,
                job.language,
                job.price,
            )

            display_job(job)

            notify(job)

        if new_projects == 0:
            logger.info("No new projects found.")

        logger.info("Next check in %s seconds.", CHECK_INTERVAL)

        time.sleep(CHECK_INTERVAL)
