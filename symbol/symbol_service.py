import logging

from config.config_reader import get_config
from grql import companies_microservice
from symbol import symbol_api_delegator

_log = logging.getLogger(__name__)


async def update_symbols():
    _log.info("Updating symbols")
    external_symbol_set = set()
    symbol_apis = get_config()['rest']['symbol_api']

    for api in symbol_apis:
        external_symbol_set |= symbol_api_delegator.get_from(api)

    microservice_symbol_set = set(await companies_microservice.retrieve_all_symbols())

    new_symbols = external_symbol_set - microservice_symbol_set
    delisted_symbols = microservice_symbol_set - external_symbol_set

    if new_symbols:
        _log.info(f'Number of symbols to be added: {len(new_symbols)}')
        await companies_microservice.insert_symbols(_generate_graphql_schema(new_symbols))

    if delisted_symbols:
        _log.info(f'Number of symbols to be delisted: {len(delisted_symbols)}')
        await companies_microservice.delete_stocks(delisted_symbols)

    _log.info("Finished updating symbols")


def _generate_graphql_schema(new_symbols):
    return [{'symbol': symbol} for symbol in new_symbols]
