import tkinter as tk
from tkinter import messagebox, ttk

from models import ValidationError
from services import FinanceService


class FinanceTrackerApp:
    def __init__(self, service: FinanceService) -> None:
        self.service = service
        self.root = tk.Tk()
        self.root.title("Finance Tracker — Step 5")
        self.root.geometry("760x560")
        frame = ttk.Frame(self.root, padding=20)
        frame.pack(fill="both", expand=True)
        ttk.Label(frame, text="My persistent account", font=("TkDefaultFont", 18, "bold")).pack(anchor="w")
        summary = ttk.Frame(frame)
        summary.pack(fill="x", pady=14)
        self.summary_labels = []
        for column, title in enumerate(("Income", "Expenses", "Balance")):
            card = ttk.LabelFrame(summary, text=title, padding=12)
            card.grid(row=0, column=column, padx=5, sticky="ew")
            summary.columnconfigure(column, weight=1)
            label = ttk.Label(card, text="$0.00", font=("TkDefaultFont", 15, "bold"))
            label.pack()
            self.summary_labels.append(label)
        form = ttk.LabelFrame(frame, text="New transaction", padding=12)
        form.pack(fill="x", pady=(0, 12))
        ttk.Label(form, text="Description").grid(row=0, column=0, sticky="w", padx=5)
        ttk.Label(form, text="Amount ($)").grid(row=0, column=1, sticky="w", padx=5)
        ttk.Label(form, text="Type").grid(row=0, column=2, sticky="w", padx=5)
        self.description = ttk.Entry(form, width=28)
        self.amount = ttk.Entry(form, width=14)
        self.kind = ttk.Combobox(form, values=("Income", "Expense"), state="readonly", width=12)
        self.kind.set("Expense")
        self.description.grid(row=1, column=0, padx=5)
        self.amount.grid(row=1, column=1, padx=5)
        self.kind.grid(row=1, column=2, padx=5)
        ttk.Button(form, text="Add", command=self.add).grid(row=1, column=3, padx=5)
        self.table = ttk.Treeview(frame, columns=("description", "type", "amount"), show="headings")
        for name, title in (("description", "Description"), ("type", "Type"), ("amount", "Amount")):
            self.table.heading(name, text=title)
        self.table.pack(fill="both", expand=True)
        ttk.Button(frame, text="Delete selected", command=self.delete).pack(anchor="e", pady=8)
        self.refresh()

    def add(self) -> None:
        try:
            self.service.add_transaction(self.description.get(), self.amount.get(), self.kind.get())
        except ValidationError as error:
            messagebox.showerror("Cannot add transaction", str(error))
            return
        self.description.delete(0, tk.END)
        self.amount.delete(0, tk.END)
        self.refresh()

    def delete(self) -> None:
        selected = self.table.selection()
        if selected:
            self.service.delete_transaction(selected[0])
            self.refresh()

    def refresh(self) -> None:
        for label, value in zip(self.summary_labels, self.service.totals()):
            label.config(text=f"${value:,.2f}")
        for row in self.table.get_children():
            self.table.delete(row)
        for item in self.service.all_transactions():
            self.table.insert("", "end", iid=item.id, values=(item.description, item.kind, f"${item.amount:,.2f}"))

    def run(self) -> None:
        self.root.mainloop()