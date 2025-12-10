import sys

from models.account import Account
from models.budget import Budget
from models.transaction import Transaction
from utils.utils import load_menu, load_menu_helper, add_timestamp_filter, toggle_filter, MESSAGES, ASCII_ART, \
    UserView as view
from utils.file_handler import FileHandler
from utils.formatters import Formatter
from utils.validators import ValidateUserInput as validator
from datetime import datetime, timedelta

fmt = Formatter()
fh = FileHandler()
try:
    acc = fh.load_account()
except FileNotFoundError:
    acc = Account()


def show_app_name():
    fmt.load_viewer(data=ASCII_ART["app_title"], kind="menu_question_main")
    fmt.load_viewer(data="### CLI BUDGET APP ###\n", kind="app_description")


def main_loop():
    """Maintains the main application loop and delegates command handling"""
    user_view = view.MAIN_MENU
    filters = {}
    editing = None
    while True:
        match user_view:
            case "main_menu":
                user_view, filters, editing = loop_main_menu(user_view, filters, editing)
            case "budgets_menu":
                user_view, filters, editing = loop_budgets_menu(user_view, filters, editing)
            case "budgets_budget_details_menu":
                user_view, filters, editing = loop_budgets_budget_details_menu(user_view, filters, editing)
            case "budgets_budget_details_categories_menu":
                user_view, filters, editing = loop_budgets_budget_details_categories_menu(user_view, filters, editing)
            case "transaction_selected_menu":
                user_view, filters, editing = loop_transaction_selected_menu(user_view, filters, editing)
            case "transaction_details_menu":
                user_view, filters, editing = loop_transactions_details_menu(user_view, filters, editing)
            case "transaction_details_category_menu":
                user_view, filters, editing = loop_transaction_details_category_menu(user_view, filters, editing)
            case "transactions_history_menu":
                """Starts up transactions history menu"""
                user_view, filters, editing = loop_transactions_history_menu(user_view, filters, editing)
            case "transactions_history_filter_menu":
                user_view, filters, editing = loop_transactions_history_filter_menu(user_view, filters, editing)
            case "transactions_history_filter_categories_menu":
                user_view, filters, editing = loop_transactions_history_filter_categories_menu(user_view, filters,
                                                                                               editing)
            case "transactions_history_filter_categories_incomes_menu":
                user_view, filters, editing = loop_transactions_history_filter_categories_incomes_menu(user_view,
                                                                                                       filters,
                                                                                                       editing)
            case "transactions_history_filter_categories_expenses_menu":
                user_view, filters, editing = loop_transactions_history_filter_categories_expenses_menu(user_view,
                                                                                                        filters,
                                                                                                        editing)
            case "transactions_history_filter_datetime_menu":
                user_view, filters, editing = loop_transactions_history_filter_datetime_menu(user_view, filters,
                                                                                             editing)
            case "transactions_history_filter_datetime_date_menu":
                user_view, filters, editing = loop_transactions_history_filter_datetime_date_menu(user_view, filters,
                                                                                                  editing)
            case "transactions_history_filter_datetime_time_menu":
                user_view, filters, editing = loop_transactions_history_filter_datetime_time_menu(user_view, filters,
                                                                                                  editing)
            case "transactions_history_filter_datetime_quick_menu":
                user_view, filters, editing = loop_transactions_history_filter_datetime_quick_menu(user_view, filters,
                                                                                                   editing)


def loop_main_menu(user_view, filters, editing):
    load_menu(user_view)
    user_input = input("> ").strip().lower()
    is_valid, user_input = validator.validate_selection(choice=user_input, user_view=user_view)
    if is_valid:
        match int(user_input):
            case 1:
                """Check current balance"""
                fmt.load_viewer(data=f"Current balance: ${acc.check_balance():.2f}",
                                kind="balance_good" if acc.check_balance() >= 0 else "balance_bad")
            case 2:
                """Add income"""
                create_transaction("income")
            case 3:
                """Add expense"""
                create_transaction("expense")
            case 4:
                """View all transactions"""
                user_view = view.TRANSACTIONS_HISTORY_MENU
            case 5:
                """View all budgets"""
                user_view = view.BUDGETS_MENU
            case 6:
                """Quit the program"""
                return sys.exit()
    return user_view, filters, editing


