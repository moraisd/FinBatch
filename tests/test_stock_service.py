import json
import os
from unittest import TestCase
from unittest.mock import patch, MagicMock, call

from pymongo import UpdateOne

from config.config_reader import get_root_dir
from stock import stock_service


@patch('scheduler.stock_service.companies_dao')
@patch('scheduler.stock_service.rest_api.get_data')
@patch('scheduler.stock_service.get_config')
@patch('scheduler.stock_service.process_stock')
class StockServiceTest(TestCase):

    def setUp(self) -> None:
        self.stock_service = stock_service
        self.rest_symbol_data = {'AAPL', 'KO', 'ALV', 'OAS', 'TSN'}
        super().setUp()

    def test_update_stocks(self, process_stock, get_config, rest_api_get_data, companies_dao):
        with open(os.path.join(get_root_dir(), os.path.dirname(__file__), 'sample_stock_json_data.json'),
                  'r') as json_file:
            json_data = json.load(json_file)
            companies_dao.find_most_outdated_stocks.return_value = self.rest_symbol_data
            rest_api_get_data.return_value.json.side_effect = json_data
            self._generate_config(get_config)

            update_one_list = [MagicMock(spec=UpdateOne) for _ in json_data]
            companies_dao.prepare_update_one.side_effect = update_one_list

            self.stock_service.update_stocks()

            companies_dao.find_most_outdated_stocks.called_once_with(5)
            rest_api_get_data.assert_has_calls(
                [call(f'URL with function: OVERVIEW, Key: key_value and Symbol: {symbol}')
                 for symbol in self.rest_symbol_data], any_order='True')
            process_stock.assert_has_calls([call(stock) for stock in json_data], any_order='True')
            self.assertEqual(process_stock.call_count, 5)
            companies_dao.prepare_update_one.called_with([[stock['Symbol'], stock] for stock in json_data])
            companies_dao.bulk_write.called_once_with(update_one_list)

    def test_blacklist_stocks(self, process_stock, get_config, rest_api_get_data, companies_dao):
        symbol_list = list(self.rest_symbol_data)
        companies_dao.find_most_outdated_stocks.return_value = symbol_list
        one_blacklisted_four_processed = [{'Symbol': symbol} if symbol != 'AAPL' else {} for symbol in symbol_list]
        rest_api_get_data.return_value.json.side_effect = one_blacklisted_four_processed
        self._generate_config(get_config)

        update_one_list = [MagicMock(spec=UpdateOne) for _ in self.rest_symbol_data]
        companies_dao.prepare_update_one.side_effect = update_one_list

        self.stock_service.update_stocks()

        process_stock.assert_has_calls([call(stock) for stock in one_blacklisted_four_processed if stock],
                                       any_order='True')
        self.assertEqual(process_stock.call_count, 4)
        expected_sucessful_processed = [[stock['Symbol'], stock] for stock in one_blacklisted_four_processed if stock]
        companies_dao.prepare_update_one.called_with(expected_sucessful_processed)
        companies_dao.prepare_update_one.called_once_with('AAPL', {'blacklisted': True})
        companies_dao.bulk_write.called_once_with(update_one_list)

    @staticmethod
    def _generate_config(get_config):
        get_config.return_value = {
            'rest': {
                'fundamental_data_api': {'url': 'URL with function: $function, Key: $key and Symbol: $symbol',
                                         'key': 'key_value',
                                         'requests_per_minute': '5'}}}
