# chapter02 — 코드 치트시트

설명("왜"·"언제")은 아티팩트: https://claude.ai/code/artifact/7567e26b-c455-441a-8338-479cda42e5ad
판단 기준("어떤 질문엔 어떤 방법")은: https://claude.ai/code/artifact/94cb6a2a-e51b-42ad-bb72-31d55d1b44ac
실전 연습(새 데이터로 처음부터 끝까지): `../practice_delivery_reviews.ipynb`

이 맥 폰트: `mpl.rc('font', family='AppleGothic')` — Malgun Gothic 아님

## 기초 통계
```python
np.mean(arr)                          # 평균
np.max(arr) / np.min(arr)             # 최댓값 / 최솟값
np.std(arr, ddof=0)                   # 표준편차(모집단, numpy 기본)
np.std(arr, ddof=1)                   # 표준편차(표본, pandas 기본과 동일)
df["A"].std()                         # pandas Series 표준편차 (ddof=1)
df["A"].describe()                    # 개수·평균·표준편차·사분위수 한번에
df["A"].value_counts()                # 범주별 개수(내림차순)
df["A"].isnull().sum()                # 결측치 개수
np.corrcoef(x, y)                     # 상관계수 2x2 행렬
```

## 그룹별 통계
```python
df.groupby("A")["B"].mean()                      # A로 묶어 B 평균
df.groupby("A").size()                           # NaN 포함 행 개수
df.groupby("A")["B"].count()                     # NaN 제외 개수
df.groupby("A")["B"].mean().sort_values(ascending=False)   # 정렬은 항상 따로
df.groupby("A").agg(평균=("B","mean"), 건수=("B","count"))  # 여러 통계 한번에
```

## 관계 / 교차
```python
df[["A","B"]].corr()                              # 상관행렬
pd.get_dummies(df["A"])                           # 범주형 → 0/1 인코딩
pd.concat([df1, df2], axis=1)                     # 옆으로 이어붙이기
pd.crosstab(df["A"], df["B"], normalize="index")  # 범주 x 범주, 비율로
pd.pivot_table(df, index="A", columns="B", values="C",
               aggfunc="mean", fill_value=0,
               margins=True, margins_name="전체")   # 교차표 + 총계
pd.pivot_table(df, ..., aggfunc=["mean","count"])  # 다중 집계 (따옴표 각각!)
np.triu(arr, k=1)                                 # 히트맵 절반 가리기용 mask
```

## 시계열
```python
s.rolling(window=3).mean()    # 이동평균 (앞부분 NaN 정상)
s.cumsum()                    # 누적합계
```

## 이상치 / 통계 검정
```python
Q1, Q3 = s.quantile(0.25), s.quantile(0.75)
IQR = Q3 - Q1
lower, upper = Q1 - 1.5*IQR, Q3 + 1.5*IQR          # IQR 이상치 범위

z = (s - s.mean()) / s.std()
outliers = s[z.abs() > 2]                          # Z-score 이상치

from scipy import stats
t_stat, p_value = stats.ttest_ind(a, b, equal_var=False)   # p<0.05면 유의미
```

## 시각화
```python
plt.bar(x, y)                                       # 막대 (범주형 비교)
plt.plot(x, y, marker="o")                           # 선 (시계열 추세)
ax.hist(s, bins=10, color=..., edgecolor="black")    # 히스토그램 (분포)
sns.boxplot(data=df, x="A", y="B")                   # 상자그림 (그룹별 분포+이상치)
sns.heatmap(corr, annot=True, cmap="coolwarm", vmin=-1, vmax=1)  # 상관관계
sns.pairplot(df[["A","B"]])                          # 여러 변수 관계 한번에
sns.clustermap(pivot, annot=True)                    # 비슷한 것끼리 자동 그룹핑
```
