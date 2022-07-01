import os.path
from unittest import TestCase

from service.eod_csv_file_reader import EodCsvFileReader
from singletons.config_singletons import ROOT_DIR


class TestEodCsvFileReader(TestCase):
    ticker_set = {'AA', 'AACIW', 'AADI', 'AACI', 'AACIU', 'A', 'AAC', 'AA-CG'}

    def setUp(self) -> None:
        self.csv_file_reader = EodCsvFileReader()
        super().setUp()

    def test_retrieve_stocks_only(self):
        with open(os.path.join(ROOT_DIR, os.path.dirname(__file__), '../service/sample_stock_csv_data.csv'), 'r',
                  newline='\r') as file:  # do not split newlines '\n' to simulate REST data
            data = self.csv_file_reader.retrieve_tickers(file.readlines()[0])
            self.assertSetEqual(data, self.ticker_set)
