from unittest import TestCase
from unittest.mock import patch

from symbol import symbol_service


@patch('symbol.symbol_service.companies_dao')
@patch('symbol.symbol_service.symbol_api_delegator')
@patch('symbol.symbol_service.get_config')
class TestSymbolService(TestCase):

    def test_update_symbols(self, get_config, symbol_api_delegator, companies_dao):
        symbol_api_data = [{'AAPL', 'KO'}, {'ALV', 'OAS', 'TSN'}]
        db_data = {'AAPL', 'KO', 'AMZN', 'ABCD'}
        get_config.return_value = {'rest': {'symbol_api': ['alphavantage', 'eodhistoricaldata']}}

        symbol_api_delegator.get_from.side_effect = symbol_api_data
        companies_dao.find_all_symbols.return_value = db_data

        symbol_service.update_symbols()

        companies_dao.insert_symbols.assert_called_once_with({'ALV', 'OAS', 'TSN'})
        companies_dao.delete_delisted.assert_called_once_with({'AMZN', 'ABCD'})
