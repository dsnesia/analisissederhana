import requests
import pandas as pd
from datetime import datetime

def get_crypto_price(coin_id):
    url = f'https://api.coingecko.com/api/v3/simple/price?ids={coin_id}&vs_currencies=usd'
    r = requests.get(url)
    data = r.json()
    return data.get(coin_id, {}).get('usd')

def get_crypto_info(coin_id):
    url = f'https://api.coingecko.com/api/v3/coins/{coin_id}'
    r = requests.get(url)
    if r.status_code != 200:
        return None
    data = r.json()
    return {
        'name': data['name'],
        'symbol': data['symbol'].upper(),
        'price': data['market_data']['current_price']['usd'],
        'market_cap': data['market_data']['market_cap']['usd'],
        'volume': data['market_data']['total_volume']['usd'],
        'change_24h': data['market_data']['price_change_percentage_24h'],
    }

def get_price_history(coin_id):
    url = f"https://api.coingecko.com/api/v3/coins/{coin_id}/market_chart?vs_currency=usd&days=7"
    r = requests.get(url)
    if r.status_code != 200:
        return None
    data = r.json()
    prices = data['prices']
    df = pd.DataFrame(prices, columns=["timestamp", "price"])
    df["date"] = pd.to_datetime(df["timestamp"], unit="ms")
    return df

def simple_trend_signal(df):
    df['ma_short'] = df['price'].rolling(window=3).mean()
    df['ma_long'] = df['price'].rolling(window=6).mean()
    if df['ma_short'].iloc[-1] > df['ma_long'].iloc[-1]:
        return "📈 Sinyal: Bullish"
    else:
        return "📉 Sinyal: Bearish"
