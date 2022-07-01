import datetime


def process_stock(stock: dict):
    stock['LastUpdated'] = datetime.datetime.utcnow()

    __process_float(stock, 'MarketCapitalization')
    __process_float(stock, 'EBITDA')
    __process_float(stock, 'PERatio')
    __process_float(stock, 'DividendPerShare')
    __process_float(stock, 'EVToEBITDA')


def __process_float(stock: dict, key):
    try:
        stock[key] = float(stock[key])
    except ValueError:
        stock.pop(key)
