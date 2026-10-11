from dataclasses import dataclass, field

@dataclass
class Transaction:
    description:str
    amount:float
    kind:str
    
    def display_text(self) -> str:
        sign = "+" if self.kind == "Income" else "-"
        return f"{self.description:<24} sign${self.amount:,.2f}"

@dataclass
class Account:
    name:str
    transactions:list[Transaction] = field(default_factory = list)
    
    def add(self, transaction: Transaction) -> None:
        self.transactions.append(transaction)
        
    @property
    def income(self) -> float:
        return sum(item.amount for item in self.transactions if item.kind == "Income")
    
    @property
    def expense(self) -> float:
        return sum(item.amount for item in self.transactions if item.kind == "Expense")
    
    @property
    def balance(self) ->float:
        return self.income - self.expense
    
    