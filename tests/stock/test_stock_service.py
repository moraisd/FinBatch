import json
import os
from unittest import TestCase
from unittest.mock import patch

from config.config_reader import get_root_dir
from stock import stock_service


@patch('stock.stock_service.companies_microservice')
@patch('stock.stock_service.stock_api_delegator')
@patch('stock.stock_service.get_config')
class StockServiceTest(TestCase):

    def setUp(self) -> None:
        self.stock_service = stock_service
        self.rest_symbol_data = ['AAPL', 'KO', 'ALV', 'OAS', 'TSN']
        super().setUp()

    def test_update_stocks(self, get_config, stock_api_delegator, companies_microservice):
        with open(os.path.join(get_root_dir(), os.path.dirname(__file__), 'sample_stock_json_data_alphavantage.json'),
                  'r') as alphavantage_json_file, open(os.path.join(get_root_dir(), os.path.dirname(__file__),
                                                                    'sample_stock_json_data_fmp.json'),
                                                       'r') as fmp_json_file:
            alphavantage_json = json.load(alphavantage_json_file)
            fmp_json = json.load(fmp_json_file)
            max_requests = len(self.rest_symbol_data)
            self._generate_config(get_config)
            stock_api_delegator.get_max_requests.return_value = max_requests
            sample_data = [stock for stock in alphavantage_json] + [stock for stock in fmp_json]
            stock_api_delegator.get_from.side_effect = sample_data
            companies_microservice.find_most_outdated_stocks.return_value = self.rest_symbol_data

            self.stock_service.update_stocks()

            companies_microservice.find_most_outdated_stocks.assert_called_once_with(max_requests)
            self.assertEqual(stock_api_delegator.get_from.call_count, max_requests)
            self.assertListEqual(sample_data,
                                 companies_microservice.update_stocks.call_args.args[0])

    @staticmethod
    def _generate_config(get_config):
        get_config.return_value = {
            'thread_pool_executor': {
                'max_workers': 250
            },
            'rest': {
                'fundamental_data_api': {
                    'fmp':
                        {
                            'url': 'URL with function: $function, Key: $key and Symbol: $symbol',
                            'key': 'key_value',
                            'requests_per_day': 3,
                            'requests_per_stock': 1
                        },
                    'alphavantage':
                        {
                            'url': 'Second URL with Key: $key, requests per day: $requests_per_day and requests per '
                                   'stock: $requests_per_stock',
                            'key': 'key value 2',
                            'requests_per_day': 2,
                            'requests_per_stock': 1

                        }
                }
            }}
