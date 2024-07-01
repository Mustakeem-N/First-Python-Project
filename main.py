from expense import Money
import calendar
import datetime

def main():
    print("""Hello User, 
    Running Budgeting App!""")
    expense_file = "expenses.csv"
    budget = 3000

    # user inputs their spending
    expense = user_spending()

    # writes the expense to a file
    save_spending(expense, expense_file)

    # reads the file and then summarizes the expense
    summarize_spending(expense_file, budget)

def user_spending():
    expense_name = input("Enter expense name: ")
    
    expense_amount = get_valid_amount("Enter amount spent: ")

    spending_categories = [
        "Home",
        "Utilities",
        "Food Delivery / Eating Out",
        "Groceries", 
        "Work", 
        "Fun", 
        "Misc"
        ]

    selected_category = get_valid_category(spending_categories)
    
    return Money(name=expense_name, category=selected_category, amount=expense_amount)

def get_valid_amount(prompt):
    while True:
        try:
            amount = float(input(prompt))
            return amount
        except ValueError:
            print("Invalid amount. Please enter a number.")

def get_valid_category(categories):
    while True:
        print("Choose a category from the following: ")
        for i, category_name in enumerate(categories):
            print(f" {i + 1}. {category_name}")

        value_range = f"[1 - {len(categories)}]"
        try:
            selected_index = int(input(f"Enter the number of category choice {value_range}: ")) - 1
            if 0 <= selected_index < len(categories):
                return categories[selected_index]
            else:
                print("Invalid category. Please try again!")
        except ValueError:
            print("Invalid input. Please enter a number.")

def save_spending(expense, expense_file):
    print(f"Saving User Expense: {expense} to {expense_file}")
    with open(expense_file, "a", encoding="utf-8") as f:
        f.write(f"{expense.name},{expense.amount:.2f},{expense.category}\n")

def summarize_spending(expense_file, budget):
    print("Summarizing User Expense")
    expenses = read_expenses(expense_file)
    if not expenses:
        return
    
    amount_by_category = calculate_amount_by_category(expenses)

    print("Expenses By Category:")
    for category, amount in amount_by_category.items():
        print(f"  {category}: ${amount:.2f}")

    total_spent = sum(expense.amount for expense in expenses)
    print(f"Total Spent: ${total_spent:.2f}")

    remaining_budget = budget - total_spent
    print(f"Budget Remaining: ${remaining_budget:.2f}")

    daily_budget = calculate_daily_budget(remaining_budget)
    print(green(f"Budget Per Day: ${daily_budget:.2f}"))

def read_expenses(expense_file):
    try:
        with open(expense_file, "r", encoding="utf-8") as f:
            lines = f.readlines()
            return [compute_expense(line.strip()) for line in lines]
    except FileNotFoundError:
        print("Expense file not found.")
    except Exception as e:
        print(f"An error occurred: {e}")
    return []

def compute_expense(line):
    expense_name, expense_amount, expense_category = line.split(",")
    return Money(name=expense_name, amount=float(expense_amount), category=expense_category)

def calculate_amount_by_category(expenses):
    amount_by_category = {}
    for expense in expenses:
        amount_by_category[expense.category] = amount_by_category.get(expense.category, 0) + expense.amount
    return amount_by_category

def calculate_daily_budget(remaining_budget):
    now = datetime.datetime.now()
    days_in_month = calendar.monthrange(now.year, now.month)[1]
    remaining_days = days_in_month - now.day
    return remaining_budget / remaining_days if remaining_days > 0 else remaining_budget

def green(text):
    return f"\033[92m{text}\033[0m"

if __name__ == "__main__":
    main()