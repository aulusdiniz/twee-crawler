#!/usr/bin/python
import twittery
import threading

# twittery.make_query()
# twittery.download_followers()
# twittery.reports()
thread1 = threading.Thread(target = twittery.make_query, args = ())
thread2 = threading.Thread(target = twittery.download_followers, args = ())
thread1.start()
thread2.start()

# print("Total number of threads: ", threading.activeCount())
# print("List of threads: ", threading.enumerate())
