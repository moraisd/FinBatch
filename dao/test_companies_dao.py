from unittest import TestCase
from unittest.mock import MagicMock

from dao.companies_dao import CompaniesDao


class TestCompaniesDao(TestCase):
    def setUp(self):
        self.ticker = 'AAPL'
        self.data = {'Symbol': self.ticker}
        self.mock_companies_collection = MagicMock()
        self.companies_dao = CompaniesDao(self.mock_companies_collection)
        self.sample_stocks = [self.data, {'Symbol': 'MSFT'},
                              {'Symbol': 'AMZN'}]
        self.ticker_set = {'AAPL', 'MSFT', 'AMZN'}

    def test_find_all_tickers(self):
        self.mock_companies_collection.find.return_value = self.sample_stocks

        result = self.companies_dao.find_all_tickers()

        from util.constants import return_tickers_only
        self.mock_companies_collection.find.assert_called_once_with(projection=return_tickers_only)
        self.assertSetEqual(result, self.ticker_set)

    def test_insert_tickers(self):
        self.companies_dao.insert_tickers(self.ticker_set)

        self.mock_companies_collection.insert_many.assert_called_once()

        args: list = self.mock_companies_collection.insert_many.call_args.args[0]
        self.assertIs(len(args), 3)
        self.assertIs(type(args), list)
        self.assertTrue('Symbol' and 'LastUpdated' in args[0] and args[1] and args[2])

    def test_delete_delisted(self):
        self.companies_dao.delete_delisted(self.ticker_set)

        self.mock_companies_collection.delete_many.assert_called_once_with(
            {'Symbol': {'$in': [ticker for ticker in self.ticker_set]}})

    def test_update_stocks(self):
        operations = MagicMock()
        self.companies_dao.bulk_write(operations)

        self.mock_companies_collection.bulk_write.assert_called_once_with(operations)

    def test_find_outdated_stocks(self):
        self.companies_dao.find_outdated_stocks(10)

        find_method = self.mock_companies_collection.find
        find_method.assert_called_once()

        import pymongo
        sort_method = find_method.return_value.sort
        sort_method.assert_called_once_with('LastUpdated', pymongo.ASCENDING)

        limit_method = sort_method.return_value.limit
        limit_method.assert_called_once_with(10)
