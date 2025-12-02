import uuid
from datetime import datetime


class Transaction:
    def __init__(self, amount: float, kind: str, category: str, identifier: str | None = None,
                 timestamp: str | None = None,
                 description: str | None = None):
        self.uuid = str(uuid.uuid4())
        self.timestamp = timestamp if timestamp else datetime.now().isoformat()
        self.amount = amount
        self.kind = kind
        self.category = category
        self.description = description

    def __str__(self):
        return f"[{self.timestamp}] Amt: ${self.amount:.2f} Cat: '{self.category}' Desc: '{self.description}'"

    def __repr__(self):
        return f'<Transaction: {self.uuid} : {self.amount} ; {self.kind} ; {self.description} ; {self.category}>'
