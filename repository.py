import json
from pathlib import Path
from typing import Protocol
from models import Transaction

class TransactionRepository(Protocol):
    def load(self) -> list[Transaction]: ...
    
    def save(self, transactions: list[Transaction]) -> None: ...
    
class JsonTransactionRepository:
    def __init__(self, path:Path) -> None:
        self.path = Path
    
    def load(self) -> list[Transaction]:
        if not self.path.exists():
            return []
        data = json.loads(self.path.read_text(encoding="utf-8"))
        return [Transaction.from_dict(item) for item in data]
    
    def save(self, transactions: list[Transaction]) -> None:
        data = [item.to_dict() for item in transactions]
        self.path.write_text(json.dumps(data, indent= 2), encoding="utf-8")