import requests
import json
import os
from dotenv import load_dotenv           #.env 파일 읽어서 환경변수로 등록
from collections import defaultdict      # 키가 없어도 에러 없이 빈 리스트를 만들어 주는 딕셔너리

load_dotenv()
API_KEY = os.getenv("OPENWEATHER_API_KEY")

def get_5day_forecast(city):
    url = "https://api.openweathermap.org/data/2.5/forecast"
    params = {
        "q":city,
        "appid":API_KEY, 
        "units":"metric", 
        "lang":"kr"
    }

    res = requests.get(url, params=params)
    if res.status_code == 404:
        return None
    res.raise_for_status()
    data = res.json()
    # print(data)

    # 3시간 간격 데이터를 날짜별로 묶어서 평균/최고/최저 계산
    # defaultdict : 없는 key를 조회했을 때, 에러 내지 말고 내가 정해둔 기본값을 자동으로 만들어주는 딕셔너리
    daily = defaultdict(list)

    for item in data['list']:
        date_str = item['dt_txt'].split(" ")[0]    #2026-08-28 03:00:00 에서 날짜만 가져오기
        daily[date_str].append(item)

    results = []
    for date, items in daily.items():
        temps = [i['main']['temp'] for i in items]
        weather_desc = items[len(items) // 2]['weather'][0]['description']     # 날짜별 중간 시점 날씨를 대표

        results.append({
            "날짜":date,
            "최고 기온":round(max(temps), 1),
            "최저 기온":round(min(temps), 1),
            "날씨": weather_desc
        })
    return results      # 5일치 

def main():
    city = "Seoul"
    forcast = get_5day_forecast(city)
    print(forcast)
    #예외처
    if forcast is None:
        print("도시를 찾을 수 없음")
        return
    
    print(f"=== {city} 5일 예보 ===")
    for day in forcast:
        print(f"{day['날짜']} | 최고 {day['최고 기온']}도 / 최저 {day['최저 기온']}도 / {day['날씨']}")

    with open("weather_5days.json", "w", encoding='utf-8') as f:
        json.dump(forcast, f, ensure_ascii=False, indent=2)

    print("\n저장 완료: weather_json")
    

if __name__ == "__main__":
    main()