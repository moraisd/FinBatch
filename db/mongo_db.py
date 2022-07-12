import pymongo


def get_database(db_config: dict):
    my_client = pymongo.MongoClient(db_config['database_url'])
    return my_client[db_config['database']]
