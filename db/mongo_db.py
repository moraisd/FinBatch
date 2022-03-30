import pymongo

from config.config_reader import config


def get_database(db):
    my_client = pymongo.MongoClient(config['db']['database_url'])
    mydb = my_client[db]
    return mydb


database = get_database(config['db']['database'])

