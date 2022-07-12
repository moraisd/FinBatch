import json
import os
from unittest import TestCase
from unittest.mock import patch, MagicMock, call

from pymongo import UpdateOne

from config.config_reader import get_root_dir
from service import stock_service


@patch('service.stock_service.companies_dao')
@patch('service.stock_service.rest_api.get_data')
@patch('service.stock_service.get_config')
class StockServiceTest(TestCase):

    def setUp(self) -> None:
        self.stock_service = stock_service
        self.rest_symbol_data = {'AAPL', 'KO', 'ALV', 'OAS', 'TSN'}
        super().setUp()

    @patch('service.stock_service.reader')
    def test_update_symbols(self, reader, get_config, rest_api_get_data, companies_dao):
        db_data = {'AAPL', 'KO', 'AMZN', 'ABCD'}
        get_config.return_value = {
            'exchange_list': ['US'],
            'rest': {'symbol_api': {'url': 'URL with Exchange: $exchange and Key: $key', 'key': 'key_value'}}}

        rest_api_get_data.return_value = MagicMock()
        rest_api_get_data.return_value.text = 'any_response'
        reader.read.return_value = self.rest_symbol_data
        companies_dao.find_all_symbols.return_value = db_data

        self.stock_service.update_symbols()

        reader.read.assert_called_once_with('any_response')
        rest_api_get_data.assert_called_once_with('URL with Exchange: US and Key: key_value')
        companies_dao.insert_symbols.assert_called_once_with({'ALV', 'OAS', 'TSN'})
        companies_dao.delete_delisted.assert_called_once_with({'AMZN', 'ABCD'})

    @patch('service.stock_service.process_stock')
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

    @patch('service.stock_service.process_stock')
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
