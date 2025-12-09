from datetime import datetime
from utils.utils import UserView as view, MESSAGES, CATEGORIES_INCOME, CATEGORIES_EXPENSES, MAIN_MENU_OPT, \
    BUDGETS_MENU_OPT, BUDGETS_BUDGET_DETAILS_MENU_OPT, BUDGETS_BUDGET_DETAILS_CATEGORIES_MENU_OPT, \
    BUDGETS_BUDGET_CATEGORIES_MENU_OPT, TRANSACTIONS_HISTORY_MENU_OPT, \
    TRANSACTIONS_HISTORY_FILTER_MENU_OPT, \
    TRANSACTIONS_HISTORY_FILTER_DATETIME_MENU_OPT, TRANSACTIONS_HISTORY_FILTER_DATETIME_QUICK_MENU_OPT, \
    TRANSACTION_SELECTED_MENU_OPT, TRANSACTION_SELECTED_DELETE_MENU_OPT, \
    TRANSACTION_DETAILS_MENU_OPT, TRANSACTION_DETAILS_CATEGORY_INCOMES_MENU_OPT, \
    TRANSACTION_DETAILS_CATEGORY_EXPENSES_MENU_OPT, \
    TRANSACTIONS_HISTORY_FILTER_CATEGORIES_EXPENSES_MENU_OPT, \
    TRANSACTIONS_HISTORY_FILTER_CATEGORIES_MENU_OPT, TRANSACTIONS_HISTORY_FILTER_CATEGORIES_INCOMES_MENU_OPT, \
    MAX_NAME_LENGTH, MAX_DESCRIPTION_LENGTH
from utils.exceptions import InsufficientFundsError
from utils.formatters import Formatter as fmt
from models.account import Account
from models.transaction import Transaction

import re


