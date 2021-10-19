# coding: UTF-8

# Packages
import discord
import platform
import subprocess

# Custom Libraries
import loadenv


# clientの宣言
# ゲームアクティビティに'<OSの名前> <バージョン>をプレイ中'と表示
# memo: 余裕があればここ 'xx件の未承認' とかにしたい
client = discord.Client(activity=discord.Game(
    name=platform.system() + ' ' + platform.release()))


# デフォルトの送信先チャンネルのIDを静的に与えた方が良いかも
#main_channel = discord.channel


# =====以下予定=====
# Twitter APIを定期実行して新しいツイートがあるか確認する
# あった場合は main_channel で指定したチャンネルに各ツイートをメッセージとして送信（jsonとかで返ってくるのかしら、詳しくは追々確認する予定）
#   then.送信を確認したらサムズアップ、ダウンの絵文字をスタンプ
#   then.サムズアップが増えたらDB登録→〇をスタンプ
#   then.サムズアップが減ったら破棄→×をスタンプ
# 
# 備考: DB登録はsmpny7がAPI作るのでそれを叩く
#       Discord botをアプリケーションとして常駐させる予定だが、その上でTwitter APIを叩けるかどうかは未確認
# ==================


# 以下は編集する必要なし

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
client.run(loadenv.TOKEN)
