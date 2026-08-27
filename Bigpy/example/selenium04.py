from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time
import os
import re
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
Py_Scrap= BASE_DIR.parent/"Py_Scrap"

# Chrome WebDriver 경로 설정
chrome_driver_path = Py_Scrap/"chromedriver"/"chromedriver.exe"

#Selenium WebDriver 설정
chrome_options = Options()
chrome_options.add_argument("--headless")  #브라우저 창을 띄우지 않음
chrome_options.add_argument("--disable-gpu")   # GPU 비활성화
chrome_options.add_argument("--no-sandbox")   #보안 비활성화


service = Service(executable_path=chrome_driver_path)
driver = webdriver.Chrome(service=service, options=chrome_options)

try:
    # 영화 검색 페이지 열기 (ex: "말할 수 없는 비밀")
    search_query = "말할 수 없는 비밀 영화 평점"
    search_url = f"https://search.naver.com/search.naver?query={search_query}"
    driver.get(search_url)      # 브라우저 리모컨한테 "이 주소로 이동해라" 명령

    time.sleep(3)

    #영화 제목 가져오기
    try: 
        title_element = driver.find_element(By.CLASS_NAME, "title_area")
        title = title_element.text.strip()
    except:
        title = "제목을 찾을 수 없습니다."

    # 영화 평점 가져오기
    try: 
        # find_element(찾는 방식, 찾을 값)
        # ex) By.ID : html의 id 속성값으로 찾아라.
        # By.CLASS_NAME은 클래스 이름 하나만 검색가능함. 
        # 클래스가 여러개 붙어있으면 By.CSS_SELECTOR, "title_area.sub_title" 처럼 css 선택자를 써야함.

        score_element = driver.find_element(By.CLASS_NAME, "score_area")
        score = score_element.text.strip()
    except:
        score = "평점을 찾을 수 없습니다."

    # 결과 출력
    print(f"영화 제목: {title}")
    print(f"평점: {score}")

    # 특수문자 제거
    filename = re.sub(r'[^a-zA-Z0-9가-힣]', '', title)

    # 평점만 파일로 저장
    # os.getcwd() : 지금 이 파이썬 프로그램이 실행되고 있는 위치(현재 작업 디렉터리)"를 문자열로 돌려줌
    # 터미널에서 실행되는 그 경로를 말하는 것
    file_path = os.path.join(os.getcwd(), f"{filename}.txt")
    with open(file_path, "w", encoding='utf-8') as f:
        f.write(score)

    print(f"파일 저장 완료: {file_path}")
    print(file_path)

finally:
    driver.close()