import tkinter as tk
from tkinter import messagebox, ttk
from models import CATEGORIES, ValidationError
from services import BudgetService, FinanceService, ReportService


class FinanceTrackerApp:
    def __init__(self, finance: FinanceService, reports: ReportService, budgets: BudgetService) -> None:
        self.finance, self.budgets = finance, budgets
        self.reports = reports
        self.root = tk.Tk(); self.root.title("Finance Tracker — Step 7"); self.root.geometry("850x610")
        notebook = ttk.Notebook(self.root); notebook.pack(fill="both", expand=True, padx=15, pady=15)
        self.transactions_tab, self.budgets_tab = ttk.Frame(notebook, padding=15), ttk.Frame(notebook, padding=15)
        notebook.add(self.transactions_tab, text="Transactions"); notebook.add(self.budgets_tab, text="Budgets")
        self.build_transactions(); self.build_budgets(); self.refresh()

    def build_transactions(self) -> None:
        summary = ttk.Frame(self.transactions_tab); summary.pack(fill="x")
        self.summary = []
        for col, title in enumerate(("Income", "Expenses", "Balance")):
            box = ttk.LabelFrame(summary, text=title, padding=8); box.grid(row=0, column=col, sticky="ew", padx=4); summary.columnconfigure(col, weight=1)
            label = ttk.Label(box, font=("TkDefaultFont", 14, "bold")); label.pack(); self.summary.append(label)
        form = ttk.LabelFrame(self.transactions_tab, text="New transaction", padding=10); form.pack(fill="x", pady=12)
        for col, text in enumerate(("Description", "Amount ($)", "Type", "Category")):
            ttk.Label(form, text=text).grid(row=0, column=col, sticky="w", padx=4)
        self.description, self.amount = ttk.Entry(form, width=24), ttk.Entry(form, width=12)
        self.kind = ttk.Combobox(form, values=("Income", "Expense"), state="readonly", width=10); self.kind.set("Expense")
        self.category = ttk.Combobox(form, values=CATEGORIES, state="readonly", width=12); self.category.set("Food")
        for col, widget in enumerate((self.description, self.amount, self.kind, self.category)): widget.grid(row=1, column=col, padx=4)
        ttk.Button(form, text="Add", command=self.add_transaction).grid(row=1, column=4)
        tools = ttk.Frame(self.transactions_tab)
        tools.pack(fill="x", pady=12)
        ttk.Label(tools, text="Show category:").pack(side="left")
        self.filter = ttk.Combobox(tools, values=("All",) + CATEGORIES, state="readonly", width=14)
        self.filter.set("All")
        self.filter.pack(side="left", padx=8)
        self.filter.bind("<<ComboboxSelected>>", lambda _event: self.refresh())
        self.report_label = ttk.Label(tools, text="")
        self.report_label.pack(side="right")
        self.table = ttk.Treeview(self.transactions_tab, columns=("description", "category", "type", "amount"), show="headings")
        for name in ("description", "category", "type", "amount"): self.table.heading(name, text=name.title())
        self.table.pack(fill="both", expand=True)
        ttk.Button(self.transactions_tab, text="Delete selected", command=self.delete_transaction).pack(anchor="e", pady=8)

    def build_budgets(self) -> None:
        form = ttk.LabelFrame(self.budgets_tab, text="Set or replace a category budget", padding=10); form.pack(fill="x")
        ttk.Label(form, text="Category").grid(row=0, column=0, sticky="w", padx=5)
        ttk.Label(form, text="Budget limit ($)").grid(row=0, column=1, sticky="w", padx=5)
        self.budget_category = ttk.Combobox(form, values=CATEGORIES, state="readonly"); self.budget_category.set("Food")
        self.budget_limit = ttk.Entry(form)
        self.budget_category.grid(row=1, column=0, padx=5)
        self.budget_limit.grid(row=1, column=1, padx=5)
        ttk.Button(form, text="Set budget", command=self.add_budget).grid(row=1, column=2, padx=5)
        self.budget_rows = ttk.Frame(self.budgets_tab); self.budget_rows.pack(fill="both", expand=True, pady=15)

    def add_transaction(self) -> None:
        try: self.finance.add_transaction(self.description.get(), self.amount.get(), self.kind.get(), self.category.get())
        except ValidationError as error: messagebox.showerror("Invalid transaction", str(error)); return
        self.description.delete(0, tk.END); self.amount.delete(0, tk.END); self.refresh()

    def delete_transaction(self) -> None:
        if self.table.selection(): self.finance.delete_transaction(self.table.selection()[0]); self.refresh()

    def add_budget(self) -> None:
        try: self.budgets.add(self.budget_category.get(), self.budget_limit.get())
        except ValidationError as error: messagebox.showerror("Invalid budget", str(error)); return
        self.budget_limit.delete(0, tk.END); self.refresh()

    def refresh(self) -> None:
        for label, value in zip(self.summary, self.finance.totals()): label.config(text=f"${value:,.2f}")
        category = self.filter.get()
        self.report_label.config(text=f"Visible expenses: ${self.reports.expense_total_for(category):,.2f}")
        for row in self.table.get_children(): self.table.delete(row)
        for item in self.reports.transactions_for(category): self.table.insert("", "end", iid=item.id, values=(item.description, item.category, item.kind, f"${item.amount:,.2f}"))
        for widget in self.budget_rows.winfo_children(): widget.destroy()
        for row, budget in enumerate(self.finance.account.budgets):
            spent, percent = self.budgets.progress(budget)
            ttk.Label(self.budget_rows, text=f"{budget.category}: ${spent:,.2f} / ${budget.limit:,.2f}").grid(row=row, column=0, sticky="w", pady=8)
            ttk.Progressbar(self.budget_rows, value=percent, maximum=100, length=350).grid(row=row, column=1, padx=15)
            ttk.Label(self.budget_rows, text=f"{percent:.0f}%").grid(row=row, column=2)
            ttk.Button(
                self.budget_rows,
                text="Delete",
                command=lambda budget_id=budget.id: self.delete_budget(budget_id),
            ).grid(row=row, column=3, padx=(15, 0))

    def delete_budget(self, budget_id: str) -> None:
        self.budgets.delete(budget_id)
        self.refresh()

    def run(self) -> None: self.root.mainloop()