from pymongo.database import Database


class CompaniesDao:
    def __init__(self, database: Database):
        self.database = database

    def insert_one(self, data) -> None:
        self.database['companies'].insert_one(data)

    def update_one(self, ticker, data):
        self.database['companies'].update_one({'Symbol': ticker}, {"$set": data})

    def find_one(self, ticker) -> dict:
        return self.database['companies'].find_one({'Symbol': ticker})

    def find_all_tickers(self):
        return self.database['companies'].find({'Symbol': {"$exists": True}}, {'Symbol': True, '_id': False})

# goog_data = {
#     'Symbol': 'GOOG',
#     'AssetType': 'Common Stock',
#     'Name': 'Alphabet Inc',
#     'Exchange': 'NASDAQ',
#     'Currency': 'USD',
#     'Country': 'USA',
#     'Sector': 'TECHNOLOGY',
#     'Industry': 'SERVICES-COMPUTER PROGRAMMING, DATA PROCESSING, ETC.',
#     'MarketCapitalization': '1671384269000',
#     'EBITDA': '91144004000',
#     'PERatio': '22.59',
#     'EPS': '112.2',
#     'RevenuePerShareTTM': '385.89',
#     'ReturnOnAssetsTTM': '0.145',
#     'ReturnOnEquityTTM': '0.321',
#     'TrailingPE': '22.59',
#     'ForwardPE': '23.58',
#     'PriceToBookRatio': '7.07',
#     'EVToRevenue': '6.47',
#     'EVToEBITDA': '16.1',
#     'SharesOutstanding': '315639000',
# }
#
# CompaniesDao().update('GOOG', goog_data)
