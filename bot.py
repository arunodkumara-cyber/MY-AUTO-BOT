import requests

# Function to get all trading pairs from Binance
def get_all_trading_pairs():
    url = "https://api.binance.com/api/v3/exchangeInfo"
    response = requests.get(url)
    data = response.json()
    
    # Extracting only the symbol (e.g., BTCUSDT, ETHUSDT)
    symbols = [item['symbol'] for item in data['symbols'] if item['status'] == 'TRADING']
    return symbols

# Function to get live price of a specific coin
def get_live_price(symbol):
    url = f"https://api.binance.com/api/v3/ticker/price?symbol={symbol}"
    response = requests.get(url)
    data = response.json()
    return data['price']

# --- Execution ---
print("--- KD AI AUTO BOT ---")

# 1. Fetching all available coins
all_coins = get_all_trading_pairs()
print(f"Total Trading Pairs Found: {len(all_coins)}")

# 2. Let's check prices for a few examples (First 5 coins)
print("\nScanning Top Coins:")
for coin in all_coins[:5]:
    price = get_live_price(coin)
    print(f"Coin: {coin} | Current Price: ${price}")
