from utils.formatters import Formatter

fmt = Formatter()


class UserView:
    MAIN_MENU = "main_menu"
    BUDGETS_MENU = "budgets_menu"
    BUDGETS_BUDGET_DETAILS_MENU = "budgets_budget_details_menu"
    BUDGETS_BUDGET_DETAILS_CATEGORIES_MENU = "budgets_budget_details_categories_menu"
    BUDGETS_BUDGET_CATEGORIES_MENU = "budgets_budget_categories_menu"
    ADD_INCOME_MENU = "add_income_menu"
    ADD_EXPENSE_MENU = "add_expense_menu"
    TRANSACTION_DETAILS_MENU = "transaction_details_menu"
    TRANSACTION_DETAILS_CATEGORY_MENU = "transaction_details_category_menu"
    TRANSACTION_SELECTED_MENU = "transaction_selected_menu"
    TRANSACTION_SELECTED_DELETE_MENU = "transaction_selected_delete_menu"
    TRANSACTIONS_HISTORY_MENU = "transactions_history_menu"
    TRANSACTIONS_HISTORY_FILTER_MENU = "transactions_history_filter_menu"
    TRANSACTIONS_HISTORY_FILTER_CATEGORIES_MENU = "transactions_history_filter_categories_menu"
    TRANSACTIONS_HISTORY_FILTER_CATEGORIES_INCOMES_MENU = "transactions_history_filter_categories_incomes_menu"
    TRANSACTIONS_HISTORY_FILTER_CATEGORIES_EXPENSES_MENU = "transactions_history_filter_categories_expenses_menu"
    TRANSACTIONS_HISTORY_FILTER_DATETIME_MENU = "transactions_history_filter_datetime_menu"
    TRANSACTIONS_HISTORY_FILTER_DATETIME_DATE_MENU = "transactions_history_filter_datetime_date_menu"
    TRANSACTIONS_HISTORY_FILTER_DATETIME_TIME_MENU = "transactions_history_filter_datetime_time_menu"
    TRANSACTIONS_HISTORY_FILTER_DATETIME_QUICK_MENU = "transactions_history_filter_datetime_quick_menu"
    TRANSACTIONS_HISTORY_SELECTION_MENU = "transactions_history_selection_menu"


MAIN_MENU_OPT = 6
BUDGETS_MENU_OPT = 3
BUDGETS_BUDGET_DETAILS_MENU_OPT = 5
BUDGETS_BUDGET_DETAILS_CATEGORIES_MENU_OPT = 3
BUDGETS_BUDGET_CATEGORIES_MENU_OPT = 8
TRANSACTIONS_HISTORY_MENU_OPT = 3
TRANSACTIONS_HISTORY_FILTER_MENU_OPT = 5
TRANSACTIONS_HISTORY_FILTER_CATEGORIES_MENU_OPT = 3
TRANSACTIONS_HISTORY_FILTER_CATEGORIES_INCOMES_MENU_OPT = 9
TRANSACTIONS_HISTORY_FILTER_CATEGORIES_EXPENSES_MENU_OPT = 10
TRANSACTIONS_HISTORY_FILTER_DATETIME_MENU_OPT = 4
TRANSACTIONS_HISTORY_FILTER_DATETIME_QUICK_MENU_OPT = 4
TRANSACTION_SELECTED_MENU_OPT = 3
TRANSACTION_SELECTED_DELETE_MENU_OPT = 2
TRANSACTION_DETAILS_MENU_OPT = 5
TRANSACTION_DETAILS_CATEGORY_INCOMES_MENU_OPT = 8
TRANSACTION_DETAILS_CATEGORY_EXPENSES_MENU_OPT = 9

MAX_DESCRIPTION_LENGTH = 50
MAX_NAME_LENGTH = 20

BREADCRUMBS = {
    "main_menu": "You Are Here:\n[Main Menu]",
    "budgets_menu": "You Are Here:\nMain Menu > [Budgets]",
    "budgets_budget_details_menu": "You Are Here:\nMain Menu > Budgets > [Budget Details]",
    "budgets_budget_details_categories_menu": "You Are Here:\nMain Menu > Budgets > Budget Details > [Categories]",
    "transactions_history_menu": "You Are Here:\nMain Menu > [Transactions]",
    "transactions_history_filter_menu": "You Are Here:\nMain Menu > Transactions > [Manage Filters]",
    "transactions_history_filter_categories_menu": "You Are Here:\nMain Menu > Transactions > Manage Filters > [Categories]",
    "transactions_history_filter_categories_incomes_menu": "You Are Here:\nMain Menu > Transactions > Manage Filters > Categories > [Incomes]",
    "transactions_history_filter_categories_expenses_menu": "You Are Here:\nMain Menu > Transactions > Manage Filters > Categories > [Expenses]",
    "transactions_history_filter_datetime_menu": "You Are Here:\nMain Menu > Transactions > Manage Filters > [Date & Time]",
    "transactions_history_filter_datetime_quick_menu": "You Are Here:\nMain Menu > Transactions > Manage Filters > Date & Time > [Quick Filters]",
    "transaction_selected_menu": "You Are Here:\nMain Menu > Transactions > [Selected Transaction]",
    "transaction_selected_delete_menu": "You Are Here:\nMain Menu > Transactions > Selected Transaction > [Confirm Deletion]",
    "transaction_details_menu": "You Are Here:\nMain Menu > Transactions > Selected Transaction > [Transaction Details]",
    "transaction_details_category_menu": "You Are Here:\nMain Menu > Transactions > Selected Transaction > Transaction Details > [Categories]",
}

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

