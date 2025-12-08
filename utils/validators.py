from datetime import datetime
from utils.utils import messages, CATEGORIES_INCOME, CATEGORIES_EXPENSES, MAIN_MENU_OPTIONS, \
    TRANSACTIONS_HISTORY_MENU, \
    TRANSACTIONS_HISTORY_FILTER_MENU, \
    TRANSACTIONS_HISTORY_FILTER_DATETIME_MENU, TRANSACTIONS_HISTORY_FILTER_DATETIME_QUICK_MENU, \
    TRANSACTION_SELECTED_MENU, TRANSACTION_SELECTED_DELETE_MENU, \
    TRANSACTION_DETAILS_MENU, TRANSACTION_DETAILS_CATEGORY_INCOMES_MENU, TRANSACTION_DETAILS_CATEGORY_EXPENSES_MENU, \
    TRANSACTIONS_HISTORY_FILTER_CATEGORIES_EXPENSES_MENU, \
    TRANSACTIONS_HISTORY_FILTER_CATEGORIES_MENU, TRANSACTIONS_HISTORY_FILTER_CATEGORIES_INCOMES_MENU
from utils.exceptions import InsufficientFundsError
from utils.formatters import Formatter as fmt
from models.account import Account
from models.transaction import Transaction

import re


class ValidateUserInput:
    CURRENT_YEAR = datetime.now().year
    YEARS = range(1970, CURRENT_YEAR + 1)

    def __init__(self, user_input: str | None, validation_type: str | None = None):
        self.user_input = user_input
        self.validation_type = validation_type

    @staticmethod
    def validate_selection(choice: str, user_view: str | None = None, kind: str | None = None):
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
                    case "transaction_selected_menu":
                        if choice not in range(1, TRANSACTION_SELECTED_MENU + 1):
                            raise ValueError
                    case "transaction_selected_delete_menu":
                        if choice not in range(1, TRANSACTION_SELECTED_DELETE_MENU + 1):
                            raise ValueError
                    case "transaction_details_menu":
                        if choice not in range(1, TRANSACTION_DETAILS_MENU + 1):
                            raise ValueError
                    case "transaction_details_category_menu":
                        if kind == "income":
                            if choice not in range(1, TRANSACTION_DETAILS_CATEGORY_INCOMES_MENU + 1):
                                raise ValueError
                        elif kind == "expense":
                            if choice not in range(1, TRANSACTION_DETAILS_CATEGORY_EXPENSES_MENU + 1):
                                raise ValueError
                    case "add_income":
                        if choice not in range(1, len(CATEGORIES_INCOME) + 1):
                            raise ValueError
                    case "add_expense":
                        if choice not in range(1, len(CATEGORIES_EXPENSES) + 1):
                            raise ValueError
                break
            except ValueError:
                fmt.load_viewer(data="Type in number corresponding to your choice\nOr type 'cancel' to abort.",
                                kind="warning")
                choice = input("> ").strip().lower()
        if kind and user_view != "transaction_details_category_menu":
            i = 1
            if kind == "income":
                for cat in CATEGORIES_INCOME:
                    if i == choice:
                        choice = CATEGORIES_INCOME[cat]
                    i += 1
            elif kind == "expense":
                for cat in CATEGORIES_EXPENSES:
                    if i == choice:
                        choice = CATEGORIES_EXPENSES[cat]
                    i += 1
        return True, choice

    @staticmethod
    def is_amount_valid(account: "Account", amount: str, kind: str | None = None,
                        transaction: "Transaction | None" = None):
        if kind == "income":
            while True:
                if amount == "cancel":
                    return False, amount
                try:
                    amount = float(amount)
                    if amount <= 0:
                        raise ValueError
                    break
                except ValueError:
                    fmt.load_viewer(data=messages["invalid_amount"], kind="warning")
                    amount = input("> ").strip().lower()
            return True, amount
        if kind == "expense":
            causing_negative_balance = False
            initial_amount = ""
            while True:
                if amount == "cancel":
                    return False, amount
                if amount == "" and causing_negative_balance:
                    amount = initial_amount
                try:
                    amount = float(amount)
                    if amount <= 0:
                        raise ValueError
                    if not transaction:
                        if amount > account.check_balance():
                            if not causing_negative_balance:
                                raise InsufficientFundsError
                            else:
                                causing_negative_balance = False
                    else:
                        if amount >= transaction.amount:
                            diff = amount - transaction.amount
                            if account.check_balance() - diff < 0:
                                if not causing_negative_balance:
                                    raise InsufficientFundsError
                                else:
                                    causing_negative_balance = False
                    break
                except InsufficientFundsError:
                    fmt.load_viewer(data=messages["insufficient_funds"], kind="warning")
                    fmt.load_viewer(data=messages["insufficient_funds_continue"], kind="warning")
                    causing_negative_balance = True
                    initial_amount = amount
                    amount = input("> ").strip().lower()
                except ValueError:
                    fmt.load_viewer(data=messages["invalid_amount"], kind="warning")
                    amount = input("> ").strip().lower()
            return True, amount

    @staticmethod
    def is_description_valid(description: str):
        while True:
            if description == "cancel":
                return False, description
            if len(description) > 50:
                fmt.load_viewer(data=messages["invalid_description"], kind="warning")
                description = input("> ").strip().lower()
            break
        return True, description

    @staticmethod
    def is_date_valid(date: str):
        date_sub_pattern = r'[\\ /:]'
        if not date:
            return False, date
        while True:
            if date == "cancel":
                return False, date
            try:
                normalized = re.sub(pattern=date_sub_pattern, repl='-', string=date)
                dt = datetime.strptime(normalized, "%Y-%m-%d")
                date = normalized
                break
            except ValueError:
                fmt.load_viewer(data=messages["invalid_date"], kind="warning")
                date = input("> ").strip().lower()
        return True, date

    @staticmethod
    def is_time_valid(time_input: str):
        time_sub_pattern = r'[\\ /-]'
        if not time_input:
            return False, time_input
        while True:
            if time_input == "cancel":
                return False, time_input
            try:
                normalized = re.sub(pattern=time_sub_pattern, repl=':', string=time_input)
                if len(normalized) == 5:
                    normalized += ":00"
                dt = datetime.strptime(normalized, "%H:%M:%S")
                time_input = normalized
                break
            except ValueError:
                fmt.load_viewer(data=messages["invalid_time"], kind="warning")
                time_input = input("> ").strip().lower()
        return True, time_input
