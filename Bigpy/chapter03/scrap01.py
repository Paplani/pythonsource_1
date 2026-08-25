import sys
import io
import urllib.request as dw


imgUrl="https://search.pstatic.net/common/?src=http%3A%2F%2Fblogfiles.naver.net%2FMjAyMDA3MTdfMTgw%2FMDAxNTk0OTYzOTUwOTYw.IKn6Jj8o-SoRTbZI3c9fWfqbRlXp8Kn6mm2mrUZj2Vcg.g-mWpamKt2jzpt0gw3B3jeC9z3ozWwsF3czu6h3XHK0g.PNG.ohj3437%2F2020-07-17_14%253B32%253B11_%25288%2529.png&type=sc960_832"
htmlURL="http://google.com"

# 방법 1
# savePath1 = "C:/source/pythonsource/Bigpy/Py_Scrap/imgtest1.jpg"
# savePath2 = "C:/source/pythonsource/Bigpy/Py_Scrap/imdex.html"
# dw.urlretrieve(imgUrl, savePath1)
# dw.urlretrieve(htmlURL, savePath2)

f1 = dw.urlopen(imgUrl).read()
f2 = dw.urlopen(htmlURL).read()

savePath1 = "C:/source/pythonsource/Bigpy/Py_Scrap/imgtest2.jpg"
savePath2 = "C:/source/pythonsource/Bigpy/Py_Scrap/imdex2.html"

# 방법 2
# saveFile1 = open(savePath1, 'wb')
# saveFile1.write(f1)
# saveFile1.close()

# 방법 3
with open(savePath2, 'wb') as saveFile2:
    saveFile2.write(f2)

print("save 완료")