def loop_budgets_menu(user_view, filters, editing):
    budgets = acc.get_budgets()
    fmt.display_budgets(budgets, acc.get_transactions())
    load_menu(user_view)
    user_input = input("> ").strip().lower()
    is_valid, user_input = validator.validate_selection(choice=user_input, user_view=user_view)
    if is_valid:
        match int(user_input):
            case 1:
                """Back to main menu"""
                editing = None
                user_view = view.MAIN_MENU
            case 2:
                """Create budget"""
                create_budget()
            case 3:
                """Select budget"""
                editing = select_entry(items_list=budgets, mode="budget")
                if editing:
                    user_view = view.BUDGETS_BUDGET_DETAILS_MENU
    return user_view, filters, editing


def loop_budgets_budget_details_menu(user_view, filters, editing):
    fmt.display_budgets(data=editing, transactions=acc.get_transactions())
    load_menu(user_view)
    user_input = input("> ").strip().lower()
    is_valid, user_input = validator.validate_selection(choice=user_input, user_view=user_view)
    if is_valid:
        match int(user_input):
            case 1:
                """Back to budgets menu"""
                user_view = view.BUDGETS_MENU
            case 2:
                """Edit budget name"""
                fmt.load_viewer(data=MESSAGES["add_name"], kind="menu_question_main")
                new_name = input("> ").strip().lower()
                is_name_valid, new_name = validator.validate_text(text=new_name, kind="name")
                if is_name_valid:
                    for budget in acc.get_budgets():
                        if budget == editing:
                            budget.name = new_name.capitalize()
                            editing = budget
                    fh.save_account(acc)
                    fmt.load_viewer(data=MESSAGES["budget_save_successful"], kind="success")
                else:
                    fmt.load_viewer(data=MESSAGES["error_message_general"], kind="failure")
            case 3:
                """Edit spending limit"""
                fmt.load_viewer(data=MESSAGES["insert_amount"], kind="menu_question_main")
                new_limit = input("> ").strip().lower()
                is_amount_valid, new_limit = validator.is_amount_valid(account=acc, amount=new_limit, kind="income")
                if is_amount_valid:
                    for budget in acc.get_budgets():
                        if budget == editing:
                            budget.limit = new_limit
                            editing = budget
                    fh.save_account(acc)
                    fmt.load_viewer(data=MESSAGES["budget_save_successful"], kind="success")
                else:
                    fmt.load_viewer(data=MESSAGES["error_message_general"], kind="failure")
            case 4:
                """Edit categories"""
                user_view = view.BUDGETS_BUDGET_DETAILS_CATEGORIES_MENU
            case 5:
                """Delete budget"""
                fmt.load_viewer(data=f"This will permanently delete {editing}\nAre you sure?", kind="warning")
                load_menu(view.TRANSACTION_SELECTED_DELETE_MENU)
                user_input = input("> ").strip().lower()
                is_valid, user_input = validator.validate_selection(choice=user_input,
                                                                    user_view="transaction_selected_delete_menu")
                if is_valid:
                    match int(user_input):
                        case 1:
                            """Back to selected transaction"""
                            return user_view, filters, editing
                        case 2:
                            """Delete selected transaction"""
                            acc.delete_budget(editing)
                            editing = None
                            fh.save_account(account=acc)
                            fmt.load_viewer(data=MESSAGES["budget_delete_successful"], kind="success")
                            user_view = view.BUDGETS_MENU
    return user_view, filters, editing


