from util.csv_reader import read_csv


@read_csv
def read(csv_data):
    return {line[0] for line in csv_data if line[3] == 'Stock'}
