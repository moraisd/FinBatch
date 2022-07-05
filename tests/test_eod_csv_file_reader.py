import os.path
from unittest import TestCase

from service.eod_csv_file_reader import EodCsvFileReader
from singletons.config_singletons import ROOT_DIR


class TestEodCsvFileReader(TestCase):

    def test_retrieve_stocks_only(self):
        with open(os.path.join(ROOT_DIR, os.path.dirname(__file__), '../service/sample_stock_csv_data.csv'), 'r',
                  newline='\r') as file:  # do not split newlines '\n' to simulate REST data
            data = EodCsvFileReader().retrieve_tickers(file.readlines()[0])
            self.assertSetEqual(data, {'AA', 'AACIW', 'AADI', 'AACI', 'AACIU', 'A', 'AAC', 'AA-CG'})
