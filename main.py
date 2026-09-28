import tkinter as tk
from tkinter import ttk, messagebox
from models import Transaction

class FinanceTrackerApp:
    def __init__(self) -> None:
        self.root = tk.Tk()
        self.root.title("Finance Tracker")
        self.root.geometry("650x480")
        self.root.minsize(420,250)
        self.transactions:list[Transaction] = []
        self.build_ui()
        
    def build_ui(self) -> None:
        frame = ttk.Frame(self.root, padding=32)
        frame.pack(fill="both", expand=True)
        ttk.Label(frame, text="Add Transaction", font=("TkDefaultFont", 20, "bold")).pack(anchor="w")
        form = ttk.Frame(frame)
        form.pack(fill="x", pady=15)
        ttk.Label(form, text="Description").grid(row=0, column=0, sticky="w")
        ttk.Label(form, text="Amount").grid(row=0, column=1, sticky="w")
        ttk.Label(form, text="Type").grid(row=0, column=2, sticky="w")
        
        self.description_entry = ttk.Entry(form,width=28)
        self.amount_entry = ttk.Entry(form, width=14)
        self.kind_box = ttk.Combobox(form, values=('Income', 'Expense'), state='readonly', width=12)
        self.kind_box.set('Expense')
        self.description_entry.grid(row=1, column=0, padx=(0, 10))
        self.amount_entry.grid(row=1, column=1, padx=(0, 10))
        self.kind_box.grid(row=1, column=2, padx=(0, 10))
        ttk.Button(form, text="Add", command=self.add_transaction).grid(row = 1, column = 3)
        self.transaction_list = tk.Listbox(frame, font= ("TkFixedFont", 11), height = 14)
        self.transaction_list.pack(fill="both", expand=True)
        
    def add_transaction(self) -> None:
        try:
            amount = float(self.amount_entry.get())
        except ValueError:
            messagebox.showerror("Invalid amount", "Enter a number")
            return
        transaction = Transaction(
            description = self.description_entry.get() or "Untitled",
            amount= amount, 
            kind= self.kind_box.get()
        )
        self.transactions.append(transaction)
        self.description_entry.delete(0,tk.END)
        self.amount_entry.delete(0, tk.END)
        self.refresh_list()
        
    def refresh_list(self) -> None:
        self.transaction_list.delete(0, tk.END)
        for transaction in self.transactions:
            self.transaction_list.insert(tk.END, transaction.display_text())
            
        
        
    def run(self) -> None:
        self.root.mainloop()


if __name__ == "__main__":
    app = FinanceTrackerApp()
    app.run()