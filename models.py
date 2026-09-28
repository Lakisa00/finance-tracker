from dataclasses import dataclass

@dataclass
class Transaction:
    description:str
    amount:float
    kind:str
    
    def display_text(self) -> str:
        sign = "+" if self.kind == "Income" else "-"
        return f"{self.description:<24} {sign}${self.amount:,.2f}"