def loop_budgets_budget_details_categories_menu(user_view, filters, editing):
    fmt.display_budgets(data=editing, transactions=acc.get_transactions())
    load_menu(user_view)
    user_input = input("> ").strip().lower()
    is_valid, user_input = validator.validate_selection(choice=user_input, user_view=user_view)
    if is_valid:
        match int(user_input):
            case 1:
                """Back to budget details"""
                user_view = view.BUDGETS_BUDGET_DETAILS_MENU
            case 2:
                """Add category"""
                fmt.load_viewer(data=MESSAGES["select_budget_category"], kind="menu_question_main")
                load_menu_helper(mode="budget")
                user_choice = input("> ").strip().lower()
                is_choice_valid, user_choice = validator.validate_selection(choice=user_choice,
                                                                            user_view=view.BUDGETS_BUDGET_CATEGORIES_MENU,
                                                                            kind="budget")
                for budget in acc.get_budgets():
                    if budget == editing:
                        while True:
                            if user_choice in budget.categories:
                                fmt.load_viewer(data=MESSAGES["category_already_selected"], kind="warning")
                                user_choice = input("> ").strip().lower()
                                is_choice_valid, user_choice = validator.validate_selection(choice=user_choice,
                                                                                            user_view=view.BUDGETS_BUDGET_CATEGORIES_MENU,
                                                                                            kind="budget")
                                continue
                            if is_choice_valid:
                                if user_choice not in budget.categories:
                                    budget.categories.append(user_choice)
                                fmt.load_viewer(
                                    data="Would you like to add another category?\n\t* Y / N *\nYou can also type 'cancel' to abort.",
                                    kind="menu_question")
                                confirmation = input("> ").strip().lower()
                                if confirmation == "n" or confirmation == "cancel":
                                    break
                                elif confirmation == "y":
                                    fmt.load_viewer(data=MESSAGES["select_budget_category"], kind="menu_question_main")
                                    load_menu_helper(mode="budget")
                                    user_choice = input("> ").strip().lower()
                                    is_choice_valid, user_choice = validator.validate_selection(choice=user_choice,
                                                                                                user_view=view.BUDGETS_BUDGET_CATEGORIES_MENU,
                                                                                                kind="budget")
                                else:
                                    fmt.load_viewer(data="Type in either 'y' or 'n'", kind="warning")
                                    user_choice = input("> ").strip().lower()
                                    is_choice_valid, user_choice = validator.validate_selection(choice=user_choice,
                                                                                                user_view=view.BUDGETS_BUDGET_CATEGORIES_MENU,
                                                                                                kind="budget")
                            else:
                                return user_view, filters, editing
                return user_view, filters, editing
            case 3:
                """Delete category"""
                fmt.load_viewer(data=MESSAGES["select_budget_category"], kind="menu_question_main")
                for budget in acc.get_budgets():
                    if budget == editing:
                        if len(budget.categories) <= 1:
                            fmt.load_viewer(data=f"A budget must have at least one category! Cannot complete action.",
                                            kind="failure")
                            return user_view, filters, editing
                        i = 1
                        choices = []
                        for category in budget.categories:
                            fmt.load_viewer(data=f"{i}. {category}", kind="menu_option")
                            choices.append(i)
                            i += 1
                            print(f"[DEBUG] i after each: {i}")
                        fmt.load_viewer(data=MESSAGES["select_option"], kind="menu_question")
                        user_input = input("> ").strip().lower()
                        while True:
                            try:
                                if user_input == "cancel":
                                    return user_view, filters, editing
                                user_input = int(user_input)
                                if user_input not in choices:
                                    raise ValueError
                                break
                            except ValueError:
                                fmt.load_viewer(data=MESSAGES["select_option"], kind="warning")
                                user_input = input("> ").strip().lower()
                        print(f"[DEBUG] i before c: {i}")
                        c = 2
                        for category in budget.categories:
                            if c == i:
                                budget.categories.remove(category)
                                fh.save_account(acc)
                                fmt.load_viewer(data=MESSAGES["category_delete_successful"], kind="success")
                            c += 1
    return user_view, filters, editing


def loop_transactions_history_menu(user_view, filters, editing):
    filtered_transactions = acc.filter_transactions(transactions=acc.get_transactions(), filters=filters)
    fmt.load_viewer(data=filtered_transactions, kind="transactions_list")
    load_menu(user_view)
    user_input = input("> ").strip().lower()
    is_valid, user_input = validator.validate_selection(choice=user_input, user_view=user_view)
    if is_valid:
        match int(user_input):
            case 1:
                """Go back to main menu"""
                filters = {}
                user_view = view.MAIN_MENU
            case 2:
                """Manage filters"""
                user_view = view.TRANSACTIONS_HISTORY_FILTER_MENU
            case 3:
                """Select transaction"""
                selected_transaction = select_entry(items_list=filtered_transactions, mode="transaction")
                if selected_transaction:
                    editing = selected_transaction
                    user_view = view.TRANSACTION_SELECTED_MENU
    return user_view, filters, editing


