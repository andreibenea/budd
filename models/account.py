from models.transaction import Transaction
from datetime import datetime


class Account:
    def __init__(self):
        self._balance = 0
        self._transactions = []

    def check_balance(self) -> int:
        return self._balance

    def get_transactions(self):
        transactions = self.order_transactions(self._transactions)
        return transactions

    def order_transactions(self, transactions):
        transactions_copy = transactions[:]
        ordered_transactions = []
        if len(transactions_copy) <= 1:
            return transactions_copy[:]
        midpoint = len(transactions_copy) // 2
        left, right = transactions_copy[:midpoint], transactions_copy[midpoint:]
        sorted_left = self.order_transactions(left)
        sorted_right = self.order_transactions(right)
        i, j = 0, 0
        while i < len(sorted_left) and j < len(sorted_right):
            if datetime.fromisoformat(sorted_left[i].timestamp) >= datetime.fromisoformat(sorted_right[j].timestamp):
                ordered_transactions.append(sorted_left[i])
                i += 1
            else:
                ordered_transactions.append(sorted_right[j])
                j += 1
        for i in range(i, len(sorted_left)):
            ordered_transactions.append(sorted_left[i])
        for j in range(j, len(sorted_right)):
            ordered_transactions.append(sorted_right[j])

        self._transactions = ordered_transactions
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
        self._balance = tentative_balance
        self._transactions.append(transaction)
