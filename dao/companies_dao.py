import datetime

import pymongo
from pymongo import UpdateOne
from pymongo.collection import Collection

from util.constants import return_tickers_only


class CompaniesDao:

    def __init__(self, companies_collection: Collection):
        self.companies = companies_collection

    def insert_tickers(self, tickers: set) -> None:
        self.companies.insert_many(
            [{'Symbol': ticker, 'LastUpdated': datetime.datetime.utcnow()} for ticker in tickers])

    def find_all_tickers(self) -> set:
        return {stock['Symbol'] for stock in
                self.companies.find(projection=return_tickers_only)}

    def delete_delisted(self, delisted_tickers: set) -> None:
        self.companies.delete_many({'Symbol': {'$in': list(delisted_tickers)}})

    def prepare_update_one(self, ticker, data) -> UpdateOne:
        return UpdateOne({'Symbol': ticker}, {"$set": data})

    # TODO: Run this once per program execution,
    #  store and update locally to avoid many IO op. Update on DB on a timely basis
    def find_outdated_stocks(self, limit):
        return {stock['Symbol'] for stock in
                self.companies.find({'blacklisted': {'$exists': False}}, return_tickers_only).sort(
                    'LastUpdated', pymongo.ASCENDING).limit(limit)}

    def retrieve_sectors_and_industries(self) -> list:
        return [{stock['_id']['Sector']: stock['Industry']} for stock in self.companies.aggregate(
            [{'$group': {"_id": {'Sector': "$Sector"}, 'Industry': {"$addToSet": "$Industry"}}}]) if
                stock['Industry']]

    def bulk_write(self, operations: list):
        return self.companies.bulk_write(operations)

    def find_by(self, args):
        return self.companies.find(
            {'Sector': args.get('Sector'), 'Industry': args.get('Industry'),
             args['OrderBy']: {'$exists': True}}).sort(args['OrderBy'], pymongo.ASCENDING)
