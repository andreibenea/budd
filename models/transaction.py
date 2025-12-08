import uuid
from datetime import datetime


class Transaction:
    def __init__(self, amount: float, kind: str, category: str, identifier: str | None = None,
                 index: str | None = None,
                 timestamp: str | None = None,
                 description: str | None = None):
        self.identifier = str(uuid.uuid4()) if identifier is None else identifier
        self.index = index if index else None
        self.timestamp = timestamp if timestamp else datetime.now().isoformat()
        self.amount = amount
        self.kind = kind
        self.category = category
        self.description = description

    def __str__(self):
        return f"[{self.timestamp}] Amt: ${self.amount:.2f} Cat: '{self.category}' Desc: '{self.description}'"

    def __repr__(self):
        return f'<Transaction: {self.identifier} : {self.amount} ; {self.kind} ; {self.description} ; {self.category}>'

    def set_index(self, index: int):
        self.index = index
