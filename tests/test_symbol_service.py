from unittest import TestCase
from unittest.mock import patch

from symbol import symbol_service


@patch('symbol.symbol_service.companies_microservice')
@patch('symbol.symbol_service.symbol_api_delegator')
@patch('symbol.symbol_service.get_config')
class TestSymbolService(TestCase):

    def test_update_symbols(self, get_config, symbol_api_delegator, companies_microservice):
        symbol_api_data = [{'AAPL', 'KO'}, {'ALV', 'OAS', 'TSN'}]
        microservice_data = {'AAPL', 'KO', 'AMZN', 'ABCD'}
        get_config.return_value = {'rest': {'symbol_api': ['alphavantage', 'eodhistoricaldata']}}

        symbol_api_delegator.get_from.side_effect = symbol_api_data
        companies_microservice.retrieve_all_symbols.return_value = microservice_data

        symbol_service.update_symbols()

        companies_microservice.insert_symbols.assert_called_once()
        args = companies_microservice.insert_symbols.call_args.args[0]
        self.assertListEqual(
            sorted([{'symbol': 'ALV'}, {'symbol': 'OAS'}, {'symbol': 'TSN'}], key=lambda data: data['symbol']),
            sorted(args, key=lambda data: data['symbol']))

        companies_microservice.delete_stocks.assert_called_once_with({'AMZN', 'ABCD'})
