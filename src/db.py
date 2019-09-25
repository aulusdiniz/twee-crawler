#!/usr/bin/python
from pymongo import MongoClient
import settings
import os
import pdb
import bson
from pandas.io.json import json_normalize
# import subprocess


class MongoAccess(object):

    host = 'localhost'
    port = 27017
    database = 'twitter'
    client = MongoClient(host, port)


    def __init__(self):
        print("Creating database indexes to search quickly...")
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


    def export_all_tweets(self):
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


    def import_all_followers(self):
        c = settings.medias_accounts_toSearch
        for i in c[0]:
            # pdb.set_trace()
            collection = str(i) + "_followers"
            print(collection)
            self.import_collection(self.database, collection, collection)


    def import_all_tweets(self):
        c = settings.urls_toSearch
        for i in c[0]:
            # pdb.set_trace()
            collection = "tweets_" + str(i.replace(" ", "_"))
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
            print("Saving new ID ["+str(data["id"])+"] in collection ["+str(collection)+"]")
            return self.client[self.database][collection].insert_one(data)
        else:
            print("this ID is already collected")


    def delete_one(self, data, collection):
        if self.client[self.database][collection].find_one({"id": data["id"]}) != None:
            print("Deleting id ["+data["id"]+"] in collection ["+collection+"]")
            return self.client[self.database][collection].delete_one(data)
        else:
            print("ID not present in collection \n")


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
        query = {"id": {"$nin": forbArr[:100]}}
        # print(forbArr)
        ffile = open('data_bolso_lulahaddad.txt', 'w')
        result = self.skiplimit(collection, query, 5000, 1)
        for i in result:
            print(i)
        print(len(result))


    def findIntersection(self, collection, collectionCompare):
        print("Finding intersection.. this may take a while.")
        print(collection, collectionCompare)
        """ Algoritmo responsável por extrair a intersecção entre duas collections. """
        result = self.client[self.database][collection].aggregate_raw_batches([{
            "$lookup": {
                    "from": collectionCompare,
                    "localField": "id",
                    "foreignField": "id",
                    "as": "result",
                }
            },
            {
                "$match": {
                    "result": {"$ne": []}
                }
            },
            {
                "$project": {
                    "_id": 0,
                    "result": 0
                }
            }
        ])
        print("Intersection found.")

        x = []
        for itr in result:
            it = bson.decode_all(itr)
            print(it)
            print(len(it))
            x.append([it.id for it in result])
        # pdb.set_trace()
        return x


    def shuffleCollections(self):
        """ Algoritmo que faz o cruzamento das collections para fazer o cálculo da intersecção em seguida. """
        collectionsName = self.client[self.database].list_collections()
        collections = []

        print("Combinating collections to have the size of each intersection.")

        for cc in collectionsName:
            collections.append(cc)

        wArray = tuple(collections)
        wasteArr = []

        resultJSON = []

        for i in wArray:
            wasteArr.append(i['name'])
            for k in wArray:
                try:
                    if(wasteArr.index(k['name']) < 0):
                        if(("_followers" in i['name']) and ("_followers" in k['name'])):
                            if(i['name'] != k['name']):
                                # print(i['name'], k['name'])
                                resultJSON.append({
                                    "coll1": i['name'],
                                    "coll2": k['name'],
                                    # "ids": self.findIntersection(i['name'], k['name']),
                                    "qtd": len(self.findIntersection(i['name'], k['name']))
                                })


                except ValueError:
                    pass
                else:
                    if(("_followers" in i['name']) and ("_followers" in k['name'])):
                        if(i['name'] != k['name']):
                            # print(i['name'], k['name'])
                            resultJSON.append({
                                "coll1": i['name'],
                                "coll2": k['name'],
                                # "ids": self.findIntersection(i['name'], k['name']),
                                "qtd": len(self.findIntersection(i['name'], k['name']))

                            })

                            #PS: resultJSON only must be this format when it is a dict data type.
                            #PS: other way is use it as array.
        # pdb.set_trace()


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
