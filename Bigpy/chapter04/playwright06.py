from playwright.sync_api import sync_playwright
# uv pip install playwright
# python -m playwright install chromium
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
Py_Scrap= BASE_DIR.parent/"Py_Scrap"

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page()

    page.goto('https://google.com')
    page.screenshot(path=Py_Scrap / "img" / "Web1.png")

    page.goto('https://daum.net')
    page.screenshot(path=Py_Scrap / "img" / "Web2.png")

    browser.close()

print('스크린샷 성공')