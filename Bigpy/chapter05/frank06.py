import requests
import csv
from datetime import datetime, timedelta

# 최근 30일간의 원/달러 환율을 API로 가져와서, 날짜별로 출력하고, 최고/최저 환율과 등락률을 계산한 뒤 CSV로 저장

def get_exchange_rate_trend():
    end_date = datetime.now().strftime("%Y-%m-%d")
    start_date = (datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d")

    url = f"https://api.frankfurter.dev/v1/{start_date}..{end_date}"
    params = {
        "base":"USD",
        "symbols":"KRW"
    }

    res = requests.get(url, params=params)
    res.raise_for_status()
    data = res.json()
    # print(data)

    rates = data['rates']   # {"2026-07-28 : {~~}"}

    # 날짜순 정렬
    sorted_dates = sorted(rates.keys())

    results = []
    for date in sorted_dates:
        krw = rates[date]['KRW']
        print(f"{date}:{krw:,.2f}원")
        results.append({"날짜":date, "환율":krw})
    print(results)

    # 최고/최저 환율
    # rates.items() — 딕셔너리를 (키, 값) 쌍으로 풀어주기 => 튜플들의 모음으로 바꿔줌
    # x: rates.items()에서 나온 튜플 하나, 예를 들어 ("2026-07-28", {"KRW": 1459.45})
    # x[1]: 그 튜플의 두 번째 요소(인덱스 1) → {"KRW": 1459.45} (딕셔너리 부분)
    # x[1]['KRW']: 그 딕셔너리에서 "KRW" 값만 → 1459.45 (진짜 숫자)
    max_item = max(rates.items(), key=lambda x: x[1]['KRW'])
    min_item = min(rates.items(), key=lambda x: x[1]['KRW'])

    # max_item[0]: 날짜,  max_item[1]: 환율
    max_date, max_krw = max_item[0], max_item[1]['KRW']
    min_date, min_krw = min_item[0], min_item[1]['KRW']  

    print(f"최고 환율: {max_krw:,.2f}원 ({max_date})")
    print(f"최저 환율: {min_krw:,.2f}원 ({min_date})")
    print()

    # 첫날 대비 마지막 날 등락률
    first_krw = rates[sorted_dates[0]]['KRW']
    last_krw = rates[sorted_dates[-1]]['KRW']
    change_pct=(last_krw/first_krw-1)*100

    sign = "+" if change_pct >= 0 else ""
    print(f"30일간 등락률: {sign}{change_pct:.2f}%")

    # csv 저장
    csv_path = "usd_krw_30days.csv"
    with open(csv_path, "w", newline="", encoding='utf-8-sig') as f:
        writer = csv.DictWriter(f, fieldnames=["날짜", "환율"])
        writer.writeheader()
        writer.writerows(results)

    print()
    print(f"CSV 저장 완료: {csv_path}")


if __name__ == "__main__":
    get_exchange_rate_trend()