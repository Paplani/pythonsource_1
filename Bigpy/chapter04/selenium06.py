from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import time
from pathlib import Path
import os
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent
Py_Scrap= BASE_DIR.parent/"Py_Scrap"

load_dotenv(BASE_DIR / ".env")      # 항상 스크립트 옆의 .env를 정확히 찾음
id = os.getenv("wishket_id")
password = os.getenv("wishket_pwd")

chrome_options = Options()
s = Service(Py_Scrap/ "chromedriver" / "chromedriver.exe")

driver = webdriver.Chrome(service=s, options=chrome_options)

driver.set_window_size(1920,1080) #화면크기
driver.get('https://auth.wishket.com/login')
time.sleep(3) 

driver.find_element(By.NAME, 'emailOrId').send_keys(id)
driver.find_element(By.NAME, 'password').send_keys(password)

# 로그인 버튼
login_button_xpath = '/html/body/div[2]/div[2]/div/div[2]/div/div[1]/form/div[3]/button'
driver.find_element(By.XPATH, login_button_xpath).click()
driver.save_screenshot(Py_Scrap / "img" / "Wishweb.png")
time.sleep(3)
print("로그인 성공")

#포트폴리오 페이지로 이동
driver.get('https://www.wishket.com/mywishket/partners/')
time.sleep(3)

# 프로젝트 정보 크롤링
registered_projects = driver.find_element(By.XPATH, '/html/body/div[2]/div/div[1]/div[2]/div[2]/div[1]/div[6]/div[1]/p').text
contracted_projects = driver.find_element(By.XPATH, '/html/body/div[2]/div/div[1]/div[2]/div[2]/div[1]/div[6]/div[2]/p').text
completed_amount = driver.find_element(By.XPATH, '/html/body/div[2]/div/div[1]/div[2]/div[2]/div[1]/div[6]/div[3]/p').text

# 결과 출력
print(f"등록된 프로젝트: {registered_projects}")
print(f"계약한 프로젝트: {contracted_projects}")
print(f"누적 완료 금액: {completed_amount}")
driver.quit()

print("스크린샷 성공")