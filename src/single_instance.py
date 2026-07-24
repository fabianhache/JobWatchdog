import sys

import win32api
import win32con
import win32event
import win32gui
import winerror

_MUTEX_NAME = "Global\\JobWatchdogSingleton"

_mutex = win32event.CreateMutex(
    None,
    False,
    _MUTEX_NAME,
)

if win32api.GetLastError() == winerror.ERROR_ALREADY_EXISTS:

    win32gui.MessageBox(
        0,
        "JobWatchdog is already running.",
        "JobWatchdog",
        win32con.MB_OK | win32con.MB_ICONINFORMATION,
    )

    sys.exit(0)
