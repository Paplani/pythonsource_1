import requests
from bs4 import BeautifulSoup

# soup 객체에는 항상 BeautifulSoup 메서드(select, find_all, .get(...))만 쓰시면 됩니다.

with requests.Session() as s:

    post_one = s.get("https://bbs.ruliweb.com/market/board/1020/read/106663?")
    post_one.raise_for_status

    soup = BeautifulSoup(post_one.text, 'html.parser')

    paragraph = soup.select("#board_read > div > div.board_main > div.board_main_view.row > div.view_content.autolink > article > div > p:nth-child(6)")
    for row in paragraph :
        print(row.text)

    # 추가로 이미지도 긁어오고 싶음. 
    imgs = soup.select("img")
    # print(imgs)
    for img in imgs:
        # get_attribute는 playwright의 문법임. beautifulsoup에서는 속성부여는 그냥 get
        src = img.get("src")
        if src:
            print(src)

# 추가로 p 태그 안에 있는 줄바꿈이나 공백 없앨때
#  text = p.get_text(separator=" ", strip=True)
