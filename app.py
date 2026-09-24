import streamlit as st
import json
from datetime import date


# ---------------- LOAD DATA ----------------

def load_expenses():
    try:
        with open("expenses.json", "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return []


# ---------------- SAVE DATA ----------------

def save_expenses(expenses):
    with open("expenses.json", "w") as file:
        json.dump(expenses, file, indent=4)


# ---------------- PAGE ----------------

st.set_page_config(
    page_title="Expense Tracker",
    page_icon="💰"
)

st.title("💰 Expense Tracker")
st.write("Manage your expenses easily.")


# Load expenses
expenses = load_expenses()


# ---------------- SIDEBAR ----------------

st.sidebar.title("📋 Menu")

option = st.sidebar.radio(
    "Choose an option:",
    [
        "Dashboard",
        "Add Expense",
        "View Expenses",
        "Total Spending",
        "Delete Expense",
        "Search Expense",
        "Category Summary",
        "Monthly Summary",
        "Edit Expense"
    ]
)


# ==================================================
# DASHBOARD
# ==================================================

if option == "Dashboard":

    st.header("🏠 Dashboard")

    total = 0

    for expense in expenses:
        total += expense["amount"]

    number_of_expenses = len(expenses)

    if number_of_expenses > 0:
        average_expense = total / number_of_expenses
    else:
        average_expense = 0

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "💰 Total Spending",
        f"₹{total:.2f}"
    )

    col2.metric(
        "🧾 Number of Expenses",
        number_of_expenses
    )

    col3.metric(
        "📊 Average Expense",
        f"₹{average_expense:.2f}"
    )
    
# ==================================================
# ADD EXPENSE
# ==================================================

if option == "Add Expense":

    st.header("➕ Add Expense")

    name = st.text_input("Expense name")

    amount = st.number_input(
        "Amount",
        min_value=0.0,
        step=1.0
    )

    category = st.text_input("Category")

    expense_date = st.date_input(
        "Date",
        value=date.today()
    )

    if st.button("Add Expense"):

        if name and category and amount > 0:

            new_expense = {
                "name": name,
                "amount": amount,
                "category": category,
                "date": str(expense_date)
            }

            expenses.append(new_expense)

            save_expenses(expenses)

            st.success("Expense added successfully! 🎉")

        else:
            st.error("Please fill all fields correctly.")


# ==================================================
# VIEW EXPENSES
# ==================================================

elif option == "View Expenses":

    st.header("👀 All Expenses")

    if len(expenses) == 0:

        st.info("No expenses found.")

    else:

        for i, expense in enumerate(expenses, start=1):

            st.write(f"### Expense {i}")

            col1, col2, col3, col4 = st.columns(4)

            col1.write(f"**Name**\n{expense['name']}")
            col2.write(f"**Amount**\n₹{expense['amount']}")
            col3.write(f"**Category**\n{expense['category']}")
            col4.write(f"**Date**\n{expense['date']}")

            st.divider()


# ==================================================
# TOTAL SPENDING
# ==================================================

elif option == "Total Spending":

    st.header("💰 Total Spending")

    total = 0

    for expense in expenses:
        total += expense["amount"]

    st.metric(
        "Total Amount Spent",
        f"₹{total:.2f}"
    )


# ==================================================
# DELETE EXPENSE
# ==================================================

elif option == "Delete Expense":

    st.header("🗑️ Delete Expense")

    if len(expenses) == 0:

        st.info("No expenses available.")

    else:

        expense_names = []

        for i, expense in enumerate(expenses):
            expense_names.append(
                f"{i + 1}. {expense['name']} - ₹{expense['amount']}"
            )

        selected = st.selectbox(
            "Select expense to delete",
            expense_names
        )

        if st.button("Delete Expense"):

            index = expense_names.index(selected)

            removed = expenses.pop(index)

            save_expenses(expenses)

            st.success(
                f"{removed['name']} deleted successfully!"
            )


# ==================================================
# SEARCH EXPENSE
# ==================================================

elif option == "Search Expense":

    st.header("🔎 Search Expense")

    category = st.text_input(
        "Enter category"
    )

    if st.button("Search"):

        found = False

        for expense in expenses:

            if expense["category"].lower() == category.lower():

                st.write(
                    f"**{expense['name']}** — "
                    f"₹{expense['amount']} — "
                    f"{expense['date']}"
                )

                found = True

        if not found:
            st.warning("No expense found in this category.")


# ==================================================
# CATEGORY SUMMARY
# ==================================================

elif option == "Category Summary":

    st.header("📊 Category Summary")

    category_total = {}

    for expense in expenses:

        category = expense["category"]
        amount = expense["amount"]

        if category in category_total:
            category_total[category] += amount

        else:
            category_total[category] = amount

    if len(category_total) == 0:

        st.info("No expenses available.")

    else:

        for category, total in category_total.items():

            st.metric(
                category,
                f"₹{total:.2f}"
            )

        # Chart
        st.bar_chart(category_total)


# ==================================================
# MONTHLY SUMMARY
# ==================================================

elif option == "Monthly Summary":

    st.header("📅 Monthly Summary")

    month = st.text_input(
        "Enter month (YYYY-MM)",
        value=str(date.today())[:7]
    )

    if st.button("Calculate"):

        total = 0

        for expense in expenses:

            if expense["date"].startswith(month):

                total += expense["amount"]

        st.metric(
            f"Total spent in {month}",
            f"₹{total:.2f}"
        )


# ==================================================
# EDIT EXPENSE
# ==================================================

elif option == "Edit Expense":

    st.header("✏️ Edit Expense")

    if len(expenses) == 0:

        st.info("No expenses available.")

    else:

        expense_names = []

        for i, expense in enumerate(expenses):

            expense_names.append(
                f"{i + 1}. {expense['name']} - ₹{expense['amount']}"
            )

        selected = st.selectbox(
            "Select expense to edit",
            expense_names
        )

        index = expense_names.index(selected)

        selected_expense = expenses[index]

        new_name = st.text_input(
            "Expense name",
            value=selected_expense["name"]
        )

        new_amount = st.number_input(
            "Amount",
            min_value=0.0,
            value=float(selected_expense["amount"]),
            step=1.0
        )

        new_category = st.text_input(
            "Category",
            value=selected_expense["category"]
        )

        new_date = st.date_input(
            "Date",
            value=date.fromisoformat(
                selected_expense["date"]
            )
        )

        if st.button("Update Expense"):

            selected_expense["name"] = new_name
            selected_expense["amount"] = new_amount
            selected_expense["category"] = new_category
            selected_expense["date"] = str(new_date)

            save_expenses(expenses)

            st.success("Expense updated successfully! 🎉")