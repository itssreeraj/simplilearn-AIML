import csv
from datetime import datetime

# Global variables
expenses = []
monthly_budget = 0

# Function to add an expense
def add_expense():
    print("\nAdd an Expense")
    date = input("Enter the date (YYYY-MM-DD): ")
    try:
        datetime.strptime(date, "%Y-%m-%d")  # Validate date format
    except ValueError:
        print("Invalid date format. Please use YYYY-MM-DD.")
        return

    category = input("Enter the category (e.g., Food, Travel): ").strip()
    if not category:
        print("Category cannot be empty.")
        return

    try:
        amount = float(input("Enter the amount spent: "))
        if amount <= 0:
            print("Amount must be greater than 0.")
            return
    except ValueError:
        print("Invalid amount. Please enter a numeric value.")
        return

    description = input("Enter a brief description: ").strip()
    if not description:
        print("Description cannot be empty.")
        return

    # Store the expense as a dictionary
    expense = {
        'date': date,
        'category': category,
        'amount': amount,
        'description': description
    }
    expenses.append(expense)
    print("Expense added successfully!")

# Function to view all expenses
def view_expenses():
    print("\nView Expenses")
    if not expenses:
        print("No expenses recorded yet.")
        return

    for i, expense in enumerate(expenses, 1):
        print(f"\nExpense {i}:")
        print(f"Date: {expense['date']}")
        print(f"Category: {expense['category']}")
        print(f"Amount: ${expense['amount']:.2f}")
        print(f"Description: {expense['description']}")

# Function to set monthly budget
def set_budget():
    global monthly_budget
    print("\nSet Monthly Budget")
    try:
        monthly_budget = float(input("Enter your monthly budget: "))
        if monthly_budget <= 0:
            print("Budget must be greater than 0.")
            return
        print("Budget set successfully!")
    except ValueError:
        print("Invalid input. Please enter a numeric value.")

# Function to track budget
def track_budget():
    print("\nTrack Budget")
    if monthly_budget <= 0:
        print("Monthly budget not set. Please set a budget first.")
        return

    total_expenses = sum(expense['amount'] for expense in expenses)
    remaining_balance = monthly_budget - total_expenses

    print(f"Total expenses: ${total_expenses:.2f}")
    print(f"Monthly budget: ${monthly_budget:.2f}")
    if remaining_balance < 0:
        print("Warning: You have exceeded your budget!")
    else:
        print(f"You have ${remaining_balance:.2f} left for the month.")

# Function to save expenses to a CSV file
def save_expenses():
    print("\nSave Expenses")
    if not expenses:
        print("No expenses to save.")
        return

    with open("expenses.csv", mode="w", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=['date', 'category', 'amount', 'description'])
        writer.writeheader()
        writer.writerows(expenses)
    print("Expenses saved to expenses.csv.")

# Function to load expenses from a CSV file
def load_expenses():
    global expenses
    try:
        with open("expenses.csv", mode="r") as file:
            reader = csv.DictReader(file)
            expenses = [row for row in reader]
            for expense in expenses:
                expense['amount'] = float(expense['amount'])  # Convert amount to float
        print("Expenses loaded successfully!")
    except FileNotFoundError:
        print("No saved expenses found. Starting with an empty list.")
    except Exception as e:
        print(f"Error loading expenses: {e}")

# Function to display the menu
def display_menu():
    print("\nPersonal Expense Tracker")
    print("1. Add Expense")
    print("2. View Expenses")
    print("3. Set Monthly Budget")
    print("4. Track Budget")
    print("5. Save Expenses")
    print("6. Exit")

# Main program loop
def main():
    load_expenses()  # Load expenses from file at startup
    while True:
        display_menu()
        choice = input("Enter your choice (1-6): ").strip()
        if choice == '1':
            add_expense()
        elif choice == '2':
            view_expenses()
        elif choice == '3':
            set_budget()
        elif choice == '4':
            track_budget()
        elif choice == '5':
            save_expenses()
        elif choice == '6':
            save_expenses()  # Save expenses before exiting
            print("Exiting the program. Goodbye!")
            break
        else:
            print("Invalid choice. Please enter a number between 1 and 6.")

# Run the program
if __name__ == "__main__":
    main()
