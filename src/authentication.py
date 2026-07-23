from playwright.sync_api import Page, TimeoutError

from config import STEPES_PASSWORD, STEPES_USERNAME
from exceptions import (
    LoginFailedError,
    UnknownPageError,
)
from logger import logger

# Selectors
JOB_BOARD_SELECTOR = "div.head-title-new"
LOGIN_SELECTOR = "div.login-choose-box"
LOGIN_FORM_SELECTOR = "form#form_translator"

USERNAME_SELECTOR = 'input[name="wpName"]'
PASSWORD_SELECTOR = 'input[name="wpPassword"]'
LOGIN_BUTTON_SELECTOR = "#login_submit"
LOGIN_ERROR_SELECTOR = "p.alert.alert-danger"


def is_job_board(page: Page) -> bool:
    """
    Return True if the Stepes job board is displayed.
    """

    return page.locator(JOB_BOARD_SELECTOR).count() > 0


def is_login_selector(page: Page) -> bool:
    """
    Return True if the Translator/Customer selection page is displayed.
    """

    return page.locator(LOGIN_SELECTOR).count() > 0


def is_login_form(page: Page) -> bool:
    """
    Return True if the translator login form is displayed.
    """

    return page.locator(LOGIN_FORM_SELECTOR).count() > 0


def get_login_error(page: Page) -> str | None:
    """
    Return the login error message if present.
    """

    locator = page.locator(LOGIN_ERROR_SELECTOR)

    if locator.count() == 0:
        return None

    if not locator.is_visible():
        return None

    return locator.inner_text().strip()


def login(page: Page) -> None:
    """
    Ensure the user is authenticated.
    """

    if not STEPES_USERNAME or not STEPES_PASSWORD:
        raise LoginFailedError("Stepes credentials are not configured.")

    logger.info("Credentials loaded successfully.")

    if is_job_board(page):
        logger.info("Already authenticated.")
        return

    try:

        if is_login_selector(page):
            logger.info("Translator selection page detected.")

            page.locator(LOGIN_SELECTOR).click()

            page.wait_for_selector(
                LOGIN_FORM_SELECTOR,
                timeout=10000,
            )

            logger.info("Translator selected.")

        if is_login_form(page):
            logger.info("Login form detected.")

            page.locator(USERNAME_SELECTOR).fill(STEPES_USERNAME)

            page.locator(PASSWORD_SELECTOR).fill(STEPES_PASSWORD)

            page.locator(LOGIN_BUTTON_SELECTOR).click()

            #
            # Give Stepes a moment to render an error message.
            #
            page.wait_for_timeout(1000)

            error = get_login_error(page)

            if error:
                logger.error(error)
                raise LoginFailedError(error)

            page.wait_for_selector(
                JOB_BOARD_SELECTOR,
                timeout=15000,
            )

            logger.info("Login successful.")
            return

    except TimeoutError as error:
        logger.exception("Login timed out.")

        raise LoginFailedError("Timed out while waiting for the Job Board.") from error

    raise UnknownPageError("Unable to determine the current Stepes page.")


def ensure_authenticated(page: Page) -> None:
    """
    Ensure the user is authenticated.
    """

    logger.info("Checking authentication...")

    login(page)

    logger.info("Authentication OK.")
