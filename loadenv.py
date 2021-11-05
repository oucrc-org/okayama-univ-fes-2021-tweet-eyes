import os
from os.path import join, dirname
from dotenv import load_dotenv

import tweepy

load_dotenv(verbose=True)

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

# Discord Token取得
def get_token():
    return os.getenv('DISCORD_TOKEN')

# データベースURL
def get_db_url(dir):
    return os.getenv('DB_URL') + dir

# データベースキー
def get_db_apikey():
    return os.getenv('DB_APIKEY')

# チャンネルID
def get_channel_id():
    return os.getenv('DISCORD_CHANNEL_ID')

# Twitter API
def get_tw_api():
    consumer_key = os.getenv('TW_CONSUMER_KEY')
    consumer_secret = os.getenv('TW_CONSUMER_SECRET')
    access_token = os.getenv('TW_ACCESS_TOKEN')
    access_token_secret = os.getenv('TW_ACCESS_TOKEN_SECRET')

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)

    api = tweepy.API(auth)

    return api

def get_mention_id():
    return os.getenv('MENTION')
