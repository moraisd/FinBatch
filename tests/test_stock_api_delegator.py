from unittest import TestCase
from unittest.mock import patch

from parameterized import parameterized

from stock import stock_api_delegator


class StockApiDelegatorTest(TestCase):

    def setUp(self):
        self.stock_api_delegator = stock_api_delegator
        super().setUp()

    @parameterized.expand(['fmp', 'alphavantage'])
    @patch('stock.stock_api_delegator.generic_rest_reader')
    @patch('stock.stock_api_delegator.fmp_reader')
    def test_get_from(self, api, fmp_reader, generic_rest_reader):

        self.stock_api_delegator.get_from(api, '')
        match api:
            case 'fmp':
                fmp_reader.read.assert_called_once_with('')
            case 'alphavantage':
                generic_rest_reader.get_stock_data.assert_called_once_with('alphavantage', 'OVERVIEW', '')

    def test_get_max_requests(self):
        config = self._generate_config()

        result = self.stock_api_delegator.get_max_requests(config)

        self.assertEqual(result, 24)

    def test_invalid_api(self):
        with self.assertRaises(RuntimeError):
            self.stock_api_delegator.get_from('invalid', '')

    @staticmethod
    def _generate_config():
        return {
            'rest': {
                'fundamental_data_api': {
                    'api_test1': {
                        'requests_per_day': 10,
                        'requests_per_stock': 1
                    },
                    'api_test2': {
                        'requests_per_day': 30,
                        'requests_per_stock': 3
                    },
                    'api_test3': {
                        'requests_per_day': 14,
                        'requests_per_stock': 3
                    }
                }
            }
        }
