import requests

# 1. Function to get 24h price change data for all coins
def get_market_analysis():
    url = "https://api.binance.com/api/v3/ticker/24hr"
    response = requests.get(url)
    data = response.json()
    
    # Filter only USDT pairs and calculate price drop
    market_data = []
    for coin in data:
        if coin['symbol'].endswith('USDT'):
            market_data.append({
                'symbol': coin['symbol'],
                'price': coin['lastPrice'],
                'change': float(coin['priceChangePercent'])
            })
    return market_data

# --- Execution ---
print("--- KD AI AUTO BOT: Market Scanner ---")

# Scan the market
all_data = get_market_analysis()

# Find the coin with the biggest price drop (Best to buy low)
all_data.sort(key=lambda x: x['change'])
best_opportunity = all_data[0] # The one with the highest negative percentage

print(f"Scanning {len(all_data)} USDT pairs...")
print("-" * 30)
print(f"Top Opportunity Found!")
print(f"Coin: {best_opportunity['symbol']}")
print(f"Current Price: ${best_opportunity['price']}")
print(f"24h Change: {best_opportunity['change']}%")
print("-" * 30)


