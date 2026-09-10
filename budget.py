import json
import os
import csv
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

    def delete_transaction(self, index):
        try:
            transaction = self.data["transactions"].pop(index)
            self.data["balance"] -= transaction["amount"]
            self._save_data()
            return True
        except IndexError:
            return False

    def clear_all(self):
        self.data = {"balance": 0.0, "transactions": []}
        self._save_data()

    def get_report(self):
        return self.data

    def get_category_summary(self):
        summary = {}
        for t in self.data["transactions"]:
            cat = t["category"]
            summary[cat] = summary.get(cat, 0.0) + t["amount"]
        
        return [{"Category": k, "Total": v} for k, v in summary.items()]

    def filter_transactions(self, query=None, category=None):
        filtered = self.data["transactions"]
        if category:
            filtered = [t for t in filtered if t['category'].lower() == category.lower()]
        if query:
            filtered = [t for t in filtered if query.lower() in t['description'].lower()]
        return filtered

    def export_to_csv(self, filename="budget_export.csv"):
        if not self.data["transactions"]:
            return False
        
        keys = self.data["transactions"][0].keys()
        with open(filename, "w", newline="") as f:
            dict_writer = csv.DictWriter(f, fieldnames=keys)
            dict_writer.writeheader()
            dict_writer.writerows(self.data["transactions"])
        return True

def main():
    manager = BudgetManager()
    
    while True:
        print("\n--- Pocket Budget CLI ---")
        print("1. View Balance & Report")
        print("2. Set Initial Balance")
        print("3. Add Income/Expense")
        print("4. Delete Transaction")
        print("5. Export to CSV")
        print("6. Search/Filter Transactions")
        print("7. Reset All Data")
        print("8. Exit")
        
        choice = input("Choose an option: ")
        
        if choice == "1":
            report = manager.get_report()
            print(f"\nCurrent Balance: ${report['balance']:.2f}")
            
            if report['transactions']:
                print("\nCategory Summary:")
                summary = manager.get_category_summary()
                print(tabulate(summary, headers="keys", tablefmt="grid"))
                
                print("\nTransactions:")
                # Enumerating transactions to provide index for deletion
                table_data = [[i, t['date'], t['description'], t['amount'], t['category']] 
                             for i, t in enumerate(report['transactions'])]
                print(tabulate(table_data, headers=["ID", "Date", "Description", "Amount", "Category"], tablefmt="grid"))
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
            if not manager.data["transactions"]:
                print("No transactions to delete.")
                continue
            try:
                idx = int(input("Enter Transaction ID to delete: "))
                if manager.delete_transaction(idx):
                    print("Transaction deleted.")
                else:
                    print("Invalid ID.")
            except ValueError:
                print("Please enter a valid number.")

        elif choice == "5":
            filename = input("Enter filename (default: budget_export.csv): ") or "budget_export.csv"
            if manager.export_to_csv(filename):
                print(f"Data successfully exported to {filename}")
            else:
                print("No transactions to export.")

        elif choice == "6":
            print("\n--- Filter Options ---")
            print("Leave blank to ignore filter")
            cat_filter = input("Category: ")
            query_filter = input("Keyword in description: ")
            
            filtered = manager.filter_transactions(query=query_filter, category=cat_filter)
            if filtered:
                # Note: IDs here are relative to the filtered list, not the original indices
                table_data = [[t['date'], t['description'], t['amount'], t['category']] for t in filtered]
                print(tabulate(table_data, headers=["Date", "Description", "Amount", "Category"], tablefmt="grid"))
            else:
                print("No matching transactions found.")

        elif choice == "7":
            confirm = input("Are you sure you want to clear all data? (y/N): ")
            if confirm.lower() == 'y':
                manager.clear_all()
                print("Data reset successfully.")
            else:
                print("Reset cancelled.")

        elif choice == "8":
            break
        else:
            print("Invalid choice.")

if __name__ == "__main__":
    main()