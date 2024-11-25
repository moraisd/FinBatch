import os
from unittest import TestCase

from config.config_reader import get_root_dir
from symbol import alphavantage_reader


class TestAlphavantageReader(TestCase):
    def test_read_stocks_only(self):
        with open(os.path.join(get_root_dir(), os.path.dirname(__file__), 'sample_alphavantage_symbol_data.csv'), 'r',
                  newline='\r') as file:  # do not split newlines '\n' to simulate REST data
            data = alphavantage_reader.read(file.readlines()[0])
            self.assertSetEqual(data,
                                {'FSK', 'FRSGU', 'FRXB-U', 'FROG', 'FSBC', 'FRXB', 'FRSH', 'FRWAW', 'FRONW', 'FSM',
                                 'FSLR', 'FRT-P-C', 'FRT', 'FRST', 'FRSX', 'FRXB-WS', 'FSEA', 'FSFG', 'FRW', 'FSLY',
                                 'FRO', 'FRPT', 'FRON', 'FRPH', 'FRONU', 'FRWAU', 'FRSG', 'FSBW', 'FSI', 'FRSGW'})
