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
        self._transactions = transactions
        return self._transactions

    def get_incomes(self):
        incomes = []
        for transaction in self._transactions:
            if transaction.kind == "income":
                incomes.append(transaction)
        sorted_incomes = self.order_transactions(transactions=incomes)
        return sorted_incomes

    def get_expenses(self):
        expenses = []
        for transaction in self._transactions:
            if transaction.kind == "expense":
                expenses.append(transaction)
        sorted_expenses = self.order_transactions(transactions=expenses)
        return sorted_expenses

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
        return ordered_transactions

    def load_balance(self, balance):
        self._balance = balance

    def load_transactions(self, transactions):
        self._transactions = transactions

    def add_income(self, transaction: Transaction):
        self._balance += transaction.amount
        self._transactions.append(transaction)

    def add_expense(self, transaction: Transaction):
        tentative_balance = self._balance - transaction.amount
        self._balance = tentative_balance
        self._transactions.append(transaction)
