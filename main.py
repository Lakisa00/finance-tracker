from pathlib import Path

from app import FinanceTrackerApp
from models import Account
from repository import JsonTransactionRepository
from services import FinanceService


if __name__ == "__main__":
    data_file = Path(__file__).with_name("finance_data.json")
    repository = JsonTransactionRepository(data_file)
    service = FinanceService(Account("Everyday account"), repository)
    FinanceTrackerApp(service).run()