from dataclasses import dataclass


@dataclass
class JobProject:
    """
    Represents a translation project listed on the Stepes job board.
    """

    title: str
    project_id: str
    language: str
    subject: str
    service: str
    due_date: str
    created: str
    words: int
    price: float
    status: str
