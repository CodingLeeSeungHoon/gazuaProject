import crawlsite
import time
import random

db_coin, db_title = [], []
count = 1


def init_db():
    pass


while True:
    coin, title = crawlsite.get_recent_announced_coin()
    if coin == -1 and title == -1:
        pass
    else:
        if db_coin and db_title:
            if coin == db_coin[len(db_coin)-1] and title == db_title[len(db_title)-1]:
                print("not updated {}".format(count))
                count += 1
        else:
            db_coin.append(coin), db_title.append(title)
            print("{}\n{}".format(coin, title))

    time.sleep(random.randrange(5, 10))