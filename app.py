import tkinter as tk
from tkinter import messagebox, ttk
from models import CATEGORIES, ValidationError
from services import FinanceService, ReportService


class FinanceTrackerApp:
    def __init__(self, finance: FinanceService, reports: ReportService) -> None:
        self.finance, self.reports = finance, reports
        self.root = tk.Tk()
        self.root.title("Finance Tracker — Step 6")
        self.root.geometry("850x600")
        frame = ttk.Frame(self.root, padding=20)
        frame.pack(fill="both", expand=True)
        ttk.Label(frame, text="Category report", font=("TkDefaultFont", 18, "bold")).pack(anchor="w")
        summary = ttk.Frame(frame)
        summary.pack(fill="x", pady=12)
        self.summary_labels = []
        for column, title in enumerate(("Income", "Expenses", "Balance")):
            card = ttk.LabelFrame(summary, text=title, padding=10)
            card.grid(row=0, column=column, padx=4, sticky="ew")
            summary.columnconfigure(column, weight=1)
            label = ttk.Label(card, text="$0.00", font=("TkDefaultFont", 14, "bold"))
            label.pack(); self.summary_labels.append(label)
        form = ttk.LabelFrame(frame, text="New transaction", padding=10)
        form.pack(fill="x")
        for column, text in enumerate(("Description", "Amount ($)", "Type", "Category")):
            ttk.Label(form, text=text).grid(row=0, column=column, sticky="w", padx=4)
        self.description, self.amount = ttk.Entry(form, width=24), ttk.Entry(form, width=12)
        self.kind = ttk.Combobox(form, values=("Income", "Expense"), state="readonly", width=10)
        self.category = ttk.Combobox(form, values=CATEGORIES, state="readonly", width=12)
        self.kind.set("Expense"); self.category.set("Food")
        for column, widget in enumerate((self.description, self.amount, self.kind, self.category)):
            widget.grid(row=1, column=column, padx=4)
        ttk.Button(form, text="Add", command=self.add).grid(row=1, column=4, padx=4)
        tools = ttk.Frame(frame)
        tools.pack(fill="x", pady=12)
        ttk.Label(tools, text="Show category:").pack(side="left")
        self.filter = ttk.Combobox(tools, values=("All",) + CATEGORIES, state="readonly", width=14)
        self.filter.set("All"); self.filter.pack(side="left", padx=8)
        self.filter.bind("<<ComboboxSelected>>", lambda _event: self.refresh())
        self.report_label = ttk.Label(tools, text="")
        self.report_label.pack(side="right")
        self.table = ttk.Treeview(frame, columns=("description", "category", "type", "amount"), show="headings")
        for name in ("description", "category", "type", "amount"):
            self.table.heading(name, text=name.title())
        self.table.pack(fill="both", expand=True)
        ttk.Button(frame, text="Delete selected", command=self.delete).pack(anchor="e", pady=8)
        self.refresh()

    def add(self) -> None:
        try:
            self.finance.add_transaction(self.description.get(), self.amount.get(), self.kind.get(), self.category.get())
        except ValidationError as error:
            messagebox.showerror("Cannot add transaction", str(error)); return
        self.description.delete(0, tk.END); self.amount.delete(0, tk.END); self.refresh()

    def delete(self) -> None:
        if self.table.selection():
            self.finance.delete_transaction(self.table.selection()[0]); self.refresh()

    def refresh(self) -> None:
        for label, value in zip(self.summary_labels, self.finance.totals()):
            label.config(text=f"${value:,.2f}")
        category = self.filter.get()
        self.report_label.config(text=f"Visible expenses: ${self.reports.expense_total_for(category):,.2f}")
        for row in self.table.get_children(): self.table.delete(row)
        for item in self.reports.transactions_for(category):
            self.table.insert("", "end", iid=item.id, values=(item.description, item.category, item.kind, f"${item.amount:,.2f}"))

    def run(self) -> None:
        self.root.mainloop()