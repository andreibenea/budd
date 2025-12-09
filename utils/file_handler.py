import os
import json
from models.account import Account
from models.transaction import Transaction


class FileHandler:
    def __init__(self):
        self.working_directory = os.getcwd()

    def load_account(self):
        account_file = os.path.join(self.working_directory, 'data', 'account.json')
        with open(account_file, 'r') as f:
            data = json.load(f)
            transactions = []
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
            acc = Account()
            acc.load_balance(data['balance'])
            acc.load_transactions(transactions)
        return acc

    def save_account(self, account: Account):
        self._ensure_data_directory()
        account_file = os.path.join(self.working_directory, 'data', 'account.json')
        acc_as_dict = self._account_to_json(account=account)
        with open(account_file, 'w') as f:
            f.write(json.dumps(acc_as_dict))

    def _ensure_data_directory(self):
        try:
            data_path = os.path.join(os.getcwd(), self.working_directory, 'data')
            if not os.path.exists(data_path):
                os.makedirs(data_path)
                print('Data directory created')
                return True
        except Exception as e:
            print(e)
            return False

    @staticmethod
    def _account_to_json(account: "Account"):
        transactions = [t.__dict__ for t in account.get_transactions()]
        acc_as_dict = {
            "balance": account.check_balance(),
            "transactions": transactions
        }
        return acc_as_dict
