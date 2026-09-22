import json
from datetime import date

 
print("===== EXPENSE TRACKER =====")
print("*******Personal Expense Manager******")


# LOAD EXPENSES
def load_expenses():
    try:
        with open("expenses.json", "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return []


expenses = load_expenses()


# SAVE EXPENSES
def save_expenses():
    with open("expenses.json", "w") as file:
        json.dump(expenses, file, indent=4)


# ADD EXPENSE
def add_expense():
    expense_name = input("Expense name: ")

    while True:
        try:
            amount = float(input("Amount: "))
            break
        except ValueError:
            print("Please enter a valid value.")

    category = input("Category: ")

    expense_date = str(date.today())

    expense = {
        "name": expense_name,
        "amount": amount,
        "category": category,
        "date": expense_date
    }

    expenses.append(expense)
    save_expenses()

    print("Expense Added!")
    print("You spent Rs.", amount, "on", expense_name)
    print("Category:", category)
    print("Date:", expense_date)


# VIEW EXPENSE
def view_expense():
    print("=== ALL EXPENSES ===")

    if len(expenses) == 0:
        print("No expense found!")
        return
    
    for i, expense in enumerate(expenses, start=1):
            print(f"""
                Expense {i}
                Name :{expense["name"]}
                Amount :"Rs." {expense["amount"]:.2f}
                Category :{expense["category"]}
                Date :{expense["date"]}
            ---------------------""")


# CALCULATE TOTAL
def calculate_total():
    total = 0

    for expense in expenses:
        total = total + expense["amount"]

    return total


# DELETE EXPENSE
def delete_expense():
    print("=== DELETE EXPENSE ===")

    if len(expenses) == 0:
        print("Nothing to delete!")

    else:
        for i, expense in enumerate(expenses, start=1):
            print(
                i,
                expense["name"],
                "Rs.", expense["amount"],
                expense["category"],
                expense["date"]
            )

        while True:
            try:
                choice = int(input("Enter the expense number to delete: "))

                if choice < 1 or choice > len(expenses):
                    print("Please enter a valid expense number.")
                else:
                    break

            except ValueError:
                print("Please enter a number.")

        index = choice - 1

        removed_expense = expenses.pop(index)

        save_expenses()

        print(removed_expense["name"], "deleted!")


# SEARCH EXPENSE
def search_expense():
    category = input("Enter category to search: ")

    found = False

    for i, expense in enumerate(expenses, start=1):

        if expense["category"] == category:
            print(
                i,
                expense["name"],
                "Rs.", expense["amount"],
                expense["category"],
                expense["date"]
            )

            found = True

    if found == False:
        print("No expense found in this category.")


# CATEGORY SUMMARY
def category_summary():
    category_total = {}

    for expense in expenses:
        category = expense["category"]
        amount = expense["amount"]

        if category in category_total:
            category_total[category] = category_total[category] + amount

        else:
            category_total[category] = amount

    print("=== CATEGORY SUMMARY ===")

    for category, total in category_total.items():
        print(category, "Rs.", total)

# MONTHLY SUMMARY
def monthly_summary():
    month = input("Enter month (YYYY-MM): ")

    total = 0

    for expense in expenses:

        if expense["date"].startswith(month):
            total = total + expense["amount"]

    print("=== MONTHLY SUMMARY ===")
    print("Month:", month)
    print("Total Spent: Rs.", total)

# EDIT EXPENSE
def edit_expense():
    print("=== EDIT EXPENSE ===")

    if len(expenses) == 0:
        print("No expenses to edit!")
        return

    for i, expense in enumerate(expenses, start=1):
        print(
            i,
            expense["name"],
            "Rs.", expense["amount"],
            expense["category"],
            expense["date"]
        )

    while True:
        try:
            choice = int(input("Enter expense number to edit: "))

            if choice < 1 or choice > len(expenses):
                print("Please enter a valid expense number.")
            else:
                break

        except ValueError:
            print("Please enter a number.")

    index = choice - 1

    expense = expenses[index]

    print("Enter new details:")

    new_name = input("New name: ")

    while True:
        try:
            new_amount = float(input("New amount: "))
            break
        except ValueError:
            print("Please enter a valid amount.")

    new_category = input("New category: ")

    expense["name"] = new_name
    expense["amount"] = new_amount
    expense["category"] = new_category

    save_expenses()

    print("Expense updated successfully!")

 # MAIN MENU

while True:
    print("\n======= MENU ========")
    print("1. Add expense")
    print("2. View expense")
    print("3. Show total")
    print("4. Delete expense")
    print("5. Search expense")
    print("6. Category summary")
    print("7. Monthly summary")
    print("8. Edit Expense")
    print("9. Exit")

    try:
        choice = input("Enter your choice: ")
        # print("DEBUG:",repr(choice))
        # print("i received:",choice)

    except ValueError:
        print("Please enter a number from 1 to 9.")
        continue

    if choice == "1":
        add_expense()

    elif choice == "2":
        # print("OPTION 2 WORKED")
        view_expense()

    elif choice == "3":
        total = calculate_total()
        print(f"Total amount spent: Rs.{total:.2f}")
        print(f"Number of expenses:{len(expenses)}")
        

    elif choice == "4":
        delete_expense()

    elif choice == "5":
        search_expense()

    elif choice == "6":
        category_summary()

    elif choice == "7":
        monthly_summary()

    elif choice == "8":
        edit_expense()

    elif choice == "9":
        print("Goodbye!")
        break

    else:
        print("Invalid choice!")