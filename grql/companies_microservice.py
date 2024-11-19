import logging

from gql import gql

from config import graphql_config

_log = logging.getLogger(__name__)


def retrieve_all_symbols():
    _log.info("Retrieving all symbols")

    return _run_request("""
    {
      symbols
    }
    """)['symbols']


def insert_symbols(symbols):
    _log.info("Updating symbols")
    request = """
        mutation ($companies: [CompanyInput]) {
            persistSymbols(companies: $companies)
        }
        """
    params = {'companies': symbols}
    return _run_request(request, params)


def delete_stocks(symbols):
    _log.info("Deleting stocks")
    request = """
    mutation($symbols:[String!]!){
        deleteBySymbol(symbols:$symbols)
    }
    """
    params = {'symbols': list(symbols)}
    return _run_request(request, params)


def find_most_outdated_stocks(limit):
    _log.info("Looking up outdated stocks")

    request = """
    query($limit:Int!){
        findMostOutdatedStocks(limit:$limit)
    }
    """
    params = {'limit': limit}
    return _run_request(request, params)['findMostOutdatedStocks']


def update_stocks(companies):
    _log.info("Updating stocks")

    request = """
    mutation($companies: [CompanyInput]) {
        updateCompanies(companies: $companies)
    }
    """
    params = {'companies': companies}
    _run_request(request, params)


def _run_request(request, params=None):
    return graphql_config.get_client().execute(gql(request), variable_values=params)
