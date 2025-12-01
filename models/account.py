from models.transaction import Transaction
from utils.exceptions import InsufficientFundsError


class Account:
    def __init__(self):
        self._balance = 0
        self._transactions = []

    def check_balance(self):
        return self._balance

    def get_transactions(self):
        return self._transactions

    def load_balance(self, balance):
        self._balance = balance

    def load_transactions(self, transactions):
        self._transactions = transactions

    def deposit(self, transaction: Transaction):
        self._balance += transaction.amount
        self._transactions.append(transaction)

    def withdraw(self, transaction: Transaction):
        tentative_balance = self._balance - transaction.amount
        if tentative_balance < -0.0001:
            raise InsufficientFundsError()
        self._balance = tentative_balance
        self._transactions.append(transaction)
