#!/usr/bin/python
import twittery
import threading
import report

# twittery.make_query()
# twittery.download_followers()
# twittery.reports()

thread1 = threading.Thread(target = twittery.make_query, args = ())
thread2 = threading.Thread(target = twittery.download_followers, args = ())
# thread1.start()
# thread2.start()

# create report data for visualization
report.start()

# threads DEBUG settings
# print("Total number of threads: ", threading.activeCount())
# print("List of threads: ", threading.enumerate())
