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
    "transaction_history_menu": [
        ("What do you want to do?", "menu_question_main"),
        ("1. Go back", "menu_option"),
        ("2. Filter incomes", "menu_option"),
        ("3. Filter expenses", "menu_option"),
        ("4. Filter all", "menu_option"),
        ("5. Edit transaction", "menu_option"),
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
    "transaction_details_type_category_menu": [
        ("Select new transaction type", "menu_question_main"),
        ("1. Income", "menu_option"),
        ("2. Expense", "menu_option"),
        ("Type in the number corresponding to your choice:", "menu_question"),
    ]
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
    "transaction_history_menu": "transaction_history_menu",
    "transaction_history_edit": "transaction_history_edit",
    "transaction_edit_menu": "transaction_edit_menu",
    "transaction_details_menu": "transaction_details_menu",
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
