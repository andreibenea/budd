# Press ⌃R to run script
import sys
from models.account import Account
from models.transaction import Transaction
from utils.utils import load_menu, toggle_filter, messages, menus, ascii_art, CATEGORIES_EXPENSES, CATEGORIES_INCOME, \
    USER_VIEWS, \
    MAIN_MENU_OPTIONS, TRANSACTIONS_HISTORY_MENU, TRANSACTIONS_HISTORY_FILTER_MENU, \
    TRANSACTIONS_HISTORY_FILTER_DATETIME_MENU, TRANSACTIONS_HISTORY_FILTER_DATETIME_QUICK_MENU, TRANSACTION_EDIT_MENU, \
    TRANSACTION_DETAILS_MENU, MONTHS
from utils.file_handler import FileHandler
from utils.formatters import Formatter
from utils.exceptions import InsufficientFundsError
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


def loop_main_menu(user_view, filters, editing):
    print(f"[DEBUG] user_view: {user_view}")
    print(f"[DEBUG] filters: {filters}")
    print(f"[DEBUG] editing: {editing}")
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
                user_view = USER_VIEWS["main_menu"]
            case 2:
                """Manage filters"""
                user_view = USER_VIEWS["transactions_history_filter_menu"]
            case 3:
                """Select transaction"""
                fmt.load_viewer(data="Not YET implemented!", kind="warning")
    return user_view, filters, editing


def loop_transactions_history_filter_menu(user_view, filters, editing):
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
                fmt.load_viewer(data="Not YET implemented!", kind="warning")
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


def create_transaction(kind):
    new_transaction = ""
    can_create_transaction = False
    if kind == "income":
        fmt.load_viewer(data=messages["insert_amount"], kind="menu_question")
        user_input = input("> ").strip().lower()
        is_valid, amount = validator.is_amount_valid(account=acc, amount=user_input, kind="income")
        if is_valid:
            show_categories_income_menu()
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
            show_categories_expenses_menu()
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
        fmt.load_viewer(data=messages["successful_transaction"], kind="success")
        fmt.load_viewer(data=f"Your new balance is: ${acc.check_balance():.2f}",
                        kind="balance_bad" if acc.check_balance() < 0 else "balance_good")
        fh.save_account(account=acc)


def show_transactions_history_filter_datetime_menu():
    for msg in menus["transactions_history_filter_datetime_menu"]:
        fmt.load_viewer(data=msg[0], kind=msg[1])


def show_transactions_history_filter_datetime_quick_menu():
    for msg in menus["transactions_history_filter_datetime_quick_menu"]:
        fmt.load_viewer(data=msg[0], kind=msg[1])


def show_categories_income_menu():
    """Displays all income categories available for menu selection"""
    i = 1
    for category in CATEGORIES_INCOME:
        fmt.load_viewer(data=f"{i}. {CATEGORIES_INCOME[category]}", kind="menu_option")
        i += 1


def show_categories_expenses_menu():
    """Displays all expenses categories available for menu selection"""
    i = 1
    for category in CATEGORIES_EXPENSES:
        fmt.load_viewer(data=f"{i}. {CATEGORIES_EXPENSES[category]}", kind="menu_option")
        i += 1


def show_transaction_edit_menu():
    """Displays transaction editing options for selected transaction"""
    for msg in menus["transaction_edit_menu"]:
        fmt.load_viewer(data=msg[0], kind=msg[1])


def show_transaction_details_menu():
    """Displays transaction detail modification options"""
    for msg in menus["transaction_details_menu"]:
        fmt.load_viewer(data=msg[0], kind=msg[1])


def get_transactions_filtered(filter_set):
    match filter_set:
        case "show_incomes":
            transactions = acc.get_incomes()
        case "show_expenses":
            transactions = acc.get_expenses()
        case _:
            transactions = acc.get_transactions()
    return transactions


def load_selected_month(filter_set, month, year):
    transactions = get_transactions_filtered(filter_set=filter_set)
    monthly_transactions = []
    for transaction in transactions:
        dt = datetime.fromisoformat(transaction.timestamp)
        if dt.month == month and dt.year == year:
            monthly_transactions.append(transaction)
    if len(monthly_transactions) == 0:
        return fmt.load_viewer(data="No transactions found!", kind="warning")
    else:
        return fmt.load_viewer(data=monthly_transactions, kind="transactions_list")


