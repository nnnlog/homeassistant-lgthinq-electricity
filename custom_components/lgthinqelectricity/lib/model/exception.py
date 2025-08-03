class UnauthorizedException(Exception):
    """Exception raised when the user is not authorized to perform an action."""
    def __init__(self, message: str = ""):
        super().__init__(message)
