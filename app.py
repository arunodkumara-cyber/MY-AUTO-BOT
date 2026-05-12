import streamlit as st
import requests
import pandas as pd
import streamlit.components.v1 as components

# 1. Page Configuration
st.set_page_config(page_title="KD AI MASTER SCANNER", layout="wide")

# Custom Dark Theme CSS
st.markdown("""
    <style>
    .main { background-color: #0b0e11; color: #eaecef; }
    .stMetric { background-color: #1e2329; border-radius: 10px; padding: 15px; border: 1px solid #474d57; }
    .buy-signal { background-color: #1c3d2a; padding: 15px; border-radius: 10px; border-left: 5px solid #00ff00; margin-bottom: 10px; }
    .stButton>button { background-color: #f0b90b; color: black; width: 100%; border-radius: 5px; font-weight: bold; border: none; }
    .stButton>button:hover { background-color: #d4a30a; color: black; }
    </style>
    """, unsafe_allow_html=True)

# 2. RSI Calculation Function
def get_rsi(symbol):
    try:
        url = f"https://api.binance.com/api/v3/klines?symbol={symbol}&interval=1h&limit=50"
        res = requests.get(url, timeout=5)
        data = res.json()
        if not isinstance(data, list) or len(data) < 20:
            return 50
        
        closes = [float(c[4]) for c in data]
        gains = [max(0, closes[i] - closes[i-1]) for i in range(1, len(closes))]
        losses = [max(0, closes[i-1] - closes[i]) for i in range(1, len(closes))]
        
        avg_gain = sum(gains[-14:]) / 14
        avg_loss = sum(losses[-14:]) / 14
        rs = avg_gain / (avg_loss if avg_loss != 0 else 1)
        return round(100 - (100 / (1 + rs)), 2)
    except:
        return 50

# 3. Fetch All USDT Coins from Binance
def get_all_usdt_coins():
    try:
        url = "https://api.binance.com/api/v3/ticker/24hr"
        res = requests.get(url, timeout=5).json()
        df = pd.DataFrame(res)
        # Filtering USDT pairs and excluding stablecoins
        df = df[df['symbol'].str.endswith('USDT')]
        exclude = ['USDCUSDT', 'FDUSDUSDT', 'TUSDUSDT', 'DAIUSDT', 'EURUSDT', 'GBPUSDT']
        df = df[~df['symbol'].isin(exclude)]
        
        df['lastPrice'] = df['lastPrice'].astype(float)
        df['priceChangePercent'] = df['priceChangePercent'].astype(float)
        return df
    except:
        return pd.DataFrame()

# UI Layout
st.title("🤖 KD AI MASTER SCANNER")
st.write("Professional Real-time Market Scanner for Binance USDT Pairs")

# 4. Global Market Scan Section
if st.button('RUN SYSTEM SCAN'):
    with st.spinner('Scanning Global Market Data...'):
        all_coins = get_all_usdt_coins()
        
        if not all_coins.empty:
            # Get top 15 losers for RSI analysis
            top_potentials = all_coins.sort_values(by='priceChangePercent').head(15).copy()
            top_potentials['RSI'] = top_potentials['symbol'].apply(get_rsi)
            
            col1, col2 = st.columns([1, 2])
            
            with col1:
                st.subheader("🎯 Trade Signals")
                # Logic: RSI < 40 is considered a potential entry
                signals = top_potentials[top_potentials['RSI'] < 40]
                if not signals.empty:
                    for _, row in signals.iterrows():
                        st.markdown(f"""
                        <div class="buy-signal">
                            <b>{row['symbol']}</b><br>
                            RSI: {row['RSI']} | 24h Change: {row['priceChangePercent']}%<br>
                            Last Price: ${row['lastPrice']:.4f}
                        </div>
                        """, unsafe_allow_html=True)
                else:
                    st.info("No strong Oversold signals detected at the moment.")

            with col2:
                st.subheader("📊 Market Opportunities (Top 15)")
                st.dataframe(top_potentials[['symbol', 'lastPrice', 'priceChangePercent', 'RSI']], use_container_width=True)
                
            # 5. TradingView Chart Integration
            st.divider()
            st.subheader("🔍 Technical Chart Analysis")
            selected = st.selectbox("Select Asset to View Interactive Chart:", top_potentials['symbol'].tolist())
            
            chart_html = f"""
            <div style="height:500px;">
                <script type="text/javascript" src="https://s3.tradingview.com/tv.js"></script>
                <script type="text/javascript">
                new TradingView.widget({{
                  "width": "100%", "height": 500, "symbol": "BINANCE:{selected}",
                  "interval": "60", "timezone": "Etc/UTC", "theme": "dark",
                  "style": "1", "locale": "en", "toolbar_bg": "#f1f3f6",
                  "enable_publishing": false, "allow_symbol_change": true,
                  "container_id": "tradingview_chart"
                }});
                </script>
                <div id="tradingview_chart"></div>
            </div>
            """
            components.html(chart_html, height=520)
else:
    st.info("System Standby. Click 'RUN SYSTEM SCAN' to analyze the market.")




