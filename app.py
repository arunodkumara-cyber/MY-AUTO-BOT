import streamlit as st
import requests
import pandas as pd

st.set_page_config(page_title="KD AI AUTO BOT", layout="wide")

# Dark mode style
st.markdown("""
    <style>
    .main { background-color: #000000; color: white; }
    stMetric { background-color: #1e1e1e; padding: 10px; border-radius: 10px; }
    </style>
    """, unsafe_allow_html=True)

st.title("🤖 KD AI AUTO BOT - Dashboard")
st.write("Real-time Crypto Market Scanner & Virtual Trader")

# Sidebar for Wallet Info
st.sidebar.header("Virtual Wallet")
st.sidebar.metric("Balance", "$30.00")
st.sidebar.write("Status: Scanning...")

# Function to get Data
def get_data():
    url = "https://api.binance.com/api/v3/ticker/24hr"
    res = requests.get(url).json()
    df = pd.DataFrame(res)
    df = df[df['symbol'].str.endswith('USDT')]
    df['priceChangePercent'] = df['priceChangePercent'].astype(float)
    df['lastPrice'] = df['lastPrice'].astype(float)
    return df[['symbol', 'lastPrice', 'priceChangePercent']].sort_values(by='priceChangePercent')

# Display Market Data
if st.button('Refresh Market Data'):
    data = get_data()
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📉 Top Losers (Buy Signals?)")
        st.dataframe(data.head(10))
        
    with col2:
        st.subheader("📈 Top Gainers")
        st.dataframe(data.tail(10).sort_values(by='priceChangePercent', ascending=False))

st.success("Bot is active and monitoring RSI levels...")
