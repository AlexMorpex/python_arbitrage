import aiohttp
import asyncio


filter_dict = {'STRKUSDT', 'AXSUSDT', 'INJUSDT', 'PENDLEUSDT', 'DOGEUSDT',
               'ADAUSDT', 'SUIUSDT', 'EGLDUSDT', 'AVAXUSDT', 'LDOUSDT',
               'AAVEUSDT', 'DOTUSDT', 'UNIUSDT', 'XRPUSDT', 'SOLUSDT',
               'BCHUSDT', 'NEARUSDT', 'BATUSDT', 'DYDXUSDT', 'IMXUSDT',
               'LTCUSDT', 'SANDUSDT', 'ATOMUSDT', 'EOSUSDT', 'FLOKIUSDT',
               'GMXUSDT', 'PEPEUSDT', 'SNXUSDT', 'ENJUSDT', 'SHIBUSDT',
               'FXSUSDT', 'RENDERUSDT', 'WOOUSDT', 'SUSHIUSDT', 'LRCUSDT',
               'ETCUSDT', 'FILUSDT', 'FETUSDT', 'CRVUSDT', 'GRTUSDT',
               'BTCUSDT', 'ICPUSDT', 'COMPUSDT', 'APEUSDT', 'POLUSDT',
               'WLDUSDT', 'JUPUSDT', 'OPUSDT', 'ETHUSDT', 'ORDIUSDT',
               'LINKUSDT', 'MANAUSDT', 'BONKUSDT', 'MASKUSDT', 'XTZUSDT',
               'ZROUSDT', 'CHZUSDT', 'BOMEUSDT', 'BLURUSDT', 'APTUSDT',
               'FTMUSDT', 'ARBUSDT', 'WIFUSDT', 'XLMUSDT', 'ZRXUSDT'}


async def fetch_prices_binance():
    url = 'https://api.binance.com/api/v3/ticker/price'
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            data = await response.json()  # Асинхронное получение JSON
            price_list = {res['symbol']: float(res['price'])
                          for res in data
                          if res['symbol'] in filter_dict
                          }
            price_list = dict(sorted(price_list.items()))
    return price_list


async def fetch_prices_kucoin():
    url = 'https://api.kucoin.com/api/v1/market/allTickers'
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            data = await response.json()
            price_list = {
                res['symbol'].replace('-', ''): float(res['buy'])
                for res in data['data']['ticker']
                if res['symbol'].replace('-', '') in filter_dict and res['buy'] is not None}
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
                if res['instId'].replace('-', '') in filter_dict}
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
                if res["symbol"] in filter_dict}
            price_list = dict(sorted(price_list.items()))
            return price_list


async def fetch_prices_crypto_com():
    url = 'https://api.crypto.com/v2/public/get-ticker'
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            data = await response.json()
            price_list = {
                res["i"].replace('_', ''): float(res['k'])
                for res in data["result"]["data"]
                if res["i"].replace('_', '') in filter_dict}
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
                if res["symbol"].upper() in filter_dict}
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
                if res["currency_pair"].replace('_', '') in filter_dict}
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
                if res["symbol"].replace('_', '') in filter_dict}
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
                if res["symbol"] in filter_dict}
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
                if res["market_id"].replace('-', '') in filter_dict}
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
                if res["symbol"].replace('/', '') in filter_dict}
            price_list = dict(sorted(price_list.items()))
            return price_list


# Сравнение цен
async def compare_prices():
    # Собираем цены с разных бирж
    binance_prices = await fetch_prices_binance()
    kucoin_prices = await fetch_prices_kucoin()
    okx_prices = await fetch_prices_okx()
    bybit_prices = await fetch_prices_bybit()
    crypto_com_prices = await fetch_prices_crypto_com()
    huobi_prices = await fetch_prices_huobi()
    poloniex_prices = await fetch_prices_poloniex()
    bitget_prices = await fetch_prices_bitget()
    ascendex_prices = await fetch_prices_ascendex()

    # gateio_prices = await fetch_prices_gateio()       # Есть пустые значения
    # probit_prices = await fetch_prices_probit()         # Есть NoneType

#################################################################


async def compare_prices():
    # Собираем цены с разных бирж
    tasks = [
        fetch_prices_binance(),
        fetch_prices_kucoin(),
        fetch_prices_okx(),
        fetch_prices_bybit(),
        fetch_prices_crypto_com(),
        fetch_prices_huobi(),
        fetch_prices_poloniex(),
        fetch_prices_bitget(),
        fetch_prices_ascendex(),
    ]

    # Асинхронно получаем данные
    all_prices = await asyncio.gather(*tasks)

    # Биржи для идентификации
    exchanges = [
        "Binance", "KuCoin", "OKX", "Bybit", "Crypto.com",
        "Huobi", "Bitget", "AscendEX"
    ]

    # Объединяем данные в единый словарь
    combined_prices = {}
    for exchange, prices in zip(exchanges, all_prices):
        for pair, price in prices.items():
            if pair not in combined_prices:
                combined_prices[pair] = []
            combined_prices[pair].append((price, exchange))

    # Сравнение минимальных и максимальных цен
    results = []
    for pair, price_data in combined_prices.items():
        if len(price_data) < 2:  # Пропускаем пары с данными только с одной биржи
            continue

        min_price, min_exchange = min(price_data, key=lambda x: x[0])
        max_price, max_exchange = max(price_data, key=lambda x: x[0])
        percent_diff = ((max_price - min_price) / min_price) * 100

        results.append({
            "pair": pair,
            "min_price": min_price,
            "min_exchange": min_exchange,
            "max_price": max_price,
            "max_exchange": max_exchange,
            "percent_diff": percent_diff
        })

    # Сортировка по убыванию разницы в процентах
    sorted_results = sorted(
        results, key=lambda x: x["percent_diff"], reverse=False)

    # Вывод результатов
    for idx, data in enumerate(sorted_results, start=1):
        print(f"{idx}. Пара: {data['pair']}")
        print(f"   Минимальная цена: {
              data['min_price']} (Биржа {data['min_exchange']})")
        print(f"   Максимальная цена: {
              data['max_price']} (Биржа {data['max_exchange']})")
        print(f"   Разница в процентах: {data['percent_diff']:.2f}%\n")


# Запуск анализа

while True:
    asyncio.run(compare_prices())
