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
st.title("🚀 KD AI MASTER SCANNER (All Coins)")
st.write("බයිනෑන්ස් හි සියලුම USDT Pairs ස්කෑන් කර RSI අගයන් පරීක්ෂා කරයි.")

if st.button('Start Global Market Scan'):
    with st.spinner('දත්ත එකතු කරමින් පවතී...'):
        all_coins = get_all_usdt_coins()
        
        if not all_coins.empty:
            # Sort by price drop to find potentials
            top_losers = all_coins.sort_values(by='priceChangePercent').head(15).copy()
            
            # Get RSI for top 15 losers
            top_losers['RSI'] = top_losers['symbol'].apply(get_rsi)
            
            col1, col2 = st.columns([1, 2])
            
            with col1:
                st.subheader("🎯 Buy Signals")
                # Filter for RSI < 35
                signals = top_losers[top_losers['RSI'] < 40]
                if not signals.empty:
                    for _, row in signals.iterrows():
                        st.markdown(f"""
                        <div class="buy-signal">
                            <b>{row['symbol']}</b><br>
                            RSI: {row['RSI']} | Change: {row['priceChangePercent']}%<br>
                            Price: ${row['lastPrice']:.4f}
                        </div>
                        """, unsafe_allow_html=True)
                else:
                    st.info("හොඳ Buy Signals දැනට නොමැත.")

            with col2:
                st.subheader("📊 Top Market Opportunities")
                st.dataframe(top_losers[['symbol', 'lastPrice', 'priceChangePercent', 'RSI']], use_container_width=True)
                
            # Chart Section
            st.divider()
            selected = st.selectbox("Select Coin to View Chart:", top_losers['symbol'].tolist())
            chart_html = f"""
            <div style="height:400px;">
                <script type="text/javascript" src="https://s3.tradingview.com/tv.js"></script>
                <script type="text/javascript">
                new TradingView.widget({{
                  "width": "100%", "height": 400, "symbol": "BINANCE:{selected}",
                  "interval": "H", "theme": "dark", "style": "1", "locale": "en"
                }});
                </script>
            </div>
            """
            components.html(chart_html, height=420)
else:
    st.info("පරීක්ෂාව ආරම්භ කිරීමට 'Start Global Market Scan' බොත්තම ඔබන්න.")



