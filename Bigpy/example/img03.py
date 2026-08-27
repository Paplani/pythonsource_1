from playwright.sync_api import sync_playwright
import os
import requests
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent
Py_Scrap= BASE_DIR.parent/"Py_Scrap"

savePath = Py_Scrap / "img"
os.makedirs(savePath, exist_ok=True)   #폴더가 없으면 만들고, 폴더가 있으면 통과

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()

    page.goto("https://search.naver.com/search.naver?sm=tab_hty.top&where=image&ssc=tab.image.all&query=%EB%A7%90%ED%8B%B0%ED%91%B8")
    page.wait_for_timeout(3000)

    imgs = page.query_selector_all("img")
    print("찾은 img 개수 : ", len(imgs))

    # 먼저 url만 뽑아서 리스트에 저장
    # 주의: get_attribute("src")로 얻는 건 이미지 "파일 자체"가 아니라
    # <img src="여기 적힌 주소">에서 그 주소(문자열)일 뿐이다.
    # 브라우저는 이 주소를 보고 알아서 이미지를 받아 화면에 그려주지만,
    # 우리는 그 렌더링 결과에 접근할 수 없고 주소 텍스트만 읽을 수 있다.
    img_urls = []
    for img in imgs:
        src = img.get_attribute("src")
        # 검색 페이지는 src에 실제 주소 대신 data:image/...;base64,... 같은
        # 임시 placeholder를 넣어두기도 해서, 진짜 http(s) 주소만 걸러낸다.
        if src and src.startswith("http"):
            img_urls.append(src)

    # print(img_urls[:2])

    browser.close()

print(f"수집된 이미지 URL: {len(img_urls)}개")

# requeste로 하나씩 실제 다운로드
# 위에서 모은 건 "이미지가 어디 있는지" 가리키는 주소 문자열일 뿐이라
# 실제 이미지 데이터(바이트)를 받으려면 그 주소로 HTTP 요청을 한 번 더 보내야 한다.
count = 0
for url in img_urls[:20]:
    count+=1
    try:
        img_data = requests.get(url, timeout=5).content  # .content: 응답 바디를 바이트 그대로 받음 (이미지처럼 텍스트가 아닌 바이너리 데이터라 .text가 아닌 .content를 써야 함)
        fullfilename = os.path.join(savePath, f"{count}.jpg")
        with open(fullfilename, "wb") as f:
            f.write(img_data)
        print(f"{count}.jpg 저장완료")
    except Exception as e:
        print(f"{count}번 이미지 다운로드 실패")

print("다운로드 완료")