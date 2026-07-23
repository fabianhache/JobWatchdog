"""
Custom exceptions used throughout JobWatchdog.
"""


class JobWatchdogError(Exception):
    """
    Base exception for all JobWatchdog errors.
    """


class AuthenticationError(JobWatchdogError):
    """
    Base exception for authentication-related errors.
    """


class LoginFailedError(AuthenticationError):
    """
    Raised when automatic login fails.
    """


class UnknownPageError(AuthenticationError):
    """
    Raised when the current Stepes page cannot be identified.
    """