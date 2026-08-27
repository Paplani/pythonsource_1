from bs4 import BeautifulSoup
from urllib.parse import urlparse
import urllib.request as req
import requests


# 주식요청 url

url = "http://finance.naver.com/sise/"

res = req.urlopen(url)

# encoding 아는 방법
# print(requests.get(url).encoding)

encoding = res.info().get_content_charset() or 'euc-kr'
res = res.read().decode(encoding, errors = 'ignore')
# print('res', res)

soup = BeautifulSoup(res, "html.parser")

top_companies = soup.select("#siselist_tab_7 .tltle")
companies_price = soup.select("#siselist_tab_7 td:nth-child(3)")
companies_rasing_rate = soup.select("#siselist_tab_7 td:nth-child(5)")
print("시가총액 상위 10개 기업")
for idx, row in enumerate(top_companies):
    company_price = companies_price[idx]
    company_rasing_rate = companies_rasing_rate[idx].text.strip()
    print(idx+1, row.text, company_price.text, company_rasing_rate)

#siselist_tab_7 > tbody > tr:nth-child(4) > td:nth-child(2) > a
