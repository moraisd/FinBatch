import logging

from config.config_reader import get_config
from dao import companies_dao
from symbol import symbol_api_delegator

_log = logging.getLogger(__name__)


def update_symbols():
    _log.info("Updating symbols")
    symbol_set = set()
    symbol_apis = get_config()['rest']['symbol_api']

    for api in symbol_apis:
        symbol_set |= symbol_api_delegator.get_from(api)

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
