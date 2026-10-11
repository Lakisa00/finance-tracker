import unittest
from models import Account, Transaction

class AccountTests(unittest.TestCase):
    def test_totals_income_expenses_and_balance(self) -> None:
        account = Account(name="test")
        account.add(Transaction(description="salary", kind="Income", amount=2000))
        account.add(Transaction(description="rent", kind="Expense", amount=500))
        self.assertEqual(account.income, 2000)
        self.assertEqual(account.expenses, 500)
        self.assertEqual(account.balance, 1500)
    
    def test_expenses_can_make_balance_negative(self) -> None:
        account = Account("test", [Transaction("Phone", 900, "Expense")])
        self.assertEqual(account.balance, -900)

if __name__ == "__main__":
    unittest.main()