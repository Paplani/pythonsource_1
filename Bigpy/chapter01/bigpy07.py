import pandas as pd

# 시리즈 객체
numbers = pd.Series([100, 200, 300])
print(numbers)

# 인덱스 정보를 데이터로 활용한다는 시리즈의 특징
score = pd.Series([90,88,40], index = ['혁환', '명현', '효근'])
print(score)
print(score.index)
print(score.values)

print(score.index[2], score.values[2])
