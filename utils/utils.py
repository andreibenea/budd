from utils.formatters import Formatter

fmt = Formatter()


def load_menu(user_view, filters: dict | None = None):
    match user_view:
        case "main_menu":
            fmt.load_viewer(data="You Are Here:\n[Main Menu]", kind="path_to_view")
            show_main_menu()
        case "transactions_history_menu":
            fmt.load_viewer(data="You Are Here:\nMain Menu > [Transactions]", kind="path_to_view")
            show_transactions_history_menu()
        case "transactions_history_filter_menu":
            fmt.load_viewer(data="You Are Here:\nMain Menu > Transactions > [Manage Filters]", kind="path_to_view")
            show_transactions_history_filter_menu()
        case "transactions_history_filter_categories_menu":
            if filters:
                if "kind" in filters:
                    if filters["kind"] == "income":
                        user_view = USER_VIEWS["transactions_history_filter_categories_incomes_menu"]
                        load_menu(user_view, filters)
                    elif filters["kind"] == "expense":
                        user_view = USER_VIEWS["transactions_history_filter_categories_expenses_menu"]
                        load_menu(user_view, filters)
            else:
                fmt.load_viewer(data="You Are Here:\nMain Menu > Transactions > Manage Filters > [Categories]",
                                kind="path_to_view")
                show_transactions_history_filter_categories_menu()
        case "transactions_history_filter_categories_incomes_menu":
            fmt.load_viewer(data="You Are Here:\nMain Menu > Transactions > Manage Filters > Categories > [Incomes]",
                            kind="path_to_view")
            show_categories_income_menu_new()
        case "transactions_history_filter_categories_expenses_menu":
            fmt.load_viewer(data="You Are Here:\nMain Menu > Transactions > Manage Filters > Categories > [Expenses]",
                            kind="path_to_view")
            show_categories_expenses_menu_new()
        case "transaction_selected_menu":
            fmt.load_viewer(data="You Are Here:\nMain Menu > Transactions > [Selected Transaction]",
                            kind="path_to_view")
            show_transaction_selected_menu()
        case "transaction_selected_delete_menu":
            fmt.load_viewer(data="You Are Here:\nMain Menu > Transactions > Selected Transaction > [Confirm Deletion]",
                            kind="path_to_view")
            show_transaction_selected_delete_menu()
        case "transaction_details_menu":
            fmt.load_viewer(
                data="You Are Here:\nMain Menu > Transactions > Selected Transaction > [Transaction Details]",
                kind="path_to_view")
            show_transaction_details_menu()


def show_main_menu():
    """Displays the main menu options for primary app navigation"""
    for msg in menus["main_menu"]:
        fmt.load_viewer(data=msg[0], kind=msg[1])


def show_transaction_selected_menu():
    """Displays transaction editing options for selected transaction"""
    for msg in menus["transaction_selected_menu"]:
        fmt.load_viewer(data=msg[0], kind=msg[1])


def show_transaction_selected_delete_menu():
    for msg in menus["transaction_selected_delete_menu"]:
        fmt.load_viewer(data=msg[0], kind=msg[1])


def show_transaction_details_menu():
    """Displays transaction detail modification options"""
    for msg in menus["transaction_details_menu"]:
        fmt.load_viewer(data=msg[0], kind=msg[1])


def show_transactions_history_menu():
    """Displays the transaction history submenu options"""
    for msg in menus["transactions_history_menu"]:
        fmt.load_viewer(data=msg[0], kind=msg[1])


def show_transactions_history_filter_menu():
    for msg in menus["transactions_history_filter_menu"]:
        fmt.load_viewer(data=msg[0], kind=msg[1])


def show_transactions_history_filter_categories_menu():
    for msg in menus["transactions_history_filter_categories_menu"]:
        fmt.load_viewer(data=msg[0], kind=msg[1])


def show_categories_income_menu_new():
    """Displays all income categories available for menu selection"""
    for msg in menus["transactions_history_filter_categories_incomes_menu"]:
        fmt.load_viewer(data=msg[0], kind=msg[1])


def show_categories_expenses_menu_new():
    """Displays all income categories available for menu selection"""
    for msg in menus["transactions_history_filter_categories_expenses_menu"]:
        fmt.load_viewer(data=msg[0], kind=msg[1])


