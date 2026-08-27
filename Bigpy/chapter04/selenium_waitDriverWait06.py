from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from pathlib import Path
import os
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / ".env")      # 항상 스크립트 옆의 .env를 정확히 찾음
id = os.getenv("wishket_id")
password = os.getenv("wishket_pwd")
Py_Scrap = BASE_DIR.parent/"Py_Scrap"

chrome_options = Options()
s = Service(Py_Scrap / "chromedriver" / "chromedriver.exe")

driver = webdriver.Chrome(service=s, options=chrome_options)
wait = WebDriverWait(driver, 10)      # 최대 10초까지, 조건 충족되면 즉시 진행

driver.set_window_size(1920, 1080)  # 화면크기
driver.get('https://auth.wishket.com/login')

# time.sleep(3) 대신 -> emailOrId 입력창이 DOM에 나타날 때까지만 대기
email_input = wait.until(EC.presence_of_element_located((By.NAME, 'emailOrId')))
email_input.send_keys(id)
driver.find_element(By.NAME, 'password').send_keys(password)

# 로그인 버튼
login_button_xpath = '/html/body/div[2]/div[2]/div/div[2]/div/div[1]/form/div[3]/button'
# time.sleep 없이 -> 버튼이 "클릭 가능한 상태"가 될 때까지만 대기
login_button = wait.until(EC.element_to_be_clickable((By.XPATH, login_button_xpath)))
before_click_url = driver.current_url        # 클릭 전 URL을 미리 저장해둠
login_button.click()

# time.sleep(3) 대신 -> 클릭 전 URL과 달라질 때까지 대기 (로그인 처리로 페이지가 실제로 넘어갔다는 신호)
# 주의: url_contains("wishket.com")은 로그인 페이지 URL에도 "wishket.com"이 포함돼 있어
#       클릭 직후 아직 이동 전이어도 즉시 통과해버리는 함정이 있었음 -> url_changes로 수정
wait.until(EC.url_changes(before_click_url))
driver.save_screenshot(str(Py_Scrap / "img" / "Wishweb_wait.png"))
print("로그인 성공")

# 포트폴리오 페이지로 이동
driver.get('https://www.wishket.com/mywishket/partners/')

# 프로젝트 정보 크롤링
# time.sleep(3) 대신 -> 원하는 요소가 실제로 나타날 때까지만 대기
registered_projects_el = wait.until(EC.presence_of_element_located(
    (By.XPATH, '/html/body/div[2]/div/div[1]/div[2]/div[2]/div[1]/div[6]/div[1]/p')
))
registered_projects = registered_projects_el.text
contracted_projects = driver.find_element(
    By.XPATH, '/html/body/div[2]/div/div[1]/div[2]/div[2]/div[1]/div[6]/div[2]/p'
).text
completed_amount = driver.find_element(
    By.XPATH, '/html/body/div[2]/div/div[1]/div[2]/div[2]/div[1]/div[6]/div[3]/p'
).text

# 결과 출력
print(f"등록된 프로젝트: {registered_projects}")
print(f"계약한 프로젝트: {contracted_projects}")
print(f"누적 완료 금액: {completed_amount}")
driver.quit()

print("스크린샷 성공")
