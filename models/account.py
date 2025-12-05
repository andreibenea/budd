from models.transaction import Transaction
from utils.utils import CATEGORIES_INCOME, CATEGORIES_EXPENSES
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

    def filter_transactions(self, filter_key: str | None):
        pass

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

    def delete_transaction(self, transaction: Transaction):
        if transaction.kind == "income":
            self._balance -= transaction.amount
        else:
            self._balance += transaction.amount
        self._transactions.remove(transaction)
        return self._transactions

    def edit_transaction(self, transaction: Transaction, change_type: str, value: float | str):
        # print(f"[DEBUG] Editing transaction: {transaction}")
        # print(f"[DEBUG] Change type: {change_type}")
        # print(f"[DEBUG] New value: {value}")
        match change_type:
            case "value":
                if transaction.kind == "income":
                    if value > transaction.amount:
                        self._balance += value - transaction.amount
                    elif value < transaction.amount:
                        self._balance -= transaction.amount - value
                    else:
                        pass
                transaction.amount = value
            case "kind":
                if transaction.kind == "income":
                    self._balance -= (2 * transaction.amount)
                    transaction.kind = value
                elif transaction.kind == "expense":
                    self._balance += (2 * transaction.amount)
                    transaction.kind = value
            case "category":
                if transaction.kind == "income":
                    i = 1
                    for category in CATEGORIES_INCOME:
                        if i == value:
                            transaction.category = CATEGORIES_INCOME[category]
                        i += 1
                elif transaction.kind == "expense":
                    i = 1
                    for category in CATEGORIES_EXPENSES:
                        if i == value:
                            transaction.category = CATEGORIES_EXPENSES[category]
                        i += 1
            case "description":
                transaction.description = value
