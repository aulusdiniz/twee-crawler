#!/usr/bin/python
import db

db = db.MongoAccess()

def rm_collections_ids(origin, target):
    collection = db.get_followers(origin)

    for id in collection:
        idx = { "id": id }
        db.delete_one(idx, target)

def add_collections_ids(origin, target):
    collection = db.get_followers(origin)

    for id in collection:
        idx = { "id": id }
        db.insert_one(idx, target)

def export_data():
    db.export_collection("twitter","jairbolsonaro_followers")

def import_data():
    db.import_collection("twitter","bolsonaro_lula_haddad","jairbolsonaro_followers")

def start():
    print("\n\n This may take time! please, wait until the end... \n\n")
    originAColl = "LulaOficial_followers"
    originBColl = "Haddad_Fernando_followers"
    targetABColl = "LulaHaddad_followers"
    subColl = "jairbolsonaro_followers"
    resColl = "bolsonaro_lula_haddad"

    print("\n Making LulaHaddad_followers \n")
    # add lula and haddad followers
    add_collections_ids(originAColl, targetABColl)
    add_collections_ids(originBColl, targetABColl)

    print("\n copy LulaHaddad_followers \n")
    # add jairbolsonaro_followers for operations
    add_collections_ids(subColl, resColl)

    # remove lula and haddad followers from jairbolsonaro_followers
    rm_collections_ids(targetABColl, resColl)

    print("\n ---------- the processing has finished ---------- \n")
