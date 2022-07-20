from unittest import TestCase
from unittest.mock import patch

from symbol import symbol_api_delegator


class TestSymbolApiDelegator(TestCase):

    @patch('symbol.symbol_api_delegator.from_api')
    @patch('symbol.symbol_api_delegator.alphavantage_reader')
    def test_alphavantage(self, alphavantage_reader, from_api):
        alphavantage = 'alphavantage'
        symbol_api_delegator.get_from(alphavantage)

        alphavantage_reader.read.assert_called_once_with(from_api(alphavantage).text)

    @patch('symbol.symbol_api_delegator.from_api')
    @patch('symbol.symbol_api_delegator.eod_reader')
    def test_eod(self, eod_reader, from_api):
        eod = 'eodhistoricaldata'
        symbol_api_delegator.get_from(eod)

        eod_reader.read.assert_called_once_with(from_api(eod).text)

    def test_invalid(self):
        with self.assertRaises(RuntimeError) as context:
            symbol_api_delegator.get_from('invalidAPI')

        self.assertEqual(context.exception.args[0], 'No support for API named invalidAPI found!')
