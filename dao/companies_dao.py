import datetime as dt

import pymongo
from pymongo import UpdateOne

import db.mongo_db as mongo_db
from config.config_reader import get_config
from util.constants import return_tickers_only

_companies_collection = mongo_db.get_database(get_config()['db'])['companies']


def insert_tickers(tickers: set) -> None:
    _companies_collection.insert_many(
        [{'Symbol': ticker, 'LastUpdated': dt.datetime.utcnow()} for ticker in tickers])


def find_all_tickers() -> set:
    return {stock['Symbol'] for stock in
            _companies_collection.find(projection=return_tickers_only)}


def delete_delisted(delisted_tickers: set) -> None:
    _companies_collection.delete_many({'Symbol': {'$in': list(delisted_tickers)}})


def prepare_update_one(ticker, data) -> UpdateOne:
    return UpdateOne({'Symbol': ticker}, {"$set": data})


# TODO: Run this once per program execution,
#  store and update locally to avoid many IO op. Update on DB on a timely basis
def find_most_outdated_stocks(limit):
    return {stock['Symbol'] for stock in
            _companies_collection.find({'blacklisted': {'$exists': False}}, return_tickers_only).sort(
                'LastUpdated', pymongo.ASCENDING).limit(limit)}


def bulk_write(operations: list):
    return _companies_collection.bulk_write(operations)
