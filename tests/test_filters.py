from filters import passes_filters
from models import JobProject


def make_job(
    price=50,
    words=500,
    language="English (US) > Spanish (US)",
):
    return JobProject(
        title="Test",
        project_id="1",
        language=language,
        subject="General",
        service="Translation",
        due_date="Tomorrow",
        created="Now",
        words=words,
        price=price,
        status="Open",
    )


def test_default_job_passes_filters():
    job = make_job()

    assert passes_filters(job)


def test_job_with_zero_price():
    job = make_job(price=0)

    assert passes_filters(job)


def test_job_with_zero_words():
    job = make_job(words=0)

    assert passes_filters(job)


def test_custom_language():
    job = make_job(
        language="English (UK) > Spanish (Spain)"
    )

    assert passes_filters(job)