# Press ⌃R to run script
import sys
from models.account import Account
from models.transaction import Transaction
from utils.utils import messages, CATEGORIES_EXPENSES, CATEGORIES_INCOME
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
    print("""  
  ___         _    _ 
 | _ )_  _ __| |__| |
 | _ \\ || / _` / _` |
 |___/\\_,_\\__,_\\__,_|
                     
""")
    print("####### THE BUDGET APP #######\n")


def loop_menu():
    while True:
        handle_command()


def show_main_menu():
    print("What do you want to do?")
    print("1. Check balance")
    print("2. Add income")
    print("3. Add expense")
    print("4. View transactions")
    print("5. Quit")
    print("Type in the number corresponding to your choice:")


def show_transactions_history_menu():
    print("What do you want to do?")
    print("1. Go back")


def show_categories_expenses_menu():
    i = 1
    for category in CATEGORIES_EXPENSES:
        fmt.load_viewer(f"{i}. {CATEGORIES_EXPENSES[category]}")
        i += 1


def show_categories_income_menu():
    i = 1
    for category in CATEGORIES_INCOME:
        fmt.load_viewer(f"{i}. {CATEGORIES_INCOME[category]}")
        i += 1


def handle_command():
    show_main_menu()
    user_input = input("> ").strip()
    while True:
        try:
            user_input = int(user_input)
            if user_input not in [1, 2, 3, 4, 5]:
                raise ValueError
            break
        except ValueError:
            print("Please enter a number corresponding to your choice")
            user_input = input("> ").strip()
    match user_input:
        case 1:
            print("Checking balance...")
            return print(f"Your current balance is: ${acc.check_balance():.2f}")
        case 2:
            print("What's the income amount?")
            print(messages["cancel"])
            amt = input("> ").strip().lower()
            while True:
                if amt == "cancel":
                    return handle_command()
                try:
                    amt = float(amt)
                    break
                except ValueError:
                    print("Please enter a valid amount!")
                    amt = input("> ").strip().lower()
            print("Select category")
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
            transaction = Transaction(amount=amt, kind="deposit", category=ctgr)
            acc.deposit(transaction)
            print("Income added successfully!")
            print(f"Your new balance is: ${acc.check_balance():.2f}")
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
                    print(f"{e.message}")
                    print(f"Your current balance is: ${acc.check_balance():.2f}")
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
                    print("Please enter a number corresponding to your choice")
                    category_choice = input("> ").strip().lower()
            transaction = Transaction(amount=amt, kind="withdraw", category=ctgr)
            acc.withdraw(transaction)
            print("Expense added successfully!")
            print(f"Your new balance is: ${acc.check_balance():.2f}")
            fh.save_account(acc)
        case 4:
            print("Loading transactions...")
            transactions = acc.get_transactions()
            if len(transactions) == 0:
                return print("There are no transactions!")
            fmt.load_viewer(transactions)
            show_transactions_history_menu()
            user_input = input("> ").strip()
            while True:
                if user_input == "cancel":
                    return handle_command()
                try:
                    user_input = int(user_input)
                    if user_input != 1:
                        raise ValueError
                    break
                except ValueError:
                    print("Type 1 or 'cancel' to return to the main menu!")
                    user_input = input("> ").strip()
            return handle_command()

        case 5:
            print("Good Bye!")
            return sys.exit()


if __name__ == '__main__':
    show_app_name()
    loop_menu()
