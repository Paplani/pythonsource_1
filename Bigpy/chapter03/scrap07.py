import sys
import io
import urllib.request
import urllib.parse
from urllib.parse import urlparse   #url 파싱

sys.stdout.reconfigure(encoding='utf-8')   # 콘솔 출력을 UTF-8로 강제


API = "https://mois.go.kr/gpms/view/jsp/rss/rss.jsp"

# ?ctxCd=1012  

values = {
    'ctxCd' : 1012
}

params = urllib.parse.urlencode(values)
url = API + "?" + params
print(url)

data = urllib.request.urlopen(url).read()
text = data.decode("utf-8")
print(text)

