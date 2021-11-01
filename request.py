from json import load
import requests
import loadenv


def post_database(tweet):

    print('post_database: ')
    print(tweet)

    url = loadenv.get_db_url('api/saveTweet')
    hds = {'Client-Api-Key': str(loadenv.get_db_apikey())}
    request_body = {'twitter_id':tweet.twitter_id,
                    'avatar_url':tweet.avatar_url,
                    'display_name':tweet.display_name,
                    'comment':tweet.comment,
                    'tweet_url':tweet.tweet_url,
                    'id':tweet.id}

    response = requests.post(url, headers=hds, json=request_body)
    print(response.status_code)
    return response.status_code # 成功で200、失敗で422を返す

def set_visible(id):
    print('set_visible: ' + str(id))

    url = loadenv.get_db_url('api/setVisible/'+ str(id))
    hds = {'Client-Api-Key': str(loadenv.get_db_apikey())}

    response = requests.post(url, headers=hds)

    return response.status_code # 成功で200、失敗で422を返す

if __name__ == '__main__':
    # ここにテストプログラムを書く
    print('テスト')
    class tweet:
        def __init__(self, twitter_id, avatar_url, display_name, comment, tweet_url, id):
            self.twitter_id = twitter_id
            self.avatar_url = avatar_url
            self.display_name = display_name
            self.comment = comment
            self.tweet_url = tweet_url
            self.id = id

    tw = tweet('ataa', 'https://google.com', 'aa', 'wawa', 'https://twitter.com/', '1213')
    print(post_database(tw))