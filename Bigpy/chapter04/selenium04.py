from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
Py_Scrap= BASE_DIR.parent/"Py_Scrap"



chrome_options = Options()
s = Service("C:/source/pythonsource/Bigpy/Py_Scrap/chromedriver/chromedriver.exe")

driver = webdriver.Chrome(service=s, options=chrome_options)

driver.get('https://google.com')
driver.save_screenshot(str(Py_Scrap / "img" / "Website1.png"))

driver.get('https://daum.net')
driver.save_screenshot(str(Py_Scrap / "img" / "Website2.png"))

driver.quit()

print("스크린샷 성공")