def toggle_filter(filters, sub_category, kind: str | None = None):
    try:
        if filters["category"]:
            pass
    except KeyError:
        filters["category"] = {}
    if kind == "income":
        try:
            if filters["category"][sub_category] == CATEGORIES_INCOME[sub_category]:
                del filters["category"][sub_category]
                if len(filters["category"]) == 0:
                    del filters["category"]
        except KeyError:
            filters["category"][sub_category] = CATEGORIES_INCOME[sub_category]
    if kind == "expense":
        try:
            if filters["category"][sub_category] == CATEGORIES_EXPENSES[sub_category]:
                del filters["category"][sub_category]
                if len(filters["category"]) == 0:
                    del filters["category"]
        except KeyError:
            filters["category"][sub_category] = CATEGORIES_EXPENSES[sub_category]
    return filters


messages = {
    "insert_amount": "Type in the desired amount.",
    "insufficient_funds": "Adding this expense will cause balance to be negative!",
    "insufficient_funds_continue": "Press Enter/Return to continue, insert a smaller amount or type 'cancel' to abort",
    "invalid_amount": "Amount invalid! Try again or type in 'cancel' to abort.",
    "cancel": "Type in 'cancel' if you'd like to abort.",
    "select_option": "Type in number corresponding to your choice\nOr type 'cancel' to abort.",
    "select_month": "Type in month number (1-12) or name (e.g., January)\nOr type 'cancel' to abort.",
    "select_year": "Type in year (e.g. '1970', '2025').\nOr type 'cancel' to abort.",
    "select_transaction": "Select a transaction by typing in its 'Index'\nOr type 'cancel' to abort.",
    "successful_transaction": "Transaction saved successfully!",
}

menus = {
    "main_menu": [
        ("What do you want to do?", "menu_question_main"),
        ("1. Check balance", "menu_option"),
        ("2. Add income", "menu_option"),
        ("3. Add expense", "menu_option"),
        ("4. View transactions", "menu_option"),
        ("5. Quit", "menu_option"),
        ("Type in the number corresponding to your choice:", "menu_question"),
    ],
    "transactions_history_menu": [
        ("What do you want to do?", "menu_question_main"),
        ("1. Back to main menu", "menu_option"),
        ("2. Manage filters", "menu_option"),
        ("3. Select transaction", "menu_option"),
        ("Type in the number corresponding to your choice:", "menu_question"),
    ],
    "transactions_history_filter_menu": [
        ("What do you want to do?", "menu_question_main"),
        ("1. Back to transactions", "menu_option"),
        ("2. Filter by type (income, expense)", "menu_option"),
        ("3. Filter by category", "menu_option"),
        ("4. Filter by date", "menu_option"),
        ("5. Clear all filters", "menu_option"),
        ("Type in the number corresponding to your choice:", "menu_question"),
    ],
    "transactions_history_filter_categories_menu": [
        ("What do you want to do?", "menu_question_main"),
        ("1. Back to manage filters", "menu_option"),
        ("2. Load income categories", "menu_option"),
        ("3. Load expense categories", "menu_option"),
        ("Type in the number corresponding to your choice:", "menu_question"),
    ],
    "transactions_history_filter_categories_incomes_menu": [
        ("What do you want to do?", "menu_question_main"),
        ("1. Back to filter categories", "menu_option"),
        ("2. Set filter: Salary", "menu_option"),
        ("3. Set filter: Freelance", "menu_option"),
        ("4. Set filter: Business", "menu_option"),
        ("5. Set filter: Investment", "menu_option"),
        ("6. Set filter: Gift", "menu_option"),
        ("7. Set filter: Refund", "menu_option"),
        ("8. Set filter: Other", "menu_option"),
        ("9. Clear all category filters", "menu_option"),
    ],
    "transactions_history_filter_categories_expenses_menu": [
        ("What do you want to do?", "menu_question_main"),
        ("1. Back to filter categories", "menu_option"),
        ("2. Set filter: Food & Dining", "menu_option"),
        ("3. Set filter: Housing", "menu_option"),
        ("4. Set filter: Transportation", "menu_option"),
        ("5. Set filter: Entertainment", "menu_option"),
        ("6. Set filter: Shopping", "menu_option"),
        ("7. Set filter: Healthcare", "menu_option"),
        ("8. Set filter: Utilities", "menu_option"),
        ("9. Set filter: Other", "menu_option"),
        ("10. Clear all category filters", "menu_option"),
    ],
    # Go back, Quick Filters {Go back, Today, Last 7 Days, Last 30 Days},
    # Enter Date(s) {Go back, Choose Month,
    "transactions_history_filter_datetime_menu": [
        ("What do you want to do?", "menu_question_main"),
        ("1. Go back", "menu_option"),
        ("2. Quick Filters", "menu_option"),
        ("3. Enter Date(s)", "menu_option"),
        ("4. Enter Time(s)", "menu_option"),
        ("Type in the number corresponding to your choice:", "menu_question"),
    ],
    "transactions_history_filter_datetime_quick_menu": [
        ("What do you want to do?", "menu_question_main"),
        ("1. Go back", "menu_option"),
        ("2. Today", "menu_option"),
        ("3. Last 7 Days", "menu_option"),
        ("4. Last 30 Days", "menu_option"),
        ("5. Choose month", "menu_option"),
        ("6. Choose year", "menu_option"),
        ("Type in the number corresponding to your choice:", "menu_question"),
    ],
    "transaction_selected_menu": [
        ("What do you want to do?", "menu_question_main"),
        ("1. Back to transactions", "menu_option"),
        ("2. Delete transaction", "menu_option"),
        ("3. Edit transaction", "menu_option"),
        ("Type in the number corresponding to your choice:", "menu_question"),
    ],
    "transaction_selected_delete_menu": [
        ("1. No", "menu_option"),
        ("2. Yes", "menu_option"),
    ],
    "transaction_details_menu": [
        ("What do you want to do?", "menu_question_main"),
        ("1. Back to selected transaction", "menu_option"),
        ("2. Edit transaction value", "menu_option"),
        ("3. Change transaction type", "menu_option"),
        ("4. Edit transaction category", "menu_option"),
        ("5. Edit transaction description", "menu_option"),
        ("Type in the number corresponding to your choice:", "menu_question"),
    ],
}

