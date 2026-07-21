from src.filters import passes_filters
from src.models import JobProject


def create_job(
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
    job = create_job()

    assert passes_filters(job)