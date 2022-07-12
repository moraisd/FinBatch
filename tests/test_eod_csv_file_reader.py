import os.path
from unittest import TestCase

import service.eod_csv_file_reader as eod_reader
from config.config_reader import get_root_dir


class TestEodCsvFileReader(TestCase):

    def test_retrieve_non_otc_stocks_only(self):
        with open(os.path.join(get_root_dir(), os.path.dirname(__file__), 'sample_stock_csv_data.csv'), 'r',
                  newline='\r') as file:  # do not split newlines '\n' to simulate REST data
            data = eod_reader.read(file.readlines()[0])
            self.assertSetEqual(data, {'AA', 'AACIW', 'AADI', 'AACI', 'AACIU', 'A', 'AAC', 'AA-CG'})
