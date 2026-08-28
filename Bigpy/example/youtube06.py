import sys
import io
import time
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright
import urllib.request as req
from io import BytesIO            # 이미지를 파일로 바로 저장하지 않고 메모리에 바이트로 넣고 다룰 수 있게 함. 엑셀에 이미지를 바로 끼워 넣을 때 씀.
import xlsxwriter
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
Py_Scrap= BASE_DIR.parent/"Py_Scrap"

# 유튜브 영상 페이지에 Playwright로 접속해서 무한 스크롤로 모든 댓글을 로딩시킨 뒤, 
# 각 댓글의 작성자·내용·좋아요 수·프로필 이미지를 추출해서 엑셀 파일로 저장

# workbook = xlsxwriter.Workbook(경로): 엑셀 파일 하나 전체를 나타내는 객체입니다. 파일 이름/경로를 정하고 "이 파일을 만들 준비"를 하는 단계예요. 
# 아직 디스크에 실제로 저장되는 건 아니고, 메모리 안에서 "이 파일에 뭘 넣을지" 계속 쌓아가는 그릇 같은 겁니다.
# worksheet = workbook.add_worksheet(): 엑셀 파일 안의 시트(탭) 하나를 추가하는 겁니다. 
# 엑셀 파일 하나는 시트를 여러 개 가질 수 있잖아요(하단에 "Sheet1", "Sheet2" 탭들). 데이터를 쓰려면 최소 시트가 하나 있어야 해서 이걸 만드는 거예요.
# worksheet.write('A1', '작성자'): 엑셀 셀 주소(A1, B1...)를 직접 지정해서 값을 써넣는 겁니다

workbook = xlsxwriter.Workbook(Py_Scrap/"data/you_crawl_result.xlsx")
worksheet = workbook.add_worksheet()

worksheet.write('A1', '작성자')
worksheet.write('B1', '댓글내용')
worksheet.write('C1', '좋아요')
worksheet.write('D1', '프로필이미지')



# Selenium (Options): add_argument()라는 메서드를 플래그 개수만큼 여러 번 반복 호출해서, 하나씩 옵션 객체에 쌓아 올리는 방식입니다.      selenium04.py에 나와있음
# Playwright (launch()): 애초에 launch() 함수 자체가 args라는 파라미터를 받는데, 이게 "문자열들의 리스트"를 기대합니다. 그래서 여러 플래그를 한 번에 리스트 하나로 묶어서 넘기는 거예요.


def main():
    with sync_playwright() as p:    #playwright 세션 활용
        browser = p.chromium.launch(
            headless=False, 
            # 소리끄기, 리눅스 권한 문제 방지, 공유메모리 부족 방지, gpu비활성화
            args=[
                "--mute--audio", 
                "--no-sandbox", 
                "--disable-dev-shm-usage", 
                "--disable-gpu",
            ]
        )
        page = browser.new_page(viewport={"width":1920, "height":1280})

        page.goto('https://www.youtube.com/watch?v=8CHp4j6bbaQ')
        page.wait_for_timeout(5000)

        #키보드의 page down 키를 눌러서 스크롤 수행
        page.keyboard.press("PageDown")
        page.wait_for_timeout(2000)

        scroll_pause_time = 4000
        last_height = page.evaluate("document.documentElement.scrollHeight")   #시작전 높이 기록

        # page.evaluate(자바스크립트 코드 문자열)은 지금 열려있는 브라우저 페이지 안에서, 그 자바스크립트 코드를 직접 실행시키는 Playwright 기능
        
        while True:
            page.evaluate("window.scrollTo(0, document.documentElement.scrollHeight)")    # 맨 아래로
            page.wait_for_timeout(scroll_pause_time)           # 로딩 대기

            new_height = page.evaluate("document.documentElement.scrollHeight")    # 지금 높이 다시 측정
            print(f"Last Height: {last_height}, Current Height: {new_height}")

            if new_height == last_height:             # 스크롤 전후로 높이가 같다 = 새로 로딩된 게 없음
                break

            last_height = new_height              # 높이가 늘었으면, 이번 높이를 기준으로 갱신하고 다시 while문 반복

        html_content = page.content()              #스크롤 끝나면 그 시점 렌더링된 페이지의 html전체를 문자열로 받아옴
        browser.close()

    soup = BeautifulSoup(html_content, "html.parser")

    comment = soup.select('ytd-comment-view-model#comment')
    print(f"\n총 댓글 수: {len(comment)}개\n")

    ins_cnt = 2      # 엑셀의 행을 나타내줌. 1행은 헤더라 제외하고 2행부터 시작

    for dom in comment:
        try:
            img_tag = dom.select_one("#img")                 # 프로필 이미지
            img_src = img_tag.get("src") if img_tag else None

            author_tag = dom.select_one('#author-text > span')        # 작성자
            author = author_tag.text.strip() if author_tag else '작성자 없음'

            content_tag = dom.select_one('#content-text')              # 내용
            content = content_tag.text.strip() if content_tag else '내용 없음'

            posi_tag = dom.select_one('#vote-count-middle')          # 좋아요 수
            posi_cnt = posi_tag.text.strip() if posi_tag else '0'

            print(f"작성자: {author}")
            print(f"댓글: {content}")
            print(f"좋아요: {posi_cnt}")
            print(f"이미지: {img_src if img_src else 'None'}")
            print()

            worksheet.write(f'A{ins_cnt}', author)
            worksheet.write(f'B{ins_cnt}', content)
            worksheet.write(f'C{ins_cnt}', posi_cnt)

            if img_src and img_src.startswith('http'):
                try:
                    request = req.Request(img_src, headers={
                        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
                    })
                    # 받아온 이미지 바이트를 파일로 저장하는게 아니라 BytesIO(...)로 메모리 안에 담아둠
                    img_data = BytesIO(req.urlopen(request, timeout=10).read())

                    # 파일을 거치지 않고 바로 엑셀 셀에 이미지 끼워넣음. x_scale/y_scale은 이미지 크기를 50%로 줄여서 셀 안에 적당히 들어가게 하는 옵션
                    worksheet.insert_image(
                        f'D{ins_cnt}', author, 
                        {'image_data':img_data, 'x_scale':0.5, 'y_scale':0.5}
                    )
                except Exception as e:
                    print(f"이미지 다운로드 실패:{e}")
                    worksheet.write(f'D{ins_cnt}', img_src)
            else:
                worksheet.write(f'D{ins_cnt}', None)

            ins_cnt += 1

        except Exception as e:
            print(f"댓글 파싱 오류: {e}")
            continue

    print(f"\n총 {ins_cnt -2}개 댓글 저장 완료!")

    workbook.close()
    print("엑셀 저장 완료!")


if __name__ == "__main__":
    main()