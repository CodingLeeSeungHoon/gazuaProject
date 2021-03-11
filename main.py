import crawlsite
import time

db_coin, db_title = [], []

while True:
    coin, title = crawlsite.get_recent_announced_coin()
    if db_coin and db_title:
        if coin == db_coin[len(db_coin)-1] and title == db_title[len(db_title)-1]:
            print("not updated")
    else:
        db_coin.append(coin), db_title.append(title)
        print("{}\n{}".format(coin, title))

    time.sleep(1)