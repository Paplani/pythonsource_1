import requests
from bs4 import BeautifulSoup

url = "https://www.melon.com/chart/index.htm"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/124.0.0.0 Safari/537.36"
}

res = requests.get(url, headers=headers)
soup = BeautifulSoup(res.text, "html.parser")
# print(soup)

rows = soup.select("tr.lst50")
# print(rows)

ranking = {}
# start = 1 enumerate는 0부터 시작하지만 그 0을 1로 바꿔서 1부터 시작하도록 명시함
for idx, row in enumerate(rows[:10], start=1):
    title = row.select_one(".rank01 a").string
    artist = row.select_one(".rank02 a").string.replace("\xa0", " ")
    ranking[idx] = {"title":title, "artist":artist}
    print(f"{idx}등. 곡: {title} 가수:{artist}")
    # 1: {'title': 'BiiiG', 'artist': 'BIGBANG\xa0(빅뱅)'} 이런 형식으로 \xa0 이런게 나옴. 출력 불가능한 공백을 코드로 보여주는것. ".replace("\xa0", " ")" 을 넣어서 해결해야함.

print(ranking)