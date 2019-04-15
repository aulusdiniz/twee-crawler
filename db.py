from pymongo import MongoClient

class MongoAccess(object):

    host = 'localhost'
    port = 27017
    database = 'twitter'
    client = MongoClient(host, port)

    def insert_one(self, data):
        return self.client[self.database][self.collection].insert_one(data)

    def insert_one(self, data, collection):
        if self.client[self.database][collection].find_one({"id": data["id"]}) == None:
            print "saving new id \n"
            return self.client[self.database][collection].insert_one(data)
        else:
            print "id already collected \n"
