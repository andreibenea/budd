class InsufficientFundsError(Exception):
    """Raised when withdrawal would make balance negative"""
    def __init__(self, message="Insufficient funds"):
        self.message = message
