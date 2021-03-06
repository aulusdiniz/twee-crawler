#!/usr/bin/python
import numpy as np
import pandas as pd
import json, pdb

def init():
    global config
    # Load config data twitter api use.
    with open('config.json') as config_file:
        config = json.load(config_file)

    global consumer_key
    global consumer_secret
    global access_token
    global access_token_secret

    consumer_key = config["twitter_access"]["consumer_key"]
    consumer_secret = config["twitter_access"]["consumer_secret"]
    access_token = config["twitter_access"]["access_token"]
    access_token_secret = config["twitter_access"]["access_token_secret"]

    # read the urls code should search (make it read from relative path)
    global urls_toSearch
    csv = pd.read_csv(config["enviroment"]["project"]["path"]+"/src/data/medias.csv")
    urls_names = csv[['Nome']].values.flatten()
    urls = csv[['URL']].values.flatten()
    urls_toSearch = (urls_names, urls)
    
    # read the accounts code should search (make it read from relative path)
    global accounts_toSearch
    csv = pd.read_csv(config["enviroment"]["project"]["path"]+"/src/data/profiles.csv")
    accounts = csv[['Nome']].values.flatten()
    ids = csv[['ID']].values.flatten()
    accounts_toSearch = (accounts, ids)
    

    global medias_accounts_toSearch
    csv = pd.read_csv(config["enviroment"]["project"]["path"]+"/src/data/medias-profile.csv")
    accounts = csv[['Conta']].values.flatten()
    ids = csv[['ID']].values.flatten()
    medias_accounts_toSearch = (accounts, ids)
    print(accounts, ids)
    
