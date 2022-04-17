import pymongo
from pymongo import UpdateOne
from pymongo.collection import Collection

from util.constants import return_tickers_only


class CompaniesDao:

    def __init__(self, companies_collection: Collection):
        self.companies = companies_collection

    def insert_one(self, data) -> None:
        self.companies.insert_one(data)

    def insert_tickers(self, tickers: set) -> None:
        self.companies.insert_many([{'Symbol': ticker} for ticker in tickers])

    def update_one(self, ticker: str, data) -> None:
        self.companies.update_one({'Symbol': ticker}, {"$set": data})

    def find_one(self, ticker: str) -> dict:
        return self.companies.find_one({'Symbol': ticker})

    def find_all_tickers(self) -> set:
        return {field.get('Symbol') for field in
                self.companies.find(projection=return_tickers_only)}

    def delete_delisted(self, delisted_tickers: set) -> None:
        self.companies.delete_many({'Symbol': {'$in': list(delisted_tickers)}})

    def update_stocks(self, stocks_data: list):
        return self.companies.bulk_write(
            [UpdateOne({'Symbol': stock['Symbol']}, stock) for stock in stocks_data]
        )

    def find_outdated_stocks(self, limit):
        return {
            self.companies.find(projection=return_tickers_only).sort('lastUpdated', pymongo.DESCENDING).limit(limit)}
