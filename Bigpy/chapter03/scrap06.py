import sys
import io
import urllib.request
import urllib.parse
from urllib.parse import urlparse

# ? 뒤에 붙는 key=value&key2=value2 형태를 쿼리스트링이라고 하고, 서버에 추가 조건(옵션)을 전달할 때 씁니다. 
# 문제는 값 안에 한글이나 공백, &, = 같은 특수문자가 있으면 URL 규칙상 그대로 못 넣고 퍼센트 인코딩(%XX 형태)을 해야 한다는 것 — urllib.parse가 이런 변환을 자동으로 해줍니다.

# 내 공인 IP 주소를 알려주는 API
API = "https://api.ipify.org"

# 딕셔너리
values = {
    'format':'json'
}

print('before', values)
params = urllib.parse.urlencode(values)     # 딕셔너리 → URL 쿼리 문자열 변환
print('after', params)

# 요청
url = API + "?" + params             # https://api.ipify.org?format=json
print("요청 url= ", url)

#  읽기
data = urllib.request.urlopen(url).read()
text = data.decode("utf-8")
print(text)

