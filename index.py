import json
import os
from datetime import datetime

# Function to load expenses from a file (expenses.json)
def load_expenses(file_name='expenses.json'):
    # Check if the file exists
    if not os.path.exists(file_name):
        with open(file_name, 'w') as file:
            json.dump([], file)  # Initialize with an empty list
        return []

    # Load the JSON data if the file exists
    try:
        with open(file_name, 'r') as file:
            return json.load(file)
    except json.JSONDecodeError:  # Handle the case where the file is corrupted or empty
        with open(file_name, 'w') as file:
            json.dump([], file)  # Reinitialize with an empty list
        return []

# Function to save expenses to a file (expenses.json)
def save_expenses(expenses, file_name='expenses.json'):
    with open(file_name, 'w') as file:
        json.dump(expenses, file, indent=4)

# Function to add a new expense
def add_expense(expenses):
    try:
        amount = float(input("Enter expense amount (in ₹): ₹"))
        category = input("Enter category (e.g., Food, Transport): ")
        date = input("Enter date (YYYY-MM-DD) or leave blank for today: ")
        if not date:
            date = datetime.now().strftime('%Y-%m-%d')  # Use today's date if not provided
        expense = {'amount': amount, 'category': category, 'date': date}
        expenses.append(expense)
        save_expenses(expenses)
        print("Expense added successfully!")
    except ValueError:
        print("Invalid amount entered!")

# Function to view spending over time (day, week, month)
def view_spending_by_time(expenses, time_filter):
    time_summary = {}
    for exp in expenses:
        date_obj = datetime.strptime(exp['date'], '%Y-%m-%d')
        if time_filter == 'day':
            key = date_obj.strftime('%Y-%m-%d')
        elif time_filter == 'week':
            key = f"Week {date_obj.isocalendar()[1]}, {date_obj.year}"
        elif time_filter == 'month':
            key = date_obj.strftime('%Y-%m')
        else:
            continue
        if key not in time_summary:
            time_summary[key] = 0
        time_summary[key] += exp['amount']
    for time_period, total in time_summary.items():
        print(f"{time_period}: ₹{total:.2f}")

# Function to view summary of total spending
def view_summary(expenses):
    if not expenses:
        print("No expenses recorded yet.")
        return
    total_spending = sum(expense['amount'] for expense in expenses)
    print(f"Total Spending: ₹{total_spending:.2f}")
    category = input("Enter category to see total spending (or leave blank for all categories): ")
    if category:
        category_total = sum(exp['amount'] for exp in expenses if exp['category'].lower() == category.lower())
        print(f"Total Spending on {category.capitalize()}: ₹{category_total:.2f}")
    time_filter = input("Do you want to view by day, week, or month? Leave blank for no filter: ").lower()
    if time_filter:
        view_spending_by_time(expenses, time_filter)

# Main menu function
def show_menu():
    expenses = load_expenses()
    while True:
        print("\nPersonal Expense Tracker")
        print("1. Add Expense")
        print("2. View Summary")
        print("3. Exit")
        choice = input("Enter your choice (1/2/3): ")
        if choice == '1':
            add_expense(expenses)
        elif choice == '2':
            view_summary(expenses)
        elif choice == '3':
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

# Entry point of the program
if __name__ == "__main__":
    show_menu()