def load_selected_year(filter_set, year):
    transactions = get_transactions_filtered(filter_set=filter_set)
    yearly_transactions = []
    for transaction in transactions:
        dt = datetime.fromisoformat(transaction.timestamp)
        if dt.year == year:
            yearly_transactions.append(transaction)
    if len(yearly_transactions) == 0:
        return fmt.load_viewer(data="No transactions found!", kind="warning")
    else:
        return fmt.load_viewer(data=yearly_transactions, kind="transactions_list")


def load_timeframe(set_filter):
    transactions = get_transactions_filtered(filter_set=set_filter)
    selected_transactions = []
    start_date = create_date()
    end_date = create_date(is_end_date=True)
    print(start_date)
    print(end_date)
    for transaction in transactions:
        dt_timestamp = datetime.fromisoformat(transaction.timestamp)
        if start_date <= dt_timestamp <= end_date:
            selected_transactions.append(transaction)
    if not selected_transactions:
        return fmt.load_viewer(data="No transactions found!", kind="warning")
    fmt.load_viewer(data=selected_transactions, kind="transactions_list")


def create_date(is_end_date: bool = False):
    if is_end_date:
        fmt.load_viewer(
            data="Type in year (e.g. '1970', '2025').\nor leave empty for current year\nOr type 'cancel' to abort.",
            kind="menu_question_main")
    else:
        fmt.load_viewer(data="Type in year (e.g. '1970', '2025').\nOr type 'cancel' to abort.",
                        kind="menu_question_main")
    year_input = input("> ").strip().lower()
    while True:
        if year_input == "cancel":
            return
        if not is_end_date:
            if year_input:
                break
            fmt.load_viewer(data="You need a starting year.\nType one in or type 'cancel' to abort.", kind="warning")
            year_input = input("> ").strip().lower()
        else:
            break
    fmt.load_viewer(
        data="Type in month (e.g. '1' or 'January')\nLeave empty if not needed\nOr type 'cancel' to abort.",
        kind="menu_question_main")
    month_input = input("> ").strip().lower()
    if month_input == "cancel":
        return
    fmt.load_viewer(
        data="Type in day (e.g. '1', '11', '31').\nleave empty if not needed\nOr type 'cancel' to abort.",
        kind="menu_question_main")
    day_input = input("> ").strip().lower()
    if day_input == "cancel":
        return
    while True:
        invalid_inputs = []
        if year_input:
            if not validator.is_date_valid(year=year_input):
                invalid_inputs.append(year_input)
        if month_input:
            if not validator.is_date_valid(month=month_input):
                invalid_inputs.append(month_input)
        if day_input:
            if not validator.is_date_valid(day=day_input):
                invalid_inputs.append(day_input)
        if not invalid_inputs:
            break
        if year_input in invalid_inputs:
            fmt.load_viewer(data="Type in a valid year", kind="warning")
            year_input = input("> ").strip().lower()
        if month_input in invalid_inputs:
            fmt.load_viewer(data="Type in a valid month", kind="warning")
            month_input = input("> ").strip().lower()
        if day_input in invalid_inputs:
            fmt.load_viewer(data="Type in a valid day", kind="warning")
            day_input = input("> ").strip().lower()
    print(f"[DEBUG] {year_input}, {month_input}, {day_input}")
    if year_input is None or year_input == "":
        year_input = datetime.now().year
    if month_input is None or month_input == "":
        month_input = "01" if not is_end_date else str(datetime.now().month)
    if len(month_input) == 1:
        month_input = "0" + month_input
    if month_input in MONTHS:
        month_input = MONTHS[month_input]
    if day_input is None or day_input == "":
        day_input = "01" if not is_end_date else str(datetime.now().day)
    if len(day_input) == 1:
        day_input = "0" + day_input
    date_string = f"{year_input}-{month_input}-{day_input}"
    dt = datetime.fromisoformat(date_string)
    return dt


