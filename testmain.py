import time
import random
import invest

db_coin, db_title = [], []
count = 1

def init():
    db_coin.append('TT')
    db_title.append('dummy')

def get_random_sign(number):
    coin_sign = ['TT', 'TT', 'TT', 'CRO', 'CRO', 'CRO', 'CRO']
    title_sign = ['dummy', 'dummy', 'dummy', 'test!', 'test!', 'test!', 'test!']

    return coin_sign[number], title_sign[number]

investor = invest.Investor()
init()

num = 0

while num != 6:
    coin, title = get_random_sign(num)
    if coin == -1 and title == -1:
        pass
    else:
        if db_coin and db_title and coin == db_coin[len(db_coin) - 1] and title == db_title[len(db_title) - 1]:
            # least one data in db, not updated new coin announcement
            print("not updated {}, coin_db = {}".format(count, db_coin))
            count += 1
        else:
            # no data in db or new coin announcement updated!
            db_coin.append(coin), db_title.append(title)
            now = time.localtime()
            print("{}\n{}".format(coin, title))
            print("{}/{}/{} {}:{}:{}".format(now.tm_year, now.tm_mon, now.tm_mday,
                                             now.tm_hour, now.tm_min, now.tm_sec))
            # investor.buy_coin(coin)
            resp = investor.buy_coin(coin)
            if resp != -1:
                investor.sell_coin_limit(resp, coin)

    time.sleep(random.randrange(1, 3))
    num += 1
