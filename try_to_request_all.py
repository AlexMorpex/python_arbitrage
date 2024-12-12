import aiohttp
import asyncio
import logging
import csv
import time

DEBUG = False


async def fetch_prices_binance(session: aiohttp.ClientSession):
    url = 'https://api.binance.com/api/v3/ticker/24hr'
    async with session.get(url) as response:
        data = await response.json()
        price_list = {
            res['symbol']: float(res['askPrice'])
            for res in data
            if res['symbol'].endswith('USDT')
            and res['askPrice'] is not None
            and float(res['askPrice']) != 0
            and float(res['volume']) != 0
        }
        return price_list


async def fetch_prices_kucoin(session: aiohttp.ClientSession):
    url = 'https://api.kucoin.com/api/v1/market/allTickers'
    async with session.get(url) as response:
        data = await response.json()
        price_list = {
            res['symbol'].replace('-', ''): float(res['buy'])
            for res in data['data']['ticker']
            if res['symbol'].replace('-', '').endswith('USDT')
            and res['buy'] is not None
            and float(res['buy']) != 0

        }
        return price_list


async def fetch_prices_okx(session: aiohttp.ClientSession):
    url = 'https://www.okx.com/api/v5/market/tickers?instType=SPOT'
    async with session.get(url) as response:
        data = await response.json()
        price_list = {
            res['instId'].replace('-', ''): float(res['askPx'])
            for res in data['data']
            if res['instId'].replace('-', '').endswith('USDT')
            and res['askPx'] is not None
            and float(res['askPx']) != 0
            and float(res['vol24h']) != 0
        }
        return price_list


async def fetch_prices_bybit(session: aiohttp.ClientSession):
    url = 'https://api.bybit.com/v5/market/tickers?category=spot'
    async with session.get(url) as response:
        data = await response.json()
        price_list = {
            res["symbol"]: float(res['ask1Price'])
            for res in data["result"]['list']
            if res["symbol"].endswith('USDT')
            and res['ask1Price'] is not None
            and float(res['ask1Price']) != 0
            and float(res['volume24h']) != 0
        }
        return price_list


async def fetch_prices_huobi(session: aiohttp.ClientSession):
    url = 'https://api.huobi.pro/market/tickers'
    async with session.get(url) as response:
        data = await response.json()
        price_list = {
            res["symbol"].upper(): float(res['ask'])
            for res in data["data"]
            if res["symbol"].upper().endswith('USDT')
            and res['ask'] is not None
            and float(res['ask']) != 0
            and float(res['vol']) > 10000
        }
        return price_list


async def fetch_prices_gateio(session: aiohttp.ClientSession):
    url = 'https://api.gateio.ws/api/v4/spot/tickers'
    async with session.get(url) as response:
        data = await response.json()
        price_list = {
            res["currency_pair"].replace('_', ''): float(res['lowest_ask'])
            for res in data
            if res["currency_pair"].replace('_', '').endswith('USDT')
            and res['lowest_ask'] is not None
            and float(res['lowest_ask']) != 0


        }
        return price_list
# Не используется


async def fetch_prices_poloniex(session: aiohttp.ClientSession):
    url = 'https://api.poloniex.com/markets/ticker24h'
    async with session.get(url) as response:
        data = await response.json()
        price_list = {
            res["symbol"].replace('_', ''): float(res['ask'])
            for res in data
            if res["symbol"].replace('_', '').endswith('USDT')
            and res['ask'] is not None
            and float(res['ask']) != 0
            and float(res['amount']) != 0
        }
        return price_list


async def fetch_prices_bitget(session: aiohttp.ClientSession):
    url = 'https://api.bitget.com/api/spot/v1/market/tickers'
    async with session.get(url) as response:
        data = await response.json()
        price_list = {
            res["symbol"]: float(res['buyOne'])
            for res in data['data']
            if res["symbol"].endswith('USDT')
            and res['buyOne'] is not None
            and float(res['buyOne']) != 0
            and float(res['usdtVol']) != 0
        }
        return price_list


async def fetch_prices_probit(session: aiohttp.ClientSession):
    url = 'https://api.probit.com/api/exchange/v1/ticker'
    async with session.get(url) as response:
        data = await response.json()
        price_list = {
            res["market_id"].replace('-', ''): float(res['last'])
            for res in data['data']
            if res["market_id"].replace('-', '').endswith('USDT')
            and res['last'] is not None
            and float(res['quote_volume']) > 1
        }
        return price_list
# ?? Хз че за биржа, долгий ответ, тупые ключи


