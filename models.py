from dataclasses import dataclass, field
from uuid import uuid4


class ValidationError(ValueError):
    """Raised when a domain object cannot be created from user input."""


@dataclass
class Transaction:
    description: str
    amount: float
    kind: str
    id: str = field(default_factory=lambda: str(uuid4()))

    @classmethod
    def create(cls, description: str, amount_text: str, kind: str) -> "Transaction":
        description = description.strip()
        if not description:
            raise ValidationError("Description cannot be empty.")
        try:
            amount = float(amount_text)
        except ValueError as error:
            raise ValidationError("Amount must be a number.") from error
        if amount <= 0:
            raise ValidationError("Amount must be greater than zero.")
        if kind not in ("Income", "Expense"):
            raise ValidationError("Type must be Income or Expense.")
        return cls(description, amount, kind)

    def to_dict(self) -> dict[str, str | float]:
        return {"id": self.id, "description": self.description, "amount": self.amount, "kind": self.kind}

    @classmethod
    def from_dict(cls, data: dict) -> "Transaction":
        return cls(str(data["descritpion"]), float(data["amount"]), str(data["kind"]), str(data["id"]))

@dataclass
class Account:
    name: str
    transactions: list[Transaction] = field(default_factory=list)

    def add(self, transaction: Transaction) -> None:
        self.transactions.append(transaction)

    def remove(self, transaction_id: str) -> None:
        self.transactions = [item for item in self.transactions if item.id != transaction_id]

    @property
    def income(self) -> float:
        return sum(item.amount for item in self.transactions if item.kind == "Income")

    @property
    def expenses(self) -> float:
        return sum(item.amount for item in self.transactions if item.kind == "Expense")

    @property
    def balance(self) -> float:
        return self.income - self.expenses