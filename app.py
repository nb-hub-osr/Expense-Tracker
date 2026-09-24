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

    category_total = {}

    for expense in expenses:
      category = expense["category"]
      amount = expense["amount"]

      if category in category_total:
        category_total[category] += amount
      else:
        category_total[category] = amount

    if category_total:
      st.subheader("📊 Spending by Category")
      st.bar_chart(category_total)
    
# ==================================================
# ADD EXPENSE
# ==================================================
if option == "Add Expense":

    st.header("➕ Add Expense")

    col1, col2 = st.columns(2)

    with col1:
        name = st.text_input("Expense name")

        category = st.selectbox(
    "Category",
    [
        "Food",
        "Travel",
        "Shopping",
        "Education",
        "Entertainment",
        "Bills",
        "Other"
    ]
)

    with col2:
        amount = st.number_input(
            "Amount",
            min_value=0.0,
            step=1.0
        )

        expense_date = st.date_input(
            "Date",
            value=date.today()
        )

    if st.button("💾 Add Expense"):

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

        st.dataframe(
            expenses,
            use_container_width=True
        )

    categories = ["All"]

    for expense in expenses:
      if expense["category"] not in categories:
        categories.append(expense["category"])

    selected_category = st.selectbox(
          "Filter by category",
    categories
)

    if selected_category == "All":
       filtered_expenses = expenses
    else:
        filtered_expenses = [
        expense
        for expense in expenses
         if expense["category"] == selected_category
    ]

    st.dataframe(
    filtered_expenses,
    use_container_width=True
)
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
