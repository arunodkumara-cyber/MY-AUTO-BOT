import requests

# 1. Function to get 24h price change data
def get_market_analysis():
    try:
        url = "https://api.binance.com/api/v3/ticker/24hr"
        response = requests.get(url)
        data = response.json()
        
        market_data = []
        for coin in data:
            # Filtering only USDT pairs
            if coin['symbol'].endswith('USDT'):
                market_data.append({
                    'symbol': coin['symbol'],
                    'price': coin['lastPrice'],
                    'change': float(coin['priceChangePercent'])
                })
        return market_data
    except Exception as e:
        print(f"Error: {e}")
        return []

# --- Execution ---
print("--- KD AI AUTO BOT: Market Scanner ---")

all_data = get_market_analysis()

if all_data:
    # Sort to find the biggest drop
    all_data.sort(key=lambda x: x['change'])
    best_opportunity = all_data[0]

    print(f"Scanning {len(all_data)} USDT pairs...")
    print("-" * 30)
    print(f"Top Opportunity Found!")
    print(f"Coin: {best_opportunity['symbol']}")
    print(f"Current Price: ${best_opportunity['price']}")
    print(f"24h Change: {best_opportunity['change']}%")
    print("-" * 30)
else:
    print("Could not fetch data.")



