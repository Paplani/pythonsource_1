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

# 메인
car_func("#gr")                 # 가장 단순
car_func("li#gr")               # li 이면서 아이디가 gr
car_func("ul>#gr")              # ul의 직계자식중 아이디가 gr : 가장 많이 쓰이는 방법
car_func("#cars #gr")           # 아이디가 #cars이면서 그 아래 어딘가에 있는 아이디가 gr
car_func("#cars>#gr")           # 아이디가 #cars의 직계자식중 id가 gr
car_func("//*[@id='gr']")
