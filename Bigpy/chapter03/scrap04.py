import sys
import io
from bs4 import BeautifulSoup
from urllib.parse import urljoin


html = """
<html><body>
  <ul>
    <li><a href="http://www.naver.com">naver</a></li>
    <li><a href="http://www.daum.net">daum</a></li>
    <li><a href="https://www.google.com">google</a></li>
    <li><a href="https://www.tistory.com">tistory</a></li>
  </ul>
</body></html>
"""

soup = BeautifulSoup(html, 'html.parser')
print('prettify', soup.prettify())

# <a> 태그중에서 찾기
a = soup.find_all("a", string="daum")      # select 도 동일함
b = soup.find_all("a", string=["naver", "daum"])
c = soup.find_all("a", limit=2)
d = soup.find("a")      # select_one과 동일

print('a', a)
print('b', b)
print('c', c)
print('d', d)

print("--------------------------------")
links = soup.find_all("a")
print('links -> ', links)

for a in links:
    href = a.attrs['href']
    print('href -> ', href)
    text = a.string
    print('text -> ', text)


baseUrl = "http://test.com/html/a.html"

print(urljoin(baseUrl, "sub/c.html"))           #http://test.com/html/sub/c.html  이렇게 나옴
print(urljoin(baseUrl, "../index.html"))           #http://test.com/index.html  이렇게 나옴
print(urljoin(baseUrl, "../img/ho.png"))           #http://test.com/img/ho.png  이렇게 나옴
print(urljoin(baseUrl, "../css/ho.css"))           #http://test.com/css/ho.css  이렇게 나옴