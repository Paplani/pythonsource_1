import simplejson as json

data={}
data['people'] = []
print(data)

# value
data['people'].append({
    'name':'kim', 
    'website':'naver.com',
    'from':'Seoul', 
    'grade':[95,77,89,91]
})
data['people'].append({
    'name':'park', 
    'website':'google.com',
    'from':'Busan', 
    'grade':[85,88,79,81]
})
data['people'].append({
    'name':'Lee', 
    'website':'daum.net',
    'from':'Incheon', 
    'grade':[80,85,90,96]
})

# print(data)

# json 객체로 파일 생성
with open('member.json', 'w') as outfile:
    json.dump(data, outfile)

with open('member.json', 'r') as infile:
    r=json.load(infile)
    for p in r['people']:
        print('Name: '+p['name'])
        print('Website: '+p['website'])
        print('from: '+p['from'])
        t=p['grade']
        grade=''
        for g in t:
            grade = grade + ' ' + str(g)
        print('Grade: ' + grade.lstrip())   #왼쪽 공백까지 제거. 에러대비해서