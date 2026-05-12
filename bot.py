import requests

def get_rsi(symbol):
    try:
        url = f"https://api.binance.com/api/v3/klines?symbol={symbol}&interval=1h&limit=50"
        response = requests.get(url)
        data = response.json()
        
        # Check if we got a valid list
        if not isinstance(data, list): return 50
        
        closes = [float(c[4]) for c in data]
        if len(closes) < 2: return 50
        
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
        return 50

def start_scanning():
    print("--- KD AI AUTO BOT: Strategy V2 ---")
    try:
        # 24hr ticker data
        url = "https://api.binance.com/api/v3/ticker/24hr"
        response = requests.get(url)
        coins = response.json()
        
        # Security check: Ensure 'coins' is a list
        if not isinstance(coins, list):
            print("Error: Could not get market data.")
            return

        # Filtering USDT pairs and cleaning data
        usdt_pairs = []
        for c in coins:
            if isinstance(c, dict) and 'symbol' in c and c['symbol'].endswith('USDT'):
                usdt_pairs.append(c)

        # Sort by price change percentage
        usdt_pairs.sort(key=lambda x: float(x.get('priceChangePercent', 0)))

        print(f"Checking top 5 potential coins...\n")
        for coin in usdt_pairs[:5]:
            symbol = coin['symbol']
            price = coin['lastPrice']
            change = coin['priceChangePercent']
            rsi_val = get_rsi(symbol)
            
            print(f"Coin: {symbol} | Change: {change}% | RSI: {rsi_val}")
            
            if rsi_val < 35:
                print(f"🚀 SIGNAL: {symbol} is OVERSOLD! Good time to buy.")
            elif rsi_val > 70:
                print(f"⚠️ ALERT: {symbol} is OVERBOUGHT! Risk of price drop.")
            print("-" * 20)

    except Exception as e:
        print(f"Main Error: {e}")

if __name__ == "__main__":
    start_scanning()





