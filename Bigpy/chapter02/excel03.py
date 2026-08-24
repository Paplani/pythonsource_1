import pandas as pd
import openpyxl

from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent
file_path = BASE_DIR/"excel_s1.xlsx"


# 첫 번째 시트 읽어오기
df=pd.read_excel(file_path, sheet_name=0, engine='openpyxl')
# print(df)
# print(df.head())   # 상위 5개
# print(df.tail())              # 하위 5개


df=pd.read_excel(file_path, sheet_name=0, skiprows=[1])
# print(df.head())      

df=pd.read_excel(file_path, sheet_name=0, skiprows=[1], skipfooter=5)
# print(df.tail())     

df=pd.read_excel(file_path, header=0)
# print(df.head()) 
# print(list(df))     # 헤더만 리스트로 출력
print(list(df.columns.values))

# 전처리
# ^Unnamed : Unnamed로 시작하는 열
df = df.loc[:, ~df.columns.str.contains('^Unnamed')]
# pandas는 엑셀/CSV에 이름 없는 컬럼(예: 엑셀에 저장할 때 딸려온 빈 인덱스 열)을 만나면 자동으로 Unnamed: 0, Unnamed: 1처럼 이름을 붙입니다.
# df.columns.str.contains('^Unnamed'): 컬럼명이 'Unnamed'로 시작하는지(^는 정규식에서 "문자열 시작"을 의미) 검사해서, 컬럼마다 True/False를 반환
# ~: 그 결과를 반전(NOT) → "Unnamed로 시작 안 하는 컬럼"만 True
# df.loc[:, mask]: 모든 행(:)은 그대로 두고, 컬럼만 mask가 True인 것들로 필터링

# na_values = '...'=> null : 셸 안에 문자열 '...'(점 3개)가 들어있으면 그것을 결측치(NaN)으로 최급해라.
# converters={"2019": lambda w: w if w>60000 else None} : 6만 달러 이하는 None(결측)으로 바꾸라는 필터링
df=pd.read_excel(file_path, header=0, na_values='...', converters={"2019": lambda w: w if w>60000 else None})
print(df)