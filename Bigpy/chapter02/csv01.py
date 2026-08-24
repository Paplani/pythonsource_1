import pandas as pd

from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent
file_path = BASE_DIR/"csv_s1.csv"
file_path_1 = BASE_DIR/"csv_s2.csv"


# 기본읽기
df = pd.read_csv(file_path)
# print(df)

# 0번째 행 스킵, Header 생략
df=pd.read_csv(file_path, skiprows=[0], header=None)
# print(df)

# 0번째 행 스킵, Header 생략
df=pd.read_csv(file_path, skiprows=[0], header=None, names=["Month", 2023, 2024, 2025])
# print(df)

# 0번째 행 스킵, Header 생략, 인덱스 지정
# skiprows = 2 : 맨 앞에서부터 딱 2개만 스킵해라.
# skiprows = [0,3] : 0번째, 3번째 줄을 골라서 스킵
df=pd.read_csv(file_path, skiprows=2, header=None, names=["Month", 2023, 2024, 2025], index_col=[0])
# print(df)

df2 = pd.read_csv(file_path_1, sep = ';', skiprows=[0], \
                  header=None, names = ["First name", 'Test1', 'Test2', 'Test3', 'Final', 'Grade'])
# print(df2)

# 합계
df2['Sum'] = df2[['Test1', 'Test2', 'Test3', 'Final']].sum(axis=1)   # axis = 1 행단위
print(df2)

# axis=0 (기본값): 위→아래, 컬럼 방향으로 계산 → "각 시험(컬럼)마다 전체 학생 합/평균" (Test1 시험 점수들의 합계 등)
# axis=1: 왼쪽→오른쪽, 행 방향으로 계산 → "각 학생(행)마다 자기 점수들의 합/평균"


# 평균
df2['Avg'] = df2[['Test1', 'Test2', 'Test3', 'Final']].mean(axis=1)
print(df2)

# 저장하기
df2.to_csv("result.csv", index=False)
print('저장완료')