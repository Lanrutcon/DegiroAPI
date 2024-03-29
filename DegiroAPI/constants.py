actions = {
    "buy": 0,
    "sell": 1
}

order_types = {
    "limited": 0,
    "stop_limited": 1,
    "market_order": 2,
    "stop_loss": 3
}

time_types = {
    "day": 1,
    "permanent": 3
}

product_types = {
    "all": None,
    "shares": 1,
    "bonds": 2,
    "futures": 7,
    "options": 8,
    "invest_funds": 13,
    "leverage_products": 14,
    "etfs": 131,
    "cfds": 535,
    "warrants": 536
}

sort = {
    "asc": "asc",
    "desc": "desc"
}

base_trade_url = 'https://trader.degiro.nl'

base_headers = {"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36"}