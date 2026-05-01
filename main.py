import streamlit as st
from collections import defaultdict
import matplotlib.pyplot as plt
from datetime import datetime
import pytz


# Stack Class
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

    def clear(self):
        self.stack = []


# Page Config
st.set_page_config(page_title="Expense Tracker", layout="centered")
st.title("Expense Tracker")


# Session State
if "stack" not in st.session_state:
    st.session_state.stack = ExpenseStack()

stack = st.session_state.stack


# Input Section
st.subheader("Add Expense")
category = st.text_input("Category (e.g. Food, Travel)")
amount = st.number_input("Amount", min_value=0.0, step=1.0)


# Buttons
col1, col2, col3 = st.columns(3)

with col1:
    if st.button("Add Expense"):
        if category == "":
            st.warning("Please enter category")
        else:
            # ✅ FIX: Use Pakistan Standard Time (PKT = UTC+5)
            pkt = pytz.timezone("Asia/Karachi")
            date_time = datetime.now(pkt).strftime("%d %b %Y | %I:%M %p")
            stack.push((category, amount, date_time))
            st.success(f"Added: {category} - {amount} on {date_time}")

with col2:
    if st.button("Undo Last"):
        removed = stack.pop()
        if removed:
            st.info(f"Removed: {removed[0]} - {removed[1]}")
        else:
            st.warning("No expense to undo")

with col3:
    if st.button("Reset All"):
        stack.clear()
        st.warning("All expenses cleared!")


# Display Expenses
st.subheader("Expenses List")
all_items = stack.get_all()

if all_items:
    for i, item in enumerate(reversed(all_items), 1):
        st.write(f"{i}. {item[2]} | {item[0]} — Rs. {item[1]}")
else:
    st.write("No expenses added yet.")


# Total Expense
st.subheader("Total Expense")
total = sum(item[1] for item in all_items)
st.metric("Total", f"Rs. {total}")


# Graph
st.subheader("Category-wise Graph")
data = defaultdict(float)

for item in all_items:
    data[item[0]] += item[1]

if data:
    fig, ax = plt.subplots()
    ax.bar(list(data.keys()), list(data.values()))
    ax.set_xlabel("Category")
    ax.set_ylabel("Amount")
    ax.set_title("Expenses Breakdown")
    st.pyplot(fig)
else:
    st.info("No data for graph")