class ValidateUserInput:
    CURRENT_YEAR = datetime.now().year
    YEARS = range(1970, CURRENT_YEAR + 1)

    def __init__(self):
        pass

    @staticmethod
    def validate_selection(choice: str, user_view: str | None = None, kind: str | None = None):
        while True:
            if choice == "cancel":
                return False, choice
            try:
                choice = int(choice)
                match user_view:
                    case view.MAIN_MENU:
                        if choice not in range(1, MAIN_MENU_OPT + 1):
                            raise ValueError
                    case view.BUDGETS_MENU:
                        if choice not in range(1, BUDGETS_MENU_OPT + 1):
                            raise ValueError
                    case view.BUDGETS_BUDGET_DETAILS_MENU:
                        if choice not in range(1, BUDGETS_BUDGET_DETAILS_MENU_OPT + 1):
                            raise ValueError
                    case view.BUDGETS_BUDGET_DETAILS_CATEGORIES_MENU:
                        if choice not in range(1, BUDGETS_BUDGET_DETAILS_CATEGORIES_MENU_OPT + 1):
                            raise ValueError
                    case view.BUDGETS_BUDGET_CATEGORIES_MENU:
                        if choice not in range(1, BUDGETS_BUDGET_CATEGORIES_MENU_OPT + 1):
                            raise ValueError
                    case view.TRANSACTIONS_HISTORY_MENU:
                        if choice not in range(1, TRANSACTIONS_HISTORY_MENU_OPT + 1):
                            raise ValueError
                    case view.TRANSACTIONS_HISTORY_FILTER_MENU:
                        if choice not in range(1, TRANSACTIONS_HISTORY_FILTER_MENU_OPT + 1):
                            raise ValueError
                    case view.TRANSACTIONS_HISTORY_FILTER_CATEGORIES_MENU:
                        if choice not in range(1, TRANSACTIONS_HISTORY_FILTER_CATEGORIES_MENU_OPT + 1):
                            raise ValueError
                    case view.TRANSACTIONS_HISTORY_FILTER_CATEGORIES_INCOMES_MENU:
                        if choice not in range(1, TRANSACTIONS_HISTORY_FILTER_CATEGORIES_INCOMES_MENU_OPT + 1):
                            raise ValueError
                    case view.TRANSACTIONS_HISTORY_FILTER_CATEGORIES_EXPENSES_MENU:
                        if choice not in range(1, TRANSACTIONS_HISTORY_FILTER_CATEGORIES_EXPENSES_MENU_OPT + 1):
                            raise ValueError
                    case view.TRANSACTIONS_HISTORY_FILTER_DATETIME_MENU:
                        if choice not in range(1, TRANSACTIONS_HISTORY_FILTER_DATETIME_MENU_OPT + 1):
                            raise ValueError
                    case view.TRANSACTIONS_HISTORY_FILTER_DATETIME_QUICK_MENU:
                        if choice not in range(1, TRANSACTIONS_HISTORY_FILTER_DATETIME_QUICK_MENU_OPT + 1):
                            raise ValueError
                    case view.TRANSACTION_SELECTED_MENU:
                        if choice not in range(1, TRANSACTION_SELECTED_MENU_OPT + 1):
                            raise ValueError
                    case view.TRANSACTION_SELECTED_DELETE_MENU:
                        if choice not in range(1, TRANSACTION_SELECTED_DELETE_MENU_OPT + 1):
                            raise ValueError
                    case view.TRANSACTION_DETAILS_MENU:
                        if choice not in range(1, TRANSACTION_DETAILS_MENU_OPT + 1):
                            raise ValueError
                    case view.TRANSACTION_DETAILS_CATEGORY_MENU:
                        if kind == "income":
                            if choice not in range(1, TRANSACTION_DETAILS_CATEGORY_INCOMES_MENU_OPT + 1):
                                raise ValueError
                        elif kind == "expense":
                            if choice not in range(1, TRANSACTION_DETAILS_CATEGORY_EXPENSES_MENU_OPT + 1):
                                raise ValueError
                    case view.ADD_INCOME_MENU:
                        if choice not in range(1, len(CATEGORIES_INCOME) + 1):
                            raise ValueError
                    case view.ADD_EXPENSE_MENU:
                        if choice not in range(1, len(CATEGORIES_EXPENSES) + 1):
                            raise ValueError
                break
            except ValueError:
                fmt.load_viewer(data="Type in number corresponding to your choice\nOr type 'cancel' to abort.",
                                kind="warning")
                choice = input("> ").strip().lower()
        if kind == "budget":
            i = 1
            categories_combo = []
            for cat in CATEGORIES_INCOME:
                categories_combo.append(CATEGORIES_INCOME[cat])
            for cat in CATEGORIES_EXPENSES:
                if cat not in categories_combo:
                    categories_combo.append(CATEGORIES_EXPENSES[cat])
            for c in categories_combo:
                if i == choice:
                    choice = c
                i += 1
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
                        transaction: "Transaction | None" = None) -> tuple[bool, float | str]:
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
                    fmt.load_viewer(data=MESSAGES["invalid_amount"], kind="warning")
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
                    fmt.load_viewer(data=MESSAGES["insufficient_funds"], kind="warning")
                    fmt.load_viewer(data=MESSAGES["insufficient_funds_continue"], kind="warning")
                    causing_negative_balance = True
                    initial_amount = amount
                    amount = input("> ").strip().lower()
                except ValueError:
                    fmt.load_viewer(data=MESSAGES["invalid_amount"], kind="warning")
                    amount = input("> ").strip().lower()
            return True, amount

    @staticmethod
    def validate_text(text: str, kind: str):
        while True:
            if text == "cancel":
                return False, text
            try:
                if not text and kind != "name":
                    break
                if not text.replace(" ", "").isalnum():
                    raise ValueError
                if kind == "description":
                    assert len(text) < MAX_DESCRIPTION_LENGTH
                elif kind == "name":
                    assert len(text) < MAX_NAME_LENGTH
                break
            except ValueError:
                fmt.load_viewer(data=MESSAGES["invalid_text"], kind="warning")
                text = input("> ").strip().lower()
            except AssertionError:
                if kind == "description":
                    fmt.load_viewer(data=MESSAGES["invalid_description"], kind="warning")
                elif kind == "name":
                    fmt.load_viewer(data=MESSAGES["invalid_name"], kind="warning")
                text = input("> ").strip().lower()
        return True, text

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
                fmt.load_viewer(data=MESSAGES["invalid_date"], kind="warning")
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
                fmt.load_viewer(data=MESSAGES["invalid_time"], kind="warning")
                time_input = input("> ").strip().lower()
        return True, time_input
