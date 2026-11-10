from pathlib import Path

from app import FinanceTrackerApp
from models import Account
from repository import JsonTransactionRepository
from services import FinanceService, ReportService


if __name__ == "__main__":
    account = Account("Everyday account")
    data_file = Path(__file__).with_name("finance_data.json")
    repository = JsonTransactionRepository(data_file)
    finance = FinanceService(account, repository)
    FinanceTrackerApp(finance, ReportService(account)).run()