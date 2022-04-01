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

    def find_all_tickers(self) -> list:
        return [symbol.get('Symbol') for symbol in
                self.database['companies'].find({'Symbol': {"$exists": True}}, {'Symbol': True, '_id': False})]
