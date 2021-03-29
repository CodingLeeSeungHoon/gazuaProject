import os
import jwt
import uuid
import hashlib
import time
from urllib.parse import urlencode

import requests

class Investor:
    def __init__(self):
        """
        self.access_key = os.environ['UPBIT_OPEN_API_ACCESS_KEY']
        self.secret_key = os.environ['UPBIT_OPEN_API_SECRET_KEY']
        self.server_url = "https://api.upbit.com"
        """

        self.my_account = self.update_account()

    def update_account(self):
        payload = {
            'access_key': self.access_key,
            'nonce': str(uuid.uuid4())
        }

        jwt_token = jwt.encode(payload, self.secret_key)
        authorize_token = 'Bearer {}'.format(jwt_token)
        headers = {"Authorization": authorize_token}

        res = requests.get(self.server_url + "/v1/accounts", headers=headers)

        return res.json()

    @staticmethod
    def exist_krw(coin_name):
        url = "https://api.upbit.com/v1/market/all"
        querystring = {"isDetails": "false"}
        response = requests.request("GET", url, params=querystring)
        krw_coin = "KRW-" + coin_name  # COIN_ID
        check = krw_coin in response.text

        return check

    def buy_coin(self, coin):
        if self.exist_krw(coin):
            coin_id = 'KRW-' + coin
        else:
            print("KRW 코인이 아닙니다. 거래를 중지합니다.")
            return -1

        """
        market : 마켓 ID, 'KRW-***' 형식으로 구성. 필수 기입
        side : 주문 종류, 'bid'는 매수 'ask'는 매도 필수 기입
        volume : 주문량, 지정가거나 시장가 매도 시 필수 기입
        price : 주문가격, 지정가거나 시장가 매수 시 필수 기입
        ord_type : 주문타입, 필수, 'limit'은 지정가 주문, 'price'는 시장가 주문 매수, 'market'은 시장가 주문 매도
        """
        whole_krw = -1
        if len(self.my_account) == 1:
            if self.my_account['currency'] == 'KRW':
                whole_krw = self.my_account['balance']
        else:
            for a in self.my_account:
                if a['currency'] == 'KRW':
                    whole_krw = a['balance']
                    break

        # 5000원 이하 금액을 주문하면 오류.
        if float(whole_krw) < 5000:
            print("보유 KRW 5000원 미만, 거래를 중지합니다.")
            return -1

        query = {
            'market': coin_id,
            'side': 'bid',
            'price': whole_krw,
            'ord_type': 'price'
        }
        query_string = urlencode(query).encode()

        m = hashlib.sha512()
        m.update(query_string)
        query_hash = m.hexdigest()

        payload = {
            'access_key': self.access_key,
            'nonce': str(uuid.uuid4()),
            'query_hash': query_hash,
            'query_hash_alg': 'SHA512'
        }

        jwt_token = jwt.encode(payload, self.secret_key)
        authorize_token = 'Bearer {}'.format(jwt_token)
        headers = {"Authorization": authorize_token}

        res = requests.post(self.server_url + "/v1/orders", params=query, headers=headers)
        self.my_account = self.update_account()
        return res


    def is_not_sold(self, sell_uuid):
        query = {
            'uuid': sell_uuid
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

        res = requests.get(self.server_url + "/v1/order", params=query, headers=headers)
        remaining_volume = res.json()["remaining_volume"]
        return float(remaining_volume)


    def order_cancel(self, sell_uuid):

        query = {
            'uuid': sell_uuid
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
        headers = {"Authorization":authorize_token}

        res = requests.delete(self.server_url + "/v1/order", params=query, headers=headers)

        if "error" not in res:
            print("Cancel Success")
        else:
            self.order_cancel(sell_uuid)


    def sell_coin_market(self, coin_id, volume):
        query = {
            'market': coin_id,
            'side': 'ask',
            'volume': str(volume),
            'ord_type': 'market',
        }

        query_string = urlencode(query).encode()

        m = hashlib.sha512()
        m.update(query_string)
        query_hash = m.hexdigest()

        payload = {
            'access_key': self.access_key,
            'nonce': str(uuid.uuid4()),
            'query_hash': query_hash,
            'query_hash_alg': 'SHA512'
        }

        jwt_token = jwt.encode(payload, self.secret_key)
        authorize_token = 'Bearer {}'.format(jwt_token)
        headers = {"Authorization": authorize_token}

        res = requests.post(self.server_url + "/v1/orders", params=query, headers=headers)
        if "error" not in res:
            print("Sell_market Order Success")
        else:
            self.sell_coin_market(coin_id, volume)

    @staticmethod
    def _cal_price(price):
        # price == float
        limit_price = price * 1.1
        if limit_price >= 2000000:
            changes = limit_price % 1000
            return str(limit_price - changes)

        elif limit_price >= 1000000:
            changes = limit_price % 500
            return str(limit_price - changes)

        elif limit_price >= 500000:
            changes = limit_price % 100
            return str(limit_price - changes)

        elif limit_price >= 100000:
            changes = limit_price % 50
            return str(limit_price - changes)

        elif limit_price >= 10000:
            changes = limit_price % 10
            return str(limit_price - changes)

        elif limit_price >= 1000:
            changes = limit_price % 5
            return str(limit_price - changes)

        elif limit_price >= 100:
            changes = limit_price % 1
            return str(limit_price - changes)

        elif limit_price >= 10:
            tmp = round(limit_price, 1)
            if tmp > limit_price:
                return str(tmp - 0.1)
            else:
                return str(tmp)

        else:
            tmp = round(limit_price, 2)
            if tmp > limit_price:
                return str(tmp - 0.01)
            else:
                return str(tmp)



    def sell_coin_limit(self, resp):
        """
        @ 21.03.24 이승훈
        params resp =
        {
          "uuid":"cdd92199-2897-4e14-9448-f923320408ad", -> 주문 취소할 때 필요
          "price":"100.0", -> 주문 당시 화폐 가격
          "market":"KRW-BTC", -> 마켓의 유일 키
          "volume":"0.01", -> 사용자가 입력한 주문양
          ...
        }
        """
        response = resp.json()
        if "error" not in response:
            # resp 200 Success
            order_uuid = response['uuid']
            bought_price = float(response['price'])
            coin_id = response['market']
            coin_volume = response['volume']

            # 구매한 코인을 매도, 구매한 코인의 양 만큼 구매가격의 10% 인상시 매도
            query = {
                'market': coin_id,
                'side': 'ask',
                'volume': coin_volume,
                'price': self._cal_price(bought_price),
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
            if "error" not in res.json():
                # wait 5 minutes and check coins are sold
                time.sleep(300)
                not_sold = self.is_not_sold(res.json()['uuid'])
                if not_sold:
                    # K초가 지나도 팔리지 않은 경우, 취소 및 시장가로 매도
                    self.order_cancel(order_uuid)
                    self.sell_coin_market(coin_id, not_sold)
                    print("sell {} coin market price.".format(coin_id.replace("KRW-", "")))
                    self.my_account = self.update_account()
                else:
                    # 판매 완료 MSG, Investor 계좌 갱신
                    print("Success sell {} coin!".format(coin_id.replace("KRW-", "")))
                    self.my_account = self.update_account()

            else:
                # res 400 Failed
                print("Warning : Failed Sell Coin!! retry sell coin")
                self.sell_coin_limit(resp)

        else:
            # resp 400 Failed
            print("Warning : Failed Buy Coin!!")
