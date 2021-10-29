def post_database(tweet):
    print('post_database: ')
    print(tweet)
    return 200 # 成功で200、失敗で422を返す

def set_visible(id):
    print('set_visible: ' + str(id))
    return 200 # 結果

if __name__ == '__main__':
    # ここにテストプログラムを書く
    print('テスト')
