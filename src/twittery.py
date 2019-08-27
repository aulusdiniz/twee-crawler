#!/usr/bin/python
# from tweepy.parsers import JSONParser
import db, tweepy, time, settings, math, pdb
import numpy as np
# import json
# import pandas as pd
# global db
db = db.MongoAccess()

settings.init()
auth = tweepy.OAuthHandler(settings.consumer_key, settings.consumer_secret)
auth.set_access_token(settings.access_token, settings.access_token_secret)
api = tweepy.API(auth)
# api = tweepy.API(auth, parser=JSONParser())

def limit_handled(cursor):
    try:
        # pdb.set_trace()
        # import sys; exc_type, exc_value, tb = sys.exc_info()
        # from pprint import pprint; pprint(tb.tb_frame.f_locals)
        if(len(cursor.method()) < 500):
            yield cursor.method()
        else:
            yield cursor.next()
        print("Waiting a minute for request \n")
        time.sleep(1*60)

    except tweepy.RateLimitError:
        # pdb.set_trace()
        # import sys; exc_type, exc_value, tb = sys.exc_info()
        # from pprint import pprint; pprint(tb.tb_frame.f_locals)
        print("Rate limit reached \n")
        time.sleep(15*60)

    except tweepy.TweepError:
        # pdb.set_trace()
        # import sys; exc_type, exc_value, tb = sys.exc_info()
        # from pprint import pprint; pprint(tb.tb_frame.f_locals)
        print("TweepError Error \n")

    except StopIteration:
        print("StopIteration Error \n")

    except Exception:
        # pdb.set_trace()
        # import sys; exc_type, exc_value, tb = sys.exc_info()
        # from pprint import pprint; pprint(tb.tb_frame.f_locals)
        print("Erro Desconhecido \n")

def download_followers():
    # this line defines which input take
    # data = settings.medias_accounts_toSearch
    dt = settings.accounts_toSearch
    data = np.dstack((dt[1],dt[0]))[0]

    while True:
        for account in data:
            nids = 5000 # number of results
            user = api.get_user(account[1])
            nfollowers = user.followers_count
            nfullpages = nfollowers/nids
            frac, dec = math.modf(nfullpages)
            # print(nfollowers/5000, nfollowers%5000)
            print(frac, dec)
            print(nfollowers)
            pages = []
            if ((nfollowers/nids) > 1):
                pages = tweepy.Cursor(api.followers_ids, id=account[0], count=nids).pages(dec)
                last_page = tweepy.Cursor(api.followers_ids, id=account[0], count=nfollowers, page=(dec+1)).pages()
            else:
                # print("len(pages)", len(pages))
                pages = tweepy.Cursor(api.followers_ids, id=account[0], count=nfollowers).pages()

            print("Start retrieve followers \n")
            for page in limit_handled(pages):
                count = 0
                # pdb.set_trace()
                for id in page:
                    count = count+1
                    follower = {"id": str(id)}
                    db.insert_one(follower, account[1]+"_followers")
                print(count)

def download_timeline():
    dt = settings.medias_accounts_toSearch
    data = np.dstack((dt[1],dt[0]))[0]

    print("Start retrieve followers \n")
    while True:
        for account in data:
            user = api.get_user(account[1])
            username = user.screen_name
            number_of_tweets = 20 #200 MAX
            pages = tweepy.Cursor(api.user_timeline, id=account[0], count=number_of_tweets).pages()
            for page in limit_handled(pages):
                # count = 0
                for status in page:
                    # count = count+1
                    # print(count)
                    tweet = {
                        "id": status.id,
                        "text": status.text
                        # "screen_name": status.screen_name,
                        # "location": status.location,
                    }
                    db.insert_one(tweet, str(account[1])+"_statuses")

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
