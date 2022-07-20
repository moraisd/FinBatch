from unittest import TestCase
from unittest.mock import MagicMock

from pymongo import UpdateOne

import dao.companies_dao as companies_dao


class TestCompaniesDao(TestCase):
    def setUp(self):
        self.symbol = 'AAPL'
        self.data = {'Symbol': self.symbol}
        self.companies_dao = companies_dao
        self.sample_stocks = [self.data, {'Symbol': 'MSFT'},
                              {'Symbol': 'AMZN'}]
        self.symbol_set = {'AAPL', 'MSFT', 'AMZN'}
        self.companies_dao._companies_collection = MagicMock()

    def test_find_all_symbols(self):
        self.companies_dao._companies_collection.find.return_value = self.sample_stocks

        result = self.companies_dao.find_all_symbols()

        from util.constants import SYMBOLS_ONLY
        self.companies_dao._companies_collection.find.assert_called_once_with(projection=SYMBOLS_ONLY)
        self.assertSetEqual(result, self.symbol_set)

    def test_insert_symbols(self):
        self.companies_dao.insert_symbols(self.symbol_set)

        self.companies_dao._companies_collection.insert_many.assert_called_once()

        args = self.companies_dao._companies_collection.insert_many.call_args.args[0]
        self.assertIs(len(args), 3)
        self.assertIs(type(args), list)
        self.assertTrue('Symbol' and 'LastUpdated' in args[0] and args[1] and args[2])

    def test_delete_delisted(self):
        self.companies_dao.delete_delisted(self.symbol_set)

        self.companies_dao._companies_collection.delete_many.assert_called_once_with(
            {'Symbol': {'$in': [symbol for symbol in self.symbol_set]}})

    def test_update_stocks(self):
        operations = MagicMock()
        self.companies_dao.bulk_write(operations)

        self.companies_dao._companies_collection.bulk_write.assert_called_once_with(operations)

    def test_find_most_outdated_stocks(self):
        self.companies_dao.find_most_outdated_stocks(10)

        find_method = self.companies_dao._companies_collection.find
        find_method.assert_called_once()

        import pymongo
        sort_method = find_method.return_value.sort
        sort_method.assert_called_once_with('LastUpdated', pymongo.ASCENDING)

        limit_method = sort_method.return_value.limit
        limit_method.assert_called_once_with(10)

    def test_prepare_update_one(self):
        stock_data = {
            'MarketCapilalization': 12345
        }

        result = self.companies_dao.prepare_update_one(self.symbol, stock_data)
        self.assertEqual(result, UpdateOne({'Symbol': self.symbol}, {"$set": stock_data}))
