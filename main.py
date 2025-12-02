# Press ⌃R to run script
import sys
from models.account import Account
from models.transaction import Transaction
from utils.utils import messages, menus, ascii_art, CATEGORIES_EXPENSES, CATEGORIES_INCOME, USER_STATUSES
from utils.file_handler import FileHandler
from utils.formatters import Formatter
from utils.exceptions import InsufficientFundsError

fmt = Formatter()
fh = FileHandler()
try:
    acc = fh.load_account()
except FileNotFoundError:
    acc = Account()


def show_app_name():
    fmt.load_viewer(data=ascii_art["app_title"], kind="menu_question_main")
    fmt.load_viewer(data="### CLI BUDGET APP ###\n", kind="app_description")


def loop_menu():
    user_status = USER_STATUSES["main_menu"]
    while True:
        handle_command(user_status)


def show_main_menu():
    """Displays the main menu options for primary app navigation"""
    for msg in menus["main_menu"]:
        fmt.load_viewer(data=msg[0], kind=msg[1])


def show_transactions_history_menu():
    """Displays the transaction history submenu options"""
    for msg in menus["transaction_history_menu"]:
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


def handle_command(user_status: str | None = None):
    print(f"[DEBUG] {user_status}")
    match user_status:
        case "main_menu":
            """Handle actions for main menu"""
            show_main_menu()
            user_input = input("> ").strip()
            while True:
                try:
                    user_input = int(user_input)
                    if user_input not in [1, 2, 3, 4, 5]:
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
                    fh.save_account(acc)
                case 3:
                    print("What's the expense amount?")
                    print(messages["cancel"])
                    amt = input("> ").strip().lower()
                    while True:
                        if amt == "cancel":
                            return handle_command()
                        try:
                            amt = float(amt)
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
                    fh.save_account(acc)
                case 4:
                    print("Loading transactions...")
                    transactions = acc.get_transactions()
                    if len(transactions) == 0:
                        return fmt.load_viewer(data=f"There are no transactions!", kind="warning")
                    fmt.load_viewer(data=transactions, kind="transactions_list")
                    return handle_command(USER_STATUSES["transaction_history_menu"])
                case 5:
                    fmt.load_viewer(data="Good Bye!", kind="menu_question_main")
                    return sys.exit()
        case "transaction_history_menu":
            print(f"[DEBUG] In Transaction History Menu")
            show_transactions_history_menu()
            user_input = input("> ").strip()
            while True:
                if user_input == "cancel":
                    return handle_command()
                try:
                    user_input = int(user_input)
                    if user_input not in range(1, 5):
                        raise ValueError
                    break
                except ValueError:
                    fmt.load_viewer(data=messages["select_option"], kind="warning")
                    user_input = input("> ").strip()
            print(f"[DEBUG] Matching user input...")
            match user_input:
                case 1:
                    return handle_command(USER_STATUSES["main_menu"])
                case 2:
                    transactions = acc.get_incomes()
                    if len(transactions) == 0:
                        fmt.load_viewer(data=f"There are no transactions!", kind="warning")
                    fmt.load_viewer(data=transactions, kind="incomes_list")
                    return handle_command(USER_STATUSES["transaction_history_menu"])
                case 3:
                    transactions = acc.get_expenses()
                    if len(transactions) == 0:
                        fmt.load_viewer(data=f"There are no transactions!", kind="warning")
                    fmt.load_viewer(data=transactions, kind="expenses_list")
                    return handle_command(USER_STATUSES["transaction_history_menu"])
                case 4:
                    transactions = acc.get_transactions()
                    fmt.load_viewer(data=transactions, kind="transactions_list")
                    return handle_command(USER_STATUSES["transaction_history_menu"])


if __name__ == '__main__':
    show_app_name()
    loop_menu()
