import requests
from fake_useragent import UserAgent

ua = UserAgent()

headers = {
    'User-Agent': ua.random,    # 가짜 브라우저
    'referer': 'http://finance.daum.net/'
}

# 주식 요청 url
url = "http://finance.daum.net/api/search/ranks?limit=10"

# 요청
res = requests.get(url, headers=headers)
rank_json = res.json()['data']   # json.loads(...decode('utf-8')) 이 한 줄로 끝

for element in rank_json:
    print('순위:{}, 금액:{}, 회사명:{}'.format(element['rank'], element['tradePrice'], element['name']))
