from math import floor

from stock import fmp_reader, fmp_processor, alphavantage_processor
from stock import generic_rest_reader


def get_from(api, symbol):
    match api:
        case 'fmp':
            stock = fmp_reader.read(symbol)
            return fmp_processor.process(stock)
        case 'alphavantage':
            stock = generic_rest_reader.get_stock_data(api, 'OVERVIEW', symbol)
            return alphavantage_processor.process(stock)
        case _:
            raise RuntimeError(f'No support for API named {api} found!')


def get_max_requests(config):
    total = 0
    apis = config['rest']['fundamental_data_api']
    for api in apis:
        total += floor(apis[api]['requests_per_day'] / apis[api]['requests_per_stock'])
    return total
