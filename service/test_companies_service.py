import json
import os
from unittest import TestCase
from unittest.mock import Mock, MagicMock

from service.companies_service import CompaniesService
from singletons.config_singletons import ROOT_DIR


class CompaniesServiceTest(TestCase):

    def setUp(self) -> None:
        self.companies_service = CompaniesService(MagicMock(), Mock(), Mock(), Mock())
        super().setUp()

    def test_update_tickers(self):
        rest_ticker_data = {'AAPL', 'MSFT', 'AMZN', 'FB', 'V', 'VALE3'}
        db_data = {'AAPL', 'MSFT', 'AMZN', 'ABCD'}

        self.companies_service.config.__getitem__.side_effect = [['any'], {'ticker_api': {'url': 'any'}},
                                                                 {'ticker_api': {'key': 'any'}}]
        self.companies_service.csv_reader.retrieve_tickers.return_value = rest_ticker_data
        self.companies_service.companies_dao.find_all_tickers.return_value = db_data

        self.companies_service.update_tickers()

        companies_dao = self.companies_service.companies_dao

        companies_dao.insert_tickers.assert_called_once_with({'V', 'VALE3', 'FB'})
        companies_dao.delete_delisted.assert_called_once_with({'ABCD'})

    def test_update_stocks(self):
        with open(os.path.join(ROOT_DIR, os.path.dirname(__file__), 'sample_stock_json_data.json'), 'r') as json_file:
            json_data = json.load(json_file)
            self.companies_service.companies_dao.find_outdated_stocks.return_value = json_data

            # self.companies_service.rest_api.request_get_data.side_effect =

            [stock for stock in json_data]

            result = self.companies_service.update_stocks()

            self.assertListEqual(result, json_data)
