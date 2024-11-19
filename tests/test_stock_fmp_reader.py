from unittest import TestCase
from unittest.mock import patch

from stock import fmp_reader


@patch('stock.fmp_reader.get_config')
@patch('stock.fmp_reader.fmpsdk')
class StockFmpReaderTest(TestCase):

    def setUp(self):
        self.fmp_reader = fmp_reader
        self.symbol = 'SYMBOL'
        self.key = 'key'
        self.config = {'rest': {'fundamental_data_api': {'fmp': {'key': self.key}}}}
        super().setUp()

    def test_complete_data(self, fmpsdk, get_config):
        get_config.return_value = self.config
        fmpsdk.company_profile.return_value = [{'symbol': self.symbol}]
        fmpsdk.key_metrics_ttm.return_value = [{'someDataTTM': 'data'}]
        fmpsdk.key_metrics.return_value = [{'someData': 'data'}, {'someData2': 'data'}]

        result = self.fmp_reader.read(self.symbol)

        self.assertDictEqual(result,
                             {'symbol': self.symbol, 'ttmFundamentalMetrics': {'someDataTTM': 'data'},
                              'annualFundamentalMetrics': [{'someData': 'data'}, {'someData2': 'data'}]})

        fmpsdk.key_metrics_ttm.assert_called_once_with(self.key, self.symbol)
        fmpsdk.key_metrics.assert_called_once_with(self.key, self.symbol)

    def test_only_profile(self, fmpsdk, get_config):
        get_config.return_value = self.config
        fmpsdk.company_profile.return_value = [{'someProfileData': 'data'}]
        fmpsdk.key_metrics_ttm.return_value = []

        self.assertDictEqual(self.fmp_reader.read(self.symbol), {'someProfileData': 'data'})

        fmpsdk.key_metrics_ttm.assert_called_once_with(self.key, self.symbol)
        fmpsdk.key_metrics.assert_not_called()

    def test_no_profile(self, fmpsdk, get_config):
        get_config.return_value = self.config
        fmpsdk.company_profile.return_value = []

        self.assertDictEqual(self.fmp_reader.read(self.symbol), {'symbol': self.symbol})

        fmpsdk.key_metrics_ttm.assert_not_called()
        fmpsdk.key_metrics.assert_not_called()

    def test_no_annual_data(self, fmpsdk, get_config):
        get_config.return_value = self.config
        fmpsdk.company_profile.return_value = [{'symbol': self.symbol}]
        fmpsdk.key_metrics_ttm.return_value = [{'someDataTTM': 'data'}]
        fmpsdk.key_metrics.return_value = []

        self.assertDictEqual(self.fmp_reader.read(self.symbol),
                         {'symbol': 'SYMBOL', 'ttmFundamentalMetrics': {'someDataTTM': 'data'}})

        fmpsdk.key_metrics_ttm.assert_called_once_with(self.key, self.symbol)
        fmpsdk.key_metrics.assert_called_once_with(self.key, self.symbol)