async def fetch_prices_ascendex(session: aiohttp.ClientSession):
    url = 'https://ascendex.com/api/pro/v1/ticker'
    async with session.get(url) as response:
        data = await response.json()
        price_list = {
            res["symbol"].replace('/', ''): float(res['ask'][0])
            for res in data['data']
            if res["symbol"].replace('/', '').endswith('USDT') and
            res['ask'][0] is not None
            and float(res['ask'][0]) != 0
            and float(res['ask'][0]) != 999999999
            and float(res['volume']) != 0
        }
        return price_list

#################################################################


async def fetch_all_prices() -> dict:
    async with aiohttp.ClientSession() as session:
        tasks = {
            'Binance': fetch_prices_binance(session),
            'Kucoin': fetch_prices_kucoin(session),
            'Bybit': fetch_prices_bybit(session),
            'Huobi/HTX': fetch_prices_huobi(session),
            'Poloniex': fetch_prices_poloniex(session),
            'Bitget': fetch_prices_bitget(session),
            'Ascendex': fetch_prices_ascendex(session),
            'Probit': fetch_prices_probit(session),
            'Okx': fetch_prices_okx(session),
        }

        results = await asyncio.gather(*tasks.values(), return_exceptions=True)
        all_prices = {}

        if DEBUG:
            print('\n'*2,
                  '='*10,
                  'AMOUNT OF PAIRS',
                  '='*10,
                  '\n'*2,)

            for exchange, result in zip(tasks.keys(), results):
                if isinstance(result, Exception):
                    print(f"Ошибка при запросе к {exchange}: {result}")
                else:
                    print(f"{exchange}: {len(result)} пар")

        for exchange, result in zip(tasks.keys(), results):
            if isinstance(result, Exception):
                print(f"Ошибка при запросе к {exchange}: {result}")
            else:
                all_prices[exchange] = result

    return all_prices


def filter_prices(prices_dict: dict):
    filtered_dict = {}

    for exchange, pairs in prices_dict.items():
        for pair, price in pairs.items():
            filtered_dict.setdefault(pair, []).append({exchange: price})

    filtered_dict = {pair: data for pair,
                     data in filtered_dict.items() if len(data) >= 2}

    if DEBUG:
        print('\n'*2,
              '='*10,
              'FILTERED DICT PRICES',
              '='*10,
              '\n'*2,)
        for pair, data in filtered_dict.items():
            print(pair, data)

    return filtered_dict


def sort_prices(filtered_dict: dict):
    sorted_list = []

    for pair, price_list in filtered_dict.items():
        first_exchange = ''
        min_price = float('inf')
        second_exchange = ''
        max_price = -float('inf')

        for price_dict in price_list:
            for exchange, price in price_dict.items():
                if price < min_price:
                    min_price = price
                    first_exchange = exchange
                if price > max_price:
                    max_price = price
                    second_exchange = exchange

        if min_price > 0:
            percent = ((max_price - min_price) / min_price) * 100
        else:
            percent = 0

        if percent < 1:
            continue
        sorted_list.append({
            pair: round(percent, 3),
            'Buy': {
                'Exchange': first_exchange,
                'Price': min_price
            },
            'Sell': {
                'Exchange': second_exchange,
                'Price': max_price
            }
        })

    # Сортировка списка по процентам (по убыванию)
    sorted_list = sorted(sorted_list, key=lambda x: list(
        x.values())[0], reverse=True)

    return sorted_list


async def main():

    all_prices = await fetch_all_prices()

    if not all_prices:
        logging.error("Не удалось получить данные с бирж.")
        return {}

    filtered_prices = filter_prices(all_prices)
    sorted_prices = sort_prices(filtered_prices)
    if DEBUG:
        print('\n'*2,
              '='*10,
              'SORTED PRICES',
              '='*10,
              '\n'*2,)
        for el in sorted_prices:
            print(el)

    try:
        with open('response.csv', 'w', newline='') as res:
            writer = csv.writer(res)
            writer.writerow(['Pair', 'Percent', 'Where to Buy',
                            'Price', 'Where to sell', 'Price'])
            for el in sorted_prices:
                row = [list(el)[0], el[list(el)[0]], el[list(el)[1]]['Exchange'], el[list(
                    el)[1]]['Price'], el[list(el)[2]]['Exchange'], el[list(el)[2]]['Price']]
                writer.writerow(row)
    except Exception as e:
        print(f"Error: {e}")

    return sorted_prices

if __name__ == '__main__':
    while True:
        asyncio.run(main())
