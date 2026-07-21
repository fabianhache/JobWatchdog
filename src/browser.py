from playwright.sync_api import (
    BrowserContext,
    Page,
    Playwright,
    sync_playwright,
)

from config import PROFILE_DIR, STEPES_URL


def launch_browser() -> tuple[Playwright, BrowserContext, Page]:
    """
    Launch a persistent Chromium browser session.

    The first time the application runs, the user must sign in manually.
    The browser profile is then reused across future sessions.
    """

    playwright = sync_playwright().start()

    browser = playwright.chromium.launch_persistent_context(
        user_data_dir=str(PROFILE_DIR),
        headless=False,
    )

    page = browser.pages[0] if browser.pages else browser.new_page()

    page.goto(STEPES_URL, wait_until="networkidle")

    return playwright, browser, page
