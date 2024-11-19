import json
import os
from unittest import TestCase
from unittest.mock import patch

from config.config_reader import get_root_dir
from symbol import fmp_reader


class TestSymbolFmpReader(TestCase):
    def setUp(self):
        self.fmp_reader = fmp_reader
        super().setUp()

    @patch('symbol.fmp_reader.fmpsdk')
    def test_read_us_stocks(self, fmpsdk):
        with open(os.path.join(get_root_dir(), os.path.dirname(__file__), 'sample_fmp_symbol_data.json'),
                  'r') as fmp_symbol_data:

            fmpsdk.symbols_list.return_value = json.load(fmp_symbol_data)

            result = self.fmp_reader.read()

            self.assertSetEqual(result, {'AAPL', 'ACU', 'SQM', 'IBKR'})
