import turtle
from datetime import datetime
import os

EXPENSES_FILE = "expenses.txt"
BUDGET_FILE = "budget.txt"
CATEGORIES = ["Food", "Housing", "Transportation", "Education", "Entertainment", "Shopping", "Other"]

def load_file(filepath):
    try:
        with open(filepath, "r") as file:
            return [line.strip().split("\t") for line in file if line.strip()]
    except FileNotFoundError:
        return []

def save_expense(expense):
    with open(EXPENSES_FILE, "a") as file:
        file.write("\t".join(expense) + "\n")

def validate_date(date_text):
    try:
        datetime.strptime(date_text, "%Y-%m-%d")
        return True
    except ValueError:
        return False

def add_expenses():
    while True:
        date = input("Date (YYYY-MM-DD): ")
        if validate_date(date):
            break
        print("Invalid date format. Try again.")
    while True:
        try:
            amount = float(input("Amount: "))
            break
        except ValueError:
            print("Invalid number. Try again.")
    while True:
        category = input(f"Category {CATEGORIES}: ")
        if category in CATEGORIES:
            break
        print("Invalid category. Try again.")
    description = input("Description: ")
    save_expense([date, str(amount), category, description])
    print("✅ Expense added successfully.")

def view_expenses(expenses):
    choice = input("View (all/categorized): ").strip().lower()
    if choice == "all":
        print("\n--- All Expenses ---")
        for expense in expenses:
            print("\t".join(expense))
    else:
        print("\n--- Expenses by Category ---")
        categorized = {cat: [] for cat in CATEGORIES}
        for expense in expenses:
            categorized[expense[2]].append(expense)
        for category, items in categorized.items():
            if items:
                print(f"\n{category}:")
                for item in items:
                    print("\t".join(item))

def total_expenses(expenses):
    totals = {cat: 0.0 for cat in CATEGORIES}
    for expense in expenses:
        try:
            totals[expense[2]] += float(expense[1])
        except (ValueError, IndexError):
            continue
    return totals

def bar_chart(totals):
    wn = turtle.Screen()
    wn.bgcolor("white")
    wn.title("Expense Chart")
    wn.setup(width=800, height=600)
    wn.tracer(0)

    drawer = turtle.Turtle()
    labeler = turtle.Turtle()
    legend = turtle.Turtle()
    drawer.speed(0)
    drawer.hideturtle()
    labeler.hideturtle()
    legend.hideturtle()
    labeler.penup()
    legend.penup()

    max_amount = max(totals.values()) if totals.values() else 1
    scale_factor = 300 / max_amount
    bar_width = 50
    spacing = 30
    colors = ["red", "blue", "green", "orange", "purple", "yellow", "cyan"]

    x = -((bar_width + spacing) * len(CATEGORIES)) // 2

    for i, category in enumerate(CATEGORIES):
        amount = totals[category]
        height = amount * scale_factor

        drawer.penup()
        drawer.goto(x, -200)
        drawer.pendown()
        drawer.color(colors[i % len(colors)])
        drawer.begin_fill()
        for _ in range(2):
            drawer.forward(bar_width)
            drawer.left(90)
            drawer.forward(height)
            drawer.left(90)
        drawer.end_fill()

        labeler.goto(x + bar_width / 2, -210)
        labeler.write(category, align="center", font=("Arial", 9, "normal"))
        labeler.goto(x + bar_width / 2, -200 + height + 5)
        labeler.write(f"{amount:.2f}", align="center", font=("Arial", 9, "bold"))

        x += bar_width + spacing

    wn.update()
    wn.exitonclick()

def search_expenses(expenses):
    keyword = input("Search keyword: ").lower()
    print(f"\n--- Search Results for '{keyword}' ---")
    found = False
    for expense in expenses:
        if keyword in expense[2].lower() or keyword in expense[3].lower():
            print("\t".join(expense))
            found = True
    if not found:
        print("No results found.")

def budget_alerts(totals, budgets):
    print("\n--- Budget Check ---")
    for budget in budgets:
        try:
            category, limit = budget[0], float(budget[1])
            spent = totals.get(category, 0)
            if spent > limit:
                print(f"⚠️ Over budget in {category}! Spent: {spent}, Limit: {limit}")
            else:
                print(f"{category}: Remaining budget = {round(limit - spent, 2)}")
        except (IndexError, ValueError):
            continue

def menu():
    options = {
        "1": ("Add Expense", add_expenses),
        "2": ("View Expenses", lambda: view_expenses(load_file(EXPENSES_FILE))),
        "3": ("Bar Chart", lambda: bar_chart(total_expenses(load_file(EXPENSES_FILE)))),
        "4": ("Search Expenses", lambda: search_expenses(load_file(EXPENSES_FILE))),
        "5": ("Budget Alerts", lambda: budget_alerts(total_expenses(load_file(EXPENSES_FILE)), load_file(BUDGET_FILE))),
        "6": ("Exit", exit)
    }

    while True:
        print("\n=== Expense Tracker Menu ===")
        for key, (desc, _) in options.items():
            print(f"{key}. {desc}")
        choice = input("Choose an option: ").strip()
        action = options.get(choice)
        if action:
            action[1]()
        else:
            print("❌ Invalid selection. Try again.")

if __name__ == "__main__":
    for file in [EXPENSES_FILE, BUDGET_FILE]:
        if not os.path.exists(file):
            open(file, "w").close()
    menu()
