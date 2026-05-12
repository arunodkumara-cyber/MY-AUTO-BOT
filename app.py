import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from datetime import datetime
import time

# --- Page Config ---
st.set_page_config(page_title="KD AI MACHINE-GUN TERMINAL", layout="wide", initial_sidebar_state="collapsed")

# Custom CSS for Pro Dark UI
st.markdown("""
    <style>
    .main { background-color: #080a0d; color: #e1e1e1; }
    .stMetric { background-color: #11151c; padding: 20px; border-radius: 10px; border: 1px solid #1f2633; }
    .status-active { color: #00ff00; font-weight: bold; animation: blinker 1.5s linear infinite; }
    @keyframes blinker { 50% { opacity: 0; } }
    .trade-card { background-color: #161b22; padding: 15px; border-radius: 10px; border-left: 5px solid #00d1ff; margin-bottom: 10px; }
    </style>
    """, unsafe_allow_html=True)

# --- Session State for Continuous Logic ---
if 'balance' not in st.session_state: st.session_state.balance = 30.00
if 'profit_history' not in st.session_state: st.session_state.profit_history = [30.00]
if 'bot_running' not in st.session_state: st.session_state.bot_running = False

# --- Sidebar Controls ---
with st.sidebar:
    st.header("🤖 KD AI CONTROL")
    mode = st.toggle("Live Execution Mode", value=False)
    st.divider()
    st.write("Strategy: **Machine-Gun Scalper v6**")
    st.write("Target: **All Binance USDT Pairs**")
    st.divider()
    if st.button("RESET DEMO BALANCE"):
        st.session_state.balance = 30.00
        st.session_state.profit_history = [30.00]

# --- Header Section ---
c1, c2 = st.columns([3, 1])
with c1:
    st.title("🔫 KD AI AUTO-BOT: MACHINE-GUN MODE")
with c2:
    status_label = '<span class="status-active">● SCANNING MARKET...</span>' if st.session_state.bot_running else '<span style="color:red;">● SYSTEM IDLE</span>'
    st.markdown(f"<h3>{status_label}</h3>", unsafe_allow_html=True)

# --- Top Row: Dynamic Metrics ---
m1, m2, m3, m4 = st.columns(4)
current_profit = st.session_state.balance - 30.00
m1.metric("Current Wallet", f"${st.session_state.balance:.2f}", f"{((current_profit/30)*100):.2f}%")
m2.metric("Net Profit (Today)", f"${current_profit:.2f}", "Auto-Compounding")
m3.metric("Active Scans", "342 Pairs", "Binance Global")
m4.metric("Risk Level", "Low (1-3% Margin)", "Safe Mode")

st.divider()

# --- Main Dashboard Layout ---
left_col, right_col = st.columns([2, 1])

with left_col:
    # 1. Profit Line Chart (ප්‍රොෆිට් එක උඩ පහළ යන රේඛාව)
    st.subheader("📈 Profit Growth Curve (Real-time)")
    fig = go.Figure()
    fig.add_trace(go.Scatter(y=st.session_state.profit_history, mode='lines+markers', 
                             line=dict(color='#00d1ff', width=3),
                             fill='tozeroy', fillcolor='rgba(0, 209, 255, 0.1)'))
    fig.update_layout(template="plotly_dark", height=350, margin=dict(l=0,r=0,t=0,b=0),
                      xaxis_title="Trade Count", yaxis_title="Balance ($)")
    st.plotly_chart(fig, use_container_width=True)

    # 2. Market Scanner Simulation
    st.subheader("🔍 Real-time Multi-Coin Scanner")
    scan_data = pd.DataFrame({
        "Coin": ["BTC/USDT", "ETH/USDT", "SOL/USDT", "XRP/USDT", "ADA/USDT"],
        "Signal": ["STRONG BUY", "NEUTRAL", "STRONG BUY", "SCALPING", "BUY"],
        "Sniper Logic": ["98%", "45%", "92%", "88%", "76%"],
        "Status": ["Executing...", "Waiting", "Executing...", "Analyzing", "Analyzing"]
    })
    st.table(scan_data)

with right_col:
    # 3. Control Center
    st.subheader("🎮 Bot Execution")
    col_btn1, col_btn2 = st.columns(2)
    
    if col_btn1.button("🚀 START AUTO-TRADING", use_container_width=True):
        st.session_state.bot_active = True
        st.session_state.bot_running = True
    
    if col_btn2.button("🛑 STOP & SECURE", use_container_width=True):
        st.session_state.bot_active = False
        st.session_state.bot_running = False

    # 4. Live Position Visual (Binance Style)
    st.subheader("⚡ Live Positions")
    if st.session_state.bot_running:
        # Simulate Balance Growth for Demo
        time.sleep(0.1) # Smoothness
        if np.random.rand() > 0.7: # Simulate a winning trade
            st.session_state.balance += np.random.uniform(0.10, 0.50)
            st.session_state.profit_history.append(st.session_state.balance)

        st.markdown(f"""
        <div class="trade-card">
            <b style="color:#00ff00;">LONG: SOL/USDT 20x</b><br>
            <small>Entry: 145.20 | Mark: 146.85</small><br>
            <b style="font-size:18px; color:#00ff00;">PNL: +${np.random.uniform(0.5, 2.0):.2f} (Active)</b>
        </div>
        <div class="trade-card">
            <b style="color:#00ff00;">LONG: BTC/USDT 10x</b><br>
            <small>Entry: 64,100 | Mark: 64,320</small><br>
            <b style="font-size:18px; color:#00ff00;">PNL: +${np.random.uniform(1.0, 3.5):.2f} (Active)</b>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.info("Bot is Offline. Start the engine to analyze coins.")

# --- Footer System Logs ---
st.divider()
st.subheader("🛠 System Intelligence Logs")
logs = [
    f"[{datetime.now().strftime('%H:%M:%S')}] - Scanning 300+ pairs on Binance...",
    f"[{datetime.now().strftime('%H:%M:%S')}] - Sniper Logic v6: Potential entry found on SOL/USDT",
    f"[{datetime.now().strftime('%H:%M:%S')}] - Risk Check: 3% Margin allocated. Balance secured."
]
for log in logs:
    st.text(log)

st.caption("KD AI AUTO BOT PRO | Version 2026.05 | High-Frequency Machine-Gun Mode")
