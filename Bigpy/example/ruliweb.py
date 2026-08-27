import requests
from bs4 import BeautifulSoup

with requests.Session() as s:
    # 게시글 가져오기
    post_one = s.get("https://bbs.ruliweb.com/market/board/1020/read/37546")

    post_one.raise_for_status
    # print(post_one)

    print("--------------------------------------------")
    print()
    soup = BeautifulSoup(post_one.text, 'html.parser')
    # print(soup.prettify)

    # #board_read > div > div.board_main > div.board_main_view.row > div.view_content.autolink > article > div > p:nth-child(3)

    print("-------------------------")

    # 문서 출력
    article = soup.select("#board_read > div > div.board_main > div.board_main_view.row > div.view_content.autolink > article > div > p")
    # print(article)

    # string 처리
    for i in article:
        if i.string is not None and i.img == None:
            # p에 이미지가 딸려있는 문장이면 텍스트 문장을 자식으로 취급함. text는 자식은 가져오지 못하므로 string씀
            print(i.string)