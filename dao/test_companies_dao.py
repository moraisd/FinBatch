from unittest import TestCase
from unittest.mock import MagicMock

from dao.companies_dao import CompaniesDao


class TestCompaniesDao(TestCase):
    def setUp(self):
        self.ticker = 'AAPL'
        self.data = {'Symbol': self.ticker, 'Price': '10'}
        self.mock_companies_collection = MagicMock()
        self.companies_dao = CompaniesDao(self.mock_companies_collection)
        self.sample_stocks = [self.data, {'Symbol': 'MSFT', 'Price': '11'},
                              {'Symbol': 'AMZN', 'Price': '12'}]
        self.ticker_set = {'AAPL', 'MSFT', 'AMZN'}

    def test_insert_one(self):
        self.companies_dao.insert_one(self.data)

        collection = self.mock_companies_collection
        collection.insert_one.assert_called_once_with(self.data)

    def test_update_and_replacing(self):
        self.companies_dao.update_one(self.ticker, self.data)

        self.mock_companies_collection.update_one.assert_called_once_with({'Symbol': self.ticker},
                                                                          {"$set": self.data})

    def test_find_one(self):
        self.mock_companies_collection.find_one.return_value = self.data

        result = self.companies_dao.find_one(self.ticker)

        self.mock_companies_collection.find_one.assert_called_once_with({'Symbol': self.ticker})
        self.assertDictEqual(result, self.data)

    def test_find_all_tickers(self):
        self.mock_companies_collection.find.return_value = self.sample_stocks

        result = self.companies_dao.find_all_tickers()

        from util.constants import return_tickers_only
        self.mock_companies_collection.find.assert_called_once_with(projection=return_tickers_only)
        self.assertSetEqual(result, self.ticker_set)

    def test_delete_delisted(self):
        self.companies_dao.delete_delisted(self.ticker_set)

        self.mock_companies_collection.delete_many.assert_called_once_with(
            {'Symbol': {'$in': [ticker for ticker in self.ticker_set]}})

    def test_update_stocks(self):
        self.companies_dao.update_stocks(self.sample_stocks)

        from pymongo import UpdateOne
        self.mock_companies_collection.bulk_write.assert_called_once_with(
            [UpdateOne({'Symbol': stock['Symbol']}, stock) for stock in self.sample_stocks])

    def test_find_outdated_stocks(self):
        self.companies_dao.find_outdated_stocks(10)

        find_method = self.mock_companies_collection.find
        find_method.assert_called_once()

        import pymongo
        sort_method = find_method.return_value.sort
        sort_method.assert_called_once_with('lastUpdated', pymongo.DESCENDING)

        limit_method = sort_method.return_value.limit
        limit_method.assert_called_once_with(10)
