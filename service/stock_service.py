import logging

from config.config_reader import get_config
from dao import companies_dao
from processor.stock_processor import process_stock
from rest import rest_api
from service import eod_csv_file_reader as reader

_log = logging.getLogger(__name__)


def update_symbols():
    _log.info("Updating symbols")
    symbol_set = set()
    for exchange in get_config()['exchange_list']:
        listed_stocks = rest_api.get_data(_build_symbol_url(exchange))
        symbol_set |= reader.read(listed_stocks.text)

    database_symbol_set = companies_dao.find_all_symbols()

    new_symbols = symbol_set - database_symbol_set
    delisted_symbols = database_symbol_set - symbol_set

    new_symbols_total = len(new_symbols)
    if new_symbols_total:
        _log.info(f'Number of symbols to be inserted: {new_symbols_total}')
        companies_dao.insert_symbols(new_symbols)

    delisted_symbols_total = len(delisted_symbols)
    if delisted_symbols_total:
        _log.info(f'Number of symbols to be delisted: {delisted_symbols_total}')
        companies_dao.delete_delisted(delisted_symbols)

    _log.info("Finished updating symbols")


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
        stock = rest_api.get_data(_build_stocks_data_url(symbol)).json()
        if stock.get('Symbol'):
            process_stock(stock)
            stocks.append(companies_dao.prepare_update_one(symbol, stock))
        else:
            _log.debug(stock)
            _log.info(f'Blacklisting {symbol}: No data found')
            stocks.append(companies_dao.prepare_update_one(symbol, {'blacklisted': True}))
    return stocks


def _build_symbol_url(exchange) -> str:
    return str((get_config()['rest']['symbol_api']['url'])
               .replace('$exchange', exchange)
               .replace('$key', get_config()['rest']['symbol_api']['key']))


def _build_stocks_data_url(symbol):
    return str((get_config()["rest"]["fundamental_data_api"]["url"])
               .replace('$function', 'OVERVIEW')
               .replace('$symbol', symbol)
               .replace('$key', get_config()["rest"]["fundamental_data_api"]["key"]))
