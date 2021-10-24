# coding: UTF-8

# Packages
from discord.ext import tasks
import discord
import platform
import subprocess

# Custom Libraries
import loadenv
import request


# clientの宣言
# ゲームアクティビティに'<OSの名前> <バージョン>をプレイ中'と表示
# memo: 余裕があればここ 'xx件の未承認' とかにしたい
client = discord.Client(activity=discord.Game(
    name=platform.system() + ' ' + platform.release()))


# デフォルトの送信先チャンネルのIDを静的に与えた方が良いかも
main_channel = client.get_channel(loadenv.get_channel_id())


# ツイート内容を格納するクラス
# 引数はDBと同じ
class tweet:
    def __init__(self, twitter_id, avatar_url, display_name, comment, tweet_url):
        self.twitter_id = twitter_id
        self.avatar_url = avatar_url
        self.display_name = display_name
        self.comment = comment
        self.tweet_url = tweet_url


# =====以下予定=====
# Twitter APIを定期実行して新しいツイートがあるか確認する
# あった場合はツイートのデータをDBに登録
#   then. main_channel で指定したチャンネルに各ツイートをメッセージとして送信（jsonとかで返ってくるのかしら、詳しくは追々確認する予定）
#   then. 送信を確認したらサムズアップ、ダウンの絵文字をスタンプ
#   then. サムズアップが増えたらDBのaccepted_atに時刻を追加→〇をスタンプ→1分後とかにメッセ削除
#   then. サムズアップが減ったらDBのaccepted_atはnull→×をスタンプ→1分後とかにメッセ削除
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
    return embed


@tasks.loop(minutes=30.0)
async def loop():
    # ツイート一覧の取得


    # for: ツイートごとの処理
        # ツイートから中身を取ってくる
        tw = tweet('@ID', 'アイコンURL', 'ツイート主の名前', 'ツイート本文', 'ツイートURL')

        # DB登録
        request.post_database(tw, id)
        
        embed = set_embed(tw)
        await main_channel.send(embed)
        # スタンプ設置
        # このあとスタンプが押されたのを検知したら個別に関数呼び出して処理


# 以下は基本的に編集する必要なし

# Botの動作確認用
@client.event
async def on_message(message):
    if message.author.bot:
        return

    # Ping Pong Test
    if 'ping' in message.content:
        await message.channel.send('pong')
        print('Ping Pong Test')
        print(message.channel)
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
@client.event
async def on_ready():

    print('ready...')


# ログイン処理
client.run(loadenv.get_token())