ascii_art = {
    "app_title": """
  ___         _    _ 
 | _ )_  _ __| |__| |
 | _ \\ || / _` / _` |
 |___/\\_,_\\__,_\\__,_|
 """
}

USER_VIEWS = {
    "main_menu": "main_menu",
    "add_income": "add_income",
    "add_expense": "add_expense",
    "transaction_details_menu": "transaction_details_menu",
    "transaction_selected_menu": "transaction_selected_menu",
    "transactions_history_menu": "transactions_history_menu",
    "transactions_history_filter_menu": "transactions_history_filter_menu",
    "transactions_history_filter_categories_menu": "transactions_history_filter_categories_menu",
    "transactions_history_filter_categories_incomes_menu": "transactions_history_filter_categories_incomes_menu",
    "transactions_history_filter_categories_expenses_menu": "transactions_history_filter_categories_expenses_menu",
    "transactions_history_filter_datetime_menu": "transactions_history_filter_datetime_menu",
    "transactions_history_filter_datetime_quick_menu": "transactions_history_filter_datetime_quick_menu",
    "transactions_history_filter_datetime_timeframe_menu": "transactions_history_filter_datetime_timeframe_menu",
    "transactions_history_selection": "transactions_history_selection",
}

MONTHS = {
    "january": "01", "jan": "01",
    "february": "02", "feb": "02",
    "march": "03", "mar": "03",
    "april": "04", "apr": "04",
    "may": "05",
    "june": "06", "jun": "06",
    "july": "07", "jul": "07",
    "august": "08", "aug": "08",
    "september": "09", "sep": "09", "sept": "09",
    "october": "10", "oct": "10",
    "november": "11", "nov": "11",
    "december": "12", "dec": "12"
}

MAIN_MENU_OPTIONS = 5
TRANSACTIONS_HISTORY_MENU = 3
TRANSACTIONS_HISTORY_FILTER_MENU = 5
TRANSACTIONS_HISTORY_FILTER_CATEGORIES_MENU = 3
TRANSACTIONS_HISTORY_FILTER_CATEGORIES_INCOMES_MENU = 9
TRANSACTIONS_HISTORY_FILTER_CATEGORIES_EXPENSES_MENU = 10
TRANSACTIONS_HISTORY_FILTER_DATETIME_MENU = 4
TRANSACTIONS_HISTORY_FILTER_DATETIME_QUICK_MENU = 6
TRANSACTION_SELECTED_MENU = 3
TRANSACTION_SELECTED_DELETE_MENU = 2
TRANSACTION_DETAILS_MENU = 5

CATEGORIES_EXPENSES = {
    "food_and_dining": "Food & Dining",
    "housing": "Housing",
    "transportation": "Transportation",
    "entertainment": "Entertainment",
    "shopping": "Shopping",
    "healthcare": "Healthcare",
    "utilities": "Utilities",
    "other": "Other",
}

CATEGORIES_INCOME = {
    "salary": "Salary",
    "freelance": "Freelance",
    "business": "Business",
    "investment": "Investment",
    "gift": "Gift",
    "refund": "Refund",
    "other": "Other",
}
