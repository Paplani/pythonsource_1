# - `requests` + `BeautifulSoup` 기본 사용
# - `select()` / `select_one()`으로 원하는 요소 찾기
# - CSV 저장 (`csv.DictWriter`)

# 1. `https://books.toscrape.com/` 에서 첫 페이지에 있는 책 20권의 **제목, 가격, 별점**을 크롤링하세요.
# 2. 콘솔에 다음 형식으로 출력하세요.
    
#     ```
#     1. A Light in the Attic | £51.77 | 별점: Three 2. Tipping the Velvet | £53.74 | 별점: One...
#     ```
    
# 3. 결과를 `books_top20.csv` 파일로 저장하세요. (컬럼: 순번, 제목, 가격, 별점)

# - 책 하나는 `<article class="product_pod">` 안에 들어있습니다.
# - 별점은 `<p class="star-rating Three">`처럼 class의 두 번째 값에 들어있습니다. (`tag['class']`로 리스트를 가져올 수 있음)

from bs4 import BeautifulSoup
import requests
from pathlib import Path
import csv

BASE_DIR = Path(__file__).resolve().parent
Py_Scrap= BASE_DIR.parent/"Py_Scrap"
csv_path = Py_Scrap/"books_top20.csv"

url = "https://books.toscrape.com/"

res = requests.get(url)
soup = BeautifulSoup(res.text, 'html.parser')

# #default > div > div > div > div > section > div:nth-child(2) > ol > li:nth-child(1) > article > h3 > a
book_section = soup.select('section')
# print(book_section)
book_acticle = soup.select('section .product_pod')
# print(book_acticle)

book_result = []

for idx, book in enumerate(book_acticle[:20], start=1):
    book_title = book.select_one('h3 a')['title']
    print(book_title)
    book_price = book.select_one('.price_color').string.replace("Â", "")
    book_rating = book.select_one('.star-rating')['class'][1]

    print(f"{idx}. {book_title} | {book_price} | 별점: {book_rating}\n")

    # DictWriter는 row 딕셔너리의 key가 fieldnames랑 일치해야 그 값을 해당 컬럼에 넣어즘
    book_result.append({
        "순번":idx,
        "제목":book_title, 
        "가격":book_price,
        "별점":book_rating
    })

with open(csv_path, "w", newline="", encoding='utf-8-sig') as f:
    writer = csv.DictWriter(f, fieldnames=["순번", "제목", "가격", "별점"])
    writer.writeheader()
    writer.writerows(book_result)