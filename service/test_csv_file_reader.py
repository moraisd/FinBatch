from unittest import TestCase

from service.csv_file_reader import CsvFileReader


class TestCsvFileReader(TestCase):

    def setUp(self) -> None:
        self.csv_file_reader = CsvFileReader()
        super().setUp()

    def test_read_first_column(self):
        with open('../sample_stock_csv_data.csv', 'r',
                  newline='\r') as file:  # do not split newlines '\n' to simulate rest data
            data = self.csv_file_reader.read_first_column(file.readlines()[0])
            print(data)
