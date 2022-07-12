import datetime as dt

import pymongo
from pymongo import UpdateOne

import db.mongo_db as mongo_db
from config.config_reader import get_config
from util.constants import return_symbols_only

_companies_collection = mongo_db.get_database(get_config()['db'])['companies']


def insert_symbols(symbols: set) -> None:
    _companies_collection.insert_many(
        [{'Symbol': symbol, 'LastUpdated': dt.datetime.utcnow()} for symbol in symbols])


def find_all_symbols() -> set:
    return {stock['Symbol'] for stock in
            _companies_collection.find(projection=return_symbols_only)}


def delete_delisted(delisted_symbols: set) -> None:
    _companies_collection.delete_many({'Symbol': {'$in': list(delisted_symbols)}})


def prepare_update_one(symbol, data) -> UpdateOne:
    return UpdateOne({'Symbol': symbol}, {"$set": data})


# TODO: Run this once per program execution,
#  store and update locally to avoid many IO op. Update on DB on a timely basis
def find_most_outdated_stocks(limit):
    return {stock['Symbol'] for stock in
            _companies_collection.find({'blacklisted': {'$exists': False}}, return_symbols_only).sort(
                'LastUpdated', pymongo.ASCENDING).limit(limit)}


def bulk_write(operations: list):
    return _companies_collection.bulk_write(operations)
