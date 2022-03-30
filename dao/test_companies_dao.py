from unittest import TestCase
from unittest.mock import MagicMock

from dao.companies_dao import CompaniesDao


class TestCompaniesDao(TestCase):
    def setUp(self):
        self.ticker = 'AAPL'
        self.data = 'Apple'
        self.mock_database = MagicMock()
        self.companies_dao = CompaniesDao(self.mock_database)

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
        self.companies_dao.find_one(self.ticker)

        self.mock_database.__getitem__.assert_called_once_with('companies')

        collection = self.mock_database['companies']
        collection.find_one.assert_called_once_with({'Symbol': self.ticker})

    def test_find_all_tickers(self):
        self.companies_dao.find_all_tickers()

        self.mock_database.__getitem__.assert_called_once_with('companies')

        collection = self.mock_database['companies']
        collection.find.assert_called_once_with({'Symbol': {"$exists": True}}, {'Symbol': True, '_id': False})
