from config import (
    EXCLUDED_LANGUAGES,
    LANGUAGES,
    MINIMUM_PRICE,
    MINIMUM_WORDS,
)
from models import JobProject


def passes_filters(job: JobProject) -> bool:
    """
    Check whether a project matches the configured filters.

    Only projects with Open status are considered available
    and eligible for notification.
    """

    # Only notify projects that are currently available.
    if job.status.strip().lower() != "open":
        return False

    # Ignore explicitly excluded language pairs.
    if job.language in EXCLUDED_LANGUAGES:
        return False

    # Ignore projects below the configured minimum price.
    if job.price < MINIMUM_PRICE:
        return False

    # Ignore projects below the configured minimum word count.
    if job.words < MINIMUM_WORDS:
        return False

    # If specific languages are configured, only allow those languages.
    if LANGUAGES and job.language not in LANGUAGES:
        return False

    return True
