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

        self.companies_service.csv_reader.retrieve_tickers.return_value = rest_ticker_data
        self.companies_service.companies_dao.find_all_tickers.return_value = db_data

        self.companies_service.update_tickers()

        companies_dao = self.companies_service.companies_dao

        companies_dao.insert_tickers.assert_called_once_with({'V', 'VALE3', 'FB'})
        companies_dao.delete_delisted.assert_called_once_with({'ABCD'})

    def test_update_stocks(self):
        with open(os.path.join(ROOT_DIR, os.path.dirname(__file__), 'sample_stock_json_data.json'), 'r') as json_file:
            rest_stock_data = self.companies_service.rest_api.return_value = json.load(json_file)

            relevant_stock_data = {"Symbol": "KO", "EVToEBITDA": "19.47", "MarketCapitalization": "276615692000",
                                   "PERatio": "28.36"}

            companies_dao = self.companies_service.companies_dao
            companies_dao.update_stocks.assert_called_once_with('KO', relevant_stock_data)
