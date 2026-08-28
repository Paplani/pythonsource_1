# 1. Selenium 또는 Playwright 중 하나를 선택해서, 로그인이 필요 없는 사이트(예: 아무 커뮤니티 게시판이나 무한 스크롤이 있는 사이트) 하나를 골라 접속하세요.
# 2. 페이지 끝까지 **무한 스크롤**하여 로딩되는 게시글(또는 상품, 뉴스 등) 제목을 최소 30개 이상 수집하세요.
# 3. 수집한 제목을 텍스트 파일(`titles.txt`)로 한 줄씩 저장하세요.
# 4. (선택 심화) 만약 로그인이 필요한 사이트로 진행한다면, 최초 1회 수동 로그인 후 세션(쿠키)을 저장해두고, 재실행 시 그 세션을 재사용하도록 구현해보세요.

# - 무한 스크롤은 "스크롤 → 대기 → 페이지 높이 비교 → 높이가 같으면 종료" 패턴을 씁니다.
# - 로그인 세션 재사용은 Playwright의 `storage_state`를 활용하면 편합니다.

from playwright.sync_api import sync_playwright
from pathlib import Path
import os
from dotenv import load_dotenv


BASE_DIR = Path(__file__).resolve().parent
Py_Scrap= BASE_DIR.parent/"Py_Scrap"

load_dotenv()

SESSION_FILE = "dcinside_session.json"

def save_login_session():

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
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
                args=[
                    "--mute--audio", 
                    "--no-sandbox", 
                    "--disable-dev-shm-usage", 
                    "--disable-gpu",
                ]
            )
            context = browser.new_context(storage_state=SESSION_FILE)
            page = context.new_page()

            page.goto("https://gall.dcinside.com/mgallery/board/lists?id=theroyal")
            page.wait_for_timeout(3000)

            page.once("dialog", lambda dialog: dialog.accept())

            # 여기에 이제 스크롤 처리해야함

            # #container > section.left_content > article:nth-child(3) > div.gall_listwrap.list > table > tbody
            post_body = page.query_selector_all("#container > section.left_content > article:nth-child(3) > div.gall_listwrap.list > table > tbody")





    else:
        save_login_session()


if __name__ == "__main__":
    get_dcinside_post_title()