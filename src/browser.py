from playwright.sync_api import (
    BrowserContext,
    Error,
    Page,
    Playwright,
    sync_playwright,
)

from config import HEADLESS, PROFILE_DIR, STEPES_URL


def launch_browser() -> tuple[Playwright, BrowserContext, Page, str]:
    """
    Launch a persistent browser session.

    Prefer Google Chrome when available. If Chrome is not installed,
    automatically fall back to the bundled Chromium browser.
    """

    playwright = sync_playwright().start()

    browser_name = "Google Chrome"

    try:
        browser = playwright.chromium.launch_persistent_context(
            user_data_dir=str(PROFILE_DIR),
            channel="chrome",
            headless=HEADLESS,
        )

    except Error:

        browser_name = "Chromium"

        browser = playwright.chromium.launch_persistent_context(
            user_data_dir=str(PROFILE_DIR),
            headless=HEADLESS,
        )

    page = browser.pages[0] if browser.pages else browser.new_page()

    page.goto(STEPES_URL, wait_until="networkidle")

    return playwright, browser, page, browser_name