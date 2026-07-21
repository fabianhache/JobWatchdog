from config import HISTORY_FILE


def load_history() -> set[str]:
    """
    Load all known project IDs from the history file.

    Returns:
        A set containing every previously seen project ID.
    """

    if not HISTORY_FILE.exists():
        return set()

    with open(HISTORY_FILE, "r", encoding="utf-8") as file:
        return {line.strip() for line in file if line.strip()}


def save_project(project_id: str) -> None:
    """
    Append a project ID to the history file.
    """

    HISTORY_FILE.parent.mkdir(exist_ok=True)

    with open(HISTORY_FILE, "a", encoding="utf-8") as file:
        file.write(project_id + "\n")


def is_new_project(project_id: str, history: set[str]) -> bool:
    """
    Check whether a project ID is new.
    """

    return project_id not in history
