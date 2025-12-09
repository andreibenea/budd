from datetime import datetime


class Budget:
    def __init__(self, index: int | None
                 , name: str, timestamp: str | None, category: str, limit: float | int):
        self.index = index if index else None
        self.name = name
        self.timestamp = timestamp if timestamp else datetime.now().isoformat()
        self.category = category
        self.limit = limit
