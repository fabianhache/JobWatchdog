import threading

pause_event = threading.Event()
pause_event.set()

stop_event = threading.Event()
