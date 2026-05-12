import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from streamlit_tradingview_widget import streamlit_tradingview_widget

# --- Page Setup ---
st.set_page_config(page_title="KD AI ULTIMATE TERMINAL", layout="wide", initial_sidebar_state="collapsed")

# Custom Professional CSS
st.markdown("""
    <style>
    .main { background-color: #0b0e11; }
    .metric-container { background-color: #161b22; border: 1px solid #30363d; padding: 15px; border-radius: 10px; text-align: center; }
    .profit-text { color: #00ff00; font-size: 20px; font-weight: bold; }
    .loss-text { color: #ff4b4b; font-size: 20px; font-weight: bold; }
    .position-box { border-left: 5px solid #f0b90b; background-color: #1e2329; padding: 15px; border-radius: 8px; margin-top: 10px; }
    .sidebar-story { background: linear-gradient(135deg, #1e2329 0%, #0b0e11 100%); padding: 15px; border-radius: 10px; border: 1px solid #f0b90b; }
    </style>
    """, unsafe_allow_html=True)

# --- Top Bar: Real-time Wallet & Profit ---
st.markdown("### 🖥️ Trading Desktop Home")
col_w1, col_w2, col_w3, col_w4, col_w5 = st.columns(5)

with col_w1:
    st.markdown('<div class="metric-container"><caption>Wallet Balance</caption><h2 style="color:#f0b90b;">$25,430.50</h2></div>', unsafe_allow_html=True)
with col_w2:
    st.markdown('<div class="metric-container"><caption>Target Profit (TP)</caption><h2 style="color:#00ff00;">$65,200.00</h2></div>', unsafe_allow_html=True)
with col_w3:
    st.markdown('<div class="metric-container"><caption>Stop Loss (SL)</caption><h2 style="color:#ff4b4b;">$62,100.00</h2></div>', unsafe_allow_html=True)
with col_w4:
    st.markdown('<div class="metric-container"><caption>Gross Profit</caption><h2>+$850.25</h2></div>', unsafe_allow_html=True)
with col_w5:
    st.markdown('<div class="metric-container"><caption>Net Profit</caption><h2 style="color:#00d1ff;">+$720.40</h2></div>', unsafe_allow_html=True)

st.write("---")

# --- Main Interface Layout ---
left_panel, mid_panel, right_panel = st.columns([1, 2.5, 1.2])

# 1. Left Panel: Account & Stories
with left_panel:
    st.subheader("🚀 Success Stories")
    st.markdown("""
    <div class="sidebar-story">
        <small>Latest Win:</small><br>
        <b>BTC/USDT +15%</b><br>
        <small>Strategy: Sniper Logic</small>
    </div><br>
    <div class="sidebar-story">
        <small>Monthly ROI:</small><br>
        <b style="color:#00ff00;">+42.5% Profit</b>
    </div>
    """, unsafe_allow_html=True)
    
    st.divider()
    st.subheader("🔑 Access Keys")
    st.text_input("Binance API Key", type="password")
    st.radio("Mode", ["Live Account", "Demo Account"])

# 2. Mid Panel: Live TradingView Analysis
with mid_panel:
    st.subheader("📊 Live Market Analysis")
    # සැබෑ TradingView Chart එකක් ඇතුළත් කිරීම
    streamlit_tradingview_widget(
        symbol="BINANCE:BTCUSDT",
        datasetName="BTC Price",
        elemId="tradingview_btc",
        height=500,
        width="100%"
    )

# 3. Right Panel: Active Position Tracker (Binance Style)
with right_panel:
    st.subheader("⚡ Active Positions")
    
    # Position UI
    st.markdown("""
    <div class="position-box">
        <span style="background-color:#00ff00; color:black; padding:2px 5px; border-radius:3px; font-weight:bold;">LONG</span> 
        <b>BTC/USDT 20x</b><br>
        <small>Size: 0.52 BTC</small><br>
        <hr style="margin:10px 0;">
        <div style="display:flex; justify-content:space-between;">
            <span>Entry: 63,400.0</span>
            <span>Mark: 64,150.2</span>
        </div>
        <div style="margin-top:10px;">
            <span style="color:#00ff00; font-size:22px; font-weight:bold;">Unrealized PNL: +$390.12 (12.4%)</span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.write("")
    if st.button("🔴 EMERGENCY CLOSE POSITION", use_container_width=True):
        st.error("Closing all Binance orders...")

    st.divider()
    st.subheader("🤖 Bot Control")
    st.checkbox("Run Sniper Logic Engine", value=True)
    st.checkbox("Auto-Trail Take Profit", value=True)
    
    c1, c2 = st.columns(2)
    if c1.button("🟢 ON", use_container_width=True):
        st.success("BOT ACTIVE")
    if c2.button("🔴 OFF", use_container_width=True):
        st.warning("BOT IDLE")

# --- Bottom Bar: Order Logs ---
st.write("---")
st.subheader("📜 Live Order Logs")
log_data = pd.DataFrame({
    "Time": ["12:45:01", "12:48:22", "12:55:10"],
    "Action": ["Limit Buy BTC", "Signal Detected", "Take Profit Updated"],
    "Status": ["Filled", "Sniper Active", "Success"]
})
st.table(log_data)

st.caption("KD AI ULTIMATE TERMINAL | v5.0 Pro | Binance API Integrated")
