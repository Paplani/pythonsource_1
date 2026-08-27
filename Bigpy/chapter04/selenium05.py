from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
import time
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
Py_Scrap= BASE_DIR.parent/"Py_Scrap"

chrome_options = Options()
s = Service()

driver = webdriver.Chrome(service=s, options=chrome_options)

driver.set_window_size(1920,1080) #화면크기
driver.get('https://google.com')
time.sleep(3)     #대기(모든 load 1초가 걸려도 3초 기다림)
driver.save_screenshot(str(Py_Scrap / "img" / "Website3.png"))

driver.set_window_size(1920,1080) #화면크기
driver.get('https://daum.net')
time.sleep(3)     #대기(모든 load 1초가 걸려도 3초 기다림)
driver.save_screenshot(str(Py_Scrap / "img" / "Website4.png"))

driver.quit()

print("스크린샷 성공")