import requests

# Function to get all trading pairs from Binance
def get_all_trading_pairs():
    try:
        url = "https://api.binance.com/api/v3/exchangeInfo"
        response = requests.get(url)
        data = response.json()
        symbols = [item['symbol'] for item in data['symbols'] if item['status'] == 'TRADING']
        return symbols
    except Exception as e:
        print(f"Error fetching symbols: {e}")
        return []

# Function to get live price
def get_live_price(symbol):
    try:
        url = f"https://api.binance.com/api/v3/ticker/price?symbol={symbol}"
        response = requests.get(url)
        data = response.json()
        return data['price']
    except Exception as e:
        return "N/A"

# --- Execution ---
print("--- KD AI AUTO BOT ---")

all_coins = get_all_trading_pairs()
print(f"Total Trading Pairs Found: {len(all_coins)}")

if all_coins:
    print("\nScanning Top Coins:")
    # Checking only the first 5 coins for testing
    for coin in all_coins[:5]:
        price = get_live_price(coin)
        print(f"Coin: {coin} | Current Price: ${price}")
else:
    print("No coins found. Please check connection.")

