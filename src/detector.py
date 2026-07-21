from playwright.sync_api import Page

from models import JobProject


def find_job_cards(page: Page) -> list[JobProject]:
    """
    Extract all available job cards from the Stepes job board.

    Returns:
        A list of JobProject objects.
    """

    jobs: list[JobProject] = []

    cards = page.locator("div.job-list.search-job-wrapper")

    for index in range(cards.count()):
        card = cards.nth(index)

        # Job title
        title = card.locator("div.filename").inner_text().strip()

        # Project ID
        project_id = card.locator("span.text-777").inner_text().strip()

        # General information
        info = card.locator("li.mb-8")

        language = info.nth(1).inner_text().strip()
        subject = info.nth(2).locator("span.text-666").inner_text().strip()
        service = info.nth(3).locator("span.text-666").inner_text().strip()
        due_date = info.nth(4).locator("span.text-666").inner_text().strip()
        created = info.nth(5).locator("span.text-666").inner_text().strip()

        # Word count
        words_text = (
            card.locator("div.font-30")
            .first.inner_text()
            .replace("Words", "")
            .replace("Word", "")
            .replace(",", "")
            .strip()
        )

        words = int(words_text)

        # Project price
        price_text = (
            card.locator("div.item-price.font-30")
            .inner_text()
            .replace("$", "")
            .replace(",", "")
            .strip()
        )

        price = float(price_text)

        # Project status
        status_locator = card.locator("div.pull-right.label")

        status = (
            status_locator.inner_text().strip() if status_locator.count() > 0 else ""
        )

        jobs.append(
            JobProject(
                title=title,
                project_id=project_id,
                language=language,
                subject=subject,
                service=service,
                due_date=due_date,
                created=created,
                words=words,
                price=price,
                status=status,
            )
        )

    return jobs