MESSAGES = {
    "error_message_general": "Something went wrong. Please try again.",
    "add_date": "Type in the date (YYYY-MM-DD / YYYY MM DD) or type 'cancel' to abort.",
    "add_date_end": "Type in the end date. Press Enter/Return to continue\nor type 'cancel' to abort.",
    "add_time": "Type in the time (HH:MM:SS / HH:MM) or type 'cancel' to abort.",
    "add_time_end": "Type in the end time. Press Enter/Return to continue\nor type 'cancel' to abort.",
    "add_limit": "Type in the budget's limit or type 'cancel' to abort.",
    "add_name": "Type in the desired name or type 'cancel' to abort.",
    "insert_amount": "Type in the desired amount.",
    "insert_description": "Type in the desired description, or type in 'cancel' to abort.",
    "insufficient_funds": "Adding this expense will cause balance to be negative!",
    "insufficient_funds_continue": "Press Enter/Return to continue, insert a smaller amount or type 'cancel' to abort",
    "invalid_amount": "Amount invalid! Try again or type in 'cancel' to abort.",
    "invalid_date": "Date invalid! Accepted format is YYYY-MM-DD or YYYY MM DD.\nType 'cancel' to abort.",
    "invalid_time": "Time invalid! Accepted format is HH:MM:DD or HH:MM.\nType 'cancel' to abort.",
    "invalid_description": "Desired description is too long! Try again or type in 'cancel' to abort.",
    "invalid_name": "The name you entered is too long! Try again or type in 'cancel' to abort.",
    "invalid_text": "Try typing in only letters and numbers, nothing fancier than that.\nOr 'cancel' to abort.",
    "cancel": "Type in 'cancel' if you'd like to abort.",
    "category_already_selected": "This category is already selected. Choose a different one or type 'cancel' to abort.",
    "category_delete_successful": "Category was successfully deleted.",
    "select_budget": "Select a budget by typing in its 'Index'\nOr type 'cancel' to abort.",
    "select_budget_category": "Choose a budget category or type 'cancel' to abort.",
    "select_option": "Type in number corresponding to your choice\nOr type 'cancel' to abort.",
    "select_month": "Type in month number (1-12) or name (e.g., January)\nOr type 'cancel' to abort.",
    "select_year": "Type in year (e.g. '1970', '2025').\nOr type 'cancel' to abort.",
    "select_transaction": "Select a transaction by typing in its 'Index'\nOr type 'cancel' to abort.",
    "budget_save_successful": "Budget saved successfully!",
    "budget_delete_successful": "Budget deleted successfully!",
    "successful_transaction": "Transaction saved successfully!",
    "successful_transaction_update": "Transaction updated successfully!",
    "successful_transaction_deleted": "Transaction deleted successfully!",
}

