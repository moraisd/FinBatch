import datetime as dt


def process_stock(stock: dict):
    stock['LastUpdated'] = dt.datetime.utcnow()

    _process_float(stock, 'MarketCapitalization')
    _process_float(stock, 'EBITDA')
    _process_float(stock, 'PERatio')
    _process_float(stock, 'DividendPerShare')
    _process_float(stock, 'EVToEBITDA')


def _process_float(stock: dict, key):
    try:
        stock[key] = float(stock[key])
    except ValueError:
        stock.pop(key)
