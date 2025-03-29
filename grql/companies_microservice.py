import logging

from gql import gql

from config.graphql_config import get_client

_log = logging.getLogger(__name__)


async def retrieve_all_symbols():
    _log.info('Retrieving all symbols')

    return (await _run_request("""
    {
      symbols
    }
    """))['symbols']


async def insert_symbols(symbols):
    _log.info('Updating symbols')
    request = """
        mutation ($companies: [CompanyInput]) {
            persistSymbols(companies: $companies)
        }
        """
    params = {'companies': symbols}
    _log.info(f'Inserting result: {await _run_request(request, params)}')


async def delete_stocks(symbols):
    _log.info('Deleting stocks')
    request = """
    mutation($symbols:[String!]!){
        deleteBySymbol(symbols:$symbols)
    }
    """
    params = {'symbols': list(symbols)}
    await _run_request(request, params)


async def find_most_outdated_stocks(limit):
    _log.info('Looking up outdated stocks')

    request = """
    query($limit:Int!){
        findMostOutdatedStocks(limit:$limit)
    }
    """
    params = {'limit': limit}
    return (await _run_request(request, params))['findMostOutdatedStocks']


async def update_stocks(companies):
    _log.info('Updating stocks')

    request = """
    mutation($companies: [CompanyInput]) {
        updateCompanies(companies: $companies)
    }
    """
    params = {'companies': companies}
    await _run_request(request, params)


async def _run_request(request, params=None):
    async with get_client() as session:
        return await session.execute(gql(request), variable_values=params)
