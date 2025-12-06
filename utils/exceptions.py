class InsufficientFundsError(Exception):
    """Raised when expense would make balance negative"""

    def __init__(self, message="Entering negative balance!"):
        self.message = message


class InvalidYearError(Exception):
    """Raised when inputted year is not valid"""

    def __init__(self, message="Invalid year!"):
        self.message = message


class InvalidMonthError(Exception):
    """Raised when inputted month is not valid"""

    def __init__(self, message="Invalid month!"):
        self.message = message


class InvalidDayError(Exception):
    """Raised when inputted day is not valid"""

    def __init__(self, message="Invalid day!"):
        self.message = message
