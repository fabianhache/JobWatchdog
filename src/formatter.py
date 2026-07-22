from config import STEPES_URL
from models import JobProject


def format_notification(job: JobProject) -> str:
    """
    Build the notification message for a job project.
    """

    price_per_word = (job.price / job.words) * 100 if job.words else 0

    return (
        f"🟢 {job.title}\n\n"
        f"💵 ${job.price:.2f} • {job.words:,}w • {price_per_word:.1f}¢/w\n"
        f"📚 {job.subject}\n\n"
        f"🔗 {STEPES_URL}"
    )