from models import Account, Transaction
from repository import TransactionRepository


class FinanceService:
    def __init__(self, account: Account, repository: TransactionRepository) -> None:
        self.account = account
        self.repository = repository
        self.account.transactions = repository.load()

    def add_transaction(self, description: str, amount_text: str, kind: str) -> None:
        self.account.add(Transaction.create(description, amount_text, kind))
        self.repository.save(self.account.transactions)

    def delete_transaction(self, transaction_id: str) -> None:
        self.account.remove(transaction_id)
        self.repository.save(self.account.transactions)

    def all_transactions(self) -> list[Transaction]:
        return list(self.account.transactions)

    def totals(self) -> tuple[float, float, float]:
        return self.account.income, self.account.expenses, self.account.balance