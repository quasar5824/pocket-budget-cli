import json
import os
from datetime import datetime
from tabulate import tabulate

DATA_FILE = "budget_data.json"

class BudgetManager:
    def __init__(self):
        self.data = self._load_data()

    def _load_data(self):
        if os.path.exists(DATA_FILE):
            with open(DATA_FILE, "r") as f:
                return json.load(f)
        return {"balance": 0.0, "transactions": []}

    def _save_data(self):
        with open(DATA_FILE, "w") as f:
            json.dump(self.data, f, indent=4)

    def set_balance(self, amount):
        self.data["balance"] = float(amount)
        self._save_data()

    def add_transaction(self, description, amount, category):
        amount = float(amount)
        self.data["balance"] += amount
        self.data["transactions"].append({
            "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "description": description,
            "amount": amount,
            "category": category
        })
        self._save_data()

    def get_report(self):
        return self.data

def main():
    manager = BudgetManager()
    
    while True:
        print("\n--- Pocket Budget CLI ---")
        print("1. View Balance & Report")
        print("2. Set Initial Balance")
        print("3. Add Income/Expense")
        print("4. Exit")
        
        choice = input("Choose an option: ")
        
        if choice == "1":
            report = manager.get_report()
            print(f"\nCurrent Balance: ${report['balance']:.2f}")
            if report['transactions']:
                print("\nTransactions:")
                print(tabulate(report['transactions'], headers="keys", tablefmt="grid"))
            else:
                print("No transactions yet.")
                
        elif choice == "2":
            try:
                amount = float(input("Enter starting balance: "))
                manager.set_balance(amount)
                print("Balance updated.")
            except ValueError:
                print("Invalid amount.")
                
        elif choice == "3":
            try:
                desc = input("Description: ")
                amount = float(input("Amount (negative for expense, positive for income): "))
                cat = input("Category: ")
                manager.add_transaction(desc, amount, cat)
                print("Transaction recorded.")
            except ValueError:
                print("Invalid amount.")
                
        elif choice == "4":
            break
        else:
            print("Invalid choice.")

if __name__ == "__main__":
    main()