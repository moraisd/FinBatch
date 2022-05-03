import datetime


def process_stock(stock: dict):
    stock['LastUpdated'] = datetime.datetime.utcnow()

    __process_float(stock, 'MarketCapitalization', stock['MarketCapitalization'])
    __process_float(stock, 'EBITDA', stock['EBITDA'])
    __process_float(stock, 'PERatio', stock['PERatio'])
    __process_float(stock, 'DividendPerShare', stock['DividendPerShare'])
    __process_float(stock, 'EVToEBITDA', stock['EVToEBITDA'])


def __process_float(stock, key, value):
    try:
        stock[key] = float(value)
    except Exception:
        stock.pop(key)
