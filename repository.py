import json
from pathlib import Path
from typing import Protocol
from models import Budget, Transaction


class TransactionRepository(Protocol):
    def load(self) -> list[Transaction]: ...
    def save(self, transactions: list[Transaction]) -> None: ...


class JsonTransactionRepository:
    def __init__(self, path: Path) -> None:
        self.path = path

    def load(self) -> list[Transaction]:
        if not self.path.exists():
            return []
        return [Transaction.from_dict(x) for x in json.loads(self.path.read_text(encoding="utf-8"))]

    def save(self, transactions: list[Transaction]) -> None:
        self.path.write_text(json.dumps([x.to_dict() for x in transactions], indent=2), encoding="utf-8")


class BudgetRepository(Protocol):
    def load(self) -> list[Budget]: ...
    def save(self, budgets: list[Budget]) -> None: ...


class JsonBudgetRepository:
    def __init__(self, path: Path) -> None:
        self.path = path

    def load(self) -> list[Budget]:
        if not self.path.exists():
            return []
        return [Budget.from_dict(x) for x in json.loads(self.path.read_text(encoding="utf-8"))]

    def save(self, budgets: list[Budget]) -> None:
        self.path.write_text(json.dumps([x.to_dict() for x in budgets], indent=2), encoding="utf-8")