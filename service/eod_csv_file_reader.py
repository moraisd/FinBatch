import csv


class EodCsvFileReader:

    def retrieve_tickers(self, data: str) -> set:
        csv_data = csv.reader(data.splitlines(), delimiter=',', quotechar='"')
        csv_data.__next__()  # ignore header
        return self.__read_first_column_stocks_remove_otc(csv_data)

    def __read_first_column_stocks_remove_otc(self, csv_data):
        return {line[0] for line in csv_data if
                len(line) > 5 and line[5] == 'Common Stock' and line[3] not in ['PINK', 'OTCCE', 'OTCQB', 'OTCQX',
                                                                                'OTCGREY', 'OTCBB', 'OTCMKTS']}
