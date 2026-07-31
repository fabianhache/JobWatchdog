from playwright.sync_api import Page, TimeoutError

from config import STEPES_PASSWORD, STEPES_URL, STEPES_USERNAME
from exceptions import LoginFailedError, UnknownPageError
from logger import logger

# ---------------------------------------------------------------------------
# URLs
# ---------------------------------------------------------------------------

CUSTOMER_LOGIN_URL = "customer.stepes.com/globalizer"
TRANSLATOR_LOGIN_URL = "translator.stepes.com/login"
LEGACY_DASHBOARD_URL = "translator.stepes.com/translator-home.html"
LEGACY_JOB_BOARD_URL = "translator.stepes.com/stepes-check-jobs.html"


# ---------------------------------------------------------------------------
# Selectors
# ---------------------------------------------------------------------------

# Legacy Job Board
JOB_BOARD_SELECTOR = "div.head-title-new"

# Legacy Translator/Customer selection page
LOGIN_SELECTOR = "div.login-choose-box"

# Legacy translator login form
LOGIN_FORM_SELECTOR = "form#form_translator"
USERNAME_SELECTOR = 'input[name="wpName"]'
PASSWORD_SELECTOR = 'input[name="wpPassword"]'
LOGIN_BUTTON_SELECTOR = "#login_submit"
LOGIN_ERROR_SELECTOR = "p.alert.alert-danger"

# Text used by Stepes navigation
TRANSLATOR_LOGIN_LINK_TEXT = "Log in as a Translator"
BACK_TO_LEGACY_TEXT = "Back to Legacy Version"


# ---------------------------------------------------------------------------
# Timing
# ---------------------------------------------------------------------------

PAGE_DETECTION_TIMEOUT = 15000
PAGE_CHECK_INTERVAL = 500


# ---------------------------------------------------------------------------
# Page detection
# ---------------------------------------------------------------------------


def is_job_board(page: Page) -> bool:
    """
    Return True if the Legacy Search Jobs page is displayed.
    """

    if LEGACY_JOB_BOARD_URL in page.url:
        return True

    return page.locator(JOB_BOARD_SELECTOR).count() > 0


def is_customer_login(page: Page) -> bool:
    """
    Return True if the Customer Login page is displayed.
    """

    return CUSTOMER_LOGIN_URL in page.url


def is_translator_login(page: Page) -> bool:
    """
    Return True if a Translator Login page is displayed.

    Stepes may use URLs such as:
        ?oldtheme=1
        ?newtheme=1
    """

    return TRANSLATOR_LOGIN_URL in page.url


def is_login_selector(page: Page) -> bool:
    """
    Return True if the legacy Translator/Customer selection page
    is displayed.
    """

    return page.locator(LOGIN_SELECTOR).count() > 0


def is_new_version(page: Page) -> bool:
    """
    Return True if the new Stepes interface is displayed.

    The new interface exposes a 'Back to Legacy Version' control.
    """

    locator = page.get_by_text(
        BACK_TO_LEGACY_TEXT,
        exact=False,
    )

    return locator.count() > 0


def is_legacy_dashboard(page: Page) -> bool:
    """
    Return True if the Legacy Translator Dashboard is displayed.
    """

    return LEGACY_DASHBOARD_URL in page.url


def wait_for_known_page(page: Page) -> str | None:
    """
    Wait until Stepes displays a page recognized by JobWatchdog.

    Possible states:
        job_board
        customer_login
        translator_login
        login_selector
        new_version
        legacy_dashboard
        None
    """

    elapsed = 0

    while elapsed < PAGE_DETECTION_TIMEOUT:

        # URL-based states are checked first because Stepes pages can
        # contain similar HTML elements.

        if is_customer_login(page):
            return "customer_login"

        if is_translator_login(page):
            return "translator_login"

        if is_legacy_dashboard(page):
            return "legacy_dashboard"

        if is_job_board(page):
            return "job_board"

        if is_new_version(page):
            return "new_version"

        if is_login_selector(page):
            return "login_selector"

        page.wait_for_timeout(PAGE_CHECK_INTERVAL)
        elapsed += PAGE_CHECK_INTERVAL

    return None


# ---------------------------------------------------------------------------
# Login errors
# ---------------------------------------------------------------------------


