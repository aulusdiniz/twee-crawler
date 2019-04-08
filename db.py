from pymongo import MongoClient

class MongoAccess(object):

    host = 'localhost'
    port = 27017
    database = 'database-followers-1'
    collection = 'jairbolsonaro_followers'
    client = MongoClient(host, port)

    def insert_one(self, data):
        return self.client[self.database][self.collection].insert_one(data).inserted_id
