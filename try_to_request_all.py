import aiohttp
import asyncio
import pandas as pd
import numpy as np


async def fetch_prices_binance(session: aiohttp.ClientSession):
    url = 'https://api.binance.com/api/v3/ticker/24hr'
    async with session.get(url) as response:
        data = await response.json()
        price_list = {
            res['symbol']: float(res['askPrice'])
            for res in data
            if res['symbol'].endswith('USDT') and res['askPrice'] is not None and float(res['askPrice']) != 0
        }
        return price_list


async def fetch_prices_kucoin(session: aiohttp.ClientSession):
    url = 'https://api.kucoin.com/api/v1/market/allTickers'
    async with session.get(url) as response:
        data = await response.json()
        price_list = {
            res['symbol'].replace('-', ''): float(res['buy'])
            for res in data['data']['ticker']
            if res['symbol'].replace('-', '').endswith('USDT') and res['buy'] is not None and float(res['buy']) != 0
        }
        return price_list


async def fetch_prices_okx(session: aiohttp.ClientSession):
    url = 'https://www.okx.com/api/v5/market/tickers?instType=SPOT'
    async with session.get(url) as response:
        data = await response.json()
        price_list = {
            res['instId'].replace('-', ''): float(res['askPx'])
            for res in data['data']
            if res['instId'].replace('-', '').endswith('USDT') and res['askPx'] is not None and float(res['askPx']) != 0
        }
        return price_list


async def fetch_prices_bybit(session: aiohttp.ClientSession):
    url = 'https://api.bybit.com/v5/market/tickers?category=spot'
    async with session.get(url) as response:
        data = await response.json()
        price_list = {
            res["symbol"]: float(res['ask1Price'])
            for res in data["result"]['list']
            if res["symbol"].endswith('USDT') and res['ask1Price'] is not None and float(res['ask1Price']) != 0
        }
        return price_list


async def fetch_prices_huobi(session: aiohttp.ClientSession):
    url = 'https://api.huobi.pro/market/tickers'
    async with session.get(url) as response:
        data = await response.json()
        price_list = {
            res["symbol"].upper(): float(res['ask'])
            for res in data["data"]
            if res["symbol"].upper().endswith('USDT') and res['ask'] is not None and float(res['ask']) != 0
        }
        return price_list


async def fetch_prices_gateio(session: aiohttp.ClientSession):
    url = 'https://api.gateio.ws/api/v4/spot/tickers'
    async with session.get(url) as response:
        data = await response.json()
        price_list = {
            res["currency_pair"].replace('_', ''): float(res['lowest_ask'])
            for res in data
            if res["currency_pair"].replace('_', '').endswith('USDT') and res['lowest_ask'] is not None and float(res['lowest_ask']) != 0
        }
        return price_list


async def fetch_prices_poloniex(session: aiohttp.ClientSession):
    url = 'https://api.poloniex.com/markets/ticker24h'
    async with session.get(url) as response:
        data = await response.json()
        price_list = {
            res["symbol"].replace('_', ''): float(res['ask'])
            for res in data
            if res["symbol"].replace('_', '').endswith('USDT') and res['ask'] is not None and float(res['ask']) != 0
        }
        return price_list


async def fetch_prices_bitget(session: aiohttp.ClientSession):
    url = 'https://api.bitget.com/api/spot/v1/market/tickers'
    async with session.get(url) as response:
        data = await response.json()
        price_list = {
            res["symbol"]: float(res['buyOne'])
            for res in data['data']
            if res["symbol"].endswith('USDT') and res['buyOne'] is not None and float(res['buyOne']) != 0
        }
        return price_list

# ?? Хз че за биржа, долгий ответ, тупые ключи


async def fetch_prices_probit(session: aiohttp.ClientSession):
    url = 'https://api.probit.com/api/exchange/v1/ticker'
    async with session.get(url) as response:
        data = await response.json()
        price_list = {
            res["market_id"].replace('-', ''): float(res['last'])
            for res in data['data']
            if res["market_id"].replace('-', '').endswith('USDT') and res['last'] is not None
        }
        return price_list


async def fetch_prices_ascendex(session: aiohttp.ClientSession):
    url = 'https://ascendex.com/api/pro/v1/ticker'
    async with session.get(url) as response:
        data = await response.json()
        price_list = {
            res["symbol"].replace('/', ''): float(res['ask'][0])
            for res in data['data']
            if res["symbol"].replace('/', '').endswith('USDT') and res['ask'][0] is not None and float(res['ask'][0]) != 0
        }
        return price_list

#################################################################


async def print_exchanges_info() -> dict:
    async with aiohttp.ClientSession() as session:
        tasks = {
            'Binance': fetch_prices_binance(session),
            'Kucoin': fetch_prices_kucoin(session),
            'Bybit': fetch_prices_bybit(session),
            'Huobi': fetch_prices_huobi(session),
            'Poloniex': fetch_prices_poloniex(session),
            'Bitget': fetch_prices_bitget(session),
            'Ascendex': fetch_prices_ascendex(session),
            'Probit': fetch_prices_probit(session),
            'Okx': fetch_prices_okx(session),
        }

        results = await asyncio.gather(*tasks.values(), return_exceptions=True)
        all_prices = {}

        for exchange, result in zip(tasks.keys(), results):
            if isinstance(result, Exception):
                print(f"Ошибка при запросе к {exchange}: {result}")
            else:
                print(f"{exchange}: {len(result)} пар")
                all_prices[exchange] = result

    return all_prices


async def sort_prices(prices_dict: dict):
    exchanges_list = prices_dict.keys()
    sorted_dict = {}
    for exchange in exchanges_list:
        for pair in prices_dict[exchange]:
            if pair not in sorted_dict:
                sorted_dict[pair] = []
            sorted_dict[pair].append({exchange: prices_dict[exchange][pair]})

    list_to_remove = []
    for pair in sorted_dict.keys():
        if len(sorted_dict[pair]) < 2:
            list_to_remove.append(pair)

    for pair in list_to_remove:
        sorted_dict.pop(pair)

    for pair in sorted_dict:
        print(pair, ': ',
              len(sorted_dict[pair]),
              )
        for el in sorted_dict[pair]:
            print(el, end='')
        print('\n')

info = asyncio.run(print_exchanges_info())
asyncio.run(sort_prices(info))
