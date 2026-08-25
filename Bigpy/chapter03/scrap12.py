import requests
from bs4 import BeautifulSoup

url = "http://books.toscrape.com/"

res = requests.get(url)
soup = BeautifulSoup(res.text, "html.parser")

# class = "product_pod" 인 article 태그 전체 선택, 이번엔 select로
# 타이틀 | 가격 | 별점     으로 출력되게 10권만

books = soup.select("article.product_pod", limit = 10)

book_detail = {}
count = 1
for book in books:
    title = book.select_one("h3 a")["title"]
    price = book.select_one("p.price_color").text.replace("Â£", "£")
    rating = book.select_one("p.star-rating")["class"][1]    #두 번째 class 가 three라는 별점을 나타내줌.
    book_detail[count] = {"title":title, "price":price, "rating":rating}
    count +=1

    print(f"{title} | {price} | {rating}")