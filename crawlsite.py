from bs4 import BeautifulSoup
import requests
import json

"""
2021.03.11
- 비동기식 Ajax 통신 URL 캐치 성공. 공시 정보 URL 캐치 후 JSON Data 추출 성공
- json_file 접근법 주석 추가
- 시간(5초)에 따라 새로운 공시 업데이트 유무 확인
"""

url = 'https://project-team.upbit.com/api/v1/disclosure?region=kr&per_page=20'


def _text_to_json(text):
    return json.loads(text)


def get_recent_announced_coin():
    resp = requests.get(url)
    soup = BeautifulSoup(resp.text, features="html.parser")

    json_file = _text_to_json(soup.text)

    """
    json_file['data']['posts'][number][parameter]
    number :: 0~19 (url per_page=20)
    parameter ::
    - assets : coin name
    - start_date : "yyyy-mm-ddT00:00:00+09:00"
    - text : announce title
    """
    return json_file['data']['posts'][0]['assets'], json_file['data']['posts'][0]['text']


def init_db():
    pass

