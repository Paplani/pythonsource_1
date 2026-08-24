import pandas as pd
import numpy as np
import openpyxl

# 0 ~ 99 사이의 수를 100행 4열로 생성
df1 = pd.DataFrame(np.random.randint(0, 100, size=(100, 4)), columns=['One', 'Two', 'Three', 'Four'])
print(df1)

# 정수 3 이전까지의 임의의 수(음수 표현)
# 평균 0이고 표준편차 1인 정규분포 실수 생성
# np.random.randn()의 randn은 "random standard normal"의 줄임말
# randn이라는 함수 이름/정의 자체에 "평균 0, 표준편차 1"이 이미 내장
# randn은 "표준(standard)" 정규분포 전용 함수라 평균 0/표준편차 1이 하드코딩된 특수 버전
# np.random.normal(loc=50, scale=10, size=(10, 2))   # 평균 50, 표준편차 10인 정규분포

df2 = pd.DataFrame(np.random.randn(10, 2), columns=list('AB'))
print(df2)

df1.to_csv("result2.csv", index=False)
df2.to_excel("result2.xlsx", header = True, index=False)
print('완료')
    