def handle_command(user_view: str | None = None, set_filter: str | None = None, timeframe: bool = False,
                   editing: "Transaction | None" = None):
    """ #### TO BE SPLIT INTO MULTIPLE SMALLER FUNCTIONS ####
        Routes user interactions based on current application state

        Manages navigation between menus, processes user input, and coordinates
        transaction operations (create, read, update, delete) across different
        application states including main menu, transaction history, and editing flows
    """
    print(f"[DEBUG] user status: {user_view}")
    print(f"[DEBUG] set filter: {set_filter}")
    print(f"[DEBUG] editing: {editing}")
    match user_view:
        case "main_menu":
            """Handle actions for main menu"""
            # show_main_menu()
            user_input = input("> ").strip()
            while True:
                try:
                    user_input = int(user_input)
                    if user_input not in [n for n in range(1, MAIN_MENU_OPTIONS + 1)]:
                        raise ValueError
                    break
                except ValueError:
                    fmt.load_viewer(data="Please enter a number corresponding to your choice:", kind="warning")
                    user_input = input("> ").strip()
            match user_input:
                case 1:
                    print("Checking balance...")
                    fmt.load_viewer(data=f"Your current balance is: ${acc.check_balance():.2f}",
                                    kind="balance_bad" if acc.check_balance() < 0 else "balance_good")
                    return
                case 2:
                    fmt.load_viewer(data="What's the income amount?", kind="menu_question_main")
                    print(messages["cancel"])
                    amt = input("> ").strip().lower()
                    while True:
                        if amt == "cancel":
                            return handle_command()
                        try:
                            amt = float(amt)
                            if amt <= 0:
                                if amt == 0:
                                    print(f"Amount cannot be 0.")
                                else:
                                    print(f"Amount cannot be negative.")
                                raise ValueError
                            break
                        except ValueError:
                            fmt.load_viewer(data="Please enter a valid amount!", kind="warning")
                            amt = input("> ").strip().lower()
                    fmt.load_viewer(data="Select category", kind="menu_question_main")
                    show_categories_income_menu()
                    print(messages["select_option"])
                    category_choice = input("> ").strip().lower()
                    ctgr = ""
                    while True:
                        if category_choice == "cancel":
                            return handle_command()
                        try:
                            category_choice = int(category_choice)
                            if category_choice in [n for n in range(1, len(CATEGORIES_INCOME) + 1)]:
                                i = 1
                                for category in CATEGORIES_INCOME:
                                    if i == category_choice:
                                        ctgr = CATEGORIES_INCOME[category]
                                        break
                                    i += 1
                                break
                            raise ValueError
                        except ValueError:
                            print(messages["select_option"])
                            category_choice = input("> ").strip().lower()
                    transaction = Transaction(amount=amt, kind="income", category=ctgr)
                    acc.add_income(transaction)
                    fmt.load_viewer(data="Income added successfully!", kind="success")
                    fmt.load_viewer(data=f"Your new balance is: ${acc.check_balance():.2f}",
                                    kind="balance_bad" if acc.check_balance() < 0 else "balance_good")
                    fh.save_account(account=acc)
                case 3:
                    print("What's the expense amount?")
                    print(messages["cancel"])
                    amt = input("> ").strip().lower()
                    while True:
                        if amt == "cancel":
                            return handle_command()
                        try:
                            amt = float(amt)
                            if amt <= 0:
                                if amt == 0:
                                    print(f"Amount cannot be 0.")
                                else:
                                    print(f"Amount cannot be negative.")
                                raise ValueError
                            curr_balance = acc.check_balance()
                            if amt > curr_balance:
                                raise InsufficientFundsError
                            else:
                                break
                        except InsufficientFundsError as e:
                            fmt.load_viewer(data=f"{e.message}", kind="warning")
                            fmt.load_viewer(data=f"Your current balance is: ${acc.check_balance():.2f}",
                                            kind="balance_good")
                            fmt.load_viewer(
                                data=f"New balance after expense: ${acc.check_balance() - amt:.2f}",
                                kind="balance_bad")
                            print("Try a smaller amount, type 'ok' to ignore, or type 'cancel'")
                            old_amt = amt
                            amt = input("> ").strip().lower()
                            if amt == "ok":
                                amt = old_amt
                                break
                        except ValueError:
                            print("Please enter a valid amount!")
                            amt = input("> ").strip().lower()
                    print("Select category")
                    show_categories_expenses_menu()
                    print(messages["select_option"])
                    category_choice = input("> ").strip().lower()
                    ctgr = ""
                    while True:
                        if category_choice == "cancel":
                            return handle_command()
                        try:
                            category_choice = int(category_choice)
                            if category_choice in [n for n in range(1, len(CATEGORIES_EXPENSES) + 1)]:
                                i = 1
                                for category in CATEGORIES_EXPENSES:
                                    if i == category_choice:
                                        ctgr = CATEGORIES_EXPENSES[category]
                                        break
                                    i += 1
                                break
                            raise ValueError
                        except ValueError:
                            fmt.load_viewer(data="Please enter a number corresponding to your choice:",
                                            kind="warning")
                            category_choice = input("> ").strip().lower()
                    transaction = Transaction(amount=amt, kind="expense", category=ctgr)
                    acc.add_expense(transaction)
                    fmt.load_viewer(data="Expense added successfully!", kind="success")
                    fmt.load_viewer(data=f"Your new balance is: ${acc.check_balance():.2f}",
                                    kind="balance_bad" if acc.check_balance() < 0 else "balance_good")
                    fh.save_account(account=acc)
                case 4:
                    transactions = acc.get_transactions()
                    if len(transactions) == 0:
                        fmt.load_viewer(data="No transactions found!", kind="warning")
                        return handle_command(user_view=USER_VIEWS["main_menu"], set_filter=None)
                    return handle_command(user_view=USER_VIEWS["transactions_history_menu"], set_filter=set_filter)
                case 5:
                    fmt.load_viewer(data="Good Bye!", kind="menu_question_main")
                    return sys.exit()
        case "transactions_history_menu":
            print(f"[DEBUG] In Transaction History Menu")
            print("Loading transactions...")
            match set_filter:
                case "show_incomes":
                    transactions = acc.get_incomes()
                    fmt.load_viewer(data=transactions, kind="incomes_list")
                case "show_expenses":
                    transactions = acc.get_expenses()
                    fmt.load_viewer(data=transactions, kind="expenses_list")
                case _:
                    transactions = acc.get_transactions()
                    fmt.load_viewer(data=transactions, kind="transactions_list")
            if len(transactions) == 0:
                fmt.load_viewer(data=f"No transactions found!", kind="warning")
            # show_transactions_history_menu()
            user_input = input("> ").strip()
            while True:
                if user_input == "cancel":
                    return handle_command(user_view=USER_VIEWS["main_menu"], set_filter=set_filter)
                try:
                    user_input = int(user_input)
                    if user_input not in range(1, TRANSACTIONS_HISTORY_MENU + 1):
                        raise ValueError
                    break
                except ValueError:
                    fmt.load_viewer(data=messages["select_option"], kind="warning")
                    user_input = input("> ").strip()
            print(f"[DEBUG] Matching user input...")
            match user_input:
                case 1:
                    return handle_command(user_view=USER_VIEWS["main_menu"], set_filter=set_filter)
                case 2:
                    return handle_command(user_view=USER_VIEWS["transactions_history_filter_menu"],
                                          set_filter=set_filter)
                case 3:
                    return handle_command(USER_VIEWS["transactions_history_menu"], set_filter=None)
                case 4:
                    transactions = acc.get_transactions()
                    if len(transactions) == 0:
                        fmt.load_viewer(data="No transactions found!", kind="warning")
                        return handle_command(user_view=USER_VIEWS["main_menu"], set_filter=None, editing=None)
                    if set_filter:
                        transactions = acc.get_incomes() if set_filter == "show_incomes" else acc.get_expenses()
                        if len(transactions) == 0:
                            fmt.load_viewer(data="No transactions found!", kind="warning")
                            print("Removing filters...")
                            return handle_command(user_view=USER_VIEWS["transactions_history_menu"],
                                                  set_filter=None, editing=None)
                    if set_filter == "show_incomes":
                        return handle_command(user_view=USER_VIEWS["transactions_history_selection"],
                                              set_filter="show_incomes")
                    elif set_filter == "show_expenses":
                        return handle_command(user_view=USER_VIEWS["transactions_history_selection"],
                                              set_filter="show_expenses")
                    else:
                        return handle_command(user_view=USER_VIEWS["transactions_history_selection"],
                                              set_filter=None)
        case "transactions_history_filter_menu":
            transactions = get_transactions_filtered(filter_set=set_filter)
            fmt.load_viewer(data=transactions, kind="transactions_list")
            # show_transactions_history_filter_menu()
            filter_choice = input("> ").strip().lower()
            while True:
                if filter_choice == "cancel":
                    return handle_command(user_view=USER_VIEWS["transactions_history_menu"],
                                          set_filter=set_filter)
                try:
                    filter_choice = int(filter_choice)
                    if filter_choice not in range(1, TRANSACTIONS_HISTORY_FILTER_MENU + 1):
                        raise ValueError
                    break
                except ValueError:
                    fmt.load_viewer(data=messages["select_option"], kind="warning")
                    filter_choice = input("> ").strip().lower()
            match filter_choice:
                case 1:
                    """Go back"""
                    print(f"[DEBUG] Going back..")
                    return handle_command(user_view=USER_VIEWS["transactions_history_menu"],
                                          set_filter=set_filter)
                case 2:
                    """Date & Time Filters"""
                    print("Implement NEXT!")
                    return handle_command(user_view=USER_VIEWS["transactions_history_filter_datetime_menu"],
                                          set_filter=set_filter)
                case 3:
                    print(f"[DEBUG] Showing income transactions")
                    handle_command(user_view=USER_VIEWS["transactions_history_menu"],
                                   set_filter="show_incomes")
                case 4:
                    print(f"[DEBUG] Showing expense transactions")
                    return handle_command(user_view=USER_VIEWS["transactions_history_menu"],
                                          set_filter="show_expenses")
        case "transactions_history_filter_datetime_menu":
            print("[DEBUG] In Transactions History DATETIME menu")
            transactions = get_transactions_filtered(filter_set=set_filter)
            if not timeframe:
                fmt.load_viewer(data=transactions, kind="transactions_list")
            show_transactions_history_filter_datetime_menu()
            filter_choice = input("> ").strip().lower()
            while True:
                if filter_choice == "cancel":
                    return handle_command(user_view=USER_VIEWS["transactions_history_menu"], set_filter=set_filter)
                try:
                    filter_choice = int(filter_choice)
                    if filter_choice not in range(1, TRANSACTIONS_HISTORY_FILTER_DATETIME_MENU + 1):
                        raise ValueError
                    break
                except ValueError:
                    fmt.load_viewer(data=messages["select_option"], kind="warning")
                    filter_choice = input("> ").strip().lower()
            transactions = get_transactions_filtered(filter_set=set_filter)
            match filter_choice:
                case 1:
                    return handle_command(user_view=USER_VIEWS["transactions_history_filter_menu"],
                                          set_filter=set_filter)
                case 2:
                    fmt.load_viewer(data=transactions, kind="transactions_list")
                    return handle_command(user_view=USER_VIEWS["transactions_history_filter_datetime_quick_menu"],
                                          set_filter=set_filter)
                case 3:
                    """Implement date (period) selection"""
                    load_timeframe(set_filter)
                    return handle_command(
                        user_view=USER_VIEWS["transactions_history_filter_datetime_menu"],
                        set_filter=set_filter, timeframe=True)
                case 4:
                    """Implement time picker / filter"""
                    print("Feature not yet implemented")
                    return handle_command(user_view=USER_VIEWS["main_menu"], set_filter=set_filter)
        case "transactions_history_filter_datetime_quick_menu":
            today = datetime.today()
            transactions = get_transactions_filtered(filter_set=set_filter)
            show_transactions_history_filter_datetime_quick_menu()
            filter_choice = input("> ").strip().lower()
            while True:
                if filter_choice == "cancel":
                    return handle_command(user_view=USER_VIEWS["transactions_history_filter_menu"],
                                          set_filter=set_filter)
                try:
                    filter_choice = int(filter_choice)
                    if filter_choice not in range(1, TRANSACTIONS_HISTORY_FILTER_DATETIME_QUICK_MENU + 1):
                        raise ValueError
                    break
                except ValueError:
                    fmt.load_viewer(data=messages["select_option"], kind="warning")
                    filter_choice = input("> ").strip().lower()
            match filter_choice:
                case 1:
                    return handle_command(user_view=USER_VIEWS["transactions_history_filter_datetime_menu"],
                                          set_filter=set_filter)
                case 2:
                    """Today"""
                    today = str(datetime.today())
                    today_transactions = []
                    for transaction in transactions:
                        if transaction.timestamp[8:10] == today[8:10]:
                            today_transactions.append(transaction)
                    if len(today_transactions) == 0:
                        fmt.load_viewer(data="No transactions found!", kind="warning")
                    else:
                        fmt.load_viewer(data=today_transactions, kind="transactions_list")
                    return handle_command(user_view=USER_VIEWS["transactions_history_filter_datetime_quick_menu"],
                                          set_filter=set_filter)
                case 3:
                    """Last 7 Days"""
                    last_seven_days_transactions = []
                    for transaction in transactions:
                        if today - timedelta(days=7) <= datetime.fromisoformat(transaction.timestamp) <= today:
                            last_seven_days_transactions.append(transaction)
                    if len(last_seven_days_transactions) == 0:
                        fmt.load_viewer(data="No transactions found!", kind="warning")
                    else:
                        fmt.load_viewer(data=last_seven_days_transactions, kind="transactions_list")
                    return handle_command(user_view=USER_VIEWS["transactions_history_filter_datetime_quick_menu"],
                                          set_filter=set_filter)
                case 4:
                    """Last 30 Days"""
                    last_seven_days_transactions = []
                    for transaction in transactions:
                        if today - timedelta(days=30) <= datetime.fromisoformat(transaction.timestamp) <= today:
                            last_seven_days_transactions.append(transaction)
                    if len(last_seven_days_transactions) == 0:
                        fmt.load_viewer(data="No transactions found!", kind="warning")
                    else:
                        fmt.load_viewer(data=last_seven_days_transactions, kind="transactions_list")
                    return handle_command(user_view=USER_VIEWS["transactions_history_filter_datetime_quick_menu"],
                                          set_filter=set_filter)
                case 5:
                    """Choose month"""
                    fmt.load_viewer(data="Type in month (e.g. 'november' or '11'?", kind="menu_question_main")
                    print(messages["cancel"])
                    month_input = input("> ").strip().lower()
                    while True:
                        if month_input == "cancel":
                            return handle_command(
                                user_view=USER_VIEWS["transactions_history_filter_datetime_quick_menu"],
                                set_filter=set_filter)
                        if month_input not in MONTHS:
                            try:
                                month_input = int(month_input)
                                if month_input in range(1, 13):
                                    break
                                raise ValueError
                            except ValueError:
                                fmt.load_viewer(data=messages["select_month"], kind="warning")
                                month_input = input("> ").strip().lower()
                        month_input = fmt.transform_month_to_int(month_input)
                        break
                    fmt.load_viewer(data="Type in year (e.g. '1970', '2025).", kind="menu_question_main")
                    print(messages["cancel"])
                    year_input = input("> ").strip().lower()
                    while True:
                        if year_input == "cancel":
                            return handle_command(
                                user_view=USER_VIEWS["transactions_history_filter_datetime_quick_menu"],
                                set_filter=set_filter)
                        try:
                            year_input = int(year_input)
                            current_year = datetime.today().year
                            if year_input not in range(1970, current_year + 1):
                                raise ValueError
                            break
                        except ValueError:
                            fmt.load_viewer(data=messages["select_year"], kind="warning")
                            year_input = input("> ").strip().lower()
                    load_selected_month(filter_set=set_filter, month=month_input, year=year_input)
                    return handle_command(
                        user_view=USER_VIEWS["transactions_history_filter_datetime_quick_menu"],
                        set_filter=set_filter)
                case 6:
                    """Choose year"""
                    fmt.load_viewer(data="Type in year (e.g. '1970', '2025).", kind="menu_question_main")
                    print(messages["cancel"])
                    year_input = input("> ").strip().lower()
                    while True:
                        if year_input == "cancel":
                            return handle_command(
                                user_view=USER_VIEWS["transactions_history_filter_datetime_quick_menu"],
                                set_filter=set_filter)
                        try:
                            year_input = int(year_input)
                            current_year = datetime.today().year
                            if year_input not in range(1970, current_year + 1):
                                raise ValueError
                            break
                        except ValueError:
                            fmt.load_viewer(data=messages["select_year"], kind="warning")
                            year_input = input("> ").strip().lower()
                    load_selected_year(filter_set=set_filter, year=year_input)
                    return handle_command(
                        user_view=USER_VIEWS["transactions_history_filter_datetime_quick_menu"],
                        set_filter=set_filter)
        case "transactions_history_filter_datetime_timeframe_menu":
            show_transactions_history_filter_datetime_menu()
        case "transactions_history_selection":
            print(f"[DEBUG] In Transaction History EDIT Menu")
            print(f"[DEBUG] set_filter: {set_filter}")
            if editing:
                fmt.load_viewer(
                    data=[editing.timestamp, editing.amount, editing.kind, editing.category,
                          editing.description], kind="transaction_details")
            else:
                match set_filter:
                    case "show_incomes":
                        transactions = acc.get_incomes()
                        fmt.load_viewer(data=transactions, kind="incomes_list")
                        fmt.load_viewer(data="Select a transaction by typing its 'Index'", kind="menu_question_main")
                    case "show_expenses":
                        transactions = acc.get_expenses()
                        fmt.load_viewer(data=transactions, kind="expenses_list")
                    case _:
                        transactions = acc.get_transactions()
                        fmt.load_viewer(data=transactions, kind="transactions_list")
                        fmt.load_viewer(data="Select a transaction by typing its 'Index'", kind="menu_question_main")
                print(messages["cancel"])
                selected_id = input("> ").strip()
                while True:
                    if selected_id == "cancel":
                        return handle_command(user_view=USER_VIEWS["transactions_history_menu"],
                                              set_filter=set_filter)
                    try:
                        selected_id = int(selected_id)
                        if selected_id not in range(1, len(transactions) + 1):
                            raise ValueError
                        break
                    except ValueError:
                        fmt.load_viewer(data=messages["select_transaction"], kind="warning")
                        selected_id = input("> ").strip()
                idx_counter = 0
                for transaction in transactions:
                    if idx_counter == selected_id - 1:
                        editing_transaction = transaction
                        return handle_command(user_view=USER_VIEWS["transaction_edit_menu"], set_filter=set_filter,
                                              editing=editing_transaction)
                    idx_counter += 1
            return handle_command(user_view=USER_VIEWS["transaction_edit_menu"], set_filter=set_filter)
        case "transaction_edit_menu":
            print(f"[DEBUG] In Transaction EDIT Menu")
            print(f"[DEBUG] set_filter: {set_filter}")
            if editing:
                fmt.load_viewer(
                    data=[editing.timestamp, editing.amount, editing.kind, editing.category,
                          editing.description], kind="transaction_details")
            show_transaction_edit_menu()
            user_input = input("> ").strip()
            if user_input == "cancel":
                return handle_command(user_view=USER_VIEWS["transactions_history_menu"], set_filter=set_filter)
            while True:
                try:
                    user_input = int(user_input)
                    if user_input not in range(1, TRANSACTION_EDIT_MENU + 1):
                        raise ValueError
                    break
                except ValueError:
                    fmt.load_viewer(data=messages["select_option"], kind="warning")
                    user_input = input("> ").strip()
            match user_input:
                case 1:
                    return handle_command(user_view=USER_VIEWS["transactions_history_menu"], set_filter=set_filter)
                case 2:
                    acc.delete_transaction(transaction=editing)
                    editing = None
                    fh.save_account(account=acc)
                    return handle_command(user_view=USER_VIEWS["transactions_history_menu"], set_filter=set_filter,
                                          editing=editing)
                case 3:
                    return handle_command(user_view=USER_VIEWS["transaction_details_menu"], set_filter=set_filter,
                                          editing=editing)
        case "transaction_details_menu":
            print(f"[DEBUG] In Transaction DETAILS Menu")
            print(f"[DEBUG] set_filter: {set_filter}")
            if editing:
                fmt.load_viewer(
                    data=[editing.timestamp, editing.amount, editing.kind, editing.category, editing.description],
                    kind="transaction_details")
            show_transaction_details_menu()
            print(messages["cancel"])
            user_input = input("> ").strip()
            if user_input == "cancel":
                return handle_command(user_view=USER_VIEWS["transaction_edit_menu"], set_filter=set_filter,
                                      editing=editing)
            while True:
                try:
                    user_input = int(user_input)
                    if user_input not in range(1, TRANSACTION_DETAILS_MENU + 1):
                        raise ValueError
                    break
                except ValueError:
                    fmt.load_viewer(data=messages["select_option"], kind="warning")
            match user_input:
                case 1:
                    fmt.load_viewer(data="Type in the new amount", kind="menu_question_main")
                    print(messages["cancel"])
                    new_amt = input("> ").strip()
                    while True:
                        if new_amt == "cancel":
                            return handle_command(user_view=USER_VIEWS["transaction_details_menu"],
                                                  set_filter=set_filter, editing=editing)
                        try:
                            new_amt = float(new_amt)
                            if new_amt <= 0:
                                if new_amt == 0:
                                    print("Amount cannot be 0.")
                                else:
                                    print("Amount cannot be negative.")
                                raise ValueError
                            break
                        except ValueError:
                            fmt.load_viewer(data="Please enter a valid amount!", kind="warning")
                            print(messages["cancel"])
                            new_amt = input("> ").strip()
                    acc.edit_transaction(transaction=editing, change_type="value", value=new_amt)
                    fh.save_account(account=acc)
                case 2:
                    if editing.kind == "income":
                        acc.edit_transaction(transaction=editing, change_type="kind", value="expense")
                    elif editing.kind == "expense":
                        acc.edit_transaction(transaction=editing, change_type="kind", value="income")
                    if editing.kind == "income":
                        print(f"New transaction type '{editing.kind}' needs a new category!")
                        fmt.load_viewer(data="Select category", kind="menu_question_main")
                        show_categories_income_menu()
                        print(messages["select_option"])
                        user_input = input("> ").strip()
                    elif editing.kind == "expense":
                        print(f"New transaction type '{editing.kind}' needs a new category!")
                        fmt.load_viewer(data="Select category", kind="menu_question_main")
                        show_categories_expenses_menu()
                        print(messages["select_option"])
                        user_input = input("> ").strip()
                    while True:
                        if user_input == "cancel":
                            return handle_command(user_view=USER_VIEWS["transaction_details_menu"],
                                                  set_filter=set_filter, editing=editing)
                        try:
                            user_input = int(user_input)
                            if editing.kind == "income":
                                if user_input not in range(1, len(CATEGORIES_INCOME) + 1):
                                    raise ValueError
                            elif editing.kind == "expense":
                                if user_input not in range(1, len(CATEGORIES_EXPENSES) + 1):
                                    raise ValueError
                            break
                        except ValueError:
                            fmt.load_viewer(data=messages["select_option"], kind="warning")
                            user_input = input("> ").strip()
                    acc.edit_transaction(transaction=editing, change_type="category", value=user_input)
                    fh.save_account(account=acc)
                case 3:
                    if editing.kind == "income":
                        fmt.load_viewer(data="Select category", kind="menu_question_main")
                        show_categories_income_menu()
                        print(messages["select_option"])
                        user_input = input("> ").strip()
                    elif editing.kind == "expense":
                        print(f"New transaction type '{editing.kind}' needs a new category!")
                        fmt.load_viewer(data="Select category", kind="menu_question_main")
                        show_categories_expenses_menu()
                        print(messages["select_option"])
                        user_input = input("> ").strip()
                    while True:
                        if user_input == "cancel":
                            return handle_command(user_view=USER_VIEWS["transaction_details_menu"],
                                                  set_filter=set_filter, editing=editing)
                        try:
                            user_input = int(user_input)
                            if editing.kind == "income":
                                if user_input not in range(1, len(CATEGORIES_INCOME) + 1):
                                    raise ValueError
                            elif editing.kind == "expense":
                                if user_input not in range(1, len(CATEGORIES_EXPENSES) + 1):
                                    raise ValueError
                            break
                        except ValueError:
                            fmt.load_viewer(data=messages["select_option"], kind="warning")
                            user_input = input("> ").strip()
                    acc.edit_transaction(transaction=editing, change_type="category", value=user_input)
                    fh.save_account(account=acc)
                case 4:
                    fmt.load_viewer(data="Describe transaction", kind="menu_question_main")
                    print(messages["cancel"])
                    user_input = input("> ").strip()
                    if user_input == "cancel":
                        return handle_command(user_view=USER_VIEWS["transaction_details_menu"],
                                              set_filter=set_filter, editing=editing)
                    acc.edit_transaction(transaction=editing, change_type="description", value=user_input)
                    fh.save_account(account=acc)


if __name__ == '__main__':
    show_app_name()
    main_loop()
