import sys
import io
from bs4 import BeautifulSoup   # uv pip install beautifulsoup4


'''
<html>
<body>
<ul id="cars">
  <li id="ge">Genesis</li>
  <li id="av">Avante</li>
  <li id="so">Sonata</li>
  <li id="gr">Grandeur</li>
  <li id="tu">Tucson</li>
</ul>
</body>
</html>
'''

fp = open("C:/source/pythonsource/Bigpy/Py_Scrap/cars.html", encoding='utf-8')

soup = BeautifulSoup(fp, 'html.parser')
print(soup)


# 함수
def car_func(select):
    print("car_func", soup.select_one(select).string)

# lambda(매개변수 : q)
car_lambda = lambda q: print("car_func: ", soup.select_one(q).string)

# 메인
car_func("#gr")                 # 가장 단순
car_func("li#gr")               # li 이면서 아이디가 gr
car_func("ul>#gr")              # ul의 직계자식중 아이디가 gr : 가장 많이 쓰이는 방법
car_func("#cars #gr")           # 아이디가 #cars이면서 그 아래 어딘가에 있는 아이디가 gr
car_func("#cars>#gr")           # 아이디가 #cars의 직계자식중 id가 gr
# car_func("//*[@id='gr']")

print('-------------------------')

print("car_func", soup.select("li")[3].string)      # select_one : 한가지 element가져올때
print("car_func", soup.find_all("li")[3].string)    # find : 한가지 element

# soup.select_one("#gr").string처럼 태그 뒤에 .string을 붙이면 그 태그 안의 텍스트만 꺼냅니다. 
# 주의할 점: .string은 그 태그 안에 텍스트 하나만 딱 있을 때만 값을 주고, 자식 태그가 여러 개 섞여 있으면 None이 됩니다. 
# 더 안전하게 텍스트를 뽑고 싶을 땐 .get_text()를 쓰면, 하위의 모든 텍스트를 합쳐서 문자열로 돌려줍니다(자식이 여러 개여도 동작).
# soup.select_one("#gr").string        "Grandeur" (자식이 텍스트 하나뿐이라 OK)
# soup.select_one("#gr").get_text()     더 범용적인 대안