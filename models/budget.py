from datetime import datetime


class Budget:
    def __init__(self, index: int | None, timestamp: str, name: str, categories: list, limit: float | int):
        self.index = index if index else None
        self.timestamp = timestamp if timestamp else datetime.now().isoformat()
        self.name = name
        self.categories = categories if categories else []
        self.limit = limit

    def set_index(self, index: int):
        self.index = index
