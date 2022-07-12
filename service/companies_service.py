import logging

from config.config_reader import get_config
from dao import companies_dao
from processor.stock_processor import process_stock
from rest import rest_api
from service import eod_csv_file_reader as reader

_log = logging.getLogger(__name__)


def update_tickers():
    _log.info("Updating tickers")
    ticker_set = set()
    for exchange in get_config()['exchange_list']:
        listed_stocks = rest_api.get_data(_build_ticker_url(exchange))
        ticker_set |= reader.read(listed_stocks.text)

    database_ticker_set = companies_dao.find_all_tickers()

    new_tickers = ticker_set - database_ticker_set
    delisted_tickers = database_ticker_set - ticker_set

    new_tickers_total = len(new_tickers)
    if new_tickers_total:
        _log.info(f'Number of tickers to be inserted: {new_tickers_total}')
        companies_dao.insert_tickers(new_tickers)

    delisted_tickers_total = len(delisted_tickers)
    if delisted_tickers_total:
        _log.info(f'Number of tickers to be delisted: {delisted_tickers_total}')
        companies_dao.delete_delisted(delisted_tickers)

    _log.info("Finished updating tickers")


def update_stocks():
    outdated_stocks_tickers = companies_dao.find_most_outdated_stocks(
        get_config()["rest"]["fundamental_data_api"]["requests_per_minute"])

    _log.info(f'Updating the following stock data: {outdated_stocks_tickers}')
    companies_dao.bulk_write(_retrieve_process_stocks(outdated_stocks_tickers))
    _log.info(f'Finished updating {outdated_stocks_tickers}')


def _retrieve_process_stocks(outdated_stocks_tickers):
    stocks = []
    # TODO: Implement concurrency on these requests
    for ticker in outdated_stocks_tickers:
        stock = rest_api.get_data(_build_stocks_data_url(ticker)).json()
        if stock.get('Symbol'):
            process_stock(stock)
            stocks.append(companies_dao.prepare_update_one(ticker, stock))
        else:
            _log.debug(stock)
            _log.info(f'Blacklisting {ticker}: No data found')
            stocks.append(companies_dao.prepare_update_one(ticker, {'blacklisted': True}))
    return stocks


def _build_ticker_url(exchange) -> str:
    return str((get_config()['rest']['ticker_api']['url'])
               .replace('$exchange', exchange)
               .replace('$key', get_config()['rest']['ticker_api']['key']))


def _build_stocks_data_url(ticker):
    return str((get_config()["rest"]["fundamental_data_api"]["url"])
               .replace('$function', 'OVERVIEW')
               .replace('$symbol', ticker)
               .replace('$key', get_config()["rest"]["fundamental_data_api"]["key"]))
