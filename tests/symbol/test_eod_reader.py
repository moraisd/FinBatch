import os.path
from unittest import TestCase

from config.config_reader import get_root_dir
from symbol import eod_reader


class TestEodReader(TestCase):

    def test_retrieve_non_otc_stocks_only(self):
        with open(os.path.join(get_root_dir(), os.path.dirname(__file__), 'sample_eod_symbol_data.csv'), 'r',
                  newline='\r') as file:  # do not split newlines '\n' to simulate REST data
            data = eod_reader.read(file.readlines()[0])
            self.assertSetEqual(data, {'AA', 'AACIW', 'AADI', 'AACI', 'AACIU', 'A', 'AAC', 'AA-CG'})
