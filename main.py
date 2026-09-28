import tkinter as tk
from tkinter import ttk

class FinanceTrackerApp:
    def __init__(self) -> None:
        self.root = tk.Tk()
        self.root.title("Finance Tracker")
        self.root.geometry("520x300")
        self.root.minsize(420,250)
        self.build_ui()
        
    def build_ui(self) -> None:
        container = ttk.Frame(self.root, padding=32)
        container.pack(fill="both", expand=True)
        ttk.Label(container, text="Personal Finance Tracker", font=("TkDefaultFont", 20, "bold")).pack(pady=(35,12))
        ttk.Label(container, text="This is my finance tracker").pack(pady=6)
        ttk.Button(container, text="Test", command=self.show_ready_message).pack(pady=18)
        self.status_label = ttk.Label(container, text="")
        self.status_label.pack()
        
    def show_ready_message(self) ->None:
        self.status_label.config(text="ready")
        
    def run(self) -> None:
        self.root.mainloop()


if __name__ == "__main__":
    app = FinanceTrackerApp()
    app.run()