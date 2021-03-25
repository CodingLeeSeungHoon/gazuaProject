import crawlsite
import time
import random
import invest

db_coin, db_title = [], []
count = 1


def init():
    c, t = crawlsite.get_recent_announced_coin()
    while c == -1:
        c, t = crawlsite.get_recent_announced_coin()

    db_coin.append(c), db_title.append(t)


investor = invest.Investor()
init()

while True:
    coin, title = crawlsite.get_recent_announced_coin()
    if coin == -1 and title == -1:
        pass
    else:
        if db_coin and db_title and coin == db_coin[len(db_coin) - 1] and title == db_title[len(db_title) - 1]:
            # least one data in db, not updated new coin announcement
            print("not updated {}".format(count))
            count += 1
        else:
            # no data in db or new coin announcement updated!
            db_coin.append(coin), db_title.append(title)
            print("{}\n{}".format(coin, title))

            # investor.buy_coin(coin)
            resp = investor.buy_coin(coin)
            if resp != -1:
                investor.sell_coin_limit(resp)

    time.sleep(random.randrange(5, 10))
