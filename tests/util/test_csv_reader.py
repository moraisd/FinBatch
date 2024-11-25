from unittest import TestCase

from util.csv_reader import read_csv


class TestCsvReader(TestCase):
    def test_read_csv_remove_header(self):
        @read_csv
        def mock_data_provider(data):
            return data

        result = mock_data_provider('HEADER\nA,B,C,D\nE,F,G,H')

        result_list = [line for line in result]

        self.assertEqual(result_list, [['A', 'B', 'C', 'D'], ['E', 'F', 'G', 'H']])
