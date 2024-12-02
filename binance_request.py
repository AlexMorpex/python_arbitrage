import aiohttp
import asyncio
import time


async def fetch_price(session, url, json_path):
    async with session.get(url) as response:
        data = await response.json()
        # Используем `json_path` для поиска нужного значения
        for key in json_path:
            data = data[key]
        return float(data)


async def main():
    urls = [
        ("Binance", "https://api.binance.com/api/v3/ticker/price?symbol=BTCUSDT",
         ['price']),
        ("Bybit", "https://api.bybit.com/v5/market/tickers?category=spot&symbol=BTCUSDT",
         ["result", "list", 0, "bid1Price"]),
        ("KuCoin", "https://api.kucoin.com/api/v1/market/orderbook/level1?symbol=BTC-USDT",
         ["data", "price"]),
        ("OKX", "https://www.okx.com/api/v5/market/ticker?instId=BTC-USDT",
         ["data", 0, "last"]),
        ("MEXC", "https://www.mexc.com/open/api/v2/market/ticker?symbol=BTC_USDT",
         ["data", 0, "last"]),
        ("GateIo", "https://api.gateio.ws/api/v4/spot/tickers?currency_pair=BTC_USDT",
         [0, "last"]),
        ("Huobi", "https://api.huobi.pro/market/detail/merged?symbol=btcusdt",
         ['tick', "bid", 0]),
        ("Crypto.com", "https://api.crypto.com/v2/public/get-ticker?instrument_name=BTC_USDT",
         ["result", "data", 0, "b"]),
    ]

    async with aiohttp.ClientSession() as session:
        tasks = [fetch_price(session, url, path) for _, url, path in urls]
        prices = await asyncio.gather(*tasks)

        for (name, _, _), price in zip(urls, prices):
            print(f"{name}: BTC/USDT {price}")

# Запускаем асинхронную программу
asyncio.run(main())
