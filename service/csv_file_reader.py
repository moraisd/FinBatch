import csv


class CsvFileReader:

    def read_first_column(self, data: str) -> set:
        csv_data = csv.reader(data.splitlines(), delimiter=',', quotechar='"')
        csv_data.__next__()  # ignore header
        return {line[0] for line in csv_data if len(line) > 0}
