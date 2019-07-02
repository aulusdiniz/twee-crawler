#!/usr/bin/python
import db
import time
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import style

db = db.MongoAccess()

style.use('fivethirtyeight')
xs, ys, history = [], [], []
fig = plt.figure()
# ax1 = fig.add_subplot(1,1,1)

def export_all_medias():
    db.export_all_medias()

def export_all_profiles():
    db.export_all_profiles()

def import_all_medias():
    db.import_all_medias()

def import_all_profiles():
    db.import_all_profiles()

def export_all():
    export_all_medias()
    export_all_profiles()

def import_all():
    import_all_medias()
    import_all_profiles()

def drop_collections():
    db.drop_collections()

def rm_collections_ids(origin, target):
    collection = db.get_followers(origin)
    for id in collection:
        idx = { "id": id }
        db.delete_one(idx, target)

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

def plotBarGeneral():
    collections = ["jairbolsonaro_followers", "LulaOficial_followers", "Haddad_Fernando_followers"]
    plt.suptitle('Database Report')
    plt.figure(1)
    values, labels = db.count_collection(collections, "followers")
    plt.subplot(211)
    plt.bar(labels, values)
    values, labels = db.count_collection(collections, "tweets")
    # plt.figure(2)
    plt.subplot(212)
    plt.bar(labels, values)
    print(labels)
    # plt.plot(labels, values)
    # plt.xlabel(labels)
    plt.show()

def animate(f):
    plt.clf()
    # plt.subplot(211)
    # plt.suptitle('Haddad Report')
    collections = ["Haddad_Fernando_followers"]
    values, labels = db.count_collection(collections, "followers")
    history.append(values[0])
    plt.scatter(range(0, len(history)), history)
    plt.plot(range(0, len(history)), history)

def animate2(f):
    plt.clf()
    # plt.subplot(211)
    # plt.suptitle('Haddad Report')
    collections = ["tweets_O_Globo", "tweets_Republica_de_Curitiba", "tweets_MBL_News", "tweets_News_Atual"]
    values, labels = db.count_collection(collections, "tweets")
    history.append(values[0])
    print(history)
    plt.plot(range(0, len(history)), history)
    plt.scatter(range(0, len(history)), history)

# ani = animation.FuncAnimation(fig, animate, interval=1000)
# plt.show()
