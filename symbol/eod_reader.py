from util.csv_reader import read_csv


@read_csv
def read(csv_data):
    return {line[0] for line in csv_data if
            len(line) > 6  # Avoids previously sent broken data
            and line[5] == 'Common Stock'
            and line[3] not in {'PINK', 'OTCCE', 'OTCQB', 'OTCQX', 'OTCGREY', 'OTCBB', 'OTCMKTS'}}
