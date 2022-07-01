import datetime
from unittest import TestCase

from processor.stock_processor import process_stock


class TestStockProcessor(TestCase):
    def test_process_stock_successful(self):
        stock = self.__generate_stock()
        process_stock(stock)

        expected_result = self.__generate_expected_result(stock)
        self.assertDictEqual(stock, expected_result)
        self.assertIsInstance(stock['LastUpdated'], datetime.datetime)

    def test_remove_non_numeric(self):
        stock = self.__generate_stock()
        stock['PERatio'] = '-'

        process_stock(stock)

        expected_result = self.__generate_expected_result(stock)

        del expected_result['PERatio']

        self.assertDictEqual(stock, expected_result)

    def __generate_stock(self):
        stock = {
            'MarketCapitalization': '1234',
            'EBITDA': '4321',
            'PERatio': '2.34',
            'DividendPerShare': '0.41',
            'EVToEBITDA': '14.98'
        }
        return stock

    def __generate_expected_result(self, stock):
        return {
            'MarketCapitalization': 1234.0,
            'EBITDA': 4321.0,
            'PERatio': 2.34,
            'DividendPerShare': 0.41,
            'EVToEBITDA': 14.98,
            'LastUpdated': stock['LastUpdated']
        }
