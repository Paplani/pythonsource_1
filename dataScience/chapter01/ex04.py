# -*- coding: utf-8 -*-

import pandas as pd

"""
- 여러 조건을 & (and), | (or)로 조합하는 법
- 조건마다 반드시 괄호로 묶어야 하는 이유(연산자 우선순위) 고려
- 파이썬 기본 and/or가 아니라 &, | 를 써야함
  -> "판다스는 행마다 비교해야 해서 파이썬 and/or로는 안됨"
- 조건 여러개는 각각 괄호로 묶기: (조건1) & (조건2)
"""

df = pd.read_csv("dataScience/data/tteokbokki_shops.csv", encoding='utf-8-sig')
print("=== 전체 떡볶이 가게 목록 ===")
print(df)

# 1. 단일 가격: 가격이 만원 이하인 가게가 몇 곳인지 검색
cheap = df[df["가격"] <= 10000]
print(f"\n === 가격이 만원 이하인 ({len(cheap)})곳")
print(cheap)

# 2. AND 조건 (&): 가격도 저렴하고 평점도 4.0 이상인 가게
best = df[(df["가격"] <= 10000) & (df["평점"] >= 4.0)]
print(f"\n === 가격이 만원 이하고 평점도 4점 이상인 ({len(best)})곳")
print(best)


# 3. OR 조건 (|) : 평점이 4.7 이상이거나 거리가 1km 이하인 곳
convenient = df[(df["평점"] >= 4.7) | (df["거리_km"] <= 1.0)]
print(f"\n === 평점이 4.7이상이거나 거리가 1km 이하인 ({len(convenient)})곳")
print(convenient)

# 4. isin(): 여러 값 중 하나에 해당하는지만 확인
target_shops = df[df["가게명"].isin(["엽떡", "청년다방","명동떡볶이"])]
print("\n === isin()으로 특정 가게 뽑기 === ")
print(target_shops)

# 5. between() : 범위 조건을 깔끔하게 사용
mid_price = df[df["가격"].between(8000, 11000)]
print("\n === between()으로 특정 가게 뽑기 === ")
print(mid_price)