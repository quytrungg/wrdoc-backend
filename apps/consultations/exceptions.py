class ConsultationActionError(Exception):
    """Base class for consultation's status actions errors."""

    def __init__(self, message: str):
        self.message = message

    def __str__(self):
        return self.message
