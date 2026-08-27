from playwright.sync_api import sync_playwright

def save_login_session():

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        page.goto('https://nid.naver.com/nidlogin.login')

        input("브라우저 창에서 아이디/비번 직접 입력 후 로그인 -> 로그인 완료되면 여기 콘솔에서 엔터를 눌러주세요...")

        page.context.storage_state(path="naver_session.json")   # naver_session.json 파일이 세션 역할을 하는 파일
        print("세션 저장 완료: naver_session.json")
        browser.close()

if __name__ == "__main__":
    save_login_session()
