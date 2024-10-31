import logging

from config.config_reader import get_config
from grql import companies_microservice
from symbol import symbol_api_delegator

_log = logging.getLogger(__name__)


def update_symbols():
    _log.info("Updating symbols")
    external_symbol_list = list()
    symbol_apis = get_config()['rest']['symbol_api']

    for api in symbol_apis:
        external_symbol_list += symbol_api_delegator.get_from(api)

    microservice_symbol_set = set(companies_microservice.retrieve_all_symbols())

    external_symbol_set = {values['symbol'] for values in external_symbol_list}

    new_symbols = external_symbol_set - microservice_symbol_set
    delisted_symbols = microservice_symbol_set - external_symbol_set

    if new_symbols:
        _log.info(f'Number of symbols to be added: {len(new_symbols)}')
        companies_microservice.insert_symbols(external_symbol_list)

    if delisted_symbols:
        _log.info(f'Number of symbols to be delisted: {len(delisted_symbols)}')
        companies_microservice.delete_stocks(delisted_symbols)

    _log.info("Finished updating symbols")
