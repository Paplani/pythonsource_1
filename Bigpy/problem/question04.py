# 1. Selenium 또는 Playwright 중 하나를 선택해서, 로그인이 필요 없는 사이트(예: 아무 커뮤니티 게시판이나 무한 스크롤이 있는 사이트) 하나를 골라 접속하세요.
# 2. 페이지 끝까지 **무한 스크롤**하여 로딩되는 게시글(또는 상품, 뉴스 등) 제목을 최소 30개 이상 수집하세요.
# 3. 수집한 제목을 텍스트 파일(`titles.txt`)로 한 줄씩 저장하세요.
# 4. (선택 심화) 만약 로그인이 필요한 사이트로 진행한다면, 최초 1회 수동 로그인 후 세션(쿠키)을 저장해두고, 재실행 시 그 세션을 재사용하도록 구현해보세요.

# - 무한 스크롤은 "스크롤 → 대기 → 페이지 높이 비교 → 높이가 같으면 종료" 패턴을 씁니다.
# - 로그인 세션 재사용은 Playwright의 `storage_state`를 활용하면 편합니다.

from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
from pathlib import Path
import os
from dotenv import load_dotenv


BASE_DIR = Path(__file__).resolve().parent
Py_Scrap= BASE_DIR.parent/"Py_Scrap"
file_path = Py_Scrap / "titles.txt"

load_dotenv()

SESSION_FILE = "dcinside_session.json"

def save_login_session():

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, channel="chrome")   # Playwright 자체 크로미움 대신 설치된 크롬을 사용
        page = browser.new_page()
        page.goto('https://sign.dcinside.com/login?s_url=https://www.dcinside.com/')

        input("브라우저 창에서 아이디/비번 직접 입력 후 로그인 -> 로그인 완료되면 여기 콘솔에서 엔터를 눌러주세요...")

        page.context.storage_state(path=SESSION_FILE)
        print("세션 저장 완료: dcinside_session.json")
        browser.close()

def get_dcinside_post_title():
    if Path("dcinside_session.json").exists():
        with sync_playwright() as p:
            browser = p.chromium.launch(
                headless=False,
                channel="chrome",   # Playwright 자체 크로미움 대신 설치된 크롬을 사용
                args=[
                    "--mute-audio", 
                    "--no-sandbox", 
                    "--disable-dev-shm-usage", 
                    "--disable-gpu",
                ]
            )
            context = browser.new_context(storage_state=SESSION_FILE)
            page = context.new_page()

            page.once("dialog", lambda dialog: dialog.accept())     # Playwright에서 브라우저의 팝업창(Dialog)이 뜨면 자동으로 확인(OK)을 눌러주는 코드

            page.goto("https://gall.dcinside.com/mgallery/board/lists?id=theroyal")
            page.wait_for_timeout(3000)

            # 여기에 이제 스크롤 처리해야함

            page.keyboard.press("PageDown")
            page.wait_for_timeout(3000)

            scroll_pause_time = 4000
            last_height = page.evaluate("document.documentElement.scrollHeight")

            while True:
                page.evaluate("window.scrollTo(0, document.documentElement.scrollHeight)")
                page.wait_for_timeout(scroll_pause_time)
                new_height = page.evaluate("document.documentElement.scrollHeight")

                if last_height == new_height:
                    break

                last_height = new_height

            html_content = page.content()
            browser.close()

        soup = BeautifulSoup(html_content, 'html.parser')

        all_post = soup.select("#container > section.left_content > article:nth-child(3) > div.gall_listwrap.list > table > tbody > tr")

        all_post_title = [
            post.select_one("td a").get_text(strip=True)
            for post in all_post
        ]

        for idx,post_title in enumerate(all_post_title, start=1):
            print(f"{idx}번 글: {post_title}\n")

        #container > section.left_content > article:nth-child(3) > div.gall_listwrap.list > table > tbody > tr:nth-child(8)

        with open(file_path, "w", encoding='utf-8') as f:
            for title in all_post_title:
                f.write(title + "\n")

    else:
        save_login_session()


if __name__ == "__main__":
    get_dcinside_post_title()