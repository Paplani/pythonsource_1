import requests
from bs4 import BeautifulSoup

url = "http://books.toscrape.com/"

res = requests.get(url)
soup = BeautifulSoup(res.text, "html.parser")
# print(soup)

# 첫 번째 책 하나만 찾기
book = soup.find("article", class_="product_pod")
# print(book)

# find는 속성으로 접근할때 .attrs[] 로 해야함!
title = book.find("h3").find("a").attrs["title"]
print("title : ", title)
price = book.find("div", class_="product_price").find("p").getText(" ", strip=True).replace("Â£", "£")    #각 테스트 조각에서 앞뒤 공백 제거
print("price : ", price)
