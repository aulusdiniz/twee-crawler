#!/usr/bin/python
from pymongo import MongoClient
import os
# import subprocess

class MongoAccess(object):

    host = 'localhost'
    port = 27017
    database = 'twitter'
    client = MongoClient(host, port)

    def db_name(self):
        return self.database

    def export_collection(self, db, collection):
        # subprocess.call(['../export.sh'])
        os.system("mongodump  --db " + db + " --collection " + collection)

    def import_collection(self, db, collectionTarget, collectionOrigin):
        # subprocess.call(['../import.sh'])
        os.system("mongorestore --collection " + collectionTarget + " --db " + db + " ./dump/" + db + "/" + collectionOrigin + ".bson")

    def insert_one(self, data, collection):
        if self.client[self.database][collection].find_one({"id": data["id"]}) == None:
            print("saving new id "+data["id"]+" in collection "+collection+" \n")
            return self.client[self.database][collection].insert_one(data)
        else:
            print("id already collected \n")

    def delete_one(self, data, collection):
        if self.client[self.database][collection].find_one({"id": data["id"]}) != None:
            print("deleting id "+data["id"]+" in collection "+collection+" \n")
            return self.client[self.database][collection].delete_one(data)
        else:
            print("id not present in collection \n")

    def get_followers(self, collection):
        # print(dir(self.client[self.database].list_collections()))
        c = self.client[self.database].list_collections()
        for i in c:
            if((str(i["name"]).find("followers") > -1) and (str(i["name"]) == collection)):
                return [e["id"] for e in self.client[self.database][i["name"]].find({})]
                    # print((e["id"]))
                    # pass
