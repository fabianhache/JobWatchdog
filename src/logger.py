import logging

from config import ROOT_DIR

LOGS_DIR = ROOT_DIR / "logs"
LOG_FILE = LOGS_DIR / "jobwatchdog.log"

LOGS_DIR.mkdir(exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)-8s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    handlers=[
        logging.FileHandler(LOG_FILE, encoding="utf-8"),
        logging.StreamHandler(),
    ],
)

logger = logging.getLogger("JobWatchdog")
