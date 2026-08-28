# - `.env` + `python-dotenv`로 API 키 안전하게 관리
# - 여러 항목 반복 조회 후 리스트로 집계
# - 예외 처리 (없는 도시명, 인증 실패)

# 1. OpenWeatherMap에서 본인 API 키를 발급받아 `.env` 파일에 저장하세요.
# 2. 서울, 부산, 인천, 대구, 광주 **5개 도시**의 현재 기온과 날씨 상태를 조회하세요.
# 3. 5개 도시 중 **가장 더운 도시**와 **가장 시원한 도시**를 찾아서 출력하세요.
    
#     ```
#     === 도시별 현재 날씨 ===서울: 29.5도, 맑음부산: 27.1도, 구름 조금...가장 더운 도시: 서울 (29.5도)가장 시원한 도시: 부산 (27.1도)
#     ```
    
# 4. 존재하지 않는 도시명이 들어와도 프로그램이 멈추지 않고 "조회 실패"로 넘어가게 처리하세요.
# 5. 전체 결과를 CSV로 저장하세요.


import requests
import csv
import os
from dotenv import load_dotenv
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
Py_Scrap= BASE_DIR.parent/"Py_Scrap"

load_dotenv()
API_KEY = os.getenv("OPENWEATHERMAP_APIKEY")
file_path = Py_Scrap/"city_weather.csv"

city_weather = []

def get_korea_city_weather(city):
    try:
        city_params = city+", KR"
        geo_res = requests.get("http://api.openweathermap.org/geo/1.0/direct", params={
            "q":city_params, 
            "appid":API_KEY, 
            "limit":1
        })
        lat = geo_res.json()[0]["lat"]
        lon = geo_res.json()[0]["lon"]

        weather_res = requests.get("https://api.openweathermap.org/data/4.0/onecall/current", params={
            "lat":lat, 
            "lon":lon, 
            "appid":API_KEY
        })
        # 이건 첫번째로 할때 틀린 부분
        # city_temp = weather_res.json()["data"]["temp"]
        # city_desc = weather_res.json()["data"]["weather"]["description"]

        print(weather_res.status_code, weather_res.json())

        city_temp = weather_res.json()["data"][0]["temp"]
        city_desc = weather_res.json()["data"][0]["weather"][0]["description"]

        city_weather.append({
            "city":city,
            "temp":city_temp, 
            "desc":city_desc
        })

        return city_temp, city_desc

    except Exception as e:
        print(f"해당 도시 {city} 조회에 실패하였습니다. ({e})")
        return None, None


def main():
    print("=== 도시별 현재 날씨 ===")
    city_list = ["Seoul", "Busan", "Incheon", "Daegu", "Gwangju"]
    for i in city_list:
        city_temp, city_desc = get_korea_city_weather(i)
        print(f"{i}: {city_temp}도, {city_desc}\n")

    if city_weather:
        hot_city = max(city_weather, key= lambda x:x["temp"])     #city_weather를 돌면서 각 요소를 꺼냄. x가 바로 그 각각의 요소
        cold_city = min(city_weather, key= lambda x:x["temp"])     #city_weather를 돌면서 각 요소를 꺼냄. x가 바로 그 각각의 요소

        print(f"가장 더운 도시: {hot_city['city']} ({hot_city['temp']}도)\n")
        print(f"가장 추운 도시: {cold_city['city']} ({cold_city['temp']}도)")
    else:
        print("조회에 성공한 도시가 하나도 없습니다.")

    with open(file_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["city", "temp", "desc"])
        writer.writeheader()
        writer.writerows(city_weather)

if __name__ == "__main__":
    main()