def loop_transactions_history_filter_menu(user_view, filters, editing):
    """ Handles filter management menu where users can:
        - Toggle transaction type (income/expense)
        - Select categories to filter
        - Add date/time filters
        - Clear all filters """
    filtered_transactions = acc.filter_transactions(acc.get_transactions(), filters)
    fmt.load_viewer(data=filtered_transactions, kind="transactions_list")
    load_menu(user_view)
    user_input = input("> ").strip().lower()
    is_valid, user_input = validator.validate_selection(choice=user_input, user_view=user_view)
    if is_valid:
        match int(user_input):
            case 1:
                """Go back to transactions history"""
                user_view = view.TRANSACTIONS_HISTORY_MENU
            case 2:
                """Type: [Current: All]"""
                if "kind" in filters:
                    if filters["kind"] == "income":
                        filters["kind"] = "expense"
                    elif filters["kind"] == "expense":
                        filters["kind"] = "income"
                else:
                    filters["kind"] = "income"
            case 3:
                """Category: [Current: All]"""
                if "kind" in filters:
                    if filters["kind"] == "income":
                        user_view = view.TRANSACTIONS_HISTORY_FILTER_CATEGORIES_INCOMES_MENU
                    elif filters["kind"] == "expense":
                        user_view = view.TRANSACTIONS_HISTORY_FILTER_CATEGORIES_EXPENSES_MENU
                else:
                    user_view = view.TRANSACTIONS_HISTORY_FILTER_CATEGORIES_MENU
            case 4:
                """Date: [Current: All years]"""
                user_view = view.TRANSACTIONS_HISTORY_FILTER_DATETIME_MENU
            case 5:
                """Clear all filters"""
                filters = {}
    return user_view, filters, editing


def loop_transactions_history_filter_categories_menu(user_view, filters, editing):
    filtered_transactions = acc.filter_transactions(acc.get_transactions(), filters)
    fmt.load_viewer(data=filtered_transactions, kind="transactions_list")
    load_menu(user_view)
    user_input = input("> ").strip().lower()
    is_valid, user_input = validator.validate_selection(choice=user_input, user_view=user_view)
    if is_valid:
        match int(user_input):
            case 1:
                """Go back to manage filters"""
                user_view = view.TRANSACTIONS_HISTORY_FILTER_MENU
            case 2:
                """Load income categories"""
                user_view = view.TRANSACTIONS_HISTORY_FILTER_CATEGORIES_INCOMES_MENU
            case 3:
                """Load expense categories"""
                user_view = view.TRANSACTIONS_HISTORY_FILTER_CATEGORIES_EXPENSES_MENU
    return user_view, filters, editing


def loop_transactions_history_filter_categories_incomes_menu(user_view, filters, editing):
    filtered_transactions = acc.filter_transactions(acc.get_transactions(), filters)
    fmt.load_viewer(data=filtered_transactions, kind="transactions_list")
    load_menu(user_view)
    user_input = input("> ").strip().lower()
    is_valid, user_input = validator.validate_selection(choice=user_input, user_view=user_view)
    if is_valid:
        match int(user_input):
            case 1:
                """Go back to filter categories menu"""
                if "kind" in filters:
                    user_view = view.TRANSACTIONS_HISTORY_FILTER_MENU
                else:
                    user_view = view.TRANSACTIONS_HISTORY_FILTER_CATEGORIES_MENU
            case 2:
                """Set filter: Salary"""
                filters = toggle_filter(filters=filters, sub_category="salary", kind="income")
            case 3:
                """Set filter: Freelance"""
                filters = toggle_filter(filters=filters, sub_category="freelance", kind="income")
            case 4:
                """Set filter: Business"""
                filters = toggle_filter(filters=filters, sub_category="business", kind="income")
            case 5:
                """Set filter: Investment"""
                filters = toggle_filter(filters=filters, sub_category="investment", kind="income")
            case 6:
                """Set filter: Gift"""
                filters = toggle_filter(filters=filters, sub_category="gift", kind="income")
            case 7:
                """Set filter: Refund"""
                filters = toggle_filter(filters=filters, sub_category="refund", kind="income")
            case 8:
                """Set filter: Other"""
                filters = toggle_filter(filters=filters, sub_category="other", kind="income")
            case 9:
                """Clear all category filters"""
                try:
                    if filters["category"]:
                        del filters["category"]
                except KeyError:
                    pass
    return user_view, filters, editing


