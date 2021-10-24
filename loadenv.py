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

def get_channel_id():
    return os.getenv('DISCORD_CHANNEL_ID')
    