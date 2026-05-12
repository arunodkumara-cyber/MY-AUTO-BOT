import requests

# 1. Function to get historical data for RSI calculation
def get_rsi(symbol):
    try:
        # Getting last 100 hourly candles
        url = f"https://api.binance.com/api/v3/klines?symbol={symbol}&interval=1h&limit=100"
        data = requests.get(url).json()
        closes = [float(c[4]) for c in data]
        
        # Simple RSI Logic
        gains = []
        losses = []
        for i in range(1, len(closes)):
            diff = closes[i] - closes[i-1]
            if diff > 0: gains.append(diff)
            else: losses.append(abs(diff))
        
        avg_gain = sum(gains) / len(gains) if gains else 0
        avg_loss = sum(losses) / len(losses) if losses else 1
        rs = avg_gain / avg_loss
        rsi = 100 - (100 / (1 + rs))
        return round(rsi, 2)
    except:
        return 50 # Default middle value

# 2. Market Scanner
def start_scanning():
    print("--- KD AI AUTO BOT: Strategy V2 ---")
    url = "https://api.binance.com/api/v3/ticker/24hr"
    coins = requests.get(url).json()
    
    usdt_pairs = [c for c in coins if c['symbol'].endswith('USDT')]
    usdt_pairs.sort(key=lambda x: float(x['priceChangePercent'])) # Sort by price drop

    print(f"Checking top 5 potential coins...")
    for coin in usdt_pairs[:5]:
        symbol = coin['symbol']
        price = coin['lastPrice']
        change = coin['priceChangePercent']
        rsi_val = get_rsi(symbol)
        
        print(f"Coin: {symbol} | Change: {change}% | RSI: {rsi_val}")
        
        if rsi_val < 30:
            print(f"🚀 SIGNAL: {symbol} is OVERSOLD! Good time to buy.")
        elif rsi_val > 70:
            print(f"⚠️ ALERT: {symbol} is OVERBOUGHT! Risk of price drop.")

start_scanning()




