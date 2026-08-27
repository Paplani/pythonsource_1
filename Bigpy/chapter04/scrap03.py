import requests, json

# 쿠키 객체 생성
jar = requests.cookies.RequestsCookieJar()
# /cookies 경로에서 사용할 쿠키 설정(ex: name = kim)
jar.set('name', 'kim', domain = 'httpbin.org', path = '/cookies')

# Get 요청
r = requests.get('http://httpbin.org/cookies', cookies=jar)
r.raise_for_status()
print(r.text)

# timeout 설정
# 3초 안에 응답 안하면 예외 처리하고 강제 종료
r = requests.get('https://github.com', timeout=3) # 3초
# print(r.text)

# Post 요청하면서 데이터도 같이 보낼 수 있음
r = requests.post('http://httpbin.org/post', data = {'name':'kim'}, cookies=jar)
# print(r.text)

# 페이로드는 요청과 함께 서버로 실제로 전달되는 "진짜 내용물(데이터)"을 말합니다.
# 우리가 지난번 URL 쿼리스트링(?key=value)으로 값을 보냈던 것과 비슷한데, 쿼리스트링은 URL 겉면에 노출되고, 페이로드는 요청의 "몸통(body)"에 숨겨져서 전달된다는 차이가 있습니다.
# get은 urlencode로 URL쿼리스트링을 주로 사용하지만 Post는 data = payload를 쓰는 경우가 많음.
payload1 = {'key1':'values1', 'key2':'values2'}         #dict
payload2 = (('key1', 'values1'), ('key2', 'values2'))   #tuple
payload3 = {'some':'nice'}

r = requests.post('http://httpbin.org/post', data=payload3)
print(r.text)