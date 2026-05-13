import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from datetime import datetime
import time
import qrcode
from io import BytesIO

# --- 1. SETUP & THEME (Cyber-Dark Professional) ---
st.set_page_config(
    page_title="KD AI QUANTUM TERMINAL",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for the "Elite" Look
st.markdown("""
    <style>
    .stApp { background-color: #050508; color: #ffffff; }
    [data-testid="stSidebar"] { background-color: #0b0e14; border-right: 1px solid #1f2633; }
    
    /* Neon Glow Metric Cards */
    .metric-container {
        background: linear-gradient(145deg, #0f111a, #07080c);
        border: 1px solid #1a1e2e;
        border-radius: 15px;
        padding: 25px;
        text-align: center;
        box-shadow: 0 0 15px rgba(0, 209, 255, 0.1);
    }
    .label { color: #888; font-size: 14px; text-transform: uppercase; letter-spacing: 1px; }
    .value-blue { color: #00d1ff; font-size: 32px; font-weight: bold; text-shadow: 0 0 10px rgba(0,209,255,0.4); }
    .value-green { color: #00ffa3; font-size: 32px; font-weight: bold; text-shadow: 0 0 10px rgba(0,255,163,0.4); }
    
    /* AI Bot Chat Box */
    .bot-chat {
        background: #0f111a;
        border-left: 4px solid #00d1ff;
        padding: 15px;
        border-radius: 5px;
        margin: 10px 0;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 2. SESSION STATE MANAGEMENT ---
if 'balance' not in st.session_state: st.session_state.balance = 30.00
if 'is_running' not in st.session_state: st.session_state.is_running = False
if 'trade_history' not in st.session_state: st.session_state.trade_history = [30.00]
if 'logs' not in st.session_state: st.session_state.logs = []
if 'total_trades' not in st.session_state: st.session_state.total_trades = 0

# --- 3. SIDEBAR (Control & QR) ---
with st.sidebar:
    st.image("https://cryptologos.cc/logos/binance-coin-bnb-logo.png", width=70)
    st.title("KD AI v9.5")
    st.markdown("User: **KALANA** | Status: <span style='color:#00ffa3;'>VIP ELITE</span>", unsafe_allow_html=True)
    st.divider()

    # System Controls
    if st.button("🚀 INITIATE START", type="primary", use_container_width=True):
        st.session_state.is_running = True
        st.session_state.logs.append(f"[{datetime.now().strftime('%H:%M')}] System Online. Scanning...")
    
    if st.button("🔴 EMERGENCY KILL", use_container_width=True):
        st.session_state.is_running = False
        st.warning("All Trades Halted.")

    st.divider()
    
    # QR Code for Mobile Link (As discussed in call)
    st.subheader("📱 Mobile Sync")
    qr_url = "https://your-app-name.streamlit.app" # GitHub එකට දැම්මම ලැබෙන link එක මෙතනට දාන්න
    qr = qrcode.make(qr_url)
    buf = BytesIO()
    qr.save(buf)
    st.image(buf.getvalue(), caption="Scan to Link iPad/Mobile", width=180)

# --- 4. MAIN DASHBOARD ---
st.markdown("<h1 style='text-align: center;'>⚡ KD AI QUANTUM DECENTRALIZED TERMINAL</h1>", unsafe_allow_html=True)

# Top Metrics Row
m1, m2, m3, m4 = st.columns(4)
with m1:
    st.markdown(f'<div class="metric-container"><div class="label">Total Equity</div><div class="value-blue">${st.session_state.balance:.2f}</div></div>', unsafe_allow_html=True)
with m2:
    profit = st.session_state.balance - 30.00
    st.markdown(f'<div class="metric-container"><div class="label">Net Realized</div><div class="value-green">+${profit:.2f}</div></div>', unsafe_allow_html=True)
with m3:
    st.markdown(f'<div class="metric-container"><div class="label">Total Trades</div><div style="font-size:32px;">{st.session_state.total_trades}</div></div>', unsafe_allow_html=True)
with m4:
    status_icon = "🟢 ACTIVE" if st.session_state.is_running else "⚪ IDLE"
    st.markdown(f'<div class="metric-container"><div class="label">Signal Engine</div><div style="font-size:24px;">{status_icon}</div></div>', unsafe_allow_html=True)

st.divider()

# --- 5. ANALYTICS & LIVE AI BOT ---
left, right = st.columns([2, 1])

with left:
    st.subheader("📈 Real-Time Profit Trajectory")
    fig = go.Figure(data=go.Scatter(y=st.session_state.trade_history, mode='lines+markers', 
                                   line=dict(color='#00d1ff', width=3), fill='tozeroy'))
    fig.update_layout(template="plotly_dark", height=400, margin=dict(l=0,r=0,t=0,b=0),
                      paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
    st.plotly_chart(fig, use_container_width=True)

with right:
    st.subheader("🤖 KD AI Assistant")
    st.markdown('<div class="bot-chat">', unsafe_allow_html=True)
    if st.session_state.is_running:
        st.write("**Bot:** I am scanning 300+ pairs. Volatility is high in BTC/USDT. Executing machine-gun scalp strategy with 3% margin.")
    else:
        st.write("**Bot:** Waiting for initiation. Please check your Binance API connection in settings.")
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.text_input("Send Command to Bot", placeholder="e.g. Analysis of SOL/USDT")
    st.button("Send Command")

# --- 6. SCALPING ENGINE (LOGIC) ---
if st.session_state.is_running:
    # Simulating the high-speed logic we discussed
    time.sleep(2)
    win_amount = round(np.random.uniform(0.10, 0.50), 2)
    st.session_state.balance += win_amount
    st.session_state.total_trades += 1
    st.session_state.trade_history.append(st.session_state.balance)
    
    log_entry = f"[{datetime.now().strftime('%H:%M:%S')}] Trade Success: +${win_amount} (99.9% Prob Match)"
    st.session_state.logs.insert(0, log_entry)
    
    # Auto-refreshing the dashboard
    st.rerun()

# --- 7. LOGS & DATA ---
st.divider()
c1, c2 = st.columns([1, 1])

with c1:
    st.subheader("📄 Intelligence Logs")
    st.code("\n".join(st.session_state.logs[:8]))

with c2:
    st.subheader("🔍 Active Market Scanner")
    pairs = ["BTC/USDT", "SOL/USDT", "DOGE/USDT", "ETH/USDT"]
    scanner_df = pd.DataFrame({
        "Pair": pairs,
        "Signal": ["STRONG BUY", "SCALPING", "ENTRY DETECTED", "WAIT"],
        "SMC Score": ["98.2%", "94.5%", "91.0%", "45.0%"]
    })
    st.dataframe(scanner_df, use_container_width=True)

st.caption("KD AI QUANTUM | OFFICIAL PRO EDITION | 2026")
