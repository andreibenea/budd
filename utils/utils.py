messages = {
    "cancel": "Type in 'cancel' if you'd like to abort.",
    "select_option": "Type in number corresponding to your choice\nOr type 'cancel' to abort.",
    "select_transaction": "Select a transaction by typing its 'Index'\nOr type 'cancel' to abort.",
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
        ("1. Go back", "menu_option"),
        ("2. Apply filter", "menu_option"),
        ("3. Reset filters", "menu_option"),
        ("4. Edit transactions", "menu_option"),
        ("Type in the number corresponding to your choice:", "menu_question"),
        # ("2. Filter incomes", "menu_option"),  # old version
        # ("3. Filter expenses", "menu_option"),  # old version
    ],
    "transactions_history_filter_menu": [
        ("What do you want to do?", "menu_question_main"),
        ("1. Go back", "menu_option"),
        ("2. Date & Time Filters", "menu_option"),
        ("3. Show income transactions", "menu_option"),
        ("4. Show expense transactions", "menu_option"),
        ("Type in the number corresponding to your choice:", "menu_question"),
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
    "transaction_edit_menu": [
        ("What do you want to do?", "menu_question_main"),
        ("1. Go back", "menu_option"),
        ("2. Delete transaction", "menu_option"),
        ("3. Edit transaction", "menu_option"),
        ("Type in the number corresponding to your choice:", "menu_question"),
    ],
    "transaction_details_menu": [
        ("What do you want to do?", "menu_question_main"),
        ("1. Edit transaction value", "menu_option"),
        ("2. Change transaction type", "menu_option"),
        ("3. Edit transaction category", "menu_option"),
        ("4. Edit transaction description", "menu_option"),
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

USER_STATUSES = {
    "main_menu": "main_menu",
    "transactions_history_menu": "transactions_history_menu",
    "transactions_history_filter_menu": "transactions_history_filter_menu",
    "transactions_history_selection": "transactions_history_selection",
    "transaction_edit_menu": "transaction_edit_menu",
    "transaction_details_menu": "transaction_details_menu",
    "transactions_history_filter_datetime_menu": "transactions_history_filter_datetime_menu",
    "transactions_history_filter_datetime_quick_menu": "transactions_history_filter_datetime_quick_menu",
}

MAIN_MENU_OPTIONS = 5
TRANSACTIONS_HISTORY_MENU = 4
TRANSACTIONS_HISTORY_FILTER_MENU = 4
TRANSACTIONS_HISTORY_FILTER_DATETIME_MENU = 4
TRANSACTIONS_HISTORY_FILTER_DATETIME_QUICK_MENU = 6
TRANSACTION_EDIT_MENU = 3
TRANSACTION_DETAILS_MENU = 4

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
