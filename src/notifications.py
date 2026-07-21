from config import NOTIFICATION_TITLE
from models import JobProject

from win11toast import toast


def notify(job: JobProject) -> None:
    """
    Display a Windows notification for a newly detected project.
    """

    message = f"{job.language}\n" f"{job.words:,} words\n" f"USD {job.price:.2f}"

    toast(
        NOTIFICATION_TITLE,
        message,
        duration="short",
    )
