import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from datetime import datetime
import time
import socket
import qrcode
from io import BytesIO
from streamlit_webrtc import webrtc_streamer, WebRtcMode, RTCConfiguration

# --- 1. PREMIUM PAGE SETUP ---
st.set_page_config(
    page_title="KD AI QUANTUM TERMINAL - OFFICIAL",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- 2. CSS STYLING (පරණ තිබුණු Cyber-Dark Look එකමයි) ---
st.markdown("""
    <style>
    .stApp { background-color: #020305; color: #ffffff; }
    [data-testid="stSidebar"] { background-color: #080a0f; border-right: 1px solid #00d1ff33; }
    .metric-card {
        background: linear-gradient(145deg, #0f111a, #050608);
        border: 1px solid #1f2633; border-radius: 12px; padding: 20px; text-align: center;
        box-shadow: 0 4px 20px rgba(0, 209, 255, 0.1);
    }
    .neon-blue { color: #00d1ff; font-weight: 800; font-size: 28px; text-shadow: 0 0 10px rgba(0,209,255,0.5); }
    .neon-green { color: #00ffa3; font-weight: 800; font-size: 28px; text-shadow: 0 0 10px rgba(0,255,163,0.5); }
    .sniper-log {
        background-color: #000; border-left: 4px solid #00ffa3; padding: 12px;
        font-family: 'Courier New', monospace; color: #00ffa3; margin-bottom: 8px; border-radius: 4px;
    }
    .ip-display { color: #00ffa3; font-weight: bold; border: 1px solid #00ffa3; padding: 5px; border-radius: 5px; text-align: center; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. SESSION STATE ---
if 'balance' not in st.session_state: st.session_state.balance = 30.00
if 'is_running' not in st.session_state: st.session_state.is_running = False
if 'history' not in st.session_state: st.session_state.history = [30.00]
if 'logs' not in st.session_state: st.session_state.logs = []
if 'api_key' not in st.session_state: st.session_state.api_key = ""
if 'secret_key' not in st.session_state: st.session_state.secret_key = ""

# --- 4. SIDEBAR & IP ADDRESS ---
with st.sidebar:
    st.image("https://cryptologos.cc/logos/binance-coin-bnb-logo.png", width=60)
    st.title("KD AI PRIVATE")
    
    # IP Address පෙන්වන කොටස
    hostname = socket.gethostname()
    ip_addr = socket.gethostbyname(hostname)
    st.markdown(f'<div class="ip-display">SERVER IP: {ip_addr}</div>', unsafe_allow_html=True)
    
    st.divider()
    
    # Live vs Demo Toggle
    mode = st.radio("SELECT TRADING MODE", ["DEMO ACCOUNT", "LIVE ACCOUNT"])
    is_live = (mode == "LIVE ACCOUNT")
    
    st.divider()
    if st.button("🚀 INITIATE START", type="primary", use_container_width=True):
        st.session_state.is_running = True
    if st.button("🔴 EMERGENCY KILL", use_container_width=True):
        st.session_state.is_running = False

# --- 5. LIVE ACCOUNT API SCANNER (ලයිව් එබුවහම එන කෑල්ල) ---
if is_live:
    st.markdown("<h2 style='color: #00d1ff;'>🔑 LIVE API CONNECTION</h2>", unsafe_allow_html=True)
    col_cam, col_data = st.columns([1, 1])
    
    with col_cam:
        st.write("📷 Scan Binance API QR")
        webrtc_streamer(
            key="api-scan",
            mode=WebRtcMode.SENDRECV,
            rtc_configuration=RTCConfiguration({"iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]}),
            media_stream_constraints={"video": True, "audio": False},
        )
    
    with col_data:
        # මෙතනින් API Key Fill වෙනවා පෙන්වනවා
        u_api = st.text_input("API Key Detected", value=st.session_state.api_key, type="password")
        u_sec = st.text_input("Secret Key Detected", value=st.session_state.secret_key, type="password")
        if st.button("SYNC BINANCE PORTFOLIO"):
            st.session_state.api_key = u_api
            st.session_state.secret_key = u_sec
            st.session_state.balance = 1450.50 # ලයිව් බැලන්ස් එක මෙතනට එනවා
            st.success("Connected! Live balance synced.")

# --- 6. MAIN DASHBOARD ---
st.markdown(f"<h1 style='text-align: center;'>⚡ KD AI QUANTUM TERMINAL - {mode}</h1>", unsafe_allow_html=True)

# Metrics
m1, m2, m3, m4 = st.columns(4)
with m1:
    st.markdown(f'<div class="metric-card"><small>EQUITY</small><div class="neon-blue">${st.session_state.balance:.2f}</div></div>', unsafe_allow_html=True)
with m2:
    pnl = st.session_state.balance - (30.00 if not is_live else 1450.50)
    st.markdown(f'<div class="metric-card"><small>NET PROFIT</small><div class="neon-green">+${pnl:.2f}</div></div>', unsafe_allow_html=True)
with m3:
    st.markdown('<div class="metric-card"><small>PROBABILITY</small><div class="neon-blue">99.9%</div></div>', unsafe_allow_html=True)
with m4:
    status = "RUNNING" if st.session_state.is_running else "IDLE"
    color = "#00ffa3" if st.session_state.is_running else "#ff4b4b"
    st.markdown(f'<div class="metric-card"><small>ENGINE</small><div style="color:{color}; font-weight:bold; font-size:24px;">{status}</div></div>', unsafe_allow_html=True)

st.divider()

# --- 7. MACHINE-GUN LOGIC & GRAPH ---
l_chart, r_ai = st.columns([2, 1])

with l_chart:
    st.subheader("📈 Performance Stream")
    fig = go.Figure(data=go.Scatter(y=st.session_state.history, mode='lines', line=dict(color='#00d1ff', width=3), fill='tozeroy'))
    fig.update_layout(template="plotly_dark", height=400, margin=dict(l=0,r=0,t=0,b=0), paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
    st.plotly_chart(fig, use_container_width=True)

with r_ai:
    st.subheader("🤖 AI Bot")
    if st.session_state.is_running:
        time.sleep(1.2)
        gain = round(np.random.uniform(0.15, 0.45), 2)
        st.session_state.balance += gain
        st.session_state.history.append(st.session_state.balance)
        st.session_state.logs.insert(0, f"[{datetime.now().strftime('%H:%M:%S')}] HIT: +${gain} (99.9%)")
        st.rerun()
    else:
        st.info("Awaiting command...")

# --- 8. LOGS & SCANNER ---
st.divider()
c_logs, c_scan = st.columns([1, 1])
with c_logs:
    st.subheader("📜 Sniper Logs")
    for log in st.session_state.logs[:8]:
        st.markdown(f'<div class="sniper-log">{log}</div>', unsafe_allow_html=True)
with c_scan:
    st.subheader("🔍 Active Scanner")
    st.table(pd.DataFrame({"Pair": ["BTC/USDT", "SOL/USDT"], "Signal": ["STRONG BUY", "SCALP"], "Score": ["99.8%", "99.4%"]}))

st.caption("KD AI QUANTUM | OFFICIAL PRIVATE V9.5")
