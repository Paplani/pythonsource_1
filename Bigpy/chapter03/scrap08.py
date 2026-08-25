import sys
import io
import urllib.request
import urllib.parse
from urllib.parse import urlparse

url = "http://www.encar.com/"

# encar 처럼 봇 차단이 있는 사이트는 기본 User-Agent
# 403/406 error가 발생하여 정상 페이지를 받지 못함
req = urllib.request.Request(
    url, 
    headers={
        "User-Agent":"Mozilla/5.0 (Linux; Android 15; Pixel 9) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/151.0.0.0 Mobile Safari/537.36"
    }
)

mem = urllib.request.urlopen(req)
# mem은 응답 "내용"이 아니라 응답을 읽을 수 있는 객체(파일 객체와 비슷) — .status, .geturl(), .getheaders()로 메타정보를, .read()로 실제 본문을 꺼냅니다.

print(type(mem))
print("getrul : ", mem.geturl())     #https://car.encar.com/?firstFg=Y&WT.hit=index_mobile_1st           
print("status : ", mem.status)      # status :  200

print("headers : ", mem.getheaders())
print("info : ", mem.info())    #header 정보를 행단위로 보여줌
print("getcode : ", mem.getcode())          #mem.status

# 서버가 사용하는 문자 인코딩, 없으면 utf-8
encoding = mem.info().get_content_charset() or 'utf-8'

# 바이트를 500개만 자르면 멀티바이트(한글, 한자, 특문 등) 중간에 끊김 => 에러날수 있음
# unicodeDecodeError가 발생할수 있음 errors='ignore' 처리
raw = mem.read(500)
print("read: ", raw.decode(encoding, errors='ignore'))

print(urlparse('http://www.encar.co.kr?test=test').query)   # query 부분만 뽑아옴  test=test