MENUS = {
    "main_menu": [
        ("What do you want to do?", "menu_question_main"),
        ("1. Check balance", "menu_option"),
        ("2. Add income", "menu_option"),
        ("3. Add expense", "menu_option"),
        ("4. View transactions", "menu_option"),
        ("5. View budgets", "menu_option"),
        ("6. Quit", "menu_option"),
        ("Type in the number corresponding to your choice:", "menu_question"),
    ],
    "budgets_menu": [
        ("What do you want to do?", "menu_question_main"),
        ("1. Back to main menu", "menu_option"),
        ("2. Create budget", "menu_option"),
        ("3. Select budget", "menu_option"),
        ("Type in the number corresponding to your choice:", "menu_question"),
    ],
    "budgets_budget_details_menu": [
        ("What do you want to do?", "menu_question_main"),
        ("1. Back to budgets", "menu_option"),
        ("2. Edit budget name", "menu_option"),
        ("3. Edit spending limit", "menu_option"),
        ("4. Edit categories", "menu_option"),
        ("5. Delete budget", "menu_option"),
        ("Type in the number corresponding to your choice:", "menu_question"),
    ],
    "budgets_budget_details_categories_menu": [
        ("What do you want to do?", "menu_question_main"),
        ("1. Back to budget details", "menu_option"),
        ("2. Add Category", "menu_option"),
        ("3. Delete Category", "menu_option"),
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
        ("4. Filter by date or time", "menu_option"),
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
    "transactions_history_filter_datetime_menu": [
        ("What do you want to do?", "menu_question_main"),
        ("1. Back to manage filters", "menu_option"),
        ("2. Quick Filters", "menu_option"),
        ("3. Enter Date(s)", "menu_option"),
        ("4. Enter Timeframe", "menu_option"),
        ("Type in the number corresponding to your choice:", "menu_question"),
    ],
    "transactions_history_filter_datetime_quick_menu": [
        ("What do you want to do?", "menu_question_main"),
        ("1. Back to date filters", "menu_option"),
        ("2. Today", "menu_option"),
        ("3. Last 7 Days", "menu_option"),
        ("4. Last 30 Days", "menu_option"),
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
    "transaction_details_category_incomes_menu": [
        ("Choose the new category", "menu_question_main"),
        ("1. Back to selected transaction", "menu_option"),
        ("2. Salary", "menu_option"),
        ("3. Freelance", "menu_option"),
        ("4. Business", "menu_option"),
        ("5. Investment", "menu_option"),
        ("6. Gift", "menu_option"),
        ("7. Refund", "menu_option"),
        ("8. Other", "menu_option"),
        ("Type in the number corresponding to your choice:", "menu_question"),
    ],
    "transaction_details_category_expenses_menu": [
        ("Choose the new category", "menu_question_main"),
        ("1. Back to selected transaction", "menu_option"),
        ("2. Food & Dining", "menu_option"),
        ("3. Housing", "menu_option"),
        ("4. Transportation", "menu_option"),
        ("5. Entertainment", "menu_option"),
        ("6. Shopping", "menu_option"),
        ("7. Healthcare", "menu_option"),
        ("8. Utilities", "menu_option"),
        ("9. Other", "menu_option"),
        ("Type in the number corresponding to your choice:", "menu_question"),
    ],
}

ASCII_ART = {
    "app_title": """
  ___         _    _ 
 | _ )_  _ __| |__| |
 | _ \\ || / _` / _` |
 |___/\\_,_\\__,_\\__,_|
 """
}


def load_menu(user_view, transaction=None):
    """Displays relevant menu items and breadcrumbs for the user"""
    if user_view in BREADCRUMBS:
        fmt.load_viewer(data=BREADCRUMBS[user_view], kind="path_to_view")
    if transaction:
        if transaction.kind == "income":
            for msg in MENUS["transaction_details_category_incomes_menu"]:
                fmt.load_viewer(data=msg[0], kind=msg[1])
        elif transaction.kind == "expense":
            for msg in MENUS["transaction_details_category_expenses_menu"]:
                fmt.load_viewer(data=msg[0], kind=msg[1])
    else:
        for msg in MENUS[user_view]:
            fmt.load_viewer(data=msg[0], kind=msg[1])


def load_menu_helper(mode):
    """Displays categories available for selection"""
    i = 1
    if mode == "income":
        for category in CATEGORIES_INCOME:
            fmt.load_viewer(data=f"{i}. {CATEGORIES_INCOME[category]}", kind="menu_option")
            i += 1
    elif mode == "expense":
        for category in CATEGORIES_EXPENSES:
            fmt.load_viewer(data=f"{i}. {CATEGORIES_EXPENSES[category]}", kind="menu_option")
            i += 1
    elif mode == "budget":
        all_cats = []
        # for category in CATEGORIES_INCOME:
        #     all_cats.append(CATEGORIES_INCOME[category])
        for category in CATEGORIES_EXPENSES:
            if CATEGORIES_EXPENSES[category] not in all_cats:
                all_cats.append(CATEGORIES_EXPENSES[category])
        for cat in all_cats:
            fmt.load_viewer(data=f"{i}. {cat}", kind="menu_option")
            i += 1
        fmt.load_viewer(data=MESSAGES["select_option"], kind="menu_question")


def add_timestamp_filter(filters: dict, start, end, mode: str | None = None):
    """Adds a filter that acts on the transaction's timestamp property"""
    date_filters = []
    new_entry = {}
    try:
        if filters["timestamp"]:
            pass
    except KeyError:
        filters["timestamp"] = []
    for entry in filters["timestamp"]:
        date_filters.append(entry)
    if mode == "date":
        new_entry["date"] = (start, end)
        if new_entry["date"] not in date_filters:
            date_filters.append(new_entry)
    elif mode == "time":
        new_entry["time"] = (start, end)
        if new_entry["time"] not in date_filters:
            date_filters.append(new_entry)
    filters["timestamp"] = date_filters
    return filters


def toggle_filter(filters, sub_category, kind: str | None = None):
    """Toggles a category filter"""
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
