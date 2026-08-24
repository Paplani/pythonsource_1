import urllib.request as req
import os.path, random
import simplejson as json    #uv pip install simplejson 터미널에서 실행

# prettify json 확장 프로그램 설치하면 좋음.

# URL 요청
url = "https://api.github.com/repositories"

# 경로와 파일명
savename = "repo.json"

# 예외처리
if not os.path.exists(savename):
    req.urlretrieve(url, savename)
    # GitHub API에서 저장소 목록을 받아서(JSON 텍스트) repo.json 파일로 저장 — 이 단계가 "직렬화된 데이터를 다운로드"하는 부분

# 직렬화(Serialize): 파이썬 객체(딕셔너리, 리스트 등) → 파일/문자열로 저장 가능한 형태 (JSON 텍스트, pickle 바이트 등)
# 역직렬화(Deserialize): 저장된 형태(JSON 텍스트, pickle 바이트) → 다시 파이썬 객체(딕셔너리, 리스트)로 복원

# 객체를 역직렬화(load) 파일에서 바로 읽어올 때
item=json.load(open(savename, 'r', encoding='utf-8'))
print('Type: ', type(item))

for i in item:
    print(i["full_name"]+" - " + i["owner"]["url"])

print("---------------------------------------------")

# json.load(파일객체): 파일 객체를 직접 넘겨서 읽으며 역직렬화 (open(...)이 반환한 파일 핸들 그대로)
# json.loads(문자열): 이미 .read()로 읽어놓은 문자열을 역직렬화 (s = string)
# json.loads(open(savename,...).read())는 "파일을 열어서 .read()로 전체 내용을 문자열로 먼저 읽은 다음, 그 문자열을 loads()로 파싱"하는 것이고, 
# 위의 json.load(open(savename,...))는 "파일 객체를 바로 넘겨서 load()가 알아서 읽고 파싱"하는 것

# 역직렬화 (loads) -s(string) / 데이터베이스에 이미 저장되어 있는 데이터 읽어오기
items=json.loads(open(savename, 'r', encoding='utf-8').read())
print('Type: ', type(items))

for i in items:
    print(i["full_name"]+" - " + i["owner"]["url"])
