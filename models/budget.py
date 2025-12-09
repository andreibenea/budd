from datetime import datetime


class Budget:
    def __init__(self, name: str, limit: float | int, categories: list, index: int | None = None,
                 timestamp: str | None = None):
        self.index = index if index else None
        self.timestamp = timestamp if timestamp else datetime.now().isoformat()[:10]
        self.name = name
        self.categories = categories if categories else []
        self.limit = limit

    def __repr__(self):
        return f"\nIndex: {self.index}\nTS: {self.timestamp}\nName: {self.name}\nCategories:\n{self.categories}\nLimit: ${self.limit:.2f}\n"

    def set_index(self, index: int):
        self.index = index