def get_login_error(page: Page) -> str | None:
    """
    Return a visible login error message if Stepes displays one.
    """

    locator = page.locator(LOGIN_ERROR_SELECTOR)

    if locator.count() == 0:
        return None

    if not locator.is_visible():
        return None

    return locator.inner_text().strip()


# ---------------------------------------------------------------------------
# Customer Login -> Translator Login
# ---------------------------------------------------------------------------


def open_translator_login(page: Page) -> None:
    """
    From the Customer Login page, click 'Log in as a Translator'.
    """

    logger.info("Customer Login page detected.")
    logger.info("Opening Translator Login...")

    translator_link = page.get_by_text(
        TRANSLATOR_LOGIN_LINK_TEXT,
        exact=False,
    )

    if translator_link.count() == 0:
        raise UnknownPageError(
            "Customer Login detected, but the "
            "'Log in as a Translator' link could not be found."
        )

    translator_link.first.click()

    try:
        page.wait_for_url(
            "**translator.stepes.com/login*",
            timeout=PAGE_DETECTION_TIMEOUT,
        )

    except TimeoutError as error:
        raise LoginFailedError("Unable to open the Translator Login page.") from error

    logger.info("Translator Login opened.")


# ---------------------------------------------------------------------------
# Translator Login fields
# ---------------------------------------------------------------------------


def find_username_field(page: Page):
    """
    Find the username/email field on the Translator Login page.
    """

    selectors = [
        'input[name="wpName"]',
        'input[type="email"]',
        'input[placeholder*="Username"]',
        'input[placeholder*="Email"]',
    ]

    for selector in selectors:
        locator = page.locator(selector)

        if locator.count() > 0:
            return locator.first

    return None


def find_password_field(page: Page):
    """
    Find the password field on the Translator Login page.
    """

    selectors = [
        'input[name="wpPassword"]',
        'input[type="password"]',
    ]

    for selector in selectors:
        locator = page.locator(selector)

        if locator.count() > 0:
            return locator.first

    return None


def find_login_button(page: Page):
    """
    Find the Log in button on the Translator Login page.
    """

    selectors = [
        "#login_submit",
        'button[type="submit"]',
        'input[type="submit"]',
    ]

    for selector in selectors:
        locator = page.locator(selector)

        if locator.count() > 0:
            return locator.first

    locator = page.get_by_text(
        "Log in",
        exact=True,
    )

    if locator.count() > 0:
        return locator.first

    return None


# ---------------------------------------------------------------------------
# Translator Login
# ---------------------------------------------------------------------------


def submit_translator_login(page: Page) -> None:
    """
    Fill and submit the Translator Login form.
    """

    if not STEPES_USERNAME or not STEPES_PASSWORD:
        raise LoginFailedError("Stepes credentials are not configured.")

    logger.info("Translator Login page detected.")

    username_field = find_username_field(page)
    password_field = find_password_field(page)
    login_button = find_login_button(page)

    if username_field is None:
        raise UnknownPageError(
            "Translator Login detected, but the username field " "could not be found."
        )

    if password_field is None:
        raise UnknownPageError(
            "Translator Login detected, but the password field " "could not be found."
        )

    if login_button is None:
        raise UnknownPageError(
            "Translator Login detected, but the Log in button " "could not be found."
        )

    logger.info("Entering Stepes credentials...")

    username_field.fill(STEPES_USERNAME)
    password_field.fill(STEPES_PASSWORD)

    logger.info("Submitting Translator Login...")

    login_button.click()

    # Give Stepes time to display an authentication error.
    page.wait_for_timeout(1000)

    error = get_login_error(page)

    if error:
        logger.error("Stepes login failed: %s", error)
        raise LoginFailedError(error)

    # Do not assume where Stepes will send us after login.
    # It may open the new UI, legacy dashboard, or job board.
    page.wait_for_timeout(2000)

    logger.info(
        "Login submitted. Current URL: %s",
        page.url,
    )


# ---------------------------------------------------------------------------
# Legacy selection page
# ---------------------------------------------------------------------------


def handle_legacy_login_selector(page: Page) -> None:
    """
    Handle the old Translator/Customer selection page.
    """

    logger.info("Legacy Translator selection page detected.")

    selector = page.locator(LOGIN_SELECTOR)

    if selector.count() == 0:
        raise UnknownPageError(
            "Legacy login selector was detected but could not be found."
        )

    selector.first.click()

    page.wait_for_timeout(1000)


