from bs4 import BeautifulSoup
import requests
import json
import numpy as np

"""
2021.03.11
- 비동기식 Ajax 통신 URL 캐치 성공. 공시 정보 URL 캐치 후 JSON Data 추출 성공
- json_file 접근법 주석 추가
2021.03.12
- avoid bot detection : random sleep, random user-agent
- 
"""

url = 'https://project-team.upbit.com/api/v1/disclosure?region=kr&per_page=1'


def _text_to_json(text):
    return json.loads(text)


def _is_successful_connected(status_code):
    if status_code // 100 == 2:
        return True
    else:
        return False


def _get_random_ua():
    random_ua = ''
    ua_file = 'ua_file.txt'

    try:
        with open(ua_file) as f:
            lines = f.readlines()
        if len(lines) > 0:
            prng = np.random.RandomState()
            index = prng.permutation(len(lines) - 1)
            idx = np.asarray(index, dtype=np.integer)[0]
            random_ua = lines[int(idx)]

    except Exception as ex:
        print('Exception in random_ua')
        print(str(ex))
    finally:
        return random_ua


def get_recent_announced_coin():
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:20.0) Gecko/20100101 Firefox/20.0'}
    resp = requests.get(url, headers=headers)
    print(resp.status_code)
    if _is_successful_connected(resp.status_code):
        soup = BeautifulSoup(resp.text, features="html.parser")
        json_file = _text_to_json(soup.text)

        """
        json_file['data']['posts'][number][parameter]
        number :: 0 (url per_page=1)
        parameter ::
        - assets : coin name
        - start_date : "yyyy-mm-ddT00:00:00+09:00"
        - text : announce title
        """

        return json_file['data']['posts'][0]['assets'], json_file['data']['posts'][0]['text']

    return -1, -1




