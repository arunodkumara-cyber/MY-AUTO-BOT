import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime
try:
    from streamlit_tradingview_widget import streamlit_tradingview_widget
except ImportError:
    st.error("Please add 'streamlit-tradingview-widget' to your requirements.txt file.")

# --- Page Setup ---
st.set_page_config(page_title="KD AI ULTIMATE TERMINAL", layout="wide", initial_sidebar_state="collapsed")

# Custom Professional CSS (Dark Theme)
st.markdown("""
    <style>
    .main { background-color: #0b0e11; }
    .metric-container { background-color: #161b22; border: 1px solid #30363d; padding: 15px; border-radius: 10px; text-align: center; }
    .position-box { border-left: 5px solid #f0b90b; background-color: #1e2329; padding: 15px; border-radius: 8px; margin-top: 10px; }
    .sidebar-story { background: linear-gradient(135deg, #1e2329 0%, #0b0e11 100%); padding: 12px; border-radius: 8px; border: 1px solid #f0b90b; margin-bottom: 10px;}
    </style>
    """, unsafe_allow_html=True)

# --- Logic for Demo & Live Modes ---
if 'bot_active' not in st.session_state: st.session_state.bot_active = False

# Sidebar for Mode Selection
with st.sidebar:
    st.title("KD AI PRO")
    app_mode = st.radio("Select Mode:", ["📈 Demo Trading", "💰 Live Trading"])
    st.divider()
    if app_mode == "💰 Live Trading":
        st.warning("Connect API Keys to enable Live mode.")
        st.text_input("Binance API Key", type="password")
        st.text_input("Binance Secret Key", type="password")
    else:
        st.success("Demo Mode Active: $30 Balance Loaded")

# --- Financial Metrics Logic ---
# Demo mode එකේදී ඩොලර් 30 කින් පටන් ගන්නා ලෙස සකසා ඇත
wallet_bal = 30.00 if app_mode == "📈 Demo Trading" else 0.00
net_profit = 2.45 if st.session_state.bot_active else 0.00
total_bal = wallet_bal + net_profit

# --- Top Bar: Wallet Display ---
st.markdown(f"### 🖥️ KD AI Desktop - {app_mode}")
m1, m2, m3, m4, m5 = st.columns(5)

with m1:
    st.markdown(f'<div class="metric-container"><caption>Wallet Balance</caption><h2 style="color:#f0b90b;">${wallet_bal:.2f}</h2></div>', unsafe_allow_html=True)
with m2:
    st.markdown('<div class="metric-container"><caption>Net Profit</caption><h2 style="color:#00ff00;">+$' + str(net_profit) + '</h2></div>', unsafe_allow_html=True)
with m3:
    st.markdown(f'<div class="metric-container"><caption>Total Equity</caption><h2 style="color:#00d1ff;">${total_bal:.2f}</h2></div>', unsafe_allow_html=True)
with m4:
    st.markdown('<div class="metric-container"><caption>Take Profit (TP)</caption><h2 style="color:#00ff00;">$0.85</h2></div>', unsafe_allow_html=True)
with m5:
    st.markdown('<div class="metric-container"><caption>Stop Loss (SL)</caption><h2 style="color:#ff4b4b;">$0.30</h2></div>', unsafe_allow_html=True)

st.write("---")

# --- Main Layout ---
left_col, mid_col, right_col = st.columns([1, 2.5, 1.2])

# 1. Left: Stories & Stats
with left_col:
    st.subheader("🚀 Stories")
    st.markdown('<div class="sidebar-story"><b>Win: SOL/USDT</b><br><small>Profit: +$4.20</small></div>', unsafe_allow_html=True)
    st.markdown('<div class="sidebar-story"><b>Win: BTC/USDT</b><br><small>Profit: +$12.50</small></div>', unsafe_allow_html=True)
    st.divider()
    st.write("Daily Target: 15%")
    st.progress(65)

# 2. Mid: Real Analysis (TradingView)
with mid_col:
    st.subheader("📊 Live Market Analysis")
    try:
        streamlit_tradingview_widget(symbol="BINANCE:BTCUSDT", height=450, width="100%")
    except:
        st.info("Chart will load once library is installed.")

# 3. Right: Binance Position Tracker
with right_col:
    st.subheader("⚡ Active Trade")
    if st.session_state.bot_active:
        st.markdown("""
        <div class="position-box">
            <span style="background-color:#00ff00; color:black; padding:2px 6px; border-radius:3px; font-weight:bold; font-size:12px;">LONG</span> 
            <b>BTC/USDT 10x</b><br>
            <small>Isolated Margin</small>
            <hr style="margin:8px 0; border-top: 1px solid #30363d;">
            <div style="display:flex; justify-content:space-between; font-size:13px;">
                <span>Size: 15.0 USDT</span>
                <span style="color:#00ff00;">PNL: +$2.45</span>
            </div>
            <div style="margin-top:10px; text-align:center;">
                <small>Entry: 63,500 | Mark: 64,210</small>
            </div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("❌ Close Trade", use_container_width=True):
             st.session_state.bot_active = False
    else:
        st.info("No Active Trades. Press ON to start Demo.")

    st.divider()
    st.subheader("🤖 Control")
    c1, c2 = st.columns(2)
    if c1.button("🟢 ON", use_container_width=True):
        st.session_state.bot_active = True
    if c2.button("🔴 OFF", use_container_width=True):
        st.session_state.bot_active = False

# --- Bottom Bar ---
st.write("---")
st.subheader("📜 System Logs")
st.code(f"[{datetime.now().strftime('%H:%M:%S')}] - System Initialized in {app_mode}\n[{datetime.now().strftime('%H:%M:%S')}] - Searching for Sniper Entry...")

st.caption("KD AI AUTO BOT v5.1 | Developed for Professional Traders")
