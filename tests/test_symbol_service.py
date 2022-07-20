from unittest import TestCase
from unittest.mock import patch


@patch('scheduler.symbol_service.companies_dao')
@patch('scheduler.symbol_service.get_config')
class TestSymbolService(TestCase):

    def test_update_symbols(self, get_config, companies_dao):
        symbol_api_data = {{'AAPL', 'KO'}, {'ALV', 'OAS', 'TSN'}}
        db_data = {'AAPL', 'KO', 'AMZN', 'ABCD'}
        get_config.return_value = {'api_1': {'url': 'URL 1 with Key: $key', 'key': 'key_value'},
                                   'api_2': {'url': 'URL 2 with Key: $key', 'key': 'key_value'}}

        get_symbols.get_from.side_effect = symbol_api_data
        companies_dao.find_all_symbols.return_value = db_data

        self.symbol_service.update_symbols()

        companies_dao.insert_symbols.assert_called_once_with({'ALV', 'OAS', 'TSN'})
        companies_dao.delete_delisted.assert_called_once_with({'AMZN', 'ABCD'})
