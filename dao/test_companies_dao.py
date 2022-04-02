from unittest import TestCase
from unittest.mock import MagicMock

from dao.companies_dao import CompaniesDao
from util.constants import symbol_exists_filter, return_tickers_only


class TestCompaniesDao(TestCase):
    def setUp(self):
        self.ticker = 'AAPL'
        self.data = {'Symbol': self.ticker, 'Price': '10'}
        self.mock_database = MagicMock()
        self.companies_dao = CompaniesDao(self.mock_database)
        self.sample_dict = [self.data, {'Symbol': 'MSFT', 'Price': '11'},
                            {'Symbol': 'AMZN', 'Price': '12'}]

    def test_insert_one(self):
        self.companies_dao.insert_one(self.data)

        self.mock_database.__getitem__.assert_called_once_with('companies')

        collection = self.mock_database['companies']
        collection.insert_one.assert_called_once_with(self.data)

    def test_update_and_replacing(self):
        self.companies_dao.update_one(self.ticker, self.data)

        self.mock_database.__getitem__.assert_called_once_with('companies')

        collection = self.mock_database['companies']
        collection.update_one.assert_called_once_with({'Symbol': self.ticker}, {"$set": self.data})

    def test_find_one(self):
        collection = self.mock_database['companies']
        collection.find_one.return_value = self.data

        result = self.companies_dao.find_one(self.ticker)

        collection.find_one.assert_called_once_with({'Symbol': self.ticker})
        self.assertDictEqual(result, self.data)

    def test_find_all_tickers(self):
        collection = self.mock_database['companies']
        collection.find.return_value = self.sample_dict

        result = self.companies_dao.find_all_tickers()
        collection.find.assert_called_once_with(symbol_exists_filter, return_tickers_only)
        self.assertListEqual(result, ['AAPL', 'MSFT', 'AMZN'])
