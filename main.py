import sys
from models.account import Account
from models.transaction import Transaction
from utils.utils import load_menu, load_menu_helper, add_timestamp_filter, toggle_filter, messages, ascii_art, \
    USER_VIEWS
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
    fmt.load_viewer(data=ascii_art["app_title"], kind="menu_question_main")
    fmt.load_viewer(data="### CLI BUDGET APP ###\n", kind="app_description")


def main_loop():
    """Maintains the main application loop and delegates command handling"""
    user_view = USER_VIEWS["main_menu"]
    filters = {}
    editing = None
    while True:
        match user_view:
            case "main_menu":
                user_view, filters, editing = loop_main_menu(user_view, filters, editing)
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
                user_view = USER_VIEWS["transactions_history_menu"]
            case 5:
                """Quit the program"""
                return sys.exit()
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
                user_view = USER_VIEWS["main_menu"]
            case 2:
                """Manage filters"""
                user_view = USER_VIEWS["transactions_history_filter_menu"]
            case 3:
                """Select transaction"""
                selected_transaction = select_transaction(filtered_transactions)
                if selected_transaction:
                    editing = selected_transaction
                    user_view = USER_VIEWS["transaction_selected_menu"]
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
                user_view = USER_VIEWS["transactions_history_menu"]
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
                        user_view = USER_VIEWS["transactions_history_filter_categories_incomes_menu"]
                    elif filters["kind"] == "expense":
                        user_view = USER_VIEWS["transactions_history_filter_categories_expenses_menu"]
                else:
                    user_view = USER_VIEWS["transactions_history_filter_categories_menu"]
            case 4:
                """Date: [Current: All years]"""
                user_view = USER_VIEWS["transactions_history_filter_datetime_menu"]
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
                user_view = USER_VIEWS["transactions_history_filter_menu"]
            case 2:
                """Load income categories"""
                user_view = USER_VIEWS["transactions_history_filter_categories_incomes_menu"]
            case 3:
                """Load expense categories"""
                user_view = USER_VIEWS["transactions_history_filter_categories_expenses_menu"]
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
                    user_view = USER_VIEWS["transactions_history_filter_menu"]
                else:
                    user_view = USER_VIEWS["transactions_history_filter_categories_menu"]
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
                    user_view = USER_VIEWS["transactions_history_filter_menu"]
                else:
                    user_view = USER_VIEWS["transactions_history_filter_categories_menu"]
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
                user_view = USER_VIEWS["transactions_history_filter_menu"]
            case 2:
                """Load quick filters menu"""
                user_view = USER_VIEWS["transactions_history_filter_datetime_quick_menu"]
            case 3:
                """Add individual dates to filters"""
                user_view = USER_VIEWS["transactions_history_filter_datetime_date_menu"]
            case 4:
                """Add individual timeframes to filters"""
                user_view = USER_VIEWS["transactions_history_filter_datetime_time_menu"]
    return user_view, filters, editing


def loop_transactions_history_filter_datetime_date_menu(user_view, filters, editing):
    start_date = None
    end_date = None
    filtered_transactions = acc.filter_transactions(acc.get_transactions(), filters)
    fmt.load_viewer(data=filtered_transactions, kind="transactions_list")
    fmt.load_viewer(data=messages["add_date"], kind="menu_question_main")
    user_input = input("> ").strip().lower()
    is_start_date_valid, user_input = validator.is_date_valid(date=user_input)
    if is_start_date_valid:
        start_date = datetime.fromisoformat(user_input)
        fmt.load_viewer(data=messages["add_date_end"], kind="menu_question_main")
        user_input = input("> ").strip().lower()
        is_end_date_valid, user_input = validator.is_date_valid(date=user_input)
        if is_end_date_valid:
            end_date = datetime.fromisoformat(user_input)
        else:
            end_date = start_date + timedelta(hours=24)
    if start_date and end_date:
        filters = add_timestamp_filter(filters, start_date, end_date, "date")
    user_view = USER_VIEWS["transactions_history_filter_datetime_menu"]
    return user_view, filters, editing


