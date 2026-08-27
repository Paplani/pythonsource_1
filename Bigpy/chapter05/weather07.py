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
    print(data)


if __name__ == "__main__":
    get_5day_forecast("Seoul")