import unittest
from models import Account, Transaction, ValidationError

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

    def test_create_valid_transaction(self) -> None:
        item = Transaction.create("30th Anniversary Box", "70", "Expense")
        self.assertEqual(item.amount, 70)

    def test_reject_invalid_values(self) -> None:
        for description, amount, kind in (("", "2", "Expense"), ("A", "no", "Expense"), ("A", "-1", "Expense"), ("A", "1", "Other")):
            with self.subTest(description=description, amount=amount, kind=kind):
                with self.assertRaises(ValidationError):
                    Transaction.create(description, amount, kind)
        
    def test_account_removes_by_id(self) -> None:
        item = Transaction.create("Phone", "200", "Expense")
        account = Account("Test", [item])
        account.remove(item.id)
        self.assertEqual(account.transactions, [])
        
if __name__ == "__main__":
    unittest.main()