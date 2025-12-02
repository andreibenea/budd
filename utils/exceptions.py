class InsufficientFundsError(Exception):
    """Raised when expense would make balance negative"""
    def __init__(self, message="Entering negative balance!"):
        self.message = message
