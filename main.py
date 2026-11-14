from pathlib import Path
from app import FinanceTrackerApp
from models import Account
from repository import JsonBudgetRepository, JsonTransactionRepository
from services import BudgetService, FinanceService, ReportService


if __name__ == "__main__":
    account = Account("Everyday account")
    finance = FinanceService(account, JsonTransactionRepository(Path(__file__).with_name("finance_data.json")))
    budgets = BudgetService(account, JsonBudgetRepository(Path(__file__).with_name("budgets.json")))
    FinanceTrackerApp(finance, ReportService(account), budgets).run()