def loop_transactions_history_filter_categories_expenses_menu(user_view, filters, editing):
    filtered_transactions = acc.filter_transactions(acc.get_transactions(), filters)
    fmt.load_viewer(data=filtered_transactions, kind="transactions_list")
    load_menu(user_view)
    user_input = input("> ").strip().lower()
    is_valid, user_input = validator.validate_selection(choice=user_input, user_view=user_view)
    if is_valid:
        match int(user_input):
            case 1:
                """Go back to filter categories menu"""
                if "kind" in filters:
                    user_view = view.TRANSACTIONS_HISTORY_FILTER_MENU
                else:
                    user_view = view.TRANSACTIONS_HISTORY_FILTER_CATEGORIES_MENU
            case 2:
                """Set filter: Food & Dining"""
                filters = toggle_filter(filters=filters, sub_category="food_and_dining", kind="expense")
            case 3:
                """Set filter: Housing"""
                filters = toggle_filter(filters=filters, sub_category="housing", kind="expense")
            case 4:
                """Set filter: Transportation"""
                filters = toggle_filter(filters=filters, sub_category="transportation", kind="expense")
            case 5:
                """Set filter: Entertainment"""
                filters = toggle_filter(filters=filters, sub_category="entertainment", kind="expense")
            case 6:
                """Set filter: Shopping"""
                filters = toggle_filter(filters=filters, sub_category="shopping", kind="expense")
            case 7:
                """Set filter: Healthcare"""
                filters = toggle_filter(filters=filters, sub_category="healthcare", kind="expense")
            case 8:
                """Set filter: Utilities"""
                filters = toggle_filter(filters=filters, sub_category="utilities", kind="expense")
            case 9:
                """Set filter: Other"""
                filters = toggle_filter(filters=filters, sub_category="other", kind="expense")
            case 10:
                """Clear all category filters"""
                try:
                    if filters["category"]:
                        del filters["category"]
                except KeyError:
                    pass
    return user_view, filters, editing


def loop_transactions_history_filter_datetime_menu(user_view, filters, editing):
    filtered_transactions = acc.filter_transactions(acc.get_transactions(), filters)
    fmt.load_viewer(data=filtered_transactions, kind="transactions_list")
    load_menu(user_view)
    user_input = input("> ").strip().lower()
    is_valid, user_input = validator.validate_selection(choice=user_input, user_view=user_view)
    if is_valid:
        match int(user_input):
            case 1:
                """Back to manage filters menu"""
                user_view = view.TRANSACTIONS_HISTORY_FILTER_MENU
            case 2:
                """Load quick filters menu"""
                user_view = view.TRANSACTIONS_HISTORY_FILTER_DATETIME_QUICK_MENU
            case 3:
                """Add individual dates to filters"""
                user_view = view.TRANSACTIONS_HISTORY_FILTER_DATETIME_DATE_MENU
            case 4:
                """Add individual timeframes to filters"""
                user_view = view.TRANSACTIONS_HISTORY_FILTER_DATETIME_TIME_MENU
    return user_view, filters, editing


def loop_transactions_history_filter_datetime_date_menu(user_view, filters, editing):
    start_date = None
    end_date = None
    filtered_transactions = acc.filter_transactions(acc.get_transactions(), filters)
    fmt.load_viewer(data=filtered_transactions, kind="transactions_list")
    fmt.load_viewer(data=MESSAGES["add_date"], kind="menu_question_main")
    user_input = input("> ").strip().lower()
    is_start_date_valid, user_input = validator.is_date_valid(date=user_input)
    if is_start_date_valid:
        start_date = datetime.fromisoformat(user_input)
        fmt.load_viewer(data=MESSAGES["add_date_end"], kind="menu_question_main")
        user_input = input("> ").strip().lower()
        is_end_date_valid, user_input = validator.is_date_valid(date=user_input)
        if is_end_date_valid:
            end_date = datetime.fromisoformat(user_input)
        else:
            end_date = start_date + timedelta(hours=24)
    if start_date and end_date:
        filters = add_timestamp_filter(filters, start_date, end_date, "date")
    user_view = view.TRANSACTIONS_HISTORY_FILTER_DATETIME_MENU
    return user_view, filters, editing


