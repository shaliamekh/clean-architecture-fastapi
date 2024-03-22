class ExternalError(Exception):
    pass


class DatabaseError(ExternalError):
    def __init__(self, error: Exception):
        self.error = error

    def __str__(self) -> str:
        return str(self.error)
