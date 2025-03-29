import asyncio
import logging
from concurrent.futures import ThreadPoolExecutor
from math import floor

from config.config_reader import get_config
from grql import companies_microservice
from stock import stock_api_delegator

_log = logging.getLogger(__name__)


async def update_stocks():
    max_requests = stock_api_delegator.get_max_requests(get_config())
    outdated_stocks_symbols = await companies_microservice.find_most_outdated_stocks(max_requests)

    _log.info(f'Updating the following stock data: {outdated_stocks_symbols}')
    await companies_microservice.update_stocks(_retrieve_and_process_stocks(outdated_stocks_symbols))
    _log.info(f'Finished updating {outdated_stocks_symbols}')


def _retrieve_and_process_stocks(outdated_stocks_symbols):
    stocks_future = []
    apis = get_config()['rest']['fundamental_data_api']
    with ThreadPoolExecutor(max_workers=get_config()['thread_pool_executor']['max_workers']) as executor:
        for api in apis:
            for _ in range(floor(apis[api]['requests_per_day'] / apis[api]['requests_per_stock'])):
                symbol = outdated_stocks_symbols.pop()
                stocks_future.append(executor.submit(stock_api_delegator.get_from, api, symbol))

    return [stock.result() for stock in stocks_future]
