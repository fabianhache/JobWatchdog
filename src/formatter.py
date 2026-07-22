from config import STEPES_URL
from models import JobProject


def format_notification(job: JobProject) -> str:
    """
    Build the notification message for a job project.
    """

    return (
        f"🟢 {job.title}\n\n"
        f"💵 ${job.price:.2f} • {job.words:,}w\n"
        f"📚 {job.subject}\n\n"
        f"🔗 {STEPES_URL}"
    )