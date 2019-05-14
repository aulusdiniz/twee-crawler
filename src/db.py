#!/usr/bin/python
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
            print("saving new id "+data["id"]+" in collection "+collection+"\n")
            return self.client[self.database][collection].insert_one(data)
        else:
            print("id already collected \n")

    def filter_by_profile(self, profile):
        # print(dir(self.client[self.database].list_collections()))
        c = self.client[self.database].list_collections()
        for i in c:
            print(i["name"], str(i["name"]).find("followers"))
            if(str(i["name"]).find("followers") > -1):
                print(self.client[self.database][i["name"]].count())
                for e in self.client[self.database][i["name"]].find({}):
                    pass
                    # print((e["id"]))
