# -*- coding: utf-8 -*-
import pandas as pd

"""
=== location, index location
- loc = '이름표'로 찾기(라벨 기준), 끝 포함
- iloc = '번호표'로 찾기(정수 위치 기준), 끝 포함 X
- df.loc[0:5, "상품명"]     # 인덱스 라벨이 0~5인 행 (총 6개!), "상품명" 컬럼
- df.iloc[0:5, 0]           # 위치상 0~4번째 행 (총 5개), 0번째 컬럼
- 조건 필터링 : df[df["별점] >= 4] 
df["컬럼명"] (문자열) → 컬럼 선택
df[불리언Series] (참/거짓 배열) → 행 필터링
"""

df = pd.read_csv("dataScience/data/delivery_reviews.csv", encoding="utf-8-sig")
print("=== 전체 데이터(상위 5개) ===")
print(df.head())

# 1. iloc: 정수 위치 기반 인덱싱 (0번째 ~ 4번째 행)
print(" === iloc[:5]: 0 ~ 4번째 행")
print(df.iloc[:5])

# 1. iloc로 특정 행 + 특정 열 위치 선택 (0번째 행의 0,1번째 열)
print("\n === iloc[0, [0,1]]: 0번째 행의 리뷰 번호, 메뉴명")
print(df.iloc[0,[0,1]])

# 3. loc: 라벨(컬럼명) 기반 인덱싱
print("\n === loc[:, ['메뉴명', '별점]]: 메뉴명과 별점 컬럼만 === ")
print(df.loc[:, ['메뉴명', '별점']].head())

# 4. boolean indexing: 조건을 만족하는 행만 추출
high_rating = df[df["별점"] >= 4.0]
print(f"\n=== 별점 4.0 이상 리뷰 ({len(high_rating)})")
print(high_rating.head())

# 5. loc + boolean indexing: 조건에 만족하는 행에서 특정 컬럼만 뽑기
print("\n === 별점 4.5 이상인 리뷰의 메뉴명, 가격만 추출 ===")
print(df.loc[df["별점"] >= 4.5, ["메뉴명", "가격"]])
print(df.iloc[df["별점"] >= 4.5, [1,4]])