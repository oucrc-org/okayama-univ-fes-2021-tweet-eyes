# coding: UTF-8

# Packages
from discord import channel, user
from discord.ext import tasks
import discord
import platform
import subprocess
import tweepy
import os

# Custom Libraries
import loadenv
import request

# clientの宣言
# ゲームアクティビティに'<OSの名前> <バージョン>をプレイ中'と表示
# memo: 余裕があればここ 'xx件の未承認' とかにしたい
intents = discord.Intents.default()
intents.reactions = True
client = discord.Client(activity=discord.Game(
    name=platform.system() + ' ' + platform.release()), intents=intents)


# ツイート内容を格納するクラス
# 引数はDBと同じ
class tweet:
    def __init__(self, twitter_id, avatar_url, display_name, comment, tweet_url, id):
        self.twitter_id = twitter_id
        self.avatar_url = avatar_url
        self.display_name = display_name
        self.comment = comment
        self.tweet_url = tweet_url
        self.id = id


# =====以下予定=====
# Twitter APIを30分ごとに定期実行して新しいツイートがあるか確認する
# あった場合はツイートのデータをDBに登録
#   then. main_channel で指定したチャンネルに各ツイートをメッセージとして送信（jsonとかで返ってくるのかしら、詳しくは追々確認する予定）
#   then. 送信を確認したらサムズアップ、ダウンの絵文字をスタンプ
#   then. サムズアップが増えたらDBのis_visibleに1を代入→メッセ削除
#   then. サムズダウンが減ったらDBのis_visibleに0→メッセ削除
#
# 備考: DB登録はsmpny7がAPI作るのでそれを叩く
#       Discord botをアプリケーションとして常駐させる予定だが、その上でTwitter APIを叩けるかどうかは未確認
# ==================


def set_embed(tweet):
    embed = discord.Embed(
        title=tweet.display_name,
        color=0x4488ff,
        description=tweet.comment,
        url=tweet.tweet_url
    )

    embed.set_author(name=tweet.twitter_id,
                     url='https://twitter.com/' + tweet.twitter_id,
                     icon_url=tweet.avatar_url
                     )
    embed.set_footer(text=tweet.id)
    embed.add_field(name='承認', value='👍')
    embed.add_field(name='却下', value='👎')
    return embed


@ tasks.loop(minutes=10)
async def loop():
    # ツイート一覧の取得
    api = loadenv.get_tw_api()
    searchResults = api.search_tweets('#岡山大学祭2021')

    # ツイートを取ってくる
    tws = [tweet(searchResult.user.screen_name, searchResult.user.profile_image_url_https, searchResult.user.name, searchResult.text, f'https://twitter.com/{searchResult.user.screen_name}/status/{searchResult.id_str}', searchResult.id_str)
           for searchResult in searchResults if not hasattr(searchResult, 'retweeted_status')]

    for tw in tws:
        # DB登録
        result = request.post_database(tw)

        # TODO: 1回投稿したツイートを除外する（resultの値が200なら実行）
        if result == 200:
            embed = set_embed(tw)
            message = await main_channel.send(embed=embed)

            # スタンプ設置
            await message.add_reaction('👍')
            await message.add_reaction('👎')

    # このあとスタンプが押されたのを検知したら個別に関数呼び出して処理


@ client.event
async def on_raw_reaction_add(payload):
    if payload.member.bot:
        return
    message = await main_channel.fetch_message(payload.message_id)
    if payload.emoji.name == '👍':
        print(message.embeds[0].footer.text)
        rsp = request.set_visible(int(message.embeds[0].footer.text))
        if rsp == 200:
            await message.delete()
        else:
            return
    if payload.emoji.name == '👎':
        await message.delete()



# 以下は基本的に編集する必要なし

# Botの動作確認用
@ client.event
async def on_message(message):
    if message.author.bot:
        return

    # Ping Pong Test
    if 'ping' in message.content:
        await message.channel.send('pong')
        print('Ping Pong Test')
        print(message.channel.id)
        return

    # ラズパイの状態確認（SSHで毎回コマンド打つのだるいので）
    if 'checkstatus' in message.content:
        print('Command > checkstatus')
        temp = subprocess.getoutput('vcgencmd measure_temp').split('=')[1]
        clock = '{0:.2f}'.format(float(subprocess.getoutput(
            'vcgencmd measure_clock arm').split('=')[1]) / 1000000000) + 'GHz'
        volt = subprocess.getoutput(
            'vcgencmd measure_volts core').split('=')[1]
        mem = subprocess.getoutput('vcgencmd get_mem arm').split('=')[1] + 'B'

        await message.channel.send('{}\n{}\n{}\n{}'.format(temp, clock, volt, mem))
        return


# 開始確認用
@ client.event
async def on_ready():
    global main_channel
    print('ready...')

    # デフォルトの送信先チャンネルのIDを静的に与えた方が良いかも
    main_channel = await client.fetch_channel(loadenv.get_channel_id())
    loop.start()


# ログイン処理
client.run(loadenv.get_token())
