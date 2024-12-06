import aiohttp
import asyncio
import pandas as pd
import numpy as np


async def fetch_prices_binance():
    url = 'https://api.binance.com/api/v3/ticker/24hr'
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            data = await response.json()  # Асинхронное получение JSON
            price_list = {res['symbol']: float(res['bidPrice'])
                          for res in data
                          if res['symbol'].endswith('USDT') and res['bidPrice'] is not None and float(res['bidPrice']) != 0
                          }
            price_list = dict(price_list.items())
    return price_list


async def fetch_prices_kucoin():
    url = 'https://api.kucoin.com/api/v1/market/allTickers'
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            data = await response.json()
            price_list = {
                res['symbol'].replace('-', ''): float(res['buy'])
                for res in data['data']['ticker']
                if res['symbol'].replace('-', '').endswith('USDT') and res['buy'] is not None and float(res['buy']) != 0}
            price_list = dict(sorted(price_list.items()))
            return price_list


async def fetch_prices_okx():
    url = 'https://www.okx.com/api/v5/market/tickers?instType=SPOT'
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            data = await response.json()
            price_list = {
                res['instId'].replace('-', ''): float(res['askPx'])
                for res in data['data']
                if res['instId'].replace('-', '').endswith('USDT') and res['askPx'] is not None and float(res['askPx']) != 0}
            price_list = dict(sorted(price_list.items()))
            return price_list


async def fetch_prices_bybit():
    url = 'https://api.bybit.com/v5/market/tickers?category=spot'
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            data = await response.json()
            price_list = {
                res["symbol"]: float(res['ask1Price'])
                for res in data["result"]['list']
                if res["symbol"].endswith('USDT')}
            price_list = dict(sorted(price_list.items()))
            return price_list


async def fetch_prices_huobi():
    url = 'https://api.huobi.pro/market/tickers'
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            data = await response.json()
            price_list = {
                res["symbol"].upper(): float(res['ask'])
                for res in data["data"]
                if res["symbol"].upper().endswith('USDT')}
            price_list = dict(sorted(price_list.items()))
            return price_list

# есть пустые значения


async def fetch_prices_gateio():
    url = 'https://api.gateio.ws/api/v4/spot/tickers'
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            data = await response.json()
            price_list = {
                res["currency_pair"].replace('_', ''): float(res['lowest_ask'])
                for res in data
                if res["currency_pair"].replace('_', '').endswith('USDT')}
            price_list = dict(sorted(price_list.items()))
            return price_list


async def fetch_prices_poloniex():
    url = 'https://api.poloniex.com/markets/ticker24h'
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            data = await response.json()
            price_list = {
                res["symbol"].replace('_', ''): float(res['ask'])
                for res in data
                if res["symbol"].replace('_', '').endswith('USDT')}
            price_list = dict(sorted(price_list.items()))
            return price_list


async def fetch_prices_bitget():
    url = 'https://api.bitget.com/api/spot/v1/market/tickers'
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            data = await response.json()
            price_list = {
                res["symbol"]: float(res['buyOne'])
                for res in data['data']
                if res["symbol"].endswith('USDT')}
            price_list = dict(sorted(price_list.items()))
            return price_list


# ?? Хз че за биржа, долгий ответ, тупые ключи
async def fetch_prices_probit():
    url = 'https://api.probit.com/api/exchange/v1/ticker'
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            data = await response.json()
            price_list = {
                res["market_id"].replace('-', ''): float(res['last'])
                for res in data['data']
                if res["market_id"].replace('-', '').endswith('USDT') and res['last'] is not None}
            price_list = dict(sorted(price_list.items()))
            return price_list


async def fetch_prices_ascendex():
    url = 'https://ascendex.com/api/pro/v1/ticker'
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            data = await response.json()
            price_list = {
                res["symbol"].replace('/', ''): float(res['ask'][0])
                for res in data['data']
                if res["symbol"].replace('/', '').endswith('USDT')}
            price_list = dict((price_list.items()))
            return price_list


# Сравнение цен


async def compare_prices():
    # Собираем цены с разных бирж
    binance_prices = await fetch_prices_binance()
    kucoin_prices = await fetch_prices_kucoin()
    okx_prices = await fetch_prices_okx()
    bybit_prices = await fetch_prices_bybit()
    huobi_prices = await fetch_prices_huobi()
    poloniex_prices = await fetch_prices_poloniex()
    bitget_prices = await fetch_prices_bitget()
    ascendex_prices = await fetch_prices_ascendex()


#################################################################
all_prices = {}

binance_response = asyncio.run(fetch_prices_binance())  # res1.keys()
print('Binance: ', len(binance_response))
all_prices['Binance'] = binance_response

kucoiun_response = asyncio.run(fetch_prices_kucoin())
print('Kucoin: ', len(kucoiun_response))
all_prices['Kucoin'] = kucoiun_response

bybit_response = asyncio.run(fetch_prices_bybit())
print('Bybit: ', len(bybit_response))
all_prices['Bybit'] = bybit_response

poloniex_huobi = asyncio.run(fetch_prices_huobi())
print('Huobi: ', len(poloniex_huobi))
all_prices['Huobi'] = poloniex_huobi

poloniex_response = asyncio.run(fetch_prices_poloniex())
print('Poloniex: ', len(poloniex_response))
all_prices['Poloniex'] = poloniex_response

bitget_response = asyncio.run(fetch_prices_bitget())
print('Bitget: ', len(bitget_response))
all_prices['Bitget'] = bitget_response

ascendex_response = asyncio.run(fetch_prices_ascendex())
print('Ascendex: ', len(ascendex_response))
all_prices['Ascendex'] = ascendex_response

probit_response = asyncio.run(fetch_prices_probit())
print('Probit: ', len(probit_response))
all_prices['Probit'] = probit_response

okx_response = asyncio.run(fetch_prices_okx())
print('Okx: ', len(okx_response))
all_prices['Okx'] = okx_response


async def sort_prices():
    exchanges_list = all_prices.keys()
    sorted_dict = {}
    for exchange in exchanges_list:
        for pair in all_prices[exchange]:
            if pair not in sorted_dict:
                sorted_dict[pair] = []
            sorted_dict[pair].append({exchange: all_prices[exchange][pair]})

    print(sorted_dict)
    # return sorted_dict['BTCUSDT']

asyncio.run(sort_prices())