def loop_transactions_history_filter_datetime_time_menu(user_view, filters, editing):
    start_time = None
    end_time = None
    filtered_transactions = acc.filter_transactions(acc.get_transactions(), filters)
    fmt.load_viewer(data=filtered_transactions, kind="transactions_list")
    fmt.load_viewer(data=MESSAGES["add_time"], kind="menu_question_main")
    user_input = input("> ").strip().lower()
    is_time_valid, user_input = validator.is_time_valid(time_input=user_input)
    if is_time_valid:
        start_time = datetime.fromisoformat(f"1900-01-01T{user_input}").time()
        fmt.load_viewer(data=MESSAGES["add_time_end"], kind="menu_question_main")
        user_input = input("> ").strip().lower()
        is_end_time_valid, user_input = validator.is_time_valid(time_input=user_input)
        if is_end_time_valid:
            end_time = datetime.fromisoformat(f"1900-01-01T{user_input}").time()
        else:
            end_time = (datetime.fromisoformat(f"1900-01-01T{start_time.strftime('%H:%M:%S')}")
                        + timedelta(minutes=1)).time()
    if start_time and end_time:
        filters = add_timestamp_filter(filters, start_time, end_time, "time")
    user_view = view.TRANSACTIONS_HISTORY_FILTER_DATETIME_MENU
    return user_view, filters, editing


def loop_transactions_history_filter_datetime_quick_menu(user_view, filters, editing):
    filtered_transactions = acc.filter_transactions(acc.get_transactions(), filters)
    fmt.load_viewer(data=filtered_transactions, kind="transactions_list")
    load_menu(user_view)
    user_input = input("> ").strip().lower()
    is_valid, user_input = validator.validate_selection(choice=user_input, user_view=user_view)
    today_midnight = datetime.today().replace(hour=0, minute=0, second=0, microsecond=0)
    if is_valid:
        match int(user_input):
            case 1:
                """Back to datetime filters menu"""
                user_view = view.TRANSACTIONS_HISTORY_FILTER_DATETIME_MENU
            case 2:
                """Today"""
                if "timestamp" in filters:
                    del filters["timestamp"]
                filters = add_timestamp_filter(filters, today_midnight, datetime.now(), "date")
            case 3:
                """Last 7 Days"""
                if "timestamp" in filters:
                    del filters["timestamp"]
                filters = add_timestamp_filter(filters, today_midnight - timedelta(days=7), datetime.now(), "date")
            case 4:
                """Last 30 Days"""
                if "timestamp" in filters:
                    del filters["timestamp"]
                filters = add_timestamp_filter(filters, today_midnight - timedelta(days=30), datetime.now(), "date")
    return user_view, filters, editing


def loop_transaction_selected_menu(user_view, filters, editing):
    fmt.load_viewer(data=[editing], kind="transaction_details")
    load_menu(user_view)
    user_input = input("> ").strip().lower()
    is_valid, user_input = validator.validate_selection(choice=user_input, user_view=user_view)
    if is_valid:
        match int(user_input):
            case 1:
                """Go back to transactions menu"""
                editing = None
                user_view = view.TRANSACTIONS_HISTORY_MENU
            case 2:
                """Delete transaction"""
                fmt.load_viewer(data=f"This will permanently delete {editing}\nAre you sure?", kind="warning")
                load_menu(view.TRANSACTION_SELECTED_DELETE_MENU)
                user_input = input("> ").strip().lower()
                is_valid, user_input = validator.validate_selection(choice=user_input,
                                                                    user_view="transaction_selected_delete_menu")
                if is_valid:
                    match int(user_input):
                        case 1:
                            """Back to selected transaction"""
                            return user_view, filters, editing
                        case 2:
                            """Delete selected transaction"""
                            acc.delete_transaction(editing)
                            fh.save_account(account=acc)
                            fmt.load_viewer(data=MESSAGES["successful_transaction_deleted"], kind="success")
                            editing = None
                            user_view = view.TRANSACTIONS_HISTORY_MENU
            case 3:
                """Edit transaction menu"""
                user_view = view.TRANSACTION_DETAILS_MENU
    return user_view, filters, editing


