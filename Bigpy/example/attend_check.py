from playwright.sync_api import sync_playwright
import os

SESSION_FILE = "naver_session.json"

def attend_with_saved_session():
    if not os.path.isfile(SESSION_FILE):
        print("저장된 세션이 없습니다. save_session.py를 먼저 실행하세요.")
        return

    with sync_playwright() as p:
        browser = p.chromium.launch()  # 자동 실행용이니 headless 유지
        context = browser.new_context(storage_state=SESSION_FILE)
        page = context.new_page()

        # %3fF = ? 식별자, %26s = & 식별자
        page.goto('http://cafe.naver.com/paramsx?iframe_url=/AttendanceView.nhn%3Fsearch.clubid=19756449%26search.menuid=103')
        page.wait_for_timeout(3000)

        page.once("dialog", lambda dialog: dialog.accept())

        frame = page.frame(name="cafe_main")
        if frame:
            frame.fill('#cmtinput', '출석합니다!')
            frame.click('#btn-submit-attendance')
            page.wait_for_timeout(3000)
            print("출석체크 완료")
        else:
            print("cafe_main iframe을 못 찾음 — 세션이 만료됐을 가능성. save_session.py 다시 실행 필요")
            page.screenshot(path="attend_fail.png")  # 실패 시 원인 파악용

        browser.close()


if __name__ == '__main__':
    attend_with_saved_session()


# ================= 코드 분석 노트 =================
#
# 4, 7~9줄  SESSION_FILE 존재 확인
#   저장된 로그인 세션 파일(naver_session.json)이 없으면 브라우저를
#   켤 필요도 없이 안내만 찍고 return으로 바로 함수를 끝냄.
#
# 13~14줄  browser.new_context(storage_state=SESSION_FILE)
#   browser(브라우저 자체) -> context(독립된 브라우징 세션 = 크롬 프로필 하나)
#   -> page(그 프로필 안의 탭)의 계층 구조. new_page()를 바로 안 쓰고
#   context를 한 단계 거치는 이유는, context가 쿠키·로그인 상태(storage_state)를
#   담는 단위이기 때문. storage_state에 저장된 JSON 파일 경로를 넘기면
#   "빈 세션으로 시작하지 말고 이 파일에 저장된 로그인 상태를 불러와서 시작해라"는
#   뜻이 되어, 매번 로그인 폼을 채우지 않고도 로그인된 상태로 바로 시작할 수 있음.
#   (save_session.py가 미리 로그인해서 이 파일을 저장해두는 역할)
#
# 17줄  URL 안의 %3F, %26
#   ?와 &를 URL에 그냥 쓰면 쿼리 파라미터 구분자로 해석돼서 주소가 깨짐.
#   iframe_url= 파라미터 값 안에 또 다른 주소+쿼리스트링을 통째로 넣어야 해서,
#   퍼센트 인코딩(%3F=?, %26=&)으로 "이건 진짜 문자다"라고 이스케이프한 것.
#
# 20줄  page.once("dialog", lambda dialog: dialog.accept())
#   alert/confirm 같은 브라우저 네이티브 팝업이 뜨면 발생하는 "dialog" 이벤트를
#   딱 한 번만(once) 구독해서 자동으로 "확인"(accept)을 눌러줌. 출석 버튼을
#   누르는 순간 팝업이 뜨므로, 버튼을 누르기 전에 미리 예약해둬야 함.
#
# 22~29줄  page.frame(name="cafe_main")
#   출석체크 내용이 <iframe name="cafe_main">, 즉 부모 페이지와는 별개인
#   문서 안에 들어있어서, page.fill/click로는 못 찾음. page.frame(name=...)으로
#   그 iframe 내부 문서를 가리키는 Frame 객체를 따로 얻어와야 그 안의 요소를
#   fill/click할 수 있음. 못 찾으면(None) 보통 세션 만료가 원인이라
#   screenshot으로 그 순간 화면을 남겨서 나중에 원인 확인 가능하게 해둠.
#
# 35~36줄  if __name__ == '__main__':
#   이 파일을 직접 실행할 때만 attend_with_saved_session()을 호출.
#   나중에 다른 스크립트에서 import해서 쓸 때는 자동 실행되지 않게 막는 안전장치.