# ---------------------------------------------------------------------------
# New Stepes -> Legacy Stepes
# ---------------------------------------------------------------------------


def switch_to_legacy_version(page: Page) -> None:
    """
    Switch from the new Stepes interface to the Legacy interface.
    """

    logger.info("New Stepes interface detected.")
    logger.info("Switching to Legacy Version...")

    legacy_link = page.get_by_text(
        BACK_TO_LEGACY_TEXT,
        exact=False,
    )

    if legacy_link.count() == 0:
        raise UnknownPageError(
            "New Stepes interface detected, but "
            "'Back to Legacy Version' could not be found."
        )

    legacy_link.first.click()

    try:
        page.wait_for_url(
            "**translator.stepes.com/translator-home.html*",
            timeout=PAGE_DETECTION_TIMEOUT,
        )

    except TimeoutError:
        # Stepes may redirect somewhere else while still switching
        # successfully. The caller will evaluate the resulting page.
        logger.warning(
            "Legacy Dashboard URL was not detected after switching. " "Current URL: %s",
            page.url,
        )

    logger.info(
        "Legacy interface opened. URL: %s",
        page.url,
    )


# ---------------------------------------------------------------------------
# Legacy Dashboard -> Search Jobs
# ---------------------------------------------------------------------------


def open_legacy_job_board(page: Page) -> None:
    """
    Open the Legacy Search Jobs page.

    Direct navigation is used instead of relying on the sidebar link.
    """

    logger.info("Opening Legacy Search Jobs...")

    page.goto(
        STEPES_URL,
        wait_until="networkidle",
    )

    try:
        page.wait_for_url(
            "**translator.stepes.com/stepes-check-jobs.html*",
            timeout=PAGE_DETECTION_TIMEOUT,
        )

    except TimeoutError:
        logger.warning(
            "Legacy Job Board URL was not reached. Current URL: %s",
            page.url,
        )

    logger.info(
        "Search Jobs navigation completed. URL: %s",
        page.url,
    )


# ---------------------------------------------------------------------------
# Authentication and navigation normalization
# ---------------------------------------------------------------------------


def login(page: Page) -> None:
    """
    Authenticate with Stepes and normalize navigation.

    JobWatchdog always attempts to finish on the Legacy Search Jobs page.

    Supported flows include:

        Existing session
            -> Legacy Job Board

        Customer Login
            -> Log in as a Translator
            -> Translator Login
            -> Stepes
            -> Legacy Job Board

        Translator Login
            -> credentials
            -> Stepes
            -> Legacy Job Board

        New Stepes interface
            -> Back to Legacy Version
            -> Legacy Dashboard
            -> Legacy Job Board

        Legacy Dashboard
            -> Legacy Job Board
    """

    logger.info("Credentials loaded successfully.")

    # Multiple transitions may be required.
    # The limit prevents an accidental infinite loop.
    max_transitions = 10

    for _ in range(max_transitions):

        page_state = wait_for_known_page(page)

        if page_state == "job_board":
            logger.info("Legacy Job Board detected.")
            logger.info("Already authenticated.")
            return

        if page_state == "customer_login":
            open_translator_login(page)
            continue

        if page_state == "translator_login":
            submit_translator_login(page)
            continue

        if page_state == "login_selector":
            handle_legacy_login_selector(page)
            continue

        if page_state == "new_version":
            switch_to_legacy_version(page)
            continue

        if page_state == "legacy_dashboard":
            logger.info("Legacy Translator Dashboard detected.")
            open_legacy_job_board(page)
            continue

        logger.warning(
            "Unknown Stepes page. URL: %s | Title: %s",
            page.url,
            page.title(),
        )

        raise UnknownPageError(
            "Unable to determine the current Stepes page. " f"URL: {page.url}"
        )

    raise LoginFailedError("Too many Stepes authentication/navigation redirects.")


# ---------------------------------------------------------------------------
# Public entry point
# ---------------------------------------------------------------------------


def ensure_authenticated(page: Page) -> None:
    """
    Ensure JobWatchdog is authenticated and positioned on the
    Legacy Search Jobs page.
    """

    logger.info("Checking authentication...")

    login(page)

    if not is_job_board(page):
        raise UnknownPageError(
            "Authentication completed, but JobWatchdog did not reach "
            f"the Legacy Job Board. URL: {page.url}"
        )

    logger.info("Authentication OK.")
