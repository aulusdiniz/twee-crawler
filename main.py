import tweepy
import time
import db
from tweepy.parsers import JSONParser
import json

db = db.MongoAccess()
# db.run_demo()

consumer_key = 'nAVCimcTL3xR3AvnWdRJRkLBl'
consumer_secret = 'k6A3eSyWn5CMbPpVjrV1h5BZkPa0QY6g9cJ1nviQBcDnGMo2M6'
access_token = '1016750186297688064-FUsaE4m3FwclQZTSJmTNOMefOenrwo'
access_token_secret = 'T4jK8OrtXRbosveqx55ZTMNbAcow4YusDaMY1WMmR2zd7'
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth, parser=JSONParser())
user = api.get_user('jairbolsonaro')
# print user.screen_name, user.followers_count

def limit_handled(cursor):
    while True:
        try:
            yield cursor.next()
        except tweepy.RateLimitError:
            print "tweepy.RateLimitError ", "\n"
            time.sleep(16*60)

def run():
    pages = tweepy.Cursor(api.followers_ids, id=128372940, count=5000).pages()

    for page in limit_handled(pages):
        for id in page:
            db.insert_one({
                "twitter_id": str(id),
                "user" : user.screen_name
            })

def search(q):
    return api.search(q)

# run()

data_searched = search("url:folha.com.br")
data = data_searched["statuses"]

for dt in data:
    # print dt
    for attribute, value in dt.iteritems():
        print attribute, value # example usage
    print "\n"

# print json.loads(data)
