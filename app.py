import streamlit as st
import mysql.connector
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import time

# ---------------- PAGE CONFIG ---------------- #
st.set_page_config(
    page_title="CASHFLOW — Track Smarter",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ---------------- GLOBAL STYLES ---------------- #
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;700;800;900&family=DM+Mono:ital,wght@0,300;0,400;0,500;1,400&display=swap');

:root {
    --bg: #030712;
    --surface: rgba(255,255,255,0.035);
    --surface2: rgba(255,255,255,0.06);
    --border: rgba(255,255,255,0.08);
    --accent: #00ff9d;
    --accent2: #ff2d78;
    --accent3: #7c3aff;
    --text: #e2e8f0;
    --muted: #64748b;
    --glow: 0 0 40px rgba(0,255,157,0.15);
}

* { box-sizing: border-box; margin: 0; padding: 0; }

html, body, [data-testid="stAppViewContainer"] {
    background: var(--bg) !important;
    background-image:
        radial-gradient(ellipse 80% 50% at 20% -10%, rgba(124,58,255,0.18) 0%, transparent 60%),
        radial-gradient(ellipse 60% 40% at 80% 110%, rgba(0,255,157,0.12) 0%, transparent 60%),
        url("data:image/svg+xml,%3Csvg width='60' height='60' viewBox='0 0 60 60' xmlns='http://www.w3.org/2000/svg'%3E%3Cg fill='none' fill-rule='evenodd'%3E%3Cg fill='%23ffffff' fill-opacity='0.015'%3E%3Cpath d='M36 34v-4h-2v4h-4v2h4v4h2v-4h4v-2h-4zm0-30V0h-2v4h-4v2h4v4h2V6h4V4h-4zM6 34v-4H4v4H0v2h4v4h2v-4h4v-2H6zM6 4V0H4v4H0v2h4v4h2V6h4V4H6z'/%3E%3C/g%3E%3C/g%3E%3C/svg%3E") !important;
    font-family: 'Outfit', sans-serif !important;
    color: var(--text) !important;
}

[data-testid="stHeader"] { display: none !important; }
[data-testid="stSidebar"] { display: none !important; }
[data-testid="stDecoration"] { display: none !important; }
.block-container { padding: 2rem 3rem !important; max-width: 1400px !important; }

/* ---- TYPOGRAPHY ---- */
h1, h2, h3, .stTitle { font-family: 'Outfit', sans-serif !important; }
p, div, span, label { font-family: 'Outfit', sans-serif !important; }

/* ---- TABS ---- */
[data-testid="stTabs"] [role="tablist"] {
    gap: 4px;
    background: var(--surface);
    padding: 6px;
    border-radius: 16px;
    border: 1px solid var(--border);
    backdrop-filter: blur(20px);
    width: fit-content;
}
[data-testid="stTabs"] [role="tab"] {
    font-family: 'Outfit', sans-serif !important;
    font-weight: 700;
    font-size: 0.85rem;
    letter-spacing: 0.05em;
    text-transform: uppercase;
    padding: 10px 28px;
    border-radius: 12px;
    color: var(--muted) !important;
    border: none !important;
    background: transparent !important;
    transition: all 0.3s ease;
}
[data-testid="stTabs"] [role="tab"][aria-selected="true"] {
    color: #030712 !important;
    background: var(--accent) !important;
    box-shadow: 0 0 20px rgba(0,255,157,0.4);
}
[data-testid="stTabs"] [role="tab"]:hover:not([aria-selected="true"]) {
    color: var(--text) !important;
    background: var(--surface2) !important;
}
[data-testid="stTabsContent"] {
    border: none !important;
    padding-top: 2rem !important;
}

/* ---- HIDE PRESS ENTER TOOLTIP ---- */
[data-testid="InputInstructions"],
[data-baseweb="input"] ~ div[style*="position: absolute"],
.st-emotion-cache-1gulkj5,
small.st-emotion-cache-1gulkj5 { display: none !important; }

/* ---- INPUTS ---- */
[data-testid="stTextInput"] input,
[data-testid="stNumberInput"] input,
[data-testid="stDateInput"] input {
    background: var(--surface) !important;
    border: 1px solid var(--border) !important;
    border-radius: 12px !important;
    color: var(--text) !important;
    font-family: 'DM Mono', monospace !important;
    font-size: 0.9rem !important;
    padding: 14px 18px !important;
    transition: all 0.3s ease !important;
}
[data-testid="stTextInput"] input:focus,
[data-testid="stNumberInput"] input:focus,
[data-testid="stDateInput"] input:focus {
    border-color: var(--accent) !important;
    box-shadow: 0 0 0 3px rgba(0,255,157,0.12) !important;
    background: rgba(0,255,157,0.04) !important;
}
[data-testid="stTextInput"] label,
[data-testid="stNumberInput"] label,
[data-testid="stDateInput"] label,
[data-testid="stSelectbox"] label {
    font-family: 'Outfit', sans-serif !important;
    font-weight: 700 !important;
    font-size: 0.72rem !important;
    letter-spacing: 0.1em !important;
    text-transform: uppercase !important;
    color: var(--muted) !important;
    margin-bottom: 6px !important;
}
[data-testid="stSelectbox"] > div > div {
    background: var(--surface) !important;
    border: 1px solid var(--border) !important;
    border-radius: 12px !important;
    color: var(--text) !important;
    font-family: 'DM Mono', monospace !important;
    transition: all 0.3s ease !important;
}
[data-testid="stSelectbox"] > div > div:focus-within {
    border-color: var(--accent) !important;
    box-shadow: 0 0 0 3px rgba(0,255,157,0.12) !important;
}
[data-testid="stSelectbox"] li { color: var(--text) !important; background: #0f172a !important; }

/* ---- BUTTONS ---- */
[data-testid="stButton"] > button {
    background: linear-gradient(135deg, var(--accent) 0%, #00cc7d 100%) !important;
    color: #030712 !important;
    font-family: 'Outfit', sans-serif !important;
    font-weight: 800 !important;
    font-size: 0.82rem !important;
    letter-spacing: 0.08em !important;
    text-transform: uppercase !important;
    border: none !important;
    border-radius: 12px !important;
    padding: 14px 32px !important;
    cursor: pointer !important;
    transition: all 0.3s cubic-bezier(0.34, 1.56, 0.64, 1) !important;
    box-shadow: 0 4px 20px rgba(0,255,157,0.25) !important;
}
[data-testid="stButton"] > button:hover {
    transform: translateY(-2px) scale(1.02) !important;
    box-shadow: 0 8px 30px rgba(0,255,157,0.4) !important;
}
[data-testid="stButton"] > button:active {
    transform: translateY(0) scale(0.98) !important;
}

/* ---- METRICS ---- */
[data-testid="stMetric"] {
    background: var(--surface) !important;
    border: 1px solid var(--border) !important;
    border-radius: 20px !important;
    padding: 24px 28px !important;
    backdrop-filter: blur(20px) !important;
    transition: all 0.3s ease !important;
    position: relative;
    overflow: hidden;
}
[data-testid="stMetric"]:hover {
    border-color: rgba(0,255,157,0.3) !important;
    transform: translateY(-3px) !important;
    box-shadow: 0 12px 40px rgba(0,0,0,0.3) !important;
}
[data-testid="stMetric"] > div:first-child {
    font-family: 'Outfit', sans-serif !important;
    font-size: 0.7rem !important;
    font-weight: 700 !important;
    letter-spacing: 0.12em !important;
    text-transform: uppercase !important;
    color: var(--muted) !important;
}
[data-testid="stMetric"] [data-testid="stMetricValue"] {
    font-family: 'DM Mono', monospace !important;
    font-size: 2rem !important;
    font-weight: 700 !important;
    color: var(--text) !important;
    letter-spacing: -0.02em !important;
}

/* ---- DATAFRAME ---- */
[data-testid="stDataFrame"] {
    border: 1px solid var(--border) !important;
    border-radius: 16px !important;
    overflow: hidden !important;
}
[data-testid="stDataFrame"] * {
    font-family: 'DM Mono', monospace !important;
    font-size: 0.82rem !important;
}

/* ---- ALERTS ---- */
[data-testid="stAlert"] {
    border-radius: 14px !important;
    border: none !important;
    backdrop-filter: blur(20px) !important;
}
.stSuccess {
    background: rgba(0,255,157,0.08) !important;
    border: 1px solid rgba(0,255,157,0.25) !important;
    color: var(--accent) !important;
}
.stError {
    background: rgba(255,45,120,0.08) !important;
    border: 1px solid rgba(255,45,120,0.25) !important;
    color: var(--accent2) !important;
}
.stInfo {
    background: rgba(124,58,255,0.08) !important;
    border: 1px solid rgba(124,58,255,0.25) !important;
}

/* ---- DOWNLOAD BUTTON ---- */
[data-testid="stDownloadButton"] > button {
    background: var(--surface) !important;
    color: var(--text) !important;
    border: 1px solid var(--border) !important;
    box-shadow: none !important;
}
[data-testid="stDownloadButton"] > button:hover {
    border-color: var(--accent) !important;
    color: var(--accent) !important;
    background: rgba(0,255,157,0.06) !important;
    transform: translateY(-2px) !important;
    box-shadow: 0 4px 15px rgba(0,255,157,0.12) !important;
}

/* ---- SCROLLBAR ---- */
::-webkit-scrollbar { width: 4px; height: 4px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb { background: rgba(255,255,255,0.1); border-radius: 2px; }
::-webkit-scrollbar-thumb:hover { background: var(--accent); }

/* ---- DIVIDER ---- */
hr { border-color: var(--border) !important; margin: 2rem 0 !important; }
</style>
""", unsafe_allow_html=True)

# ---- ANIMATED HEADER LOGO ---- #
def render_logo(subtitle=""):
    st.markdown(f"""
    <div style="
        display: flex; align-items: center; gap: 20px; margin-bottom: 2.5rem;
        animation: fadeSlideDown 0.6s cubic-bezier(0.16, 1, 0.3, 1) forwards;
    ">
        <div style="
            width: 52px; height: 52px;
            background: linear-gradient(135deg, #00ff9d, #7c3aff);
            border-radius: 16px;
            display: flex; align-items: center; justify-content: center;
            font-size: 1.4rem;
            box-shadow: 0 0 30px rgba(0,255,157,0.35);
        ">₹</div>
        <div>
            <div style="
                font-family: 'Outfit', sans-serif;
                font-weight: 800;
                font-size: 1.9rem;
                letter-spacing: -0.03em;
                color: #e2e8f0;
                line-height: 1;
            ">CASHFLOW</div>
            <div style="
                font-family: 'DM Mono', monospace;
                font-size: 0.65rem;
                color: #00ff9d;
                letter-spacing: 0.2em;
                text-transform: uppercase;
                margin-top: 3px;
            ">{subtitle if subtitle else "TRACK SMARTER"}</div>
        </div>
    </div>
    <style>
    @keyframes fadeSlideDown {{
        from {{ opacity:0; transform: translateY(-16px); }}
        to   {{ opacity:1; transform: translateY(0); }}
    }}
    </style>
    """, unsafe_allow_html=True)

# ---- SECTION HEADER ---- #
def section_header(icon, title):
    st.markdown(f"""
    <div style="
        display:flex; align-items:center; gap:12px;
        margin: 2rem 0 1.2rem;
        animation: fadeIn 0.5s ease forwards;
    ">
        <span style="font-size:1.2rem;">{icon}</span>
        <span style="
            font-family:'Outfit',sans-serif;
            font-weight:800;
            font-size:1rem;
            letter-spacing:0.06em;
            text-transform:uppercase;
            color:#e2e8f0;
        ">{title}</span>
        <div style="flex:1; height:1px; background:linear-gradient(90deg,rgba(255,255,255,0.1),transparent); margin-left:8px;"></div>
    </div>
    <style>
    @keyframes fadeIn {{ from{{opacity:0;transform:translateX(-10px)}} to{{opacity:1;transform:translateX(0)}} }}
    </style>
    """, unsafe_allow_html=True)

# ---- STAT CARD ---- #
def stat_card(label, value, color, icon):
    st.markdown(f"""
    <div style="
        background: rgba(255,255,255,0.035);
        border: 1px solid rgba(255,255,255,0.08);
        border-radius: 20px;
        padding: 24px 28px;
        backdrop-filter: blur(20px);
        position: relative;
        overflow: hidden;
        transition: all 0.3s ease;
        animation: cardPop 0.5s cubic-bezier(0.34,1.56,0.64,1) forwards;
    " onmouseover="this.style.transform='translateY(-4px)';this.style.borderColor='rgba(0,255,157,0.25)'"
       onmouseout="this.style.transform='translateY(0)';this.style.borderColor='rgba(255,255,255,0.08)'">
        <div style="
            position:absolute; top:-20px; right:-20px;
            width:80px; height:80px;
            background: radial-gradient(circle, {color}22, transparent 70%);
            border-radius:50%;
        "></div>
        <div style="font-size:1.4rem; margin-bottom:10px;">{icon}</div>
        <div style="
            font-family:'DM Mono',monospace;
            font-size:1.7rem;
            font-weight:700;
            color:{color};
            letter-spacing:-0.02em;
            line-height:1;
            margin-bottom:6px;
        ">{value}</div>
        <div style="
            font-family:'Outfit',sans-serif;
            font-size:0.7rem;
            font-weight:700;
            letter-spacing:0.12em;
            text-transform:uppercase;
            color:#64748b;
        ">{label}</div>
    </div>
    <style>
    @keyframes cardPop {{
        from {{ opacity:0; transform:scale(0.92) translateY(12px); }}
        to   {{ opacity:1; transform:scale(1) translateY(0); }}
    }}
    </style>
    """, unsafe_allow_html=True)

# ---------------- DATABASE CONNECTION ---------------- #
import streamlit as st
import mysql.connector
from urllib.parse import urlparse

# Paste your Railway MYSQL_PUBLIC_URL here
DATABASE_URL = "mysql://mysql:kIWAwtknHzaHTOLdKICqmcpLMmBmIzMJ@interchange.proxy.rlwy.net:15297/railway"

url = urlparse(DATABASE_URL)

conn = mysql.connector.connect(
    host="interchange.proxy.rlwy.net",
    user="root",
    password="kIWAwtknHzaHTOLdKICqmcpLMmBmIzMJ",   # paste your real password here
    database="railway",
    port=15297
)


cursor = conn.cursor()

# ---------------- CREATE TABLES SAFELY ---------------- #
cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(255) UNIQUE,
    password VARCHAR(255)
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS expenses (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    date DATE,
    category VARCHAR(100),
    payment VARCHAR(50),
    amount DECIMAL(10,2),
    description TEXT
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS income (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    amount DECIMAL(10,2),
    date DATE
)
""")

conn.commit()

# ---------------- AUTH FUNCTIONS ---------------- #
def register_user(username, password):
    try:
        cursor.execute("INSERT INTO users (username,password) VALUES (%s,%s)", (username, password))
        conn.commit()
        return True
    except:
        return False

def login_user(username, password):
    cursor.execute("SELECT id FROM users WHERE username=%s AND password=%s", (username, password))
    return cursor.fetchone()

# ---------------- SESSION ---------------- #
if "user_id" not in st.session_state:
    st.session_state.user_id = None

# ---------------- LOGIN PAGE ---------------- #
def login_page():
    render_logo("WELCOME BACK")

    col_c, col_mid, col_d = st.columns([1, 1.2, 1])
    with col_mid:
        st.markdown("""
        <div style="
            background: rgba(255,255,255,0.03);
            border: 1px solid rgba(255,255,255,0.07);
            border-radius: 28px;
            padding: 32px 36px 36px;
            backdrop-filter: blur(30px);
            box-shadow: 0 32px 80px rgba(0,0,0,0.4);
            animation: loginPop 0.7s cubic-bezier(0.16,1,0.3,1) forwards;
            margin-bottom: 0;
        ">
        <div style="margin-bottom:24px; text-align:center;">
            <div style="font-family:'Outfit',sans-serif; font-weight:800; font-size:1.5rem; color:#e2e8f0; margin-bottom:6px;">
                Sign in to your vault
            </div>
            <div style="font-family:'DM Mono',monospace; font-size:0.72rem; color:#64748b; letter-spacing:0.08em;">
                YOUR MONEY, YOUR STORY
            </div>
        </div>
        </div>
        <style>
        @keyframes loginPop {{
            from {{ opacity:0; transform: scale(0.92) translateY(30px); }}
            to   {{ opacity:1; transform: scale(1) translateY(0); }}
        }}
        </style>
        """, unsafe_allow_html=True)

        st.markdown("<div style='height:28px'></div>", unsafe_allow_html=True)
        tab1, tab2 = st.tabs(["→ LOGIN", "→ REGISTER"])

        with tab1:
            username = st.text_input("Username", placeholder="enter your username", key="li_user")
            password = st.text_input("Password", type="password", placeholder="••••••••", key="li_pass")
            st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
            if st.button("Login →", width='stretch'):
                user = login_user(username, password)
                if user:
                    st.session_state.user_id = user[0]
                    st.success("✓ Access granted")
                    time.sleep(0.5)
                    st.rerun()
                else:
                    st.error("✗ Invalid credentials")

        with tab2:
            new_user = st.text_input("New Username", placeholder="choose a username", key="reg_user")
            new_pass = st.text_input("New Password", type="password", placeholder="••••••••", key="reg_pass")
            st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
            if st.button("Create Account →", width='stretch'):
                if register_user(new_user, new_pass):
                    st.success("✓ Account created — login now")
                else:
                    st.error("✗ Username already taken")

# ---------------- ADD EXPENSE ---------------- #
def add_expense(user_id):
    section_header("➕", "New Expense")

    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        date = st.date_input("Date", key="exp_date")
    with col2:
        category = st.selectbox("Category", ["Food", "Transport", "Shopping", "Utilities", "Entertainment"], key="exp_cat")
    with col3:
        payment = st.selectbox("Payment Mode", ["Cash", "Card", "UPI"], key="exp_pay")
    with col4:
        amount = st.number_input("Amount (₹)", min_value=0.0, key="exp_amt")
    with col5:
        description = st.text_input("Description", placeholder="optional note", key="exp_desc")

    st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
    if st.button("⚡ Add Expense", key="btn_add_exp"):
        cursor.execute("""
            INSERT INTO expenses (user_id,date,category,payment,amount,description)
            VALUES (%s,%s,%s,%s,%s,%s)
        """, (user_id, date, category, payment, amount, description))
        conn.commit()
        st.success("✓ Expense logged")
        st.rerun()

# ---------------- ADD INCOME ---------------- #
def add_income(user_id):
    section_header("💵", "Log Income")

    col1, col2 = st.columns([1, 3])
    with col1:
        income_amount = st.number_input("Income Amount (₹)", min_value=0.0, key="inc_amt")
    with col2:
        st.markdown("<div style='height:28px'></div>", unsafe_allow_html=True)
        if st.button("💰 Add Income", key="btn_add_inc"):
            cursor.execute("""
                INSERT INTO income (user_id,amount,date) VALUES (%s,%s,%s)
            """, (user_id, income_amount, datetime.today()))
            conn.commit()
            st.success("✓ Income recorded")
            st.rerun()

# ---------------- LOAD DATA ---------------- #
def load_data(user_id):
    cursor.execute("SELECT * FROM expenses WHERE user_id=%s ORDER BY date DESC", (user_id,))
    expenses = pd.DataFrame(cursor.fetchall(), columns=[i[0] for i in cursor.description])

    cursor.execute("SELECT * FROM income WHERE user_id=%s", (user_id,))
    income = pd.DataFrame(cursor.fetchall(), columns=[i[0] for i in cursor.description])

    return expenses, income

# ---------------- DASHBOARD ---------------- #
def dashboard():
    user_id = st.session_state.user_id

    # Top bar
    col_logo, col_spacer, col_logout = st.columns([4, 3, 1])
    with col_logo:
        render_logo("FINANCIAL DASHBOARD")
    with col_logout:
        st.markdown("""
        <style>
        [data-testid="stButton"]:has(button[key="logout_btn"]) > button {
            background: transparent !important;
            color: #64748b !important;
            border: 1px solid rgba(255,255,255,0.1) !important;
            border-radius: 50px !important;
            padding: 10px 22px !important;
            font-size: 0.75rem !important;
            letter-spacing: 0.1em !important;
            box-shadow: none !important;
        }
        [data-testid="stButton"]:has(button[key="logout_btn"]) > button:hover {
            color: #ff2d78 !important;
            border-color: #ff2d78 !important;
            background: rgba(255,45,120,0.06) !important;
            transform: none !important;
            box-shadow: 0 0 16px rgba(255,45,120,0.15) !important;
        }
        </style>
        """, unsafe_allow_html=True)
        st.markdown("<div style='padding-top:22px'></div>", unsafe_allow_html=True)
        if st.button("⏻  LOGOUT", key="logout_btn"):
            st.session_state.user_id = None
            st.rerun()

    # Input forms
    add_expense(user_id)
    add_income(user_id)

    df, income_df = load_data(user_id)

    if df.empty:
        st.markdown("""
        <div style="
            text-align:center; padding:80px 20px;
            background:rgba(255,255,255,0.02);
            border:1px dashed rgba(255,255,255,0.1);
            border-radius:24px; margin-top:2rem;
        ">
            <div style="font-size:3rem; margin-bottom:12px;">📊</div>
            <div style="font-family:'Outfit',sans-serif; font-weight:700; font-size:1rem; color:#64748b; letter-spacing:0.08em; text-transform:uppercase;">
                No expenses yet — start tracking above
            </div>
        </div>
        """, unsafe_allow_html=True)
        return

    df["amount"] = df["amount"].astype(float)
    if not income_df.empty:
        income_df["amount"] = income_df["amount"].astype(float)

    total_expense = df["amount"].sum()
    total_income = income_df["amount"].sum() if not income_df.empty else 0.0
    savings = total_income - total_expense

    # ---- METRICS ---- #
    section_header("📈", "Overview")
    col1, col2, col3 = st.columns(3)
    with col1:
        stat_card("Total Expenses", f"₹{total_expense:,.2f}", "#ff2d78", "🔴")
    with col2:
        stat_card("Total Income", f"₹{total_income:,.2f}", "#00ff9d", "🟢")
    with col3:
        savings_color = "#00ff9d" if savings >= 0 else "#ff2d78"
        savings_icon = "✨" if savings >= 0 else "⚠️"
        stat_card("Net Savings", f"₹{savings:,.2f}", savings_color, savings_icon)

    st.markdown("<div style='height:1.5rem'></div>", unsafe_allow_html=True)

    # ---- CHARTS ---- #
    section_header("🍩", "Spending by Category")
    category_sum = df.groupby("category", as_index=False)["amount"].sum()
    if not category_sum.empty:
        colors = ["#00ff9d", "#7c3aff", "#ff2d78", "#fbbf24", "#38bdf8"]
        fig_pie = go.Figure(go.Pie(
            labels=category_sum["category"],
            values=category_sum["amount"],
            hole=0.55,
            marker=dict(colors=colors, line=dict(color="#030712", width=3)),
            textfont=dict(family="DM Mono", size=11, color="#e2e8f0"),
            hovertemplate="<b>%{label}</b><br>₹%{value:,.2f}<br>%{percent}<extra></extra>"
        ))
        fig_pie.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(family="Outfit", color="#e2e8f0"),
            margin=dict(t=10, b=10, l=10, r=10),
            showlegend=True,
            legend=dict(
                bgcolor="rgba(0,0,0,0)",
                font=dict(family="Outfit", size=13, color="#94a3b8"),
                orientation="h",
                y=-0.08
            ),
            annotations=[dict(
                text=f"₹{total_expense:,.0f}",
                x=0.5, y=0.5, font=dict(family="DM Mono", size=20, color="#e2e8f0"),
                showarrow=False
            )],
            height=420
        )
        st.plotly_chart(fig_pie, width='stretch')

    # ---- TRANSACTIONS TABLE ---- #
    section_header("🧾", "Transaction History")
    st.dataframe(
        df.drop(columns=["id", "user_id"], errors="ignore"),
        width='stretch',
        hide_index=True
    )

    st.markdown("<div style='height:1rem'></div>", unsafe_allow_html=True)
    col_dl, _ = st.columns([1, 4])
    with col_dl:
        st.download_button(
            label="⬇ Download CSV",
            data=df.to_csv(index=False),
            file_name="expenses.csv",
            mime="text/csv"
        )

    # ---- FOOTER ---- #
    st.markdown("""
    <div style="
        margin-top:4rem; padding-top:2rem;
        border-top:1px solid rgba(255,255,255,0.06);
        text-align:center;
        font-family:'DM Mono',monospace;
        font-size:0.68rem;
        letter-spacing:0.12em;
        color:#334155;
        text-transform:uppercase;
    ">
        CASHFLOW — Your financial clarity engine
    </div>
    """, unsafe_allow_html=True)

# ---------------- APP FLOW ---------------- #
if st.session_state.user_id is None:
    login_page()
else:
    dashboard()
