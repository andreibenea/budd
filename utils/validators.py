from datetime import datetime
from utils.utils import MONTHS, MAIN_MENU_OPTIONS, TRANSACTIONS_HISTORY_MENU, \
    TRANSACTIONS_HISTORY_FILTER_MENU, \
    TRANSACTIONS_HISTORY_FILTER_DATETIME_MENU, TRANSACTIONS_HISTORY_FILTER_DATETIME_QUICK_MENU, TRANSACTION_EDIT_MENU, \
    TRANSACTION_DETAILS_MENU, TRANSACTIONS_HISTORY_FILTER_CATEGORIES_EXPENSES_MENU, \
    TRANSACTIONS_HISTORY_FILTER_CATEGORIES_MENU, TRANSACTIONS_HISTORY_FILTER_CATEGORIES_INCOMES_MENU
from utils.formatters import Formatter as fmt


class ValidateUserInput:
    CURRENT_YEAR = datetime.now().year
    YEARS = range(1970, CURRENT_YEAR + 1)

    def __init__(self, user_input: str | None, validation_type: str | None = None):
        self.user_input = user_input
        self.validation_type = validation_type

    @staticmethod
    def validate_selection(choice: str, user_view: str | None = None):
        while True:
            if choice == "cancel":
                return False, choice
            try:
                choice = int(choice)
                match user_view:
                    case "main_menu":
                        if choice not in range(1, MAIN_MENU_OPTIONS + 1):
                            raise ValueError
                    case "transactions_history_menu":
                        if choice not in range(1, TRANSACTIONS_HISTORY_MENU + 1):
                            raise ValueError
                    case "transactions_history_filter_menu":
                        if choice not in range(1, TRANSACTIONS_HISTORY_FILTER_MENU + 1):
                            raise ValueError
                    case "transactions_history_filter_categories_menu":
                        if choice not in range(1, TRANSACTIONS_HISTORY_FILTER_CATEGORIES_MENU + 1):
                            raise ValueError
                    case "transactions_history_filter_categories_incomes_menu":
                        if choice not in range(1, TRANSACTIONS_HISTORY_FILTER_CATEGORIES_INCOMES_MENU + 1):
                            raise ValueError
                    case "transactions_history_filter_categories_expenses_menu":
                        if choice not in range(1, TRANSACTIONS_HISTORY_FILTER_CATEGORIES_EXPENSES_MENU + 1):
                            raise ValueError
                    case "transactions_history_filter_datetime_menu":
                        if choice not in range(1, TRANSACTIONS_HISTORY_FILTER_DATETIME_MENU + 1):
                            raise ValueError
                    case "transactions_history_filter_datetime_quick_menu":
                        if choice not in range(1, TRANSACTIONS_HISTORY_FILTER_DATETIME_QUICK_MENU + 1):
                            raise ValueError
                    case "transaction_details_menu":
                        if choice not in range(1, TRANSACTION_DETAILS_MENU + 1):
                            raise ValueError
                    case "transaction_edit_menu":
                        if choice not in range(1, TRANSACTION_EDIT_MENU + 1):
                            raise ValueError
                break
            except ValueError:
                fmt.load_viewer(data="Type in number corresponding to your choice\nOr type 'cancel' to abort.",
                                kind="warning")
                choice = input("> ").strip().lower()
        return True, choice

    @staticmethod
    def is_date_valid(year=None, month=None, day=None) -> bool:
        try:
            if year is not None:
                try:
                    year = int(year)
                    if year not in ValidateUserInput.YEARS:
                        raise ValueError
                except ValueError:
                    raise ValueError
            if month is not None:
                try:
                    month = int(month)
                    if month not in range(1, 13):
                        raise ValueError
                except ValueError:
                    if month not in MONTHS:
                        raise ValueError
            if day is not None:
                try:
                    day = int(day)
                    if day not in range(1, 32):
                        raise ValueError
                except ValueError:
                    raise ValueError
            return True
        except ValueError:
            return False
