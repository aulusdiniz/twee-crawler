#!/usr/bin/python
import threading
import twittery
import report

# twittery.make_query()
# twittery.download_followers()
# twittery.make_query()

thread1 = threading.Thread(target = twittery.make_query, args = ())
thread2 = threading.Thread(target = twittery.download_followers, args = ())
thread3 = threading.Thread(target = report.animate, args = ())
# thread1.start()
# thread2.start()
# thread3.start()

# threads DEBUG settings
# print("Total number of threads: ", threading.activeCount())
# print("List of threads: ", threading.enumerate())

# Descomente para gerar visualização gráfica
# report.plotBarGeneral()

# create report data for visualization
# report.start()

# Descomente para apagar as collections mongo
# report.drop_collections()

# Descomente para exportar ou importar dados da pasta dump
# report.export_all()
# report.import_all()
