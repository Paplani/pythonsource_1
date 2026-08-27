import requests

# param이 필수로 들어가야 요청이 성공되는 API
url = "https://api.open-meteo.com/v1/forecast"

params = {
    "latitude":37.5665, 
    "longitude":126.9780,
    "hourly":"temperature_2m", 
    "timezone":"Asia/Seoul"
}

# parmas = params 이게 핵심
res = requests.get(url, params=params)
print(res)
print("-"*40)
data = res.json()
# print(data)

times = data["hourly"]['time']
temps = data["hourly"]['temperature_2m']

for t, temp in zip(times, temps):
    print(f"{t} : {temp}도")

print("최고 기온:", max(temps))
print("최저 기온:", min(temps))
