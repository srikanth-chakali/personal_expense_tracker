import streamlit as st
import sqlite3
import pandas as pd
import plotly.express as px
import hashlib
from datetime import datetime

# -------------------- PAGE CONFIG --------------------
st.set_page_config(page_title="Expense Tracker SaaS", layout="wide")

# -------------------- DATABASE --------------------
conn = sqlite3.connect("saas_expenses.db", check_same_thread=False)
cursor = conn.cursor()

# Create Tables
cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE,
    password TEXT
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS expenses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    date TEXT,
    category TEXT,
    payment TEXT,
    amount REAL,
    description TEXT
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS income (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    amount REAL,
    date TEXT
)
""")

conn.commit()

# -------------------- AUTH FUNCTIONS --------------------
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def register_user(username, password):
    try:
        cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)",
                       (username, hash_password(password)))
        conn.commit()
        return True
    except:
        return False

def login_user(username, password):
    cursor.execute("SELECT id FROM users WHERE username=? AND password=?",
                   (username, hash_password(password)))
    return cursor.fetchone()

# -------------------- SESSION --------------------
if "user_id" not in st.session_state:
    st.session_state.user_id = None

# -------------------- LOGIN / REGISTER --------------------
if st.session_state.user_id is None:
    st.title("🔐 Expense Tracker SaaS")

    tab1, tab2 = st.tabs(["Login", "Register"])

    with tab1:
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        if st.button("Login"):
            user = login_user(username, password)
            if user:
                st.session_state.user_id = user[0]
                st.success("Login Successful")
                st.rerun()
            else:
                st.error("Invalid Credentials")

    with tab2:
        new_user = st.text_input("New Username")
        new_pass = st.text_input("New Password", type="password")
        if st.button("Register"):
            if register_user(new_user, new_pass):
                st.success("User Registered Successfully")
            else:
                st.error("Username already exists")

else:
    # -------------------- DASHBOARD --------------------
    st.title("💰 SaaS Expense Dashboard")

    if st.button("Logout"):
        st.session_state.user_id = None
        st.rerun()

    user_id = st.session_state.user_id

    # -------------------- ADD EXPENSE --------------------
    st.subheader("➕ Add Expense")

    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        date = st.date_input("Date")

    with col2:
        category = st.selectbox("Category",
                                ["Food", "Transport", "Shopping", "Utilities", "Entertainment"])

    with col3:
        payment = st.selectbox("Payment Mode",
                               ["Cash", "Card", "UPI"])

    with col4:
        amount = st.number_input("Amount", min_value=0.0)

    with col5:
        description = st.text_input("Description")

    if st.button("Add Expense"):
        cursor.execute("""
        INSERT INTO expenses (user_id, date, category, payment, amount, description)
        VALUES (?, ?, ?, ?, ?, ?)
        """, (user_id, date, category, payment, amount, description))
        conn.commit()
        st.success("Expense Added")
        st.rerun()

    # -------------------- ADD INCOME --------------------
    st.subheader("💵 Add Income")
    income_amount = st.number_input("Income Amount", min_value=0.0, key="income")
    if st.button("Add Income"):
        cursor.execute("""
        INSERT INTO income (user_id, amount, date)
        VALUES (?, ?, ?)
        """, (user_id, income_amount, date))
        conn.commit()
        st.success("Income Added")
        st.rerun()

    # -------------------- LOAD DATA --------------------
    df = pd.read_sql_query("SELECT * FROM expenses WHERE user_id=? ORDER BY date DESC",
                           conn, params=(user_id,))

    income_df = pd.read_sql_query("SELECT * FROM income WHERE user_id=?",
                                  conn, params=(user_id,))

    if not df.empty:
        df["amount"] = pd.to_numeric(df["amount"])

        total_expense = df["amount"].sum()
        total_income = income_df["amount"].sum() if not income_df.empty else 0
        savings = total_income - total_expense

        # -------------------- METRICS --------------------
        colA, colB, colC = st.columns(3)
        colA.metric("Total Expense", f"₹ {total_expense:.2f}")
        colB.metric("Total Income", f"₹ {total_income:.2f}")
        colC.metric("Savings", f"₹ {savings:.2f}")

        # -------------------- DONUT CHART --------------------
        st.subheader("📊 Expense by Category")
        category_sum = df.groupby("category")["amount"].sum().reset_index()

        fig = px.pie(
            category_sum,
            names="category",
            values="amount",
            hole=0.4
        )
        st.plotly_chart(fig, use_container_width=True)

        # -------------------- MONTHLY TREND --------------------
        st.subheader("📈 Monthly Trend")
        df["date"] = pd.to_datetime(df["date"])
        monthly = df.groupby(df["date"].dt.to_period("M"))["amount"].sum().reset_index()
        monthly["date"] = monthly["date"].astype(str)

        fig2 = px.line(monthly, x="date", y="amount")
        st.plotly_chart(fig2, use_container_width=True)

        # -------------------- TABLE --------------------
        st.subheader("🧾 Transactions")
        st.dataframe(df, use_container_width=True)

        # -------------------- CSV EXPORT --------------------
        st.download_button(
            label="Download CSV",
            data=df.to_csv(index=False),
            file_name="expenses.csv",
            mime="text/csv"
        )

    else:
        st.info("No expenses yet. Add one above 👆")