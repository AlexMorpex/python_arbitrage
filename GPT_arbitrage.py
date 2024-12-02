import ccxt

# Список бирж для анализа
exchanges = ['binance', 'kraken', 'mexc', 'kucoin']

# Пара для анализа
pair = 'BTC/USDT'

# Функция для получения цен


def get_prices(exchanges, pair):
    prices = {}
    for exchange_name in exchanges:
        try:
            exchange = getattr(ccxt, exchange_name)()
            ticker = exchange.fetch_ticker(pair)
            prices[exchange_name] = ticker['last']
        except Exception as e:
            print(f"Ошибка при подключении к {exchange_name}: {e}")
    return prices

# Анализ арбитражных возможностей


def analyze_arbitrage(prices):
    if len(prices) < 2:
        print("Недостаточно данных для анализа.")
        return
    sorted_prices = sorted(prices.items(), key=lambda x: x[1])
    lowest = sorted_prices[0]
    highest = sorted_prices[-1]
    profit = highest[1] - lowest[1]
    print(f"Самая низкая цена: {lowest[0]} - {lowest[1]:.2f}")
    print(f"Самая высокая цена: {highest[0]} - {highest[1]:.2f}")
    print(f"Возможный профит: {profit:.2f} USDT")


# Основная программа
if __name__ == "__main__":
    prices = get_prices(exchanges, pair)
    print("Цены на биржах:")
    for exchange, price in prices.items():
        print(f"{exchange}: {price:.2f} USDT")
    analyze_arbitrage(prices)
