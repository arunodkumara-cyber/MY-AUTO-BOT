import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import pandas_ta as ta
import time

# --- Page Configuration & Design ---
st.set_page_config(page_title="KD AI AUTO BOT", layout="wide", initial_sidebar_state="expanded")

# Custom CSS for Dark UI
st.markdown("""
    <style>
    .main { background-color: #0b0e14; color: white; }
    div[data-testid="stMetricValue"] { color: #00d1ff !important; font-size: 26px; font-weight: bold; }
    .stButton>button { width: 100%; border-radius: 8px; height: 3.5em; font-weight: bold; transition: 0.3s; }
    .card { background-color: #161b22; padding: 25px; border-radius: 12px; border: 1px solid #30363d; margin-bottom: 15px; }
    </style>
    """, unsafe_allow_html=True)

# --- Background Brain ---
def process_trading_logic():
    return "Analyzing market with Sniper Logic v3.0..."

# --- Sidebar ---
with st.sidebar:
    st.image("https://img.icons8.com/fluency/96/artificial-intelligence.png", width=80)
    st.title("KD AI AUTO BOT")
    st.write("---")
    app_mode = st.radio("Select Trading Mode:", ["📈 Demo Account", "💰 Live Account"])
    st.write("---")
    st.subheader("Risk Configuration")
    balance_limit = st.slider("Max Capital Usage (%)", 1, 100, 20)
    st.checkbox("Enable Auto Stop-Loss", value=True)
    st.checkbox("Enable Sniper Logic", value=True)

# --- Main Dashboard ---
st.markdown(f"### {app_mode} Dashboard")

# Top Row Metrics
col_m1, col_m2, col_m3, col_m4 = st.columns(4)
with col_m1:
    st.metric("Net Equity", "$15,240.50", "+2.5%")
with col_m2:
    st.metric("Today's Profit", "$420.12", "12%")
with col_m3:
    st.metric("Success Rate", "85%", "Stable")
with col_m4:
    st.metric("Active Pairs", "BTC/USDT", "Sniper Mode")

st.write("---")

# --- Bot Control Center (Fixed the NameError here) ---
if 'bot_active' not in st.session_state:
    st.session_state.bot_active = False

# Creating columns for layout
c1, c2, c3, c4 = st.columns([1, 1, 1, 1])

with c2: # This is the START button
    if st.button("🚀 START BOT"):
        st.session_state.bot_active = True
        st.toast("KD AI Bot Started!", icon="✅")

with c3: # This is the STOP button
    if st.button("🛑 STOP BOT"):
        st.session_state.bot_active = False
        st.toast("KD AI Bot Stopped.", icon="⚠️")

# Status Message
if st.session_state.bot_active:
    st.markdown('<p style="color:#00ff00; text-align:center; font-weight:bold;">● BOT STATUS: ACTIVE</p>', unsafe_allow_html=True)
else:
    st.markdown('<p style="color:#ff4b4b; text-align:center; font-weight:bold;">● BOT STATUS: OFFLINE</p>', unsafe_allow_html=True)

# --- Analytics Section ---
left_col, right_col = st.columns([2, 1])

with left_col:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("Live Market Analytics")
    chart_data = pd.DataFrame(np.random.randn(25, 2), columns=['Trend A', 'Trend B'])
    st.line_chart(chart_data, height=320)
    st.markdown('</div>', unsafe_allow_html=True)

with right_col:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("Intelligence Output")
    if st.session_state.bot_active:
        st.write("🔥 **System: Running**")
        st.info(process_trading_logic())
        st.progress(85)
    else:
        st.write("❄️ **System: Idle**")
    st.markdown('</div>', unsafe_allow_html=True)

st.caption("KD AI AUTO BOT | Professional Interface | Version 2026.05")
