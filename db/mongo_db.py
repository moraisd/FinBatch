import pymongo


def get_database(db_config: dict):
    my_client = pymongo.MongoClient(db_config['database_url'])
    mydb = my_client[db_config['database']]
    return mydb
