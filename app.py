import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from datetime import datetime
import time
import ccxt
import sqlite3
import pandas_ta as ta

# --- 1. SYSTEM CORE SETUP ---
st.set_page_config(
    page_title="KD AI QUANTUM TERMINAL - V12 ELITE",
    page_icon="💎",
    layout="wide"
)

# --- 2. DATABASE SETUP ---
def init_db():
    conn = sqlite3.connect('trade_history.db', check_same_thread=False)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS trades 
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                  time TEXT, asset TEXT, type TEXT, 
                  entry_price REAL, exit_price REAL, 
                  profit REAL, status TEXT)''')
    conn.commit()
    return conn

db_conn = init_db()

# --- 3. PREMIUM STYLING ---
st.markdown("""
    <style>
    .stApp { background-color: #010409; color: #e6edf3; }
    .st-emotion-cache-12w0qpk { background: #0d1117; border: 1px solid #30363d; border-radius: 10px; }
    .stat-card {
        background: linear-gradient(145deg, #0d1117 0%, #161b22 100%);
        border: 1px solid #30363d; border-radius: 12px; padding: 20px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.5);
        text-align: center;
    }
    .neon-text-blue { color: #58a6ff; font-weight: bold; font-size: 24px; }
    .neon-text-green { color: #3fb950; font-weight: bold; font-size: 24px; }
    .neon-text-red { color: #f85149; font-weight: bold; font-size: 24px; }
    .log-container {
        background-color: #000; border: 1px solid #30363d;
        padding: 15px; height: 250px; overflow-y: auto;
        font-family: 'Courier New', monospace; color: #3fb950;
        border-radius: 8px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 4. STATE MANAGEMENT ---
if 'balance' not in st.session_state: st.session_state.balance = 1000.00
if 'is_running' not in st.session_state: st.session_state.is_running = False
if 'position' not in st.session_state: st.session_state.position = None
if 'logs' not in st.session_state: st.session_state.logs = []

def write_log(message):
    timestamp = datetime.now().strftime("%H:%M:%S")
    st.session_state.logs.append(f"[{timestamp}] {message}")

# --- 5. DATA & ANALYTICS CORE (Updated with Connection Fix) ---
def fetch_market_data(symbol, timeframe='5m'):
    try:
        # UPDATED: Connection settings to handle time sync and recvWindow
        exchange = ccxt.binance({
            'enableRateLimit': True,
            'options': {
                'adjustForTimeDifference': True,
                'recvWindow': 10000,
            }
        })
        
        ohlcv = exchange.fetch_ohlcv(symbol, timeframe=timeframe, limit=100)
        df = pd.DataFrame(ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
        df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
        
        # Technical Indicators
        df['rsi'] = ta.rsi(df['close'], length=14)
        df['ema_20'] = ta.ema(df['close'], length=20)
        df['ema_50'] = ta.ema(df['close'], length=50)
        macd = ta.macd(df['close'])
        df = pd.concat([df, macd], axis=1)
        
        return df
    except Exception as e:
        # Display the specific error message on screen
        st.error(f"Connection Error: {e}")
        return None

def get_quantum_signal(df):
    last = df.iloc[-1]
    long_cond = (last['rsi'] < 35) and (last['close'] > last['ema_20']) and (last['MACDh_12_26_9'] > 0)
    short_cond = (last['rsi'] > 65) and (last['close'] < last['ema_20']) and (last['MACDh_12_26_9'] < 0)
    
    if long_cond: return "STRONG BUY", last['close']
    if short_cond: return "STRONG SELL", last['close']
    return "NEUTRAL", last['close']

# --- 6. SIDEBAR CONTROLS ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/2091/2091665.png", width=80)
    st.title("KD AI TERMINAL")
    
    mode = st.selectbox("Execution Mode", ["Paper Trading", "Live Binance"])
    symbol = st.text_input("Trading Pair", value="BTC/USDT")
    
    st.divider()
    st.subheader("🛡️ Risk Management")
    leverage = st.slider("Leverage (X)", 1, 50, 10)
    margin_pct = st.slider("Margin per Trade %", 1.0, 5.0, 3.0)
    tp_pct = st.slider("Take Profit %", 0.5, 5.0, 1.5)
    sl_pct = st.slider("Stop Loss %", 0.2, 2.0, 0.8)
    
    st.divider()
    c1, c2 = st.columns(2)
    with c1:
        if st.button("START BOT", use_container_width=True, type="primary"):
            st.session_state.is_running = True
            write_log(f"System Online: Scanning {symbol}")
    with c2:
        if st.button("STOP BOT", use_container_width=True):
            st.session_state.is_running = False
            write_log("System Offline.")

# --- 7. MAIN DASHBOARD ---
st.header(f"⚡ KD AI QUANTUM V12 - {symbol}")

df = fetch_market_data(symbol)

if df is not None:
    signal, current_price = get_quantum_signal(df)
    
    # KPI Metrics
    m1, m2, m3, m4 = st.columns(4)
    with m1:
        st.markdown(f'<div class="stat-card">Account Balance<div class="neon-text-blue">${st.session_state.balance:,.2f}</div></div>', unsafe_allow_html=True)
    with m2:
        sig_color = "green" if "BUY" in signal else "red" if "SELL" in signal else "blue"
        st.markdown(f'<div class="stat-card">Market Signal<div class="neon-text-{sig_color}">{signal}</div></div>', unsafe_allow_html=True)
    with m3:
        st.markdown(f'<div class="stat-card">Live Price<div class="neon-text-blue">${current_price:,.2f}</div></div>', unsafe_allow_html=True)
    with m4:
        engine_status = "RUNNING" if st.session_state.is_running else "IDLE"
        engine_col = "#3fb950" if st.session_state.is_running else "#f85149"
        st.markdown(f'<div class="stat-card">Engine Status<div style="color:{engine_col}; font-weight:bold; font-size:24px;">{engine_status}</div></div>', unsafe_allow_html=True)

    # Trading Execution
    if st.session_state.is_running:
        if st.session_state.position is None and signal != "NEUTRAL":
            trade_size = (st.session_state.balance * (margin_pct/100)) * leverage
            st.session_state.position = {
                "type": signal, "entry": current_price, "size": trade_size,
                "tp": current_price * (1 + tp_pct/100) if "BUY" in signal else current_price * (1 - tp_pct/100),
                "sl": current_price * (1 - sl_pct/100) if "BUY" in signal else current_price * (1 + sl_pct/100)
            }
            write_log(f"🚀 OPENED {signal} at {current_price}")

        elif st.session_state.position:
            pos = st.session_state.position
            is_buy = "BUY" in pos['type']
            hit_tp = (is_buy and current_price >= pos['tp']) or (not is_buy and current_price <= pos['tp'])
            hit_sl = (is_buy and current_price <= pos['sl']) or (not is_buy and current_price >= pos['sl'])
            
            if hit_tp or hit_sl:
                pnl_factor = (current_price - pos['entry']) / pos['entry'] if is_buy else (pos['entry'] - current_price) / pos['entry']
                net_profit = (pos['size'] * pnl_factor) - (pos['size'] * 0.001)
                st.session_state.balance += net_profit
                
                cursor = db_conn.cursor()
                cursor.execute("INSERT INTO trades (time, asset, type, entry_price, exit_price, profit, status) VALUES (?,?,?,?,?,?,?)",
                               (datetime.now().strftime("%Y-%m-%d %H:%M"), symbol, pos['type'], pos['entry'], current_price, net_profit, "CLOSED"))
                db_conn.commit()
                
                write_log(f"✅ CLOSED {pos['type']}: Profit ${net_profit:.2f}")
                st.session_state.position = None

    # Chart
    fig = go.Figure()
    fig.add_trace(go.Candlestick(x=df['timestamp'], open=df['open'], high=df['high'], low=df['low'], close=df['close'], name="Price"))
    fig.update_layout(template="plotly_dark", height=450, margin=dict(l=0,r=0,t=0,b=0), xaxis_rangeslider_visible=False)
    st.plotly_chart(fig, use_container_width=True)

    # History & Logs
    col_log, col_hist = st.columns([1, 2])
    with col_log:
        st.subheader("📋 Logs")
        log_html = "".join([f"<div>{l}</div>" for l in st.session_state.logs[::-1]])
        st.markdown(f'<div class="log-container">{log_html}</div>', unsafe_allow_html=True)
    with col_hist:
        st.subheader("📊 History")
        history_df = pd.read_sql_query("SELECT time, type, entry_price, exit_price, profit FROM trades ORDER BY id DESC LIMIT 5", db_conn)
        st.dataframe(history_df, use_container_width=True)

# Auto-refresh
if st.session_state.is_running:
    time.sleep(5)
    st.rerun()
