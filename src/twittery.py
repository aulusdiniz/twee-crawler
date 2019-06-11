#!/usr/bin/python
import db
from tweepy.parsers import JSONParser
import tweepy
import time
import settings
# import json
# import pandas as pd

settings.init()
auth = tweepy.OAuthHandler(settings.consumer_key, settings.consumer_secret)
auth.set_access_token(settings.access_token, settings.access_token_secret)
api = tweepy.API(auth, parser=JSONParser())
db = db.MongoAccess()

def limit_handled(cursor):
    while True:
        try:
            yield cursor.next()
            print("Waiting a minute for request \n")
            time.sleep(1*60)

        except tweepy.RateLimitError:
            print("Rate limit reached \n")
            time.sleep(15*60)

        except tweepy.TweepError:
            print("Erro \n")
            # print(TweepError.message[0]['code'])

        except:
            print("Erro desconhecido. \n")

def download_followers():
    print("Start retrieve followers \n")
    while True:
        for account in settings.accounts_toSearch:
            user = api.get_user(account[0][0])
            pages = tweepy.Cursor(api.followers_ids, id=account[1][0], count=5000).pages()

            for page in limit_handled(pages):
                for id in page["ids"]:
                    follower = {
                        "id": str(id)
                    }
                    db.insert_one(follower, account[0][0]+"_followers")

def search(q):
    # print("query search is ", q)
    return api.search(q)

def query():
    for url in settings.urls_toSearch:
        data_searched = search("url:"+url[1][0])
        data = data_searched["statuses"]
        print("requesting for "+url[0][0].replace(' ','_')+" <<<<< \n")
        # print("\n")
        # print(data_searched)

        for dt in data:
            # inspect dt for filter retweeted data
            tweet = {
                "id": str(dt["user"]["id"]),
                "text": dt["text"],
                "created_at": dt["created_at"]
            }
            db.insert_one(tweet, "tweets_"+url[0][0].replace(' ','_'))

        print("Waiting 1m30 secs to make another query request \n")
        time.sleep(1.5*60)

def make_query():
    while True:
        try:
            query()

        except tweepy.RateLimitError:
            print("Rate limit reached \n")
            time.sleep(15*60)

        except tweepy.TweepError:
            print("Erro \n")

        except:
            print("Erro desconhecido. \n")
