#!/usr/bin/python
import db
from tweepy.parsers import JSONParser
import tweepy
import json
import time
import pandas as pd

# Load config data twitter api use.
with open('config.json') as config_file:
    config = json.load(config_file)

consumer_key = config["twitter_access"]["consumer_key"]
consumer_secret = config["twitter_access"]["consumer_secret"]
access_token = config["twitter_access"]["access_token"]
access_token_secret = config["twitter_access"]["access_token_secret"]
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth, parser=JSONParser())
user = api.get_user('jairbolsonaro')
# print user.screen_name, user.followers_count

#initiate database
db = db.MongoAccess()

# read the urls code should search (make it read from relative path)
csv = pd.read_csv("~/git/taurus-software/tweeter-crawler/src/input.csv")
urls_names = csv[['Nome']].values
urls = csv[['URL']].values
urls_toSearch = zip(urls_names, urls)

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
    pages = tweepy.Cursor(api.followers_ids, id=128372940, count=5000).pages()

    for page in limit_handled(pages):
        for id in page["ids"]:
            follower = {
                "id": str(id)
            }
            db.insert_one(follower, "jairbolsonaro_followers")

def search(q):
    return api.search(q)

def query():
    for url in urls_toSearch:
        data_searched = search("url:"+url[1][0])
        data = data_searched["statuses"]

        print("requesting for "+url[0][0].replace(' ','_')+" <<<<< \n")

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

def reports():
    db.filter_by_profile('jairbolsonaro')
