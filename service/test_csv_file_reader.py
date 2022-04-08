from unittest import TestCase

from service.csv_file_reader import EodCsvFileReader


class TestCsvFileReader(TestCase):
    ticker_set = {'0P000019EV', '0P00015KF1', '0P00015KFC', 'A', 'AA', 'AAA', 'AAAAX', 'AAACX', 'AAAEX', 'AAAFX',
                  'AAAGX', 'AAAHX', 'AAAIX', 'AAAJX', 'AAAKX', 'AAALF', 'AAALX', 'AAALY', 'AAAMX', 'AAANX', 'AAAOX',
                  'AAAPX', 'AAAQX', 'AAARX', 'AAASX', 'AAATX', 'AAAU', 'AAAUX', 'AAAVX', 'AAAWX', 'AAAZX', 'AABB',
                  'AABCX', 'AABEX', 'AABFX', 'AABGX', 'AABHX', 'AABJX', 'AABKX', 'AABOX', 'AABPX', 'AABQX', 'AABRX',
                  'AABTX', 'AABVF', 'AABVX', 'AABWX', 'AABYX', 'AABZX', 'AAC', 'AACAF', 'AACAY', 'AACCX', 'AACDX',
                  'AACFX', 'AACG', 'AACGX', 'AACHX', 'AACI', 'AACIU', 'AACIW', 'AACIX', 'AACJX', 'AACKX', 'AACLX',
                  'AACMX', 'AACOX', 'AACPX', 'AACQX', 'AACRX', 'AACS', 'AACSX', 'AACTF', 'AACTX', 'AACUX', 'AACVX',
                  'AACWX', 'AACZX', 'AADAX', 'AADBX', 'AADCX', 'AADEX', 'AADHX', 'AADI', 'AADIX', 'AADJX', 'AADKX',
                  'AADLX', 'AADMX', 'AADNX', 'AADOX', 'AADPX', 'AADQX', 'AADR', 'AADRX', 'AADSX', 'AADTX', 'AADUX',
                  'AADVX'}

    def setUp(self) -> None:
        self.csv_file_reader = EodCsvFileReader()
        super().setUp()

    def test_read_first_column(self):
        with open('../sample_stock_csv_data.csv', 'r',
                  newline='\r') as file:  # do not split newlines '\n' to simulate REST data
            data = self.csv_file_reader.retrieve_tickers(file.readlines()[0])
            self.assertSetEqual(data, self.ticker_set)
