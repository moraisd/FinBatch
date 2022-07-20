import csv


def read_csv(func):
    def inner(data):
        csv_data = csv.reader(data.splitlines(), delimiter=',', quotechar='"')
        csv_data.__next__()  # ignore header
        return func(csv_data)

    return inner
