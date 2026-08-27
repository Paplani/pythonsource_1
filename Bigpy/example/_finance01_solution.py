from bs4 import BeautifulSoup
import requests

# 주식요청 url
url = "http://finance.naver.com/sise/"

res = requests.get(url)
res.encoding = res.apparent_encoding or 'euc-kr'   # requests는 인코딩을 자동으로 못 맞출 때가 있어서 직접 지정

soup = BeautifulSoup(res.text, "html.parser")

top_companies = soup.select("#siselist_tab_7 .tltle")
companies_price = soup.select("#siselist_tab_7 td:nth-child(3)")
companies_rasing_rate = soup.select("#siselist_tab_7 td:nth-child(5)")

print("시가총액 상위 10개 기업")
for idx, row in enumerate(top_companies):
    company_price = companies_price[idx]
    company_rasing_rate = companies_rasing_rate[idx].text.strip()
    print(idx+1, row.text, company_price.text, company_rasing_rate)
