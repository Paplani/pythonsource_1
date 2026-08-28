# - `requests`로 REST API 호출
# - JSON 응답 파싱 (중첩 딕셔너리/리스트 접근)
# - JSON 파일로 저장

# 1. `https://api.frankfurter.dev/v1/latest?base=USD&symbols=KRW,JPY,EUR` 를 이용해 달러 기준 원화, 엔화, 유로 환율을 가져오세요.
# 2. 콘솔에 통화별로 출력하세요.
    
#     ```
#     1 USD = 1385.20 KRW1 USD = 147.32 JPY1 USD = 0.92 EUR
#     ```
    
# 3. 결과를 `exchange_today.json` 파일로 저장하세요. (조회일자 포함)


import requests
import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
Py_Scrap= BASE_DIR.parent/"Py_Scrap"

url = "https://api.frankfurter.dev/v1/latest?base=USD&symbols=KRW,JPY,EUR"

res = requests.get(url)
data = res.json()

currency_list = []

usd_krw = data["rates"]["KRW"]
usd_jpy = data["rates"]["JPY"]
usd_eur = data["rates"]["EUR"]
currency_list.append({
    "date":data["date"],
    "USD/KRW":usd_krw,
    "USD/JPY":usd_jpy,
    "USD/EUR":usd_eur
})

print(f"1. USD = {usd_krw} 1. USD = {usd_jpy} 1. USD = {usd_eur}")

file_path = Py_Scrap/"exchange_today.json"

with open(file_path, "w", encoding='utf-8') as f:
    json.dump(currency_list, f, ensure_ascii=False, indent=2)

print("저장 완료.")