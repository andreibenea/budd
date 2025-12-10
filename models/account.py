from models.budget import Budget
from models.transaction import Transaction
from utils.utils import CATEGORIES_INCOME, CATEGORIES_EXPENSES
from datetime import datetime


class Account:
    def __init__(self):
        self._transactions = []
        self._budgets = []

    def check_balance(self) -> int:
        balance = 0
        for transaction in self._transactions:
            if transaction.kind == "income":
                balance += transaction.amount
            elif transaction.kind == "expense":
                balance -= transaction.amount
        return balance

    def add_budget(self, budget: Budget):
        self._budgets.append(budget)

    def delete_budget(self, budget: Budget):
        if budget in self._budgets:
            self._budgets.remove(budget)

    def get_budgets(self) -> list:
        budgets = self.order_transactions(self._budgets)
        i = 1
        for budget in budgets:
            budget.set_index(i)
            i += 1
        self._budgets = budgets
        return self._budgets

    def load_budgets(self, budgets):
        self._budgets = budgets

    def get_transactions(self) -> list:
        transactions = self.order_transactions(self._transactions)
        i = 1
        for transaction in transactions:
            transaction.set_index(i)
            i += 1
        self._transactions = transactions
        return self._transactions

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

    @staticmethod
    def filter_transactions(transactions: list, filters: dict):
        transactions_copy = transactions[:]
        filters_copy = filters.copy()
        filtered_transactions = []
        if not filters:
            return transactions_copy
        if "kind" in filters:
            del filters_copy["kind"]
            if filters["kind"] == "income":
                transactions_copy = list(filter(lambda tr: tr.kind == "income", transactions))
            elif filters["kind"] == "expense":
                transactions_copy = list(filter(lambda tr: tr.kind == "expense", transactions))
            if len(filters) == 1:
                filtered_transactions = transactions_copy
                return filtered_transactions
        for transaction in transactions_copy:
            for flt in filters_copy:
                if flt in transaction.__dict__:
                    if flt == "category":
                        for cat in filters_copy[flt]:
                            if cat == "other" and "kind" in filters:
                                if filters["kind"] == transaction.kind:
                                    if transaction not in filtered_transactions:
                                        filtered_transactions.append(transaction)
                            elif filters_copy[flt][cat] == transaction.__dict__[flt]:
                                if transaction not in filtered_transactions:
                                    filtered_transactions.append(transaction)
                    elif flt == "timestamp":
                        for entry in filters_copy[flt]:
                            transaction_ts = datetime.fromisoformat(transaction.timestamp)
                            if "date" in entry:
                                if entry["date"][0] <= transaction_ts <= entry["date"][1]:
                                    if transaction not in filtered_transactions:
                                        filtered_transactions.append(transaction)
                            elif "time" in entry:
                                transaction_time = datetime.fromisoformat(transaction.timestamp).time()
                                if entry["time"][0] <= transaction_time <= entry["time"][1]:
                                    if transaction not in filtered_transactions:
                                        filtered_transactions.append(transaction)
                    elif transaction.__dict__[flt] == filters_copy[flt]:
                        if transaction not in filtered_transactions:
                            filtered_transactions.append(transaction)
        return filtered_transactions

    def load_transactions(self, transactions):
        self._transactions = transactions

    def add_income(self, transaction: Transaction):
        self._transactions.append(transaction)

    def add_expense(self, transaction: Transaction):
        self._transactions.append(transaction)

    def delete_transaction(self, transaction: Transaction):
        self._transactions.remove(transaction)
        return self._transactions

    @staticmethod
    def edit_transaction(transaction: Transaction, change_type: str, value: float | str):
        match change_type:
            case "value":
                transaction.amount = value
            case "kind":
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
