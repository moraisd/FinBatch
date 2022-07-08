import json
import os
from unittest import TestCase
from unittest.mock import patch, MagicMock, call

from pymongo import UpdateOne

from config.config_reader import get_root_dir
from service import companies_service


@patch('service.companies_service.companies_dao')
@patch('service.companies_service.rest_api.get_data')
@patch('service.companies_service.get_config')
class CompaniesServiceTest(TestCase):

    def setUp(self) -> None:
        self.companies_service = companies_service
        self.rest_ticker_data = {'AAPL', 'KO', 'ALV', 'OAS', 'TSN'}
        super().setUp()

    @patch('service.companies_service.reader')
    def test_update_tickers(self, reader, get_config, rest_api_get_data, companies_dao):
        db_data = {'AAPL', 'KO', 'AMZN', 'ABCD'}
        get_config.return_value = {
            'exchange_list': ['US'],
            'rest': {'ticker_api': {'url': 'URL with Exchange: $exchange and Key: $key', 'key': 'key_value'}}}

        rest_api_get_data.return_value = MagicMock()
        rest_api_get_data.return_value.text = 'any_response'
        reader.read.return_value = self.rest_ticker_data
        companies_dao.find_all_tickers.return_value = db_data

        self.companies_service.update_tickers()

        reader.read.assert_called_once_with('any_response')
        rest_api_get_data.assert_called_once_with('URL with Exchange: US and Key: key_value')
        companies_dao.insert_tickers.assert_called_once_with({'ALV', 'OAS', 'TSN'})
        companies_dao.delete_delisted.assert_called_once_with({'AMZN', 'ABCD'})

    @patch('service.companies_service.process_stock')
    def test_update_stocks(self, process_stock, get_config, rest_api_get_data, companies_dao):
        with open(os.path.join(get_root_dir(), os.path.dirname(__file__), 'sample_stock_json_data.json'),
                  'r') as json_file:
            json_data = json.load(json_file)
            companies_dao.find_most_outdated_stocks.return_value = self.rest_ticker_data
            rest_api_get_data.return_value.json.side_effect = json_data
            get_config.return_value = {
                'rest': {
                    'fundamental_data_api': {'url': 'URL with function: $function, Key: $key and Symbol: $symbol',
                                             'key': 'key_value',
                                             'requests_per_minute': '5'}}}

            process_stock.side_effect = json_data
            update_one_list = [MagicMock(spec=UpdateOne) for _ in json_data]
            companies_dao.prepare_update_one.side_effect = update_one_list

            self.companies_service.update_stocks()

            companies_dao.find_most_outdated_stocks.called_once_with(5)
            rest_api_get_data.assert_has_calls(
                [call(f'URL with function: OVERVIEW, Key: key_value and Symbol: {ticker}')
                 for ticker in self.rest_ticker_data], any_order='True')
            process_stock.assert_has_calls([call(stock) for stock in json_data], any_order='True')
            companies_dao.prepare_update_one.called_with([[stock['Symbol'], stock] for stock in json_data])
            companies_dao.bulk_write.called_once_with(update_one_list)
