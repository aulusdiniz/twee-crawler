#!/usr/bin/python
from tweepy.parsers import JSONParser
import db, tweepy, time, settings, math
# import json
# import pandas as pd
# global db
db = db.MongoAccess()

settings.init()
auth = tweepy.OAuthHandler(settings.consumer_key, settings.consumer_secret)
auth.set_access_token(settings.access_token, settings.access_token_secret)
api = tweepy.API(auth, parser=JSONParser())

def limit_handled(cursor):
    while True:
        try:
            # import pdb; pdb.set_trace()
            # import sys; exc_type, exc_value, tb = sys.exc_info()
            # from pprint import pprint; pprint(tb.tb_frame.f_locals)
            if(cursor.limit > cursor.next_cursor):
                yield cursor.next()
                print("Waiting a minute for request \n")
                time.sleep(1*60)
            else: pass

        except tweepy.RateLimitError:
            # import pdb; pdb.set_trace()
            import sys; exc_type, exc_value, tb = sys.exc_info()
            from pprint import pprint; pprint(tb.tb_frame.f_locals)
            print("Rate limit reached \n")
            time.sleep(15*60)

        except tweepy.TweepError:
            # import pdb; pdb.set_trace()
            import sys; exc_type, exc_value, tb = sys.exc_info()
            from pprint import pprint; pprint(tb.tb_frame.f_locals)
            print("Erro \n")

        except Exception:
            # import pdb; pdb.set_trace()
            import sys; exc_type, exc_value, tb = sys.exc_info()
            from pprint import pprint; pprint(tb.tb_frame.f_locals)
            print("Erro desconhecido. \n")

def download_followers():
    # this line defines which input take
    data = settings.medias_accounts_toSearch
    # data = settings.accounts_toSearch

    while True:
        for account in data:
            user = api.get_user(account[0][0])
            nfollowers = user["followers_count"]
            nfullpages = nfollowers/5000
            frac, dec = math.modf(nfullpages)
            print(nfollowers/5000, nfollowers%5000)
            # print(frac, dec)
            pages = []
            if ((nfollowers/5000) > 1):
                pages = tweepy.Cursor(api.followers_ids, id=account[1][0], count=500).pages(dec)
                # print(pages)
                last_page = tweepy.Cursor(api.followers_ids, id=account[1][0], count=nfollowers, page=(dec+1)).pages()
            else:
                print("len(pages)", len(pages))
                pages = tweepy.Cursor(api.followers_ids, id=account[1][0], count=nfollowers).pages()

            print("Start retrieve followers \n")
            for page in limit_handled(pages):
                count=0
                print(page)
                for id in page["ids"]:
                    # count=count+1
                    # print(count)
                    follower = {
                        "id": str(id)
                    }
                    db.insert_one(follower, account[0][0]+"_followers")

def download_timeline():
    data = settings.medias_accounts_toSearch

    print("Start retrieve followers \n")
    while True:
        for account in data:
            user = api.get_user(account[0][0])
            username = user["screen_name"]
            number_of_tweets = 200 #200 MAX
            pages = tweepy.Cursor(api.user_timeline).pages()
            for page in limit_handled(pages):
                print(page)
                # db.insert_one(follower, account[0][0]+"_followers")

            # tweets = api.user_timeline(screen_name=username, count=number_of_tweets, exclude_replies=True)
            # tweets_for_csv = [[username,tweet["id_str"], tweet["created_at"], tweet["text"].encode("utf-8")] for tweet in tweets]

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
