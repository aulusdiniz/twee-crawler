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

def start():

    print("\n\n This may take time! please, wait until the end... \n\n")

    originAColl = "LulaOficial_followers"
    originBColl = "Haddad_Fernando_followers"
    targetABColl = "LulaHaddad_followers"
    subColl = "jairbolsonaro_followers"
    resColl = "bolsonaro_lula_haddad"
    db_name = db.db_name()

    # copy Bolsonaro followers to bolsonaro_lula_haddad collection
    db.export_collection(db_name, subColl)
    db.import_collection(db_name, resColl, subColl)

    # copy Haddad and Lula followers to LulaHaddad_followers
    db.export_collection(db_name, originAColl)
    db.export_collection(db_name, originBColl)
    db.import_collection(db_name, targetABColl, originBColl)
    db.import_collection(db_name, targetABColl, originAColl)

    # remove lula and haddad followers from jairbolsonaro_followers
    rm_collections_ids(targetABColl, resColl)

    print("\n ---------- the processing has finished ---------- \n")
