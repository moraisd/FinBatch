import pymongo


class MongoDb:

    def __init__(self, config: dict) -> None:
        self.config = config
        super().__init__()

    def get_database(self, db):
        my_client = pymongo.MongoClient(self.config['db']['database_url'])
        mydb = my_client[db]
        return mydb
