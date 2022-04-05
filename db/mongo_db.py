import pymongo


class MongoDb:

    def __init__(self, config: dict) -> None:
        super().__init__()
        self.config = config

    def get_database(self, db):
        my_client = pymongo.MongoClient(self.config['db']['database_url'])
        mydb = my_client[db]
        return mydb
