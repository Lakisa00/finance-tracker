import tkinter as tk
from tkinter import messagebox, ttk

from models import Account, ValidationError
from services import FinanceService


class FinanceTrackerApp:
    def __init__(self, service: FinanceService) -> None:
        self.service = service
        self.root = tk.Tk()
        self.root.title("Finance Tracker")
        self.root.geometry("760x560")
        self.build_ui()
        self.refresh_view()

    def build_ui(self) -> None:
        frame = ttk.Frame(self.root, padding=20)
        frame.pack(fill="both", expand=True)
        ttk.Label(frame, text="My account", font=("TkDefaultFont", 18, "bold")).pack(anchor="w")
        summary = ttk.Frame(frame)
        summary.pack(fill="x", pady=14)
        self.income_label = self.make_summary(summary, "Income", 0)
        self.expense_label = self.make_summary(summary, "Expenses", 1)
        self.balance_label = self.make_summary(summary, "Balance", 2)

        form = ttk.LabelFrame(frame, text="New transaction", padding=12)
        form.pack(fill="x", pady=(0, 12))
        ttk.Label(form, text="Description").grid(row=0, column=0, sticky="w", padx=5)
        ttk.Label(form, text="Amount ($)").grid(row=0, column=1, sticky="w", padx=5)
        ttk.Label(form, text="Type").grid(row=0, column=2, sticky="w", padx=5)
        self.description_entry = ttk.Entry(form, width=28)
        self.amount_entry = ttk.Entry(form, width=14)
        self.kind_box = ttk.Combobox(form, values=("Income", "Expense"), state="readonly", width=12)
        self.kind_box.set("Expense")
        self.description_entry.grid(row=1, column=0, padx=5)
        self.amount_entry.grid(row=1, column=1, padx=5)
        self.kind_box.grid(row=1, column=2, padx=5)
        ttk.Button(form, text="Add", command=self.add_transaction).grid(row=1, column=3, padx=5)

        self.table = ttk.Treeview(frame, columns=("description", "type", "amount"), show="headings", height=13)
        for name, title in (("description", "Description"), ("type", "Type"), ("amount", "Amount")):
            self.table.heading(name, text=title)
        self.table.column("description", width=360)
        self.table.column("type", width=120)
        self.table.column("amount", width=140, anchor="e")
        self.table.pack(fill="both", expand=True)
        ttk.Button(frame, text="Delete selected", command=self.delete_selected).pack(anchor="e", pady=(10, 0))

    @staticmethod
    def make_summary(parent: ttk.Frame, title: str, column: int) -> ttk.Label:
        card = ttk.LabelFrame(parent, text=title, padding=12)
        card.grid(row=0, column=column, padx=5, sticky="ew")
        parent.columnconfigure(column, weight=1)
        value = ttk.Label(card, text="$0.00", font=("TkDefaultFont", 15, "bold"))
        value.pack()
        return value

    def add_transaction(self) -> None:
        try:
            self.service.add_transaction(self.description_entry.get(),self.amount_entry.get(), self.kind_box.get())
        except ValidationError as error:
            messagebox.showerror("Cannot add transaction", str(error))
            return
        self.description_entry.delete(0, tk.END)
        self.amount_entry.delete(0, tk.END)
        self.refresh_view()

    def delete_selected(self) ->None:
        selected = self.table.selection()
        if not selected:
            messagebox.showinfo("Selected transaction", "Choose a row to delete")
            return
        self.service.delete_transaction(selected[0])
        self.refresh_view()

    def refresh_view(self) -> None:
        income, expenses, balance = self.service.totals()
        self.income_label.config(text=f"${income:,.2f}")
        self.expense_label.config(text=f"${expenses:,.2f}")
        self.balance_label.config(text=f"${balance:,.2f}")
        for row in self.table.get_children():
            self.table.delete(row)
        for item in self.service.all_transactions():
            self.table.insert("", "end", iid=item.id, values=(item.description, item.kind, f"${item.amount:,.2f}"))

    def run(self) -> None:
        self.root.mainloop()


if __name__ == "__main__":
    FinanceTrackerApp(FinanceService(Account("Everyday account"))).run()