def loop_transactions_details_menu(user_view, filters, editing):
    fmt.load_viewer(data=[editing], kind="transaction_details")
    load_menu(user_view)
    user_input = input("> ").strip().lower()
    is_valid, user_input = validator.validate_selection(choice=user_input, user_view=user_view)
    if is_valid:
        match int(user_input):
            case 1:
                """Go back to selected transaction menu"""
                user_view = view.TRANSACTION_SELECTED_MENU
            case 2:
                """Edit transaction value"""
                fmt.load_viewer(data=MESSAGES["insert_amount"], kind="menu_question_main")
                user_input = input("> ").strip().lower()
                is_amount_valid, user_input = validator.is_amount_valid(account=acc, transaction=editing,
                                                                        amount=user_input, kind=editing.kind)
                if is_amount_valid:
                    acc.edit_transaction(transaction=editing, change_type="value", value=user_input)
                    fh.save_account(account=acc)
                    fmt.load_viewer(data=MESSAGES["successful_transaction_update"], kind="success")
            case 3:
                """Change transaction type"""
                editing.temp_kind = "income" if editing.kind == "income" else "expense"
                acc.edit_transaction(transaction=editing, change_type="kind",
                                     value="expense" if editing.kind == "income" else "income")
                user_view = view.TRANSACTION_DETAILS_CATEGORY_MENU
            case 4:
                """Edit transaction category"""
                user_view = view.TRANSACTION_DETAILS_CATEGORY_MENU
            case 5:
                """Edit transaction description"""
                fmt.load_viewer(data=MESSAGES["insert_description"], kind="menu_question_main")
                user_input = input("> ").strip().lower()
                is_valid, user_input = validator.validate_text(text=user_input, kind="description")
                if is_valid:
                    acc.edit_transaction(transaction=editing, change_type="description", value=user_input)
                    fh.save_account(account=acc)
                    fmt.load_viewer(data=MESSAGES["successful_transaction_update"], kind="success")
    return user_view, filters, editing


def loop_transaction_details_category_menu(user_view, filters, editing):
    fmt.load_viewer(data=[editing], kind="transaction_details")
    load_menu(user_view=user_view, transaction=editing)
    user_input = input("> ").strip().lower()
    is_valid, user_input = validator.validate_selection(choice=user_input, user_view=user_view, kind=editing.kind)
    if is_valid:
        match int(user_input):
            case 1:
                """Back to transaction details menu"""
                if hasattr(editing, "temp_kind"):
                    editing.kind = editing.temp_kind
                    delattr(editing, "temp_kind")
            case _:
                """Change to new selected category"""
                acc.edit_transaction(transaction=editing, change_type="category", value=user_input - 1)
                fh.save_account(account=acc)
                fmt.load_viewer(data=MESSAGES["successful_transaction_update"], kind="success")
    user_view = view.TRANSACTION_DETAILS_MENU
    return user_view, filters, editing


def create_budget():
    """Validates input data and creates budget"""
    budget_categories = []
    fmt.load_viewer(data=MESSAGES["add_name"], kind="menu_question")
    budget_name = input("> ").strip().lower()
    is_name_valid, budget_name = validator.validate_text(text=budget_name, kind="name")
    if is_name_valid:
        fmt.load_viewer(data=MESSAGES["add_limit"], kind="menu_question")
        budget_limit = input("> ").strip().lower()
        is_limit_valid, budget_limit = validator.is_amount_valid(account=acc, amount=budget_limit, kind="income")
        if is_limit_valid:
            fmt.load_viewer(data=MESSAGES["select_budget_category"], kind="menu_question_main")
            load_menu_helper(mode="budget")
            user_choice = input("> ").strip().lower()
            is_choice_valid, user_choice = validator.validate_selection(choice=user_choice,
                                                                        user_view=view.BUDGETS_BUDGET_CATEGORIES_MENU,
                                                                        kind="budget")
            while True:
                if user_choice in budget_categories:
                    fmt.load_viewer(data=MESSAGES["category_already_selected"], kind="warning")
                    user_choice = input("> ").strip().lower()
                    is_choice_valid, user_choice = validator.validate_selection(choice=user_choice,
                                                                                user_view=view.BUDGETS_BUDGET_CATEGORIES_MENU,
                                                                                kind="budget")
                    continue
                if is_choice_valid:
                    if user_choice not in budget_categories:
                        budget_categories.append(user_choice)
                    fmt.load_viewer(
                        data="Would you like to add another category?\n\t* Y / N *\nYou can also type 'cancel' to abort.",
                        kind="menu_question")
                    confirmation = input("> ").strip().lower()
                    if confirmation == "n" or confirmation == "cancel":
                        break
                    elif confirmation == "y":
                        fmt.load_viewer(data=MESSAGES["select_budget_category"], kind="menu_question_main")
                        load_menu_helper(mode="budget")
                        user_choice = input("> ").strip().lower()
                        is_choice_valid, user_choice = validator.validate_selection(choice=user_choice,
                                                                                    user_view=view.BUDGETS_BUDGET_CATEGORIES_MENU,
                                                                                    kind="budget")
                    else:
                        fmt.load_viewer(data="Type in either 'y' or 'n'", kind="warning")
                        user_choice = input("> ").strip().lower()
                        is_choice_valid, user_choice = validator.validate_selection(choice=user_choice,
                                                                                    user_view=view.BUDGETS_BUDGET_CATEGORIES_MENU,
                                                                                    kind="budget")
                else:
                    return
            if is_name_valid and is_limit_valid and is_choice_valid:
                budget = Budget(name=budget_name.capitalize(), limit=budget_limit, categories=budget_categories)
                acc.add_budget(budget)
                fh.save_account(account=acc)
                fmt.load_viewer(data=MESSAGES["budget_save_successful"], kind="success")
    return


