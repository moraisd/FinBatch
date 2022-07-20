import logging

from config.config_reader import get_config
from dao import companies_dao
from rest import rest_api
from stock.stock_processor import process_stock

_log = logging.getLogger(__name__)


def update_stocks():
    outdated_stocks_symbols = companies_dao.find_most_outdated_stocks(
        get_config()["rest"]["fundamental_data_api"]["requests_per_minute"])

    _log.info(f'Updating the following stock data: {outdated_stocks_symbols}')
    companies_dao.bulk_write(_retrieve_process_stocks(outdated_stocks_symbols))
    _log.info(f'Finished updating {outdated_stocks_symbols}')


def _retrieve_process_stocks(outdated_stocks_symbols):
    stocks = []
    # TODO: Implement concurrency on these requests
    for symbol in outdated_stocks_symbols:
        stock = _get_stock_data(symbol).json()
        if stock.get('Symbol'):
            process_stock(stock)
            stocks.append(companies_dao.prepare_update_one(symbol, stock))
        else:
            _log.debug(stock)
            _log.info(f'Blacklisting {symbol}: No data found')
            stocks.append(companies_dao.prepare_update_one(symbol, {'blacklisted': True}))
    return stocks


@rest_api.get_data_dec
def _get_stock_data(symbol):
    fundamental_data_api_config = get_config()["rest"]["fundamental_data_api"]
    return str((fundamental_data_api_config["url"])
               .replace('$function', 'OVERVIEW')
               .replace('$symbol', symbol)
               .replace('$key', fundamental_data_api_config["key"]))
