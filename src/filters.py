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
    """

    # Ignore explicitly excluded language pairs.
    if job.language in EXCLUDED_LANGUAGES:
        return False

    if job.price < MINIMUM_PRICE:
        return False

    if job.words < MINIMUM_WORDS:
        return False

    if LANGUAGES and job.language not in LANGUAGES:
        return False

    return True