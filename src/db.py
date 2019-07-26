#!/usr/bin/python
from pymongo import MongoClient
import settings
import os
# import subprocess

class MongoAccess(object):

    host = 'localhost'
    port = 27017
    database = 'twitter'
    client = MongoClient(host, port)

    def __init__(self):
        print("db init...")
        c = self.client[self.database].list_collections()
        for i in c:
            collection = str(i["name"])
            self.client[self.database][collection].create_index([("id", -1)])

    def db_name(self):
        return self.database

    def export_collection(self, db, collection):
        # subprocess.call(['../export.sh'])
        os.system("mongodump  --db " + db + " --collection " + collection)

    def import_collection(self, db, collectionTarget, collectionOrigin):
        # subprocess.call(['../import.sh'])
        os.system("mongorestore --collection " + collectionTarget + " --db " + db + " ./dump/" + db + "/" + collectionOrigin + ".bson")

    def export_all_medias(self):
        c = self.client[self.database].list_collections()
        for i in c:
            if(str(i["name"]).find("tweets") > -1):
                collection = str(i["name"])
                print(collection)
                self.export_collection(self.database, collection)

    def export_all_profiles(self):
        c = self.client[self.database].list_collections()
        for i in c:
            if(str(i["name"]).find("followers") > -1):
                collection = str(i["name"])
                print(collection)
                self.export_collection(self.database, collection)

    def import_all_medias(self):
        c = settings.urls_toSearch
        for i in c:
            collection = "tweets_" + i[0][0].replace(" ","_")
            print(collection)
            self.import_collection(self.database, collection, collection)

    def import_all_profiles(self):
        c = settings.accounts_toSearch
        for i in c:
            collection = i[0][0].replace(" ","_") + "_followers"
            print(collection)
            self.import_collection(self.database, collection, collection)

    def drop_collections(self):
        c = self.client[self.database].list_collections()
        for i in c:
            collection = str(i["name"])
            print(collection)
            self.client[self.database][collection].drop()

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

    def filter1(self):
        collection = "LulaHaddad_followers"
        forbArr = self.get_followers("jairbolsonaro_followers")
        query = { "id": { "$nin": forbArr[:100] } }
        # print(forbArr)
        ffile = open('data_bolso_lulahaddad.txt', 'w')
        result = self.skiplimit(collection, query, 5000, 1)
        for i in result:
            print(i)
        print(len(result))

    def filter2(self, collection, collectionCompare):
        result = self.client[self.database][collection].aggregate([{
            "$lookup": {
                    "from": collectionCompare,
                    "localField":"id",
                    "foreignField":"id",
                    "as":"result",
                }
            },
            {"$match": {
                    "result": {"$eq": []}
                }
            },
            {"$group": {
                "_id" : None,
                # "count" : {"$sum" : 1}
                }
            }
        ])
        return result

    def skiplimit(self, collection, query, page_size, page_num):
        """returns a set of documents belonging to page number `page_num`
        where size of each page is `page_size`.
        """
        # Calculate number of documents to skip
        skips = page_size * (page_num - 1)
        # Skip and limit
        cursor = list(self.client[self.database][collection].find(query).skip(skips).limit(page_size))
        # arr = [x for x in cursor]
        # Return documents
        return cursor

    def count_collection(self, collections, type):
        c = self.client[self.database].list_collections()
        result = []
        labels = []
        for i in c:
            # print(i)
            if(type == "followers"):
                if((str(i["name"]).find("followers") > -1) and (str(i["name"]) in collections)):
                    label = str(i["name"]).split("_")[0]
                    labels.append(label)
                    result.append(self.client[self.database][i["name"]].count())

            if(type == "tweets"):
                if(str(i["name"]).find("tweets") > -1):
                    # print(str(i["name"]).split("tweets_"))
                    label = str(i["name"]).split("tweets_")[1]
                    labels.append(label)
                    result.append(self.client[self.database][i["name"]].count())

        return [result, labels]
