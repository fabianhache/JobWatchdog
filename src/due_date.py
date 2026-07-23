from datetime import datetime


def format_due_date(due_date: str) -> str:
    """
    Format the Stepes due date for notifications.
    """

    due_date = due_date.strip()

    if due_date.lower().endswith("left"):
        return f"⏰ Due in {due_date[:-5].strip()}"

    try:
        due = datetime.strptime(due_date, "%b %d, %Y, %I:%M %p")
        return f"⏰ Due: {due.strftime('%b %d, %I:%M %p')}"
    except ValueError:
        return f"⏰ Due: {due_date}"