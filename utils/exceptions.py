class InsufficientFundsError(Exception):
    """Raised when withdrawal would make balance negative"""
    def __init__(self, message="Exceeding withdrawal balance!"):
        self.message = message
