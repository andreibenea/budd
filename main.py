# Press ⌃R to run script
import sys
from models.account import Account
from models.transaction import Transaction
from utils.messages import messages
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
$$$$$$$\\                  $$\\ 
$$  __$$\\                 $$ |
$$ |  $$ |$$\\   $$\\  $$$$$$$ |
$$$$$$$\\ |$$ |  $$ |$$  __$$ |
$$  __$$\\ $$ |  $$ |$$ /  $$ |
$$ |  $$ |$$ |  $$ |$$ |  $$ |
$$$$$$$  |\\$$$$$$  |\\$$$$$$$ |
\\_______/  \\______/  \\_______|
""")
    print("####### THE BUDGET APP #######\n")


def loop_menu():
    while True:
        handle_command()


def show_main_menu():
    print("What do you want to do?")
    print("1. Check balance")
    print("2. Deposit amount")
    print("3. Withdraw amount")
    print("4. View transactions")
    print("5. Quit")
    print("Type in the number corresponding to your choice")


def show_transactions_menu():
    print("What do you want to do?")
    print("1. Go back")


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
            print("What's the amount to be deposited?")
            print(messages["cancel"])
            amt = input("> ").strip().lower()
            while True:
                if amt == "cancel":
                    return handle_command()
                try:
                    amt = float(amt)
                    transaction = Transaction(amt, "deposit")
                    acc.deposit(transaction)
                    print("Deposit successful!")
                    print(f"Your new balance is: ${acc.check_balance():.2f}")
                    fh.save_account(acc)
                    break
                except ValueError:
                    print("Please enter a valid amount!")
                    amt = input("> ").strip().lower()
        case 3:
            print("What's the amount to be withdrawn?")
            print(messages["cancel"])
            amt = input("> ").strip().lower()
            while True:
                if amt == "cancel":
                    return handle_command()
                try:
                    amt = float(amt)
                    transaction = Transaction(amt, "withdraw")
                    acc.withdraw(transaction)
                    print("Withdrawal successful!")
                    print(f"Your new balance is: ${acc.check_balance():.2f}")
                    fh.save_account(acc)
                    break
                except ValueError:
                    print("Please enter a valid amount!")
                    amt = input("> ").strip().lower()
                except InsufficientFundsError as e:
                    print(f"{e.message}")
                    print(f"Your current balance is: ${acc.check_balance():.2f}")
                    print("Try a smaller amount or type 'cancel'")
                    amt = input("> ").strip().lower()
        case 4:
            print("Loading transactions...")
            transactions = acc.get_transactions()
            if len(transactions) == 0:
                return print("There are no transactions!")
            transactions.reverse()
            fmt.load_viewer(transactions)
            show_transactions_menu()
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