def create_transaction(kind):
    new_transaction = ""
    can_create_transaction = False
    if kind == "income":
        fmt.load_viewer(data=MESSAGES["insert_amount"], kind="menu_question")
        user_input = input("> ").strip().lower()
        is_valid, amount = validator.is_amount_valid(account=acc, amount=user_input, kind="income")
        if is_valid:
            load_menu_helper(mode="income")
            fmt.load_viewer(data=MESSAGES["select_option"], kind="menu_question")
            category_choice = input("> ").strip().lower()
            is_cat_valid, category_choice = validator.validate_selection(choice=category_choice,
                                                                         user_view="add_income_menu",
                                                                         kind="income")
            if is_cat_valid:
                new_transaction = Transaction(amount=amount, category=category_choice, kind=kind)
                can_create_transaction = True
        else:
            return
    if kind == "expense":
        fmt.load_viewer(data=MESSAGES["insert_amount"], kind="menu_question")
        user_input = input("> ").strip().lower()
        is_valid, amount = validator.is_amount_valid(account=acc, amount=user_input, kind="expense")
        if is_valid:
            load_menu_helper(mode="expense")
            fmt.load_viewer(data=MESSAGES["select_option"], kind="menu_question")
            category_choice = input("> ").strip().lower()
            is_cat_valid, category_choice = validator.validate_selection(choice=category_choice,
                                                                         user_view="add_expense_menu", kind="expense")
            if is_cat_valid:
                new_transaction = Transaction(amount=amount, category=category_choice, kind=kind)
                can_create_transaction = True
        else:
            return
    if can_create_transaction:
        if kind == "income":
            acc.add_income(new_transaction)
        elif kind == "expense":
            acc.add_expense(new_transaction)
        fh.save_account(account=acc)
        fmt.load_viewer(data=MESSAGES["successful_transaction"], kind="success")
        fmt.load_viewer(data=f"Your new balance is: ${acc.check_balance():.2f}",
                        kind="balance_bad" if acc.check_balance() < 0 else "balance_good")


def select_entry(items_list: list, mode: str) -> Transaction | Budget | None:
    if mode == "transaction":
        fmt.load_viewer(data=items_list, kind="transactions_list")
        fmt.load_viewer(data=MESSAGES["select_transaction"], kind="menu_question")
    elif mode == "budget":
        fmt.display_budgets(data=items_list, transactions=acc.get_transactions())
        fmt.load_viewer(data=MESSAGES["select_budget"], kind="menu_question")
    selected_index = input("> ").strip().lower()
    available_indexes = []
    for entry in items_list:
        available_indexes.append(entry.index)
    available_indexes.sort()
    while True:
        if selected_index == "cancel":
            return None
        try:
            selected_index = int(selected_index)
            if selected_index not in available_indexes:
                raise ValueError
            break
        except ValueError:
            fmt.load_viewer(data=MESSAGES["select_option"], kind="warning")
            selected_index = input("> ").strip().lower()
    for entry in items_list:
        if selected_index == entry.index:
            return entry
    return None


if __name__ == '__main__':
    show_app_name()
    main_loop()
