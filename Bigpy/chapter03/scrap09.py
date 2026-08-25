import sys
import io
import urllib.request
import urllib.parse
from urllib.parse import urlparse
from bs4 import BeautifulSoup

url = "http://www.encar.com/"

# encar 처럼 봇 차단이 있는 사이트는 기본 User-Agent
# 403/406 error가 발생하여 정상 페이지를 받지 못함

headers={
    "User-Agent":"Mozilla/5.0 (Linux; Android 15; Pixel 9) "
                 "AppleWebKit/537.36 (KHTML, like Gecko) "
                 "Chrome/151.0.0.0 Mobile Safari/537.36"
}


req = urllib.request.Request(url, headers=headers)
mem = urllib.request.urlopen(req)

encoding = mem.info().get_content_charset() or 'utf-8'
html = mem.read().decode(encoding, errors='ignore')

soup = BeautifulSoup(html, "html.parser")
# print(soup)

# 1. title 태그에서 텍스트 가져오기
title = soup.select_one("title")
# print("title : ", title)     # 태그까지 같이 보임
print("title : ", title.text)     #텍스트만 보임ㅡ 자식 텍스트가 여러개일 경우 합침
# print("title : ", title.string)   #텍스트만 보임, 자식이 텍스트 하나일 경우 사용, '내차팔기·내차사기 | 엔카' 여기에서 엔카가 None으로 뜰수 있음. | 를 블록으로 볼수도 잇음

# 2. 속성값을 활용하여 텍스트 가져오기 (meta name = "description")
description = soup.select_one('meta[name = "description"]')
print("description : ", description.get("content") if description else "없음")

keywords = soup.select_one('meta[name="keywords"]')
print("keywords : ", keywords.get("content") if keywords else "없음")