def loop_transactions_history_filter_datetime_time_menu(user_view, filters, editing):
    start_time = None
    end_time = None
    filtered_transactions = acc.filter_transactions(acc.get_transactions(), filters)
    fmt.load_viewer(data=filtered_transactions, kind="transactions_list")
    fmt.load_viewer(data=messages["add_time"], kind="menu_question_main")
    user_input = input("> ").strip().lower()
    is_time_valid, user_input = validator.is_time_valid(time_input=user_input)
    if is_time_valid:
        start_time = datetime.fromisoformat(f"1900-01-01T{user_input}")
        fmt.load_viewer(data=messages["add_time_end"], kind="menu_question_main")
        user_input = input("> ").strip().lower()
        is_end_time_valid, user_input = validator.is_time_valid(time_input=user_input)
        if is_end_time_valid:
            end_time = datetime.fromisoformat(f"1900-01-01T{user_input}")
        else:
            end_time = start_time + timedelta(minutes=1)
    if start_time and end_time:
        filters = add_timestamp_filter(filters, start_time, end_time, "time")
    user_view = USER_VIEWS["transactions_history_filter_datetime_menu"]
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
                user_view = USER_VIEWS["transactions_history_filter_datetime_menu"]
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
                user_view = USER_VIEWS["transactions_history_menu"]
            case 2:
                """Delete transaction"""
                fmt.load_viewer(data=f"This will permanently delete {editing}\nAre you sure?", kind="warning")
                load_menu(USER_VIEWS["transaction_selected_delete_menu"])
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
                            fmt.load_viewer(data=messages["successful_transaction_deleted"], kind="success")
                            editing = None
                            user_view = USER_VIEWS["transactions_history_menu"]
            case 3:
                """Edit transaction menu"""
                user_view = USER_VIEWS["transaction_details_menu"]
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
                user_view = USER_VIEWS["transaction_selected_menu"]
            case 2:
                """Edit transaction value"""
                fmt.load_viewer(data=messages["insert_amount"], kind="menu_question_main")
                user_input = input("> ").strip().lower()
                is_amount_valid, user_input = validator.is_amount_valid(account=acc, transaction=editing,
                                                                        amount=user_input, kind=editing.kind)
                if is_amount_valid:
                    acc.edit_transaction(transaction=editing, change_type="value", value=user_input)
                    fh.save_account(account=acc)
                    fmt.load_viewer(data=messages["successful_transaction_update"], kind="success")
            case 3:
                """Change transaction type"""
                editing.temp_kind = "income" if editing.kind == "income" else "expense"
                acc.edit_transaction(transaction=editing, change_type="kind",
                                     value="expense" if editing.kind == "income" else "income")
                user_view = USER_VIEWS["transaction_details_category_menu"]
            case 4:
                """Edit transaction category"""
                user_view = USER_VIEWS["transaction_details_category_menu"]
            case 5:
                """Edit transaction description"""
                fmt.load_viewer(data=messages["insert_description"], kind="menu_question_main")
                user_input = input("> ").strip().lower()
                is_valid, user_input = validator.is_description_valid(description=user_input)
                if is_valid:
                    acc.edit_transaction(transaction=editing, change_type="description", value=user_input)
                    fh.save_account(account=acc)
                    fmt.load_viewer(data=messages["successful_transaction_update"], kind="success")
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
                try:
                    if editing.temp_kind:
                        editing.kind = editing.temp_kind
                        del editing.temp_kind
                except AttributeError:
                    pass
            case _:
                """Change to new selected category"""
                acc.edit_transaction(transaction=editing, change_type="category", value=user_input - 1)
                fh.save_account(account=acc)
                fmt.load_viewer(data=messages["successful_transaction_update"], kind="success")
    user_view = USER_VIEWS["transaction_details_menu"]
    return user_view, filters, editing


def create_transaction(kind):
    new_transaction = ""
    can_create_transaction = False
    if kind == "income":
        fmt.load_viewer(data=messages["insert_amount"], kind="menu_question")
        user_input = input("> ").strip().lower()
        is_valid, amount = validator.is_amount_valid(account=acc, amount=user_input, kind="income")
        if is_valid:
            load_menu_helper(mode="income")
            fmt.load_viewer(data=messages["select_option"], kind="menu_question")
            category_choice = input("> ").strip().lower()
            is_cat_valid, category_choice = validator.validate_selection(choice=category_choice, user_view="add_income",
                                                                         kind="income")
            if is_cat_valid:
                new_transaction = Transaction(amount=amount, category=category_choice, kind=kind)
                can_create_transaction = True
        else:
            return
    if kind == "expense":
        fmt.load_viewer(data=messages["insert_amount"], kind="menu_question")
        user_input = input("> ").strip().lower()
        is_valid, amount = validator.is_amount_valid(account=acc, amount=user_input, kind="expense")
        if is_valid:
            load_menu_helper(mode="expense")
            fmt.load_viewer(data=messages["select_option"], kind="menu_question")
            category_choice = input("> ").strip().lower()
            is_cat_valid, category_choice = validator.validate_selection(choice=category_choice,
                                                                         user_view="add_expense", kind="expense")
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
        fmt.load_viewer(data=messages["successful_transaction"], kind="success")
        fmt.load_viewer(data=f"Your new balance is: ${acc.check_balance():.2f}",
                        kind="balance_bad" if acc.check_balance() < 0 else "balance_good")


def select_transaction(transactions):
    fmt.load_viewer(data=transactions, kind="transactions_list")
    fmt.load_viewer(data=messages["select_transaction"], kind="menu_question")
    selected_index = input("> ").strip().lower()
    available_indexes = []
    for transaction in transactions:
        available_indexes.append(transaction.index)
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
            fmt.load_viewer(data=messages["select_option"], kind="warning")
            selected_index = input("> ").strip().lower()
    for transaction in transactions:
        if selected_index == transaction.index:
            return transaction
    return None


if __name__ == '__main__':
    show_app_name()
    main_loop()
