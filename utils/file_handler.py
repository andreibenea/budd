import os
import json
from models.account import Account
from models.budget import Budget
from models.transaction import Transaction


class FileHandler:
    def __init__(self):
        self.working_directory = os.getcwd()

    def load_account(self):
        account_file = os.path.join(self.working_directory, 'data', 'account.json')
        with open(account_file, 'r') as f:
            data = json.load(f)
            transactions = []
            budgets = []
            for trans_data in data['transactions']:
                amount = trans_data['amount']
                kind = trans_data['kind']
                category = trans_data['category']
                identifier = trans_data['identifier']
                index = trans_data['index']
                timestamp = trans_data['timestamp']
                description = trans_data['description']
                transaction = Transaction(amount=amount, kind=kind, category=category, identifier=identifier,
                                          timestamp=timestamp, index=index,
                                          description=description)
                transactions.append(transaction)
            for budget_data in data['budgets']:
                index = budget_data['index']
                timestamp = budget_data['timestamp']
                name = budget_data['name']
                categories = []
                for category in budget_data['categories']:
                    categories.append(category)
                limit = budget_data['limit']
                budget = Budget(index=index, name=name, timestamp=timestamp, categories=categories, limit=limit)
                budgets.append(budget)
            acc = Account()
            acc.load_transactions(transactions)
            acc.load_budgets(budgets)
        return acc

    def save_account(self, account: Account):
        self._ensure_data_directory()
        account_file = os.path.join(self.working_directory, 'data', 'account.json')
        acc_as_dict = self._data_to_json(data=account)
        with open(account_file, 'w') as f:
            f.write(json.dumps(acc_as_dict))

    def _ensure_data_directory(self):
        try:
            data_path = os.path.join(self.working_directory, 'data')
            if not os.path.exists(data_path):
                os.makedirs(data_path)
                print('Data directory created')
                return True
        except Exception as e:
            print(e)
            return False

    @staticmethod
    def _data_to_json(data: "Account") -> dict:
        transactions = [t.__dict__ for t in data.get_transactions()]
        budgets = [b.__dict__ for b in data.get_budgets()]
        acc_as_dict = {
            "transactions": transactions,
            "budgets": budgets
        }
        return acc_as_dict
