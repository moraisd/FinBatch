import datetime as dt
import json
import os
from unittest import TestCase
from unittest.mock import Mock, MagicMock

from service.companies_service import CompaniesService
from singletons.config_singletons import ROOT_DIR


class CompaniesServiceTest(TestCase):

    def setUp(self) -> None:
        self.companies_service = CompaniesService(MagicMock(spec=dict), Mock(), Mock(), Mock())
        self.rest_ticker_data = {'AAPL', 'KO', 'ALV', 'OAS', 'TSN'}
        super().setUp()

    def test_update_tickers(self):
        db_data = {'AAPL', 'KO', 'AMZN', 'ABCD'}

        self.companies_service.config.__getitem__.side_effect = [['any'], {'ticker_api': {'url': 'any'}},
                                                                 {'ticker_api': {'key': 'any'}}]
        self.companies_service.csv_reader.retrieve_tickers.return_value = self.rest_ticker_data
        self.companies_service.companies_dao.find_all_tickers.return_value = db_data

        self.companies_service.update_tickers()

        companies_dao = self.companies_service.companies_dao

        companies_dao.insert_tickers.assert_called_once_with({'ALV', 'OAS', 'TSN'})
        companies_dao.delete_delisted.assert_called_once_with({'AMZN', 'ABCD'})

    def test_update_stocks(self):
        with open(os.path.join(ROOT_DIR, os.path.dirname(__file__), '../service/sample_stock_json_data.json'),
                  'r') as json_file:
            json_data = json.load(json_file)
            self.companies_service.companies_dao.find_most_outdated_stocks.return_value = self.rest_ticker_data
            response = Mock()
            self.companies_service.rest_api.request_get_data.return_value = response
            response.json.side_effect = json_data
            self.companies_service.config.__getitem__.side_effect = [
                {'fundamental_data_api': {'requests_per_minute': 5}}, {'fundamental_data_api': {'url': 'any'}},
                {'fundamental_data_api': {'key': 'any'}}, {'fundamental_data_api': {'url': 'any'}},
                {'fundamental_data_api': {'key': 'any'}}, {'fundamental_data_api': {'url': 'any'}},
                {'fundamental_data_api': {'key': 'any'}}, {'fundamental_data_api': {'url': 'any'}},
                {'fundamental_data_api': {'key': 'any'}}, {'fundamental_data_api': {'url': 'any'}},
                {'fundamental_data_api': {'key': 'any'}}]

            self.companies_service.update_stocks()

            now = dt.datetime.utcnow()
            for stock in json_data:
                stock['LastUpdated'] = now

            self.companies_service.companies_dao.find_most_outdated_stocks.called_once_with(5)
            # self.companies_service.companies_dao.prepare_update_one.called_once_with(json_data)
