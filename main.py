# Expense Tracker using Stack + Streamlit Dashboard
# Run with: streamlit run app.py

import streamlit as st
from collections import defaultdict
import matplotlib.pyplot as plt

# -----------------------------
# STACK CLASS
# -----------------------------
class ExpenseStack:
    def __init__(self):
        self.stack = []

    def push(self, item):
        self.stack.append(item)

    def pop(self):
        if self.stack:
            return self.stack.pop()
        return None

    def get_all(self):
        return self.stack

# -----------------------------
# APP SETUP
# -----------------------------
st.set_page_config(page_title="Expense Tracker", layout="centered")
st.title("💰 Expense Tracker (Stack + Streamlit)")

if "stack" not in st.session_state:
    st.session_state.stack = ExpenseStack()

stack = st.session_state.stack

# -----------------------------
# INPUT SECTION
# -----------------------------
st.subheader("➕ Add Expense")

category = st.text_input("Category (e.g. Food, Travel)")
amount = st.number_input("Amount", min_value=0.0, step=1.0)

col1, col2 = st.columns(2)

with col1:
    if st.button("Add Expense"):
        if category == "":
            st.warning("Please enter category")
        else:
            stack.push((category, amount))
            st.success(f"Added: {category} - {amount}")

with col2:
    if st.button("↩️ Undo Last"):
        removed = stack.pop()
        if removed:
            st.info(f"Removed: {removed[0]} - {removed[1]}")
        else:
            st.warning("No expense to undo")

# -----------------------------
# DISPLAY EXPENSES
# -----------------------------
st.subheader("📂 Expenses List")

all_items = stack.get_all()

if all_items:
    for i, item in enumerate(reversed(all_items), 1):
        st.write(f"{i}. {item[0]} - {item[1]}")
else:
    st.write("No expenses added yet.")

# -----------------------------
# TOTAL
# -----------------------------
st.subheader("💰 Total Expense")
total = sum(item[1] for item in all_items)
st.metric("Total", total)

# -----------------------------
# GRAPH
# -----------------------------
st.subheader("📊 Category-wise Graph")

data = defaultdict(float)
for cat, amt in all_items:
    data[cat] += amt

if data:
    fig, ax = plt.subplots()
    ax.bar(data.keys(), data.values())
    ax.set_xlabel("Category")
    ax.set_ylabel("Amount")
    ax.set_title("Expenses Breakdown")
    st.pyplot(fig)
else:
    st.info("No data for graph")
