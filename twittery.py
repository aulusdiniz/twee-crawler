import tweepy
import time
import json
import db
from tweepy.parsers import JSONParser

db = db.MongoAccess()

with open('config.json') as json_data_file:
    data = json.load(json_data_file)

consumer_key = data["twitter_access"]["consumer_key"]
consumer_secret = data["twitter_access"]["consumer_secret"]
access_token = data["twitter_access"]["access_token"]
access_token_secret = data["twitter_access"]["access_token_secret"]

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth, parser=JSONParser())
user = api.get_user('jairbolsonaro')
# print user.screen_name, user.followers_count

def limit_handled(cursor):
    while True:
        try:
            yield cursor.next()
            print "Waiting a minute for request ", "\n"
            time.sleep(1*60)

        except tweepy.RateLimitError:
            print "Rate limit reached ", "\n"
            time.sleep(15*60)

        except tweepy.TweepError:
            print TweepError.message
            print "\n"
            print TweepError.message[0]['code']

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

def make_query():
    data_searched = search("url:folha.com.br")
    data = data_searched["statuses"]

    for dt in data:
        # inspect dt for filter retweeted data
        tweet = {
            "id": str(dt["id"]),
            "text": dt["text"],
            "created_at": dt["created_at"]
        }
        db.insert_one(tweet, "tweets_folha")
#
# download_followers()
# make_query()
