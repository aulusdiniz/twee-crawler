#!/usr/bin/python
import threading
import twittery
import report

thread1 = threading.Thread(target = twittery.make_query, args = ())
thread2 = threading.Thread(target = twittery.download_followers, args = ())
thread3 = threading.Thread(target = report.animate, args = ())
thread4 = threading.Thread(target = twittery.download_timeline, args = ())


""" Main bot threads """
thread1.start()
# thread2.start()
# thread3.start()
# thread4.start()

""" Loads backup from another bot server """
# twittery.loadBackupData()

""" Filter database ids """
# twittery.processDataGraph()


# threads DEBUG settings
# print("Total number of threads: ", threading.activeCount())
# print("List of threads: ", threading.enumerate())

# Descomente para apagar as collections mongo
# report.drop_collections()

# Descomente para exportar ou importar dados da pasta dump
# report.export_all()
# report.import_all()
