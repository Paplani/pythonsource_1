from bs4 import BeautifulSoup
import urllib.request as req
import sys
import io
import json
from fake_useragent import UserAgent

# uv pip install fake-useragent

# Fake Headers 정보
ua = UserAgent()

# 헤더정보
headers = {
    'User-Agent': ua.random,    # 가짜 브라우저
    'referer':'http://finance.daum.net/'
}

# 주식 요청 url
url = "http://finance.daum.net/api/search/ranks?limit=10"

# URL
#  ↓
# Request 생성
#  ↓
# urlopen() → 서버에 요청
#  ↓
# read() → 응답 데이터 읽기 (bytes)
#  ↓
# decode() → 문자열(str)로 변환
#  ↓
# res

# 요창
res = req.urlopen(req.Request(url, headers=headers)).read().decode('utf-8')

# print('res: ', res)
rank_json = json.loads(res)['data']
print(rank_json)

for element in rank_json:
    print('순위:{}, 금액:{}, 회사명:{}'.format(element['rank'], element['tradePrice'], element['name']))

