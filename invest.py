import os
import jwt
import uuid
import hashlib
from urllib.parse import urlencode

import requests

"""
# 전체 자산 목록 첫 호출, 거래 후 갱신 기능
# 공시정보가 갱신되었다면, 새로운 공시에 해당하는 코인 검색 후 주문하기 : 주문을 얼마나 할 것인가?
# 일정 루틴에 따라 코인 판매하기 : 얼마나 팔 것인가?, 어느 타이밍에 팔 것인가?

# crawl 기능을 계속 사용하면서 계좌 조회가 가능하다면?
# 쓰레드 기능 구현도 해보자..
"""


class Investor:
    def __init__(self, test=False):
        if not test:
            self.access_key = os.environ['UPBIT_OPEN_API_ACCESS_KEY']
            self.secret_key = os.environ['UPBIT_OPEN_API_SECRET_KEY']
            self.server_url = os.environ['UPBIT_OPEN_API_SERVER_URL']

            try:
                self.my_account = self.my_whole_account()
            except requests.exceptions.RequestException as error:
                raise SystemExit(error)

    def my_whole_account(self):
        payload = {
            'access_key': self.access_key,
            'nonce': str(uuid.uuid4()),
        }

        jwt_token = jwt.encode(payload, self.secret_key)
        authorize_token = 'Bearer {}'.format(jwt_token)
        headers = {"Authorization": authorize_token}

        res = requests.get(self.server_url + "/v1/accounts", headers=headers)

        return res.json()

    def buy_coin(self, coin, test=False):
        if test:
            print("I bought {} coin!".format(coin))
        else:
            coin_id = 'KRW-' + coin
            """
            market : 마켓 ID, 'KRW-***' 형식으로 구성. 필수 기입
            side : 주문 종류, 'bid'는 매수 'ask'는 매도 필수 기입
            volume : 주문량, 지정가거나 시장가 매도 시 필수 기입
            price : 주문가격, 지정가거나 시장가 매도시 필수 기입
            ord_type : 주문타입, 필수, 'limit'은 지정가 주문, 'price'는 시장가 주문 매수, 'market'은 시장가 주문 매도
            """
            query = {
                'market': coin_id,
                'side': 'bid',
                'volume': '0.01',
                'price': '100.0',
                'ord_type': 'limit',
            }
            query_string = urlencode(query).encode()

            m = hashlib.sha512()
            m.update(query_string)
            query_hash = m.hexdigest()

            payload = {
                'access_key': self.access_key,
                'nonce': str(uuid.uuid4()),
                'query_hash': query_hash,
                'query_hash_alg': 'SHA512',
            }

            jwt_token = jwt.encode(payload, self.secret_key)
            authorize_token = 'Bearer {}'.format(jwt_token)
            headers = {"Authorization": authorize_token}

            res = requests.post(self.server_url + "/v1/orders", params=query, headers=headers)

    def is_coin_in_account(self, coin):
        pass

