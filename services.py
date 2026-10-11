from models import Account, Transaction


class FinanceService:

    def __init__(self, account: Account) -> None:
        self.account = account

    def add_transaction(self, description: str, amount: float, kind: str) -> None:
        self.account.add(Transaction(description, amount, kind))

    def all_transactions(self) -> list[Transaction]:
        return list(self.account.transactions)

    def totals(self) -> tuple[float, float, float]:
        return self.account.income, self.account.expenses, self.account.balance