import logging
from math import floor

from config.config_reader import get_config
from grql import companies_microservice
from stock import stock_api_delegator

_log = logging.getLogger(__name__)


def update_stocks():
    max_requests = stock_api_delegator.get_max_requests(get_config())
    outdated_stocks_symbols = companies_microservice.find_most_outdated_stocks(max_requests)

    _log.info(f'Updating the following stock data: {outdated_stocks_symbols}')
    companies_microservice.update_stocks(_retrieve_process_stocks(outdated_stocks_symbols))
    _log.info(f'Finished updating {outdated_stocks_symbols}')


def _retrieve_process_stocks(outdated_stocks_symbols):
    stocks = []
    apis = get_config()['rest']['fundamental_data_api']
    for api in apis:
        for _ in range(floor(apis[api]['requests_per_day'] / apis[api]['requests_per_stock'])):
            symbol = outdated_stocks_symbols.pop()
            stock = stock_api_delegator.get_from(api, symbol)
            stocks.append(stock)

    return stocks
