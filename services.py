from models import Account, Budget, Transaction
from repository import BudgetRepository, TransactionRepository


class FinanceService:
    def __init__(self, account: Account, repository: TransactionRepository) -> None:
        self.account = account
        self.repository = repository
        self.account.transactions = repository.load()

    def add_transaction(self, description: str, amount_text: str, kind: str, category: str) -> None:
        self.account.add(Transaction.create(description, amount_text, kind, category))
        self.repository.save(self.account.transactions)

    def delete_transaction(self, transaction_id: str) -> None:
        self.account.remove(transaction_id)
        self.repository.save(self.account.transactions)

    def all_transactions(self) -> list[Transaction]:
        return list(self.account.transactions)

    def totals(self) -> tuple[float, float, float]:
        return self.account.income, self.account.expenses, self.account.balance
    
class ReportService:
    def __init__(self, account: Account) -> None:
        self.account = account
        
    def transactions_for(self, category: str) -> list[Transaction]:
        if category == "All":
            return list(self.account.transactions)
        return [transaction for transaction in self.account.transactions if transaction.category == category]
    
    def expense_total_for(self, category:str) -> float:
        return sum(transaction.amount for transaction in self.transactions_for(category) if transaction.kind == "Expense")
    
class BudgetService:
    def __init__(self, account: Account, repository: BudgetRepository) -> None:
        self.account, self.repository = account, repository
        self.account.budgets = repository.load()
        
    def add(self, category:str, limit: str) -> None:
        budget = Budget.create(category, limit)
        self.account.budgets = [x for x in self.account.budgets if x.category != category]
        self.account.budgets.append(budget)
        self.repository.save(self.account.budgets)
    
    def delete(self, budget_id:str)-> str:
        self.account.budgets = [x for x in self.account.budgets if x.id != budget_id]
        self.repository.save(self.account.budgets)
    
    def progress(self, budget: Budget) -> tuple[float, float]:
        spent = sum(x.amount for x in self.account.transactions if x.kind == "Expense" and x.category == budget.category)
        return spent, min(spent/float(budget.limit)*100, 100)