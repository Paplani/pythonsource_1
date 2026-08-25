import requests, json

s = requests.Session()
r = s.get("http://httpbin.org/get")
print(r.status_code)
print(r.ok)

print("---------------------------------------")
r = s.get('https://jsonplaceholder.typicode.com/posts/1')
print('1: ', r.text)
print('2: ', r.json())
print('3: ', r.json().keys())
print('4: ', r.json().values())
print('5: ', r.encoding)
print('6: ', r.content)
print('7: ', r.raw)

print("------------------------")
# 세션 시작
with requests.Session() as s:
    # Get으로 스트리밍 요청
    r = s.get('http://httpbin.org/stream/20', stream=True)
    if r.status_code == 200:
        # 스트리밍된 응답의 각 라인을 반복구조로 
        for line in r.iter_lines():
            # 라인을 디코드하고 출력
            if line:
                # JSON 으로 파싱해서 사용
                data = json.loads(line.decode('utf-8'))
                print(data)
    else:
        print(f'요청을 실패하였습니다. 상태코드: {r.status_code}')