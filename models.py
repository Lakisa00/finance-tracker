from dataclasses import dataclass, field
from uuid import uuid4

class ValidationError(ValueError):
    pass

@dataclass
class Transaction:
    description: str
    amount: float
    kind: str
    id: str = field(default_factory=lambda:str(uuid4()))

    def display_text(self) -> str:
        sign = "+" if self.kind == "Income" else "-"
        return f"{self.description:<24} {sign}${self.amount:,.2f}"
    
    @classmethod
    def create(cls, description: str, amount_text:str, kind:str) -> "Transaction":
        description = description.strip()
        if not description:
            raise ValidationError("Description cannot be empty")
        try:
            amount = float(amount_text)
        except ValueError as error:
            raise ValidationError("Amount must be a number") from error
        if amount<=0:
            raise ValidationError("Amount must be greater than zero")
        if kind not in ("Income", "Expense"):
            raise ValidationError("Type must be income or expense")
        return cls(description, amount, kind)

@dataclass
class Account:
    name: str
    transactions: list[Transaction] = field(default_factory=list)

    def add(self, transaction: Transaction) -> None:
        self.transactions.append(transaction)
        
    def remove(self, transaction_id:str) -> None:
        self.transactions = [item for item in self.transactions if item.id == transaction_id]

    @property
    def income(self) -> float:
        return sum(item.amount for item in self.transactions if item.kind == "Income")

    @property
    def expenses(self) -> float:
        return sum(item.amount for item in self.transactions if item.kind == "Expense")

    @property
    def balance(self) -> float:
        